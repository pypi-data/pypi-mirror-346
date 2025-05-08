from .ToDoList import *

if __name__ == "__main__":
    todo = ToDoList()
    todo.run()
"""
# todo_list_cli

#today
#1 turn into object oriented code
#2 add if __name__ == "__main__"
#3 pacakge code
#4 dockerize code
#5 make an installer and executable 
planned features (ai generated)

Make object oriented

example:
class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

class ToDoList:
    def __init__(self, filename="file.txt"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        # Load from file and convert to Task objects
        pass

    def save_tasks(self):
        # Write Task objects back to file
        pass

    def view_tasks(self):
        # Print tasks
        pass

    def add_task(self, description):
        # Add new Task object and save
        pass

    def run(self):
        # Your main CLI loop
        pass can you explain this

✅ Core Functionality (Already Done)

Display a menu with options

View all tasks

Add tasks

Exit cleanly

    Save/load tasks from file

🧱 Upgrade from Basic to Intermediate
📁 Switch from TXT to JSON (Structured persistence)

Store tasks in a JSON file as dictionaries ({"task": "...", "done": False})

    Load and write the entire task list each time (simulate a basic database)

🔁 Update Task Lifecycle

Mark tasks as complete/incomplete

Delete a specific task (by index or description)

    Edit a task's text

📅 Add Optional Metadata

Add creation dates

Add optional due dates (store as string or datetime)

    Sort tasks by date or priority

📦 Better UX and Structure

Number tasks when printing

Show completed/incomplete status with checkmarks or text

    Confirm when actions succeed (e.g., “Task deleted successfully”)

🧠 Code Structure & Error Handling

Use functions for each action (e.g., add_task(), delete_task())

Use try/except for file handling and invalid input

    Validate user input (e.g., prevent crashing on invalid index)

🔀 Advanced Features (Optional but Solid Intermediate)

Filter tasks (e.g., show only incomplete, due soon, overdue)

Use colored terminal output with colorama or rich

Sort tasks by due date or priority

Import/export tasks from a backup file

    Assign categories or tags to tasks (e.g., “work”, “personal”)

🧪 Bonus (Good Practice)

Unit test task-handling functions using unittest or pytest

Use argparse to run specific commands directly from the terminal (e.g., python todo.py --view)

checklist-style roadmap to guide your implementation using tkinter, the standard GUI library in Python:
🧱 Minimum Viable GUI To-Do List – Checklist
✅ Setup & Layout

Create a window (tk.Tk) with a title like "To-Do List".

Add a Listbox to display tasks.

Add Entry + Button to input new tasks.

Add a "Delete Task" button.

    Add a "Mark as Done" button (optional highlight, strikethrough, etc.).

🗃️ Data Management

Load tasks from a JSON file at startup.

Save tasks to the JSON file whenever they’re added/deleted/modified.

    Represent each task as a dict ({"task": "Buy milk", "done": False}).

🖱️ Event Handling

Hook up buttons to functions (.bind() or command=).

When a task is selected and "Delete" is pressed, remove it from both the Listbox and data file.

    When "Add Task" is clicked, insert it into Listbox and data file.

🎨 Optional UI Features (intermediate polish)

Use checkboxes or color-coding for completed tasks.

Add a scrollbar if the list grows too long.

Support double-click to toggle task completion.

Add a menu bar (File > Exit, Save, etc.).

    Group tasks by category or due date (if you add those fields later).

🧠 Bonus Intermediate Challenges (not required, but cool)

Use ttk widgets for a modern look.

Add due dates using a date picker (tkcalendar).

Sort tasks (e.g., alphabetically, by due date, or completed status).

Add filtering: show only "incomplete" or "due today".

Add keyboard shortcuts (e.g., Enter to add, Del to remove).


"""