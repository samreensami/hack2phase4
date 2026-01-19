from sqlmodel import Session, select
from models import Task, TaskCreate
from typing import List, Optional, Dict, Any

# Note: In a real application, you would get the session and user_id from the request context.
# For this implementation, we will pass them as arguments to the tool functions.


def task_to_dict(task: Task) -> Dict[str, Any]:
    """Convert task to JSON-serializable dict."""
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": "complete" if task.status else "pending",
        "category": task.category,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


def add_task(
    session: Session,
    user_id: int,
    title: str,
    description: Optional[str] = None,
    category: Optional[str] = None,
) -> Dict[str, Any]:
    """Adds a new task to the user's list."""
    task_in = TaskCreate(title=title, description=description, category=category)
    db_task = Task(**task_in.dict(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return task_to_dict(db_task)

def list_tasks(
    session: Session,
    user_id: int,
    category: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Lists all tasks for the current user."""
    statement = select(Task).where(Task.user_id == user_id)
    if category:
        statement = statement.where(Task.category == category)
    if status:
        if status.lower() == "complete":
            statement = statement.where(Task.status == True)
        elif status.lower() == "incomplete":
            statement = statement.where(Task.status == False)

    tasks = session.exec(statement).all()
    return [task_to_dict(task) for task in tasks]

def complete_task(
    session: Session, user_id: int, task_ids: List[int]
) -> Dict[str, Any]:
    """Marks one or more tasks as complete."""
    statement = select(Task).where(Task.user_id == user_id, Task.id.in_(task_ids))
    tasks_to_complete = session.exec(statement).all()
    
    if not tasks_to_complete:
        return {"status": "error", "message": "No tasks found with the given IDs."}

    completed_ids = []
    for task in tasks_to_complete:
        task.status = True
        session.add(task)
        completed_ids.append(task.id)
    
    session.commit()
    return {"status": "success", "completed_ids": completed_ids}

def delete_task(
    session: Session, user_id: int, task_ids: List[int]
) -> Dict[str, Any]:
    """Deletes one or more tasks."""
    statement = select(Task).where(Task.user_id == user_id, Task.id.in_(task_ids))
    tasks_to_delete = session.exec(statement).all()

    if not tasks_to_delete:
        return {"status": "error", "message": "No tasks found with the given IDs."}

    deleted_ids = []
    for task in tasks_to_delete:
        session.delete(task)
        deleted_ids.append(task.id)

    session.commit()
    return {"status": "success", "deleted_ids": deleted_ids}

def update_task(
    session: Session,
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Updates the details of a single task."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return {"status": "error", "message": "Task not found."}

    update_data = {
        "title": title,
        "description": description,
        "category": category,
    }
    if status is not None:
        update_data["status"] = status.lower() == "complete"

    for key, value in update_data.items():
        if value is not None:
            setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task.dict()
