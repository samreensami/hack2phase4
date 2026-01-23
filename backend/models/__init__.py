# models/__init__.py
from .user import User, UserCreate, UserRead
from .task import Task, TaskCreate, TaskRead
from .conversation import Conversation, ConversationCreate, ConversationRead
from .message import Message, MessageCreate, MessageRead, ChatRequest, ChatResponse  # ← ensure this line exists

__all__ = [
    "User", "UserCreate", "UserRead",
    "Task", "TaskCreate", "TaskRead",
    "Conversation", "ConversationCreate", "ConversationRead",
    "Message", "MessageCreate", "MessageRead",
    "ChatRequest", "ChatResponse",
]