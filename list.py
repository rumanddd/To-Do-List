import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
DATABASE = "tasks.db"

# Function to connect to the SQLite database and create the tasks table if it doesn't exist
def connect_db():
    """Connects to the SQLite database and creates the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE) # Connects to the database
    cursor = conn.cursor() # Create a cursor object to interact with the database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    ''') # Creates the tasks table if it doesn't exist
    conn.commit() # Commits the changes to the database
    conn.close() # Closes the connection

# Function to LOAD tasks from the database
def load_tasks():
    """Retrieves tasks from the database and returns them as a list."""
    conn = sqlite3.connect(DATABASE) # Connects to the database
    cursor = conn.cursor() # Create a cursor object to interact with the database
    cursor.execute("SELECT task FROM tasks") # Retrieves tasks from the tasks table
    tasks = cursor.fetchall() # Fetches all the tasks
    conn.close() # Closes the connection
    return [tasks[0] for task in tasks] # Returns a list of tasks

# Function to save tasks to the database
def save_tasks():
    """Saves all tasks from the listbox to the SQLite database."""
    conn = sqlite3.connect(DATABASE)  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("DELETE FROM tasks")  # Delete all tasks from the table
    tasks = listbox.get(0, tk.END)  # Get all tasks from listbox
    for task in tasks:
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))  # Insert each task into the database
    conn.commit()  # Save changes
    conn.close()  # Close the connection

# Function to ADD task
def add_tasks():
    task = entry.get().strip()  # ✅ Get text from the input field
    if task:  # Now 'task' is defined
        listbox.insert(tk.END, task)  # Add task to the listbox
        entry.delete(0, tk.END)  # Clear the input field
        save_tasks()  # Save the updated task list
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")  # Warn if empty

# Function to REMOVE task
def remove_task():
    """Removes the selected task from the listbox and the database."""
    try:
        selected_index = listbox.curselection()[0] # Retrieves the index of the selected task
        task = listbox.get(selected_index) # Retrieves the task at the selected index
        listbox.delete(selected_index) # Deletes the task from the listbox

        # Remove the task from the database
        conn = sqlite3.connect(DATABASE) # Connects to the database
        cursor = conn.cursor() # Create a cursor object to interact with the database
        cursor.execute("DELETE FROM tasks WHERE task=?", (task,)) # Deletes the task from the tasks table
        conn.commit() # Commits the changes to the database
        conn.close() # Closes the connection

        save_tasks() # Saves the tasks to the database
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove.") # Displays a warning message if no task is selected


# GUI Setup
root = tk.Tk()
root.title("To-Do List") # Set window title
root.geometry("400x400")  # Set window size

# Create widgets
frame = tk.Frame(root) # Create a frame
frame.pack(pady=10) # Adds spacing above the listbox

listbox = tk.Listbox(frame, width=40, height=10) # Create listbox
listbox.pack(side=tk.LEFT) # Places it to the left side

scrollbar = tk.Scrollbar(frame) # Creates a vertical scrollbar
scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Places scrollbar on the right and fills it vertically
listbox.config(yscrollcommand=scrollbar.set) # Links the scrollbar to the listbox, allowing the scrollbar to update when the listbox content changes.
scrollbar.config(command=listbox.yview) # Configures the scrollbar to scroll the listbox when moved, so dragging the scrollbar updates the listbox view.


entry = tk.Entry(root, width=40) # Creates an input field (Entry) where users type tasks and ets to width
entry.pack(pady=5) # Adds vertical padding of 5

add_button = tk.Button(root, text="Add Task", command=add_tasks) # Creates a button labeled "Add Task" and calls add_task() when clicked
add_button.pack(pady=5) # Adds vertical padding of 5

remove_button = tk.Button(root, text="Remove Task", command=remove_task) # Creates a button labeled "Remove Task" and calls remove_task() when clicked
remove_button.pack(pady=5) # Adds vertical padding of 5

# Initialize the database and load tasks
connect_db() # Make sure the database adn table are setup
for task in load_tasks(): # Retrieve tasks from the database
    listbox.insert(tk.END, task) # Insert each task into the listbox

# Run the Tkinter loop
root.mainloop() # Runs the application and keeps the window open.
