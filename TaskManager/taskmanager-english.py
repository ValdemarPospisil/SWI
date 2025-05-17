import datetime
import json
import os
from typing import List, Dict, Optional, Any


class Task:
    def __init__(self, title: str, description: str = "", priority: int = 1, 
                due_date: Optional[datetime.datetime] = None, completed: bool = False):
        self.id = None  # ID will be assigned when saved
        self.title = title
        self.description = description
        self.priority = priority  # 1-5, where 5 is highest
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Converts task to dictionary for serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Creates task from dictionary"""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 1),
            completed=data.get('completed', False)
        )
        
        if data.get('due_date'):
            task.due_date = datetime.datetime.fromisoformat(data['due_date'])
        
        task.id = data.get('id')
        task.created_at = datetime.datetime.fromisoformat(data['created_at'])
        return task
    
    def complete(self):
        """Marks task as completed"""
        self.completed = True


class TaskManager:
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = storage_path
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, task: Task) -> Task:
        """Adds new task and assigns ID"""
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Finds task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Updates task by ID"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        # Update attributes
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Deletes task by ID"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks"""
        return self.tasks
    
    def get_incomplete_tasks(self) -> List[Task]:
        """Returns incomplete tasks"""
        return [task for task in self.tasks if not task.completed]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Returns overdue tasks"""
        now = datetime.datetime.now()
        return [
            task for task in self.tasks 
            if task.due_date and task.due_date < now and not task.completed
        ]
    
    def save_tasks(self) -> None:
        """Saves tasks to file"""
        data = {
            'next_id': self.next_id,
            'tasks': [task.to_dict() for task in self.tasks]
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self) -> None:
        """Loads tasks from file"""
        if not os.path.exists(self.storage_path):
            self.tasks = []
            self.next_id = 1
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                
            self.next_id = data.get('next_id', 1)
            self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
        except json.JSONDecodeError:
            # If file is corrupted, start with empty list
            self.tasks = []
            self.next_id = 1
    
    def search_tasks(self, query: str) -> List[Task]:
        """Searches tasks by text in title or description"""
        query = query.lower()
        results = []
        for task in self.tasks:
            if query in task.title.lower() or (task.description and query in task.description.lower()):
                results.append(task)
        return results


# Usage example
if __name__ == "__main__":
    # Create task manager
    manager = TaskManager()
    
    # Add some tasks
    task1 = Task("Complete seminar paper", "State-of-the-art and Experiment design chapters", 5, 
                datetime.datetime(2025, 5, 30))
    task2 = Task("Buy groceries", "Bread, milk, eggs", 3)
    
    manager.add_task(task1)
    manager.add_task(task2)
    
    # Print all tasks
    for task in manager.get_all_tasks():
        print(f"{task.id}: {task.title} (Priority: {task.priority})")
        if task.due_date:
            print(f"  Due date: {task.due_date.strftime('%d.%m.%Y')}")
