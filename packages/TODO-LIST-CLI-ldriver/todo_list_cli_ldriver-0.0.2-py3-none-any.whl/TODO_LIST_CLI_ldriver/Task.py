class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed
"""
    this represents a single to-do item.

    description: The text of the task (e.g., "Buy groceries").

    completed: A Boolean that tracks whether the task is done. Defaults to False.

🔍 Why use a class here?

    To group both data (description, completed) and future behavior (e.g., mark as complete) into one unit.

    Later, add methods like .toggle_complete() or .to_dict().
"""