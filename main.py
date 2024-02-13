import tkinter as tk
import sqlite3
import openai
import os.path
from tabulate import tabulate

# Set up OpenAI API key
openai.api_key = 'YOUR OPENAI API KEY'

# Global variable to store the last selected database connection
conn = None

def open_database():
    global conn
    database_path = database_entry.get()
    if not os.path.isfile(database_path):  # Check if the file exists
        print("Error: Database file does not exist.")
        return
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        display_output("Tables in Database:\n" + "\n".join(table_names))
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
    global conn
    query = query_output.get("1.0", tk.END)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        display_output("Query result:")
        if len(rows) > 0:
            display_output(tabulate([column_names] + rows, tablefmt='plain'))
        else:
            display_output("No results found.")
    except sqlite3.Error as e:
        print("SQLite Error:", e)

def clear_output():
    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    output_text.config(state=tk.DISABLED)

def display_output(output):
    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, str(output) + "\n")  # Convert output to string
    output_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Database Viewer")
root.geometry("600x400")

# Set background color
root.config(bg="#F0F0F0")

# Frame for output text
output_frame = tk.Frame(root, bg="#F0F0F0")
output_frame.pack(fill=tk.BOTH, expand=True)

# Text widget to display output
output_text = tk.Text(output_frame, wrap=tk.WORD, width=80, height=20, bg="white", fg="black")
output_text.pack(fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)
output_text.bind("<KeyPress>", lambda e: "break")  # Disable typing in the text widget

# Frame for input elements
input_frame = tk.Frame(root, bg="#F0F0F0")
input_frame.pack(pady=10)

# Entry widget for database path
database_entry = tk.Entry(input_frame, width=50, bg="white", fg="black")
database_entry.grid(row=0, column=0)

# Button to open database
open_button = tk.Button(input_frame, text="Open Database", command=open_database, bg="#007ACC", fg="white", relief=tk.FLAT, padx=10)
open_button.grid(row=0, column=1, padx=10)

# Entry widget for plain English query
input_entry = tk.Entry(input_frame, width=50, bg="white", fg="black")
input_entry.grid(row=1, column=0)

# Button to generate SQL query
generate_button = tk.Button(input_frame, text="Enter", command=generate_sql_query, bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10)
generate_button.grid(row=1, column=1, padx=10)

# Text box to display generated SQL query
query_output = tk.Text(input_frame, width=50, height=10, bg="white", fg="black")
query_output.grid(row=2, column=0, pady=10, columnspan=2)

# Button to execute SQL query
execute_button = tk.Button(input_frame, text="Submit", command=execute_query, bg="#FF9800", fg="white", relief=tk.FLAT, padx=10)
execute_button.grid(row=3, column=0, columnspan=2)

# Button to clear output
clear_button = tk.Button(input_frame, text="Clear Output", command=clear_output, bg="#E91E63", fg="white", relief=tk.FLAT, padx=10)
clear_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
