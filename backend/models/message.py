from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageBase(SQLModel):
    """Base model shared by Message, MessageCreate, and MessageRead."""
    conversation_id: int = Field(foreign_key="conversation.id")
    sender: str  # "user" or "assistant"
    content: str


class Message(MessageBase, table=True):
    """Database table for chat messages."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Input model when creating a new message (no id or timestamp)."""
    pass


class MessageRead(MessageBase):
    """Output model when reading a message (includes id and timestamp)."""
    id: int
    created_at: datetime


# ───────────────────────────────────────────────
# Chat specific request & response models
# ───────────────────────────────────────────────

class ChatRequest(BaseModel):
    """
    Request body for /chat endpoint.
    """
    message: str                        # User's input message
    conversation_id: Optional[int] = None  # Optional: continue existing conversation


class ChatResponse(BaseModel):
    """
    Response body for /chat endpoint.
    This is what frontend will receive.
    """
    response: str                       # AI's reply or tool result
    conversation_id: int                # The conversation this belongs to
    # Optional extra fields (uncomment/add as needed later)
    # role: str = "assistant"
    # created_at: datetime
    # sources: Optional[list[str]] = None
    # confidence: Optional[float] = None