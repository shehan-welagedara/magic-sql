import tkinter as tk
import sqlite3
import openai  # Make sure to install the openai library
import os.path
from tkinter import messagebox

# Set up OpenAI API key
openai.api_key = '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'

def open_database():
    database_path = database_entry.get()
    if not os.path.isfile(database_path):  # Check if the file exists
        print("Error: Database file does not exist.")
        return
    try:
        global conn
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        display_output("Tables in the database:")
        for table in tables:
            display_output(table[0])  # Display table name
    except sqlite3.Error as e:
        print("SQLite Error:", e)

def generate_sql_query():
    input_text = input_entry.get()
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=input_text + "\nGenerate the corresponding SQL query:",
            max_tokens=50
        )
        sql_query = response.choices[0].text.strip()
        query_output.delete("1.0", tk.END)
        query_output.insert(tk.END, sql_query)
    except Exception as e:
        print("OpenAI Error:", e)

def execute_query():
    query = query_output.get("1.0", tk.END)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        display_output("Query result:")
        for row in result:
            display_output(row)
    except sqlite3.Error as e:
        print("SQLite Error:", e)

def display_output(output):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, output + "\n")
    output_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Database Viewer")

# Frame for output text
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True)

# Text widget to display output
output_text = tk.Text(output_frame, wrap=tk.WORD, width=80, height=20)
output_text.pack(fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)
output_text.bind("<KeyPress>", lambda e: "break")  # Disable typing in the text widget

# Frame for input elements
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Entry widget for database path
database_entry = tk.Entry(input_frame, width=50)
database_entry.grid(row=0, column=0)

# Button to open database
open_button = tk.Button(input_frame, text="Open Database", command=open_database)
open_button.grid(row=0, column=1, padx=10)

# Entry widget for plain English query
input_entry = tk.Entry(input_frame, width=50)
input_entry.grid(row=1, column=0)

# Button to generate SQL query
generate_button = tk.Button(input_frame, text="Enter", command=generate_sql_query)
generate_button.grid(row=1, column=1, padx=10)

# Text box to display generated SQL query
query_output = tk.Text(input_frame, width=50, height=10)
query_output.grid(row=2, column=0, pady=10, columnspan=2)

# Button to execute SQL query
execute_button = tk.Button(input_frame, text="Submit", command=execute_query)
execute_button.grid(row=3, column=0, columnspan=2)

root.mainloop()
