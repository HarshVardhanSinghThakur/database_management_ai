from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import streamlit as st
import os


def init_database(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db):
    db_uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
    return SQLDatabase.from_uri(db_uri)


def get_response(user_input, db, chat_history):
    sql_chain = build_db_chain(db)
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="llama3-70b-8192", temperature=0)
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda x: db.get_table_info(),
            response=lambda c: db.run(c["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke({
        "question": user_input,
        "chat_history": chat_history,
    })


def build_db_chain(db):
    template = """
You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

<SCHEMA>{schema}</SCHEMA>

Conversation History: {chat_history}

Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

For example:
Question: Which 3 actors have the most films?
SQL Query: SELECT actor_id, COUNT(*) as film_count FROM film_actor GROUP BY actor_id ORDER BY film_count DESC LIMIT 3;
Question: Name 10 films
SQL Query: SELECT title FROM film LIMIT 10;

Your turn:

Question: {question}
SQL Query:
"""
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="llama3-70b-8192", temperature=0)

    def get_schema(_):
        return db.get_table_info()
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()

    )


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(
            content="Hello! I'm a database manager. Ask me anything about your database."),]

st.set_page_config(page_title="dbAI",
                   page_icon="https://cdn-icons-png.flaticon.com/128/12872/12872153.png")
st.title("Query your Database")


with st.sidebar:

    st.sidebar.subheader("Database Connection Settings")

    connection_type = st.radio(
        "Select Connection Type",
        ("Localhost", "Web Database")
    )
    if connection_type == "Localhost":
        mysql_host = st.text_input('Host', value='localhost')
        mysql_user = st.text_input('User', value='root')
        mysql_port = st.text_input('Port', value=3306)
        mysql_password = st.text_input('Password', type='password')
        mysql_db = st.text_input('Database', value='sakila')
    elif connection_type == "Web Database":
        mysql_host = st.text_input('Host', 'your_web_host')
        mysql_user = st.text_input('User', 'your_web_user')
        mysql_password = st.text_input('Password', type='password')
        mysql_db = st.text_input('Database', 'your_web_database')
    if st.button("connect"):
        with st.spinner("Connecting"):
            try:
                db = init_database(mysql_host, mysql_port,
                                   mysql_user, mysql_password, mysql_db)
                st.session_state.db = db
                st.success("Connected to database")
            except Exception as e:
                st.error(f"Failed to connect: {e}")
load_dotenv()
for chat in st.session_state.chat_history:
    if isinstance(chat, AIMessage):
        with st.chat_message("AI"):
            st.markdown(chat.content)
    elif isinstance(chat, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(chat.content)


user_input = st.chat_input("Enter your message...")

if user_input is not None and user_input.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("Human"):
        st.markdown(user_input)
    with st.spinner("Getting response from Groq..."):

        try:
            with st.chat_message("AI"):
                response = get_response(
                    user_input, st.session_state.db, st.session_state.chat_history)

                st.markdown(response)
                st.session_state.chat_history.append(
                    AIMessage(content=response))
        except Exception as e:
            st.error(f"Error: {e}")
