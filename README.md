# Task Manager (Tkinter + SQLite)

A simple task manager built with Tkinter.  
Tasks are stored in a local SQLite database and remain saved between sessions.

## Features

- Add new tasks
- Choose a category (color)
- Toggle tasks between done / not done
- Delete tasks
- Open tasks and completed tasks are shown in separate sections
- Data is saved permanently in `tasks.db`

## How to Run

```
python3 -m venv .venv
source .venv/bin/activate
python main.py
```

## Files

- `main.py` – Tkinter application
- `tasks.db` – created automatically when the program runs