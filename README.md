# MagicSQL

MagicSQL is a simple graphical user interface (GUI) application built using Python and Tkinter. It allows users to interact with SQLite databases by opening a database file, executing SQL queries, and viewing the query results within the application. Also, it utilizes the OpenAI API to generate SQL queries based on user input and allows executing those queries on SQLite databases.

## Features

- Open SQLite database files.
- Execute SQL queries.
- View query results.
- Clear output.

## Requirements

- Python 3
- Tkinter
- SQLite3
- OpenAI (optional, if you want to use the AI-powered SQL query generation feature)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repository
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. Enter the path to your SQLite database file in the provided entry field and click "Open Database".
   
3. Enter a plain English query in the input field and click "Enter" to generate the corresponding SQL query (optional).
   
4. Click "Submit" to execute the SQL query on the database.

5. View the results in the output text area.

## Configuration

- Replace `'YOUR OPENAI API KEY'` with your actual OpenAI API key in the `openai.api_key` assignment in the `main.py` file if you want to use the AI-powered SQL query generation feature.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

## Credits

- This project utilizes the [OpenAI API](https://openai.com/) for AI-powered SQL query generation.
- It also relies on the [Tkinter](https://docs.python.org/3/library/tkinter.html) library for building the GUI.

## Author

- [Shehan Welagedara](https://github.com/shehan-welagedara)
