from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .conversation import Conversation

class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversation.id")
    sender: str  # "user" or "assistant"
    content: str

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime
