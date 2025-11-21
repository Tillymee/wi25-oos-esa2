import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

"""
File:           main.py
Author:         Mathilda Zechmeister
Date:           2025-11-21
Version:        1.0
Description:    A simple Tkinter task manager that uses SQLite to store tasks. 
                Users can add tasks, choose a category, mark tasks as done or 
                not done, and delete them. 
"""

# Category colors
CATEGORIES = {
    "None": None,
    "Red": "#ff6961",
    "Green": "#77dd77",
    "Blue": "#aec6cf",
    "Yellow": "#fdfd96"
}


# Helper: run an SQL command
def run_sql(query, params=(), fetch=False):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result


# Database setup
def init_db():
    run_sql("""
            CREATE TABLE IF NOT EXISTS tasks
            (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                title    TEXT,
                done     INTEGER,
                category TEXT
            )
            """)


# Task DB operations
def get_tasks():
    return run_sql("SELECT id, title, done, category FROM tasks", fetch=True)


def add_task_to_db(title, category):
    run_sql("INSERT INTO tasks (title, done, category) VALUES (?, ?, ?)",
            (title, 0, category))


def update_task_done(task_id, done_value):
    run_sql("UPDATE tasks SET done=? WHERE id=?", (done_value, task_id))


def delete_task(task_id):
    run_sql("DELETE FROM tasks WHERE id=?", (task_id,))


# Tkinter UI
class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Input section
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        self.entry = tk.Entry(top_frame, width=35)
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", lambda e: self.add_task())

        # Category dropdown
        self.category_var = tk.StringVar(value="None")
        ttk.Combobox(
            top_frame, textvariable=self.category_var,
            values=list(CATEGORIES.keys()), width=10, state="readonly"
        ).pack(side="left", padx=5)

        tk.Button(top_frame, text="Add Task", command=self.add_task).pack(side="left")

        # Sections
        tk.Label(root, text="Open Tasks", font=("Arial", 12, "bold")).pack(pady=(10, 3))
        self.open_frame = tk.Frame(root)
        self.open_frame.pack()

        tk.Label(root, text="Completed Tasks", font=("Arial", 12, "bold")).pack(pady=(15, 3))
        self.completed_frame = tk.Frame(root)
        self.completed_frame.pack()

        self.render_tasks()

    # Add task
    def add_task(self):
        title = self.entry.get().strip()
        category = self.category_var.get()

        if not title:
            messagebox.showwarning("Error", "Task title cannot be empty.")
            return

        add_task_to_db(title, None if category == "None" else category)
        self.entry.delete(0, tk.END)
        self.category_var.set("None")
        self.render_tasks()

    # Render tasks
    def render_tasks(self):
        for frame in (self.open_frame, self.completed_frame):
            for widget in frame.winfo_children():
                widget.destroy()

        for task_id, title, done, category in get_tasks():
            target_frame = self.completed_frame if done else self.open_frame
            self.create_task_row(target_frame, task_id, title, done, category)

    # Build a task row
    def create_task_row(self, parent, task_id, title, done, category):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=2)

        var = tk.IntVar(value=done)
        bg_color = CATEGORIES.get(category)

        checkbox = tk.Checkbutton(
            row, text=title, variable=var,
            command=lambda: self.toggle_done(task_id, var)
        )
        if bg_color:
            checkbox.configure(bg=bg_color)
        if done:
            checkbox.configure(fg="gray")

        checkbox.pack(side="left", padx=5)

        tk.Button(row, text="Delete", fg="red",
                  command=lambda: self.delete_task(task_id)
                  ).pack(side="right", padx=5)

    # Toggle done/undone
    def toggle_done(self, task_id, var):
        update_task_done(task_id, var.get())
        self.render_tasks()

    # Delete a task
    def delete_task(self, task_id):
        delete_task(task_id)
        self.render_tasks()


# Start program
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    TaskManager(root)
    root.mainloop()