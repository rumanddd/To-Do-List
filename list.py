import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from PIL import Image, ImageTk

# Database setup
DATABASE = "tasks.db"

def connect_db():
    """Connects to the SQLite database and creates the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def load_tasks():
    """Retrieves tasks from the database and returns them as a list."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT task FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return [task[0] for task in tasks]

def save_tasks():
    """Saves all tasks from the listbox to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    tasks = listbox.get(0, tk.END)
    for task in tasks:
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def add_task():
    """Adds a task to the listbox and saves it to the database."""
    task = entry.get().strip()
    if task:
        if task in listbox.get(0, tk.END):
            messagebox.showwarning("Warning", "Task already exists!")
            return
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter something into the text field.")

def remove_task():
    """Removes the selected task from the listbox and the database."""
    try:
        selected_index = listbox.curselection()[0]
        task = listbox.get(selected_index)
        listbox.delete(selected_index)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task=?", (task,))
        conn.commit()
        conn.close()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove.")

# GUI Setup
root = tk.Tk()
root.title("To-Do List")
root.geometry("420x500")
root.configure(bg="#121212")  # Dark background

# Add background image or pattern
bg_path = "/Users/ruman/PycharmProjects/To-Do-List/background.png"  # Absolute path to the image
if os.path.exists(bg_path):
    bg_image = Image.open(bg_path)
    bg_image = bg_image.resize((420, 500))  # Resize image to fit the window size
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
else:
    print("Warning: Background image not found. Running without it.")

# Styling
frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=40, height=10, bg="#1e1e1e", fg="white", font=("Arial", 12), relief=tk.FLAT, selectbackground="#ff9800", selectforeground="black")
listbox.pack(side=tk.LEFT, padx=5)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

entry = tk.Entry(root, width=40, font=("Arial", 12), bg="#252526", fg="white", relief=tk.FLAT, insertbackground="white")
entry.pack(pady=5)

button_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#ff9800",
    "fg": "black",
    "bd": 0,
    "relief": tk.FLAT,
    "padx": 15,
    "pady": 8,
    "activebackground": "#e68900",
    "cursor": "hand2",
    "borderwidth": 2,
    "highlightthickness": 0,
}

def on_enter(e):
    e.widget.config(bg="#e68900", relief=tk.RAISED)

def on_leave(e):
    e.widget.config(bg="#ff9800", relief=tk.FLAT)

add_button = tk.Button(root, text="Add Task", command=add_task, **button_style)
add_button.pack(pady=5, ipadx=5, ipady=2)
add_button.bind("<Enter>", on_enter)
add_button.bind("<Leave>", on_leave)
add_button.config(borderwidth=5, relief=tk.RIDGE)

remove_button = tk.Button(root, text="Remove Task", command=remove_task, **button_style)
remove_button.pack(pady=5, ipadx=5, ipady=2)
remove_button.bind("<Enter>", on_enter)
remove_button.bind("<Leave>", on_leave)
remove_button.config(borderwidth=5, relief=tk.RIDGE)

# Initialize the database and load tasks
connect_db()
for task in load_tasks():
    listbox.insert(tk.END, task)

root.mainloop()
