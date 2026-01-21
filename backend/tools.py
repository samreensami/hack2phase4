from sqlmodel import Session, select
from models import Task, TaskCreate
from typing import List, Optional, Dict, Any

def task_to_dict(task: Task) -> Dict[str, Any]:
    return {
        "id": task.id, "title": task.title, "description": task.description,
        "status": "complete" if task.status else "pending",
        "category": task.category,
    }

def add_task(session: Session, user_id: int, title: str, description: Optional[str] = None, category: Optional[str] = None):
    task_in = TaskCreate(title=title, description=description, category=category)
    db_task = Task(**task_in.dict(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return task_to_dict(db_task)

def list_tasks(session: Session, user_id: int, category: Optional[str] = None, status: Optional[str] = None):
    statement = select(Task).where(Task.user_id == user_id)
    if category: statement = statement.where(Task.category == category)
    tasks = session.exec(statement).all()
    return [task_to_dict(task) for task in tasks]

def complete_task(session: Session, user_id: int, task_ids: List[int]):
    statement = select(Task).where(Task.user_id == user_id, Task.id.in_(task_ids))
    tasks = session.exec(statement).all()
    for task in tasks:
        task.status = True
        session.add(task)
    session.commit()
    return {"status": "success", "completed_ids": task_ids}

def delete_task(session: Session, user_id: int, task_ids: List[int]):
    statement = select(Task).where(Task.user_id == user_id, Task.id.in_(task_ids))
    tasks = session.exec(statement).all()
    for task in tasks:
        session.delete(task)
    session.commit()
    return {"status": "success", "deleted_ids": task_ids}

def update_task(session: Session, user_id: int, task_id: int, **kwargs):
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()
    if not db_task: return {"error": "not found"}
    for key, value in kwargs.items():
        if value is not None: setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    return task_to_dict(db_task)