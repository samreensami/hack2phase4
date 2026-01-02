from typing import Dict, List, Optional
from models import Task

class TaskService:
    """
    In-memory service for CRUD operations on Tasks.
    This class holds the application's state.
    """
    _tasks: Dict[str, Task] = {}

    def create_task(self, title: str, description: str) -> Task:
        """Creates and stores a new task."""
        if not title:
            raise ValueError("Title cannot be empty.")
        
        new_task = Task(title=title, description=description)
        self._tasks[new_task.id] = new_task
        print(f"Task '{title}' created successfully.")
        return new_task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieves a task by its ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Returns a list of all tasks."""
        return list(self._tasks.values())

    def update_task(self, task_id: str, title: str, description: str) -> Optional[Task]:
        """Updates a task's title and description."""
        task = self.get_task(task_id)
        if task:
            task.title = title if title else task.title
            task.description = description if description else task.description
            print(f"Task '{task.title}' updated.")
            return task
        print(f"Error: Task with ID '{task_id}' not found.")
        return None

    def complete_task(self, task_id: str) -> Optional[Task]:
        """Marks a task as completed."""
        task = self.get_task(task_id)
        if task:
            task.completed = True
            print(f"Task '{task.title}' marked as complete.")
            return task
        print(f"Error: Task with ID '{task_id}' not found.")
        return None

    def delete_task(self, task_id: str) -> bool:
        """Deletes a task from memory."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            print(f"Task with ID '{task_id}' deleted.")
            return True
        print(f"Error: Task with ID '{task_id}' not found.")
        return False
