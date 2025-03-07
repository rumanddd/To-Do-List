import tkinter as tk
from tkinter import messagebox
import os

# File to store tasks
TASKS_FILE = "tasks.txt"

# Function to load tasks from a file
def load_tasks():
    """Loads tasks from tasks.txt when the program starts."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return file.read().splitlines()  # Reads each line as a task
    return []

# Function to save tasks to a file
def save_tasks():
    """Saves all tasks from the listbox to tasks.txt."""
    with open(TASKS_FILE, "w") as file:
        tasks = listbox.get(0, tk.END)  # Get all tasks from listbox
        for task in tasks:
            file.write(task + "\n")  # Write each task on a new line

# Function to add a task
def add_task():
    """Adds a task from the entry field to the listbox."""
    task = entry.get().strip()  # Get text from entry field
    if task:
        listbox.insert(tk.END, task)  # Add to listbox
        entry.delete(0, tk.END)  # Clear input field
        save_tasks()  # Save tasks
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to remove the selected task
def remove_task():
    """Removes the selected task from the listbox."""
    try:
        selected_index = listbox.curselection()[0]  # Get selected item index
        listbox.delete(selected_index)  # Remove from listbox
        save_tasks()  # Save tasks after removing
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove!")

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

add_button = tk.Button(root, text="Add Task", command=add_task) # Creates a button labeled "Add Task" and calls add_task() when clicked
add_button.pack(pady=5) # Adds vertical padding of 5

remove_button = tk.Button(root, text="Remove Task", command=remove_task) # Creates a button labeled "Remove Task" and calls remove_task() when clicked
remove_button.pack(pady=5) # Adds vertical padding of 5

# Load tasks when app starts
for task in load_tasks(): # Retrieves tasks from tasks.txt
    listbox.insert(tk.END, task) # Inserts each task into the listbox

# Run the Tkinter loop
root.mainloop() # Runs the application and keeps the window open.
