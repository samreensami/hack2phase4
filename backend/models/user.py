from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime
