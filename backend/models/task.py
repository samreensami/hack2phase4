from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: bool = False
    category: Optional[str] = None

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
