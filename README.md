

````markdown
# PyQt6 ToDo Manager

A simple and practical ToDo management application built with Python and PyQt6.  
This app allows you to add, delete, and mark tasks as done, with data stored in a SQLite database.

---

## Features

- Add tasks with title and due date  
- Display tasks in a table with sortable columns  
- Mark tasks as completed using checkboxes  
- Delete selected tasks  
- Data persistence with SQLite  
- Clean and user-friendly GUI

---

## Requirements

- Python 3.7 or higher  
- PyQt6

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
````

2. (Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv env
# On Linux/macOS:
source env/bin/activate
# On Windows:
.\env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application with:

```bash
python todo_app.py
```

* Enter the task title in the input field.
* Select the due date.
* Click "Add Task" to add it to the list.
* Use the checkbox to mark tasks as done or undone.
* Select a task and click "Delete Selected Task" to remove it.

---

## Project Structure

```
todo_app/
├── todo_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---
