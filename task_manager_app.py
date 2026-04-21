import json
from datetime import datetime

class Task:
    def __init__ (self, name, description, due_date, priority="medium"):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_complete(self):
        self.completed = True

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'due_date': self.due_date,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    
    @staticmethod
    def from_dict(data):
        task = Task(
            data["name"],
            data["description"],
            data["due_date"],
            data["priority"]
        )
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task
    
    def __str__(self):
        status = "C" if self.completed else "o"
        return f"[{status}] {self.name} (Due: {self.due_date}, priority {self.priority})"
    
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task '{task.name}' added!")

    def list_tasks (self, show_completed=True):
        if not self.tasks:
            print("No tasks found!")
            return
        
        print ("\n" + "_" * 20)
        for i, task in enumerate(self.tasks, 1):
            if show_completed or not task.completed: #filter
                print(f"{i}. {task}")
        print("_" * 20 + "\n")

    def complete_task(self, task_number):
        try:
            task = self.tasks[task_number - 1]
            task.mark_complete()
            print(f"Task '{task.name} marked as completed")
        except:
            print("Invalid task number")

    def save_to_file(self, filename="tasks.json"):
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Tasks saved to {filename}")

        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_from_file (self, filename="tasks.json"):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
            print(f"Loaded {len(self.tasks)} tasks from {filename}")
        
        except FileNotFoundError:
            print(f"No saved tasks found. Starting fresh!")
        
        except Exception as e:
            print(f"Error loading tasks: {e}")

def main():
    manager = TaskManager()
    manager.load_from_file()

    while True:
        print(".    Task Manager.     ")  
        print("1. To add a task")
        print("2. List all tasks")
        print("3. List incomplete tasks")
        print("4. Complete tasks")
        print("5. Save tasks")
        print("6. Exit")

        choice = input("\n choice option: ")

        if choice == '1':
            name = input("Task name: ")
            description = input("Description")
            due_date = input("Due date: ")
            priority = input("Priority  (high/medium/low): ") or "medium"

            task = Task(name, description, due_date, priority)
            manager.add_task(task)
        
        elif choice == '2':
            manager.list_tasks()

        elif choice == '3':
            manager.list_tasks(show_completed=False)
        
        elif choice == '4':
            manager.list_tasks()
            task_num = int(input("Task number to complete: "))
            manager.complete_task(task_num)
        
        elif choice == '5':
            manager.save_to_file()
        
        elif choice == '6':
            manager.save_to_file()
            print("Goodbye")
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
