from .Task import *

class ToDoList:
    def __init__(self, filename="src/TODO_LIST_CLI/file.txt"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        tasks = []
        with open(self.filename, 'r') as file:
            for line in file:
                tasks.append(Task(description=line.strip()))
        return tasks

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task.description}|{task.completed}\n")


    def view_tasks(self):
        # Check if there are any tasks
        if not self.tasks:
            print("No tasks to display.")
            return
    
        # Loop through tasks and display them with their completion status
        for i, task in enumerate(self.tasks, start=1):
            status = "✅" if task.completed else "❌"
            print(f"{i}. {task.description} {status}")


    def add_task(self):
        description = input('What would you like to add to your todo list?\n')
        self.tasks.append(Task(description=description))
        self.save_tasks()  # Save updated list to file

    def complete_task(self):
        # Display tasks with their indices
        for i, task in enumerate(self.tasks, start=1):
            status = "✅" if task.completed else "❌"
            print(f"{i}. {task.description} [{status}]")
    
    # Ask user which task to complete
        try:
            index = int(input("Enter the number of the task you completed: "))
            if 1 <= index <= len(self.tasks):
                self.tasks[index - 1].completed = True
                self.save_tasks()
                print("Task marked as complete.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

    def run(self):
        
        while (True):
            print("What would you like to do?\n1. View todo list\n2. Add to todo list\n3. Mark a task as complete\n4. Exit")
            choice = input()
    
            match choice:
                case '1':
                    self.view_tasks()
                case '2':
                    self.add_task()
                case '3':
                    self.complete_task()
                case '4':
                    quit()
                case _:
                    print("Please type \"1, 2 or 3\"")

