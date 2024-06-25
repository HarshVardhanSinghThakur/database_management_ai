# dbAI

dbAI is a Streamlit web application that allows users to interact with their databases using natural language queries. The application leverages the Langchain framework and Groq API for language model capabilities to translate user questions into SQL queries, which are then executed against a connected database.

## Features

- Natural language interface to query databases
- Support for both local and remote databases
- Automatically generate SQL queries based on user input
- Display query results in an easy-to-read format

## Prerequisites

- Python 3.8 or higher
- A MySQL database (either local or remote)
- Groq API Key (store in `.env` file)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/dbAI.git
    cd dbAI
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up your environment variables:

    Create a `.env` file in the root directory of the project and add your Groq API key:

    ```env
    GROQ_API_KEY=your_groq_api_key
    ```

## Usage

1. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Connect to your database:

    - For a local database, enter your MySQL host, user, port, password, and database name in the sidebar.
    - For a remote database, enter your web host, user, password, and database name.(*in development)

4. Interact with the database using natural language queries.

## Connecting to Different Databases

Currently, dbAI supports local databases. You can connect to localhost databases by providing the necessary credentials in the sidebar.

### Local Database Connection

1. Select "Localhost" as the connection type.
2. Enter your MySQL host (default is `localhost`), user (default is `root`), port (default is `3306`), password, and database name.
3. Click "Connect" to establish the connection.

### Remote Database Connection
(*in development)
1. Select "Web Database" as the connection type.
2. Enter your web host, user, password, and database name.
3. Click "Connect" to establish the connection.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs, features, or improvements.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Langchain](https://www.langchain.com/)
- [Groq](https://www.groq.com/)

## Contact

For any questions or feedback, please reach out to [harshthakur9415@gmail.com](mailto:harshthakur9415@gmail.com).
