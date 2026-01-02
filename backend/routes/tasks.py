from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..core.database import get_session
from ..core.security import get_current_user
from ..models.task import Task, TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_task = Task(**task_in.dict(), user_id=int(current_user_id))
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskRead])
def get_tasks(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Task).where(Task.user_id == int(current_user_id))
    tasks = session.exec(statement).all()
    return tasks

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Task).where(Task.id == task_id, Task.user_id == int(current_user_id))
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

    task_data = task_in.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Task).where(Task.id == task_id, Task.user_id == int(current_user_id))
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

    session.delete(db_task)
    session.commit()
    return None
