import datetime
import json
import os
from typing import List, Dict, Optional, Any


class Task:
    def __init__(self, title: str, description: str = "", priority: int = 1, 
                due_date: Optional[datetime.datetime] = None, completed: bool = False):
        self.id = None  # ID bude přiřazeno při uložení
        self.title = title
        self.description = description
        self.priority = priority  # 1-5, kde 5 je nejvyšší
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Převede úkol na slovník pro serializaci"""
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
        """Vytvoří úkol ze slovníku"""
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
        """Označí úkol jako dokončený"""
        self.completed = True


class TaskManager:
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = storage_path
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, task: Task) -> Task:
        """Přidá nový úkol a přiřadí mu ID"""
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Najde úkol podle ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Aktualizuje úkol podle ID"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        # Aktualizace atributů
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Smaže úkol podle ID"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def get_all_tasks(self) -> List[Task]:
        """Vrátí všechny úkoly"""
        return self.tasks
    
    def get_incomplete_tasks(self) -> List[Task]:
        """Vrátí nedokončené úkoly"""
        return [task for task in self.tasks if not task.completed]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Vrátí úkoly po termínu"""
        now = datetime.datetime.now()
        return [
            task for task in self.tasks 
            if task.due_date and task.due_date < now and not task.completed
        ]
    
    def save_tasks(self) -> None:
        """Uloží úkoly do souboru"""
        data = {
            'next_id': self.next_id,
            'tasks': [task.to_dict() for task in self.tasks]
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self) -> None:
        """Načte úkoly ze souboru"""
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
            # Pokud je soubor poškozen, začneme s prázdným seznamem
            self.tasks = []
            self.next_id = 1
    
    def search_tasks(self, query: str) -> List[Task]:
        """Vyhledá úkoly podle textu v názvu nebo popisu"""
        query = query.lower()
        results = []
        for task in self.tasks:
            if query in task.title.lower() or (task.description and query in task.description.lower()):
                results.append(task)
        return results


# Ukázka použití
if __name__ == "__main__":
    # Vytvoříme správce úkolů
    manager = TaskManager()
    
    # Přidáme nějaké úkoly
    task1 = Task("Dokončit seminární práci", "Kapitoly State-of-the-art, Návrh experimentu", 5, 
                datetime.datetime(2025, 5, 30))
    task2 = Task("Nakoupit potraviny", "Chleba, mléko, vejce", 3)
    
    manager.add_task(task1)
    manager.add_task(task2)
    
    # Vypíšeme všechny úkoly
    for task in manager.get_all_tasks():
        print(f"{task.id}: {task.title} (Priorita: {task.priority})")
        if task.due_date:
            print(f"  Termín: {task.due_date.strftime('%d.%m.%Y')}")
