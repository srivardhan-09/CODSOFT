import json
import uuid

# File path for storing tasks
TASKS_FILE = 'tasks.json'

class Task:
    def __init__(self, title, description, status='pending'):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        task = Task(data['title'], data['description'], data['status'])
        task.id = data['id']
        return task

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.load_tasks()

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks[task.id] = task
        self.save_tasks()

    def update_task(self, task_id, title=None, description=None, status=None):
        task = self.tasks.get(task_id)
        if not task:
            return False
        if title:
            task.title = title
        if description:
            task.description = description
        if status:
            task.status = status
        self.save_tasks()
        return True

    def complete_task(self, task_id):
        return self.update_task(task_id, status='completed')

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False

    def list_tasks(self):
        return [task.to_dict() for task in self.tasks.values()]

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks.values()], file)

    def load_tasks(self):
        try:
            with open(TASKS_FILE, 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task.from_dict(task_data)
                    self.tasks[task.id] = task
        except FileNotFoundError:
            pass

def main():
    task_manager = TaskManager()
    while True:
        print("Commands: add, update, complete, delete, list, quit")
        command = input("Enter command: ").strip().lower()

        if command == 'add':
            title = input("Enter title: ").strip()
            description = input("Enter description: ").strip()
            task_manager.add_task(title, description)
            print("Task added.")
        elif command == 'update':
            task_id = input("Enter task ID: ").strip()
            title = input("Enter new title (leave empty to keep current): ").strip()
            description = input("Enter new description (leave empty to keep current): ").strip()
            status = input("Enter new status (pending/completed, leave empty to keep current): ").strip()
            if task_manager.update_task(task_id, title or None, description or None, status or None):
                print("Task updated.")
            else:
                print("Task not found.")
        elif command == 'complete':
            task_id = input("Enter task ID: ").strip()
            if task_manager.complete_task(task_id):
                print("Task marked as completed.")
            else:
                print("Task not found.")
        elif command == 'delete':
            task_id = input("Enter task ID: ").strip()
            if task_manager.delete_task(task_id):
                print("Task deleted.")
            else:
                print("Task not found.")
        elif command == 'list':
            tasks = task_manager.list_tasks()
            for task in tasks:
                print(f"ID: {task['id']}, Title: {task['title']}, Description: {task['description']}, Status: {task['status']}")
        elif command == 'quit':
            break
        else:
            print("Unknown command.")

if __name__ == '__main__':
    main()
