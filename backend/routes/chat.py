from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from core.security import get_current_user
import os
from openai import OpenAI
import tools
from models import Conversation, Message, MessageCreate, MessageRead, ChatRequest, ChatResponse

# Response model define kar rahe hain yahan (temporary, baad mein models mein move kar sakte ho)
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int

router = APIRouter(tags=["Chat"])

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Available tools (sirf woh jo actually implement hue hain)
AVAILABLE_TOOLS = {
    "add_task": tools.add_task,
    "list_tasks": tools.list_tasks,
    "complete_task": tools.complete_task,
    "delete_task": tools.delete_task,
    "update_task": tools.update_task,
}

# OpenAI-compatible tools format for LLM
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the task"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks of the current user",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    # Agar baaki tools bhi use karna chahte ho to add kar sakte ho
]

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    user_id = int(current_user_id)

    # Conversation handle karo
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found or access denied")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # User message save karo
    user_message = Message(
        conversation_id=conversation.id,
        sender="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()

    # Puri conversation history fetch karo
    stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())
    history = session.exec(stmt).all()

    messages = [{"role": m.sender, "content": m.content} for m in history]

    # System prompt + history + tools
    system_prompt = {
        "role": "system",
        "content": (
            "You are a helpful task management assistant. "
            "Use the provided tools when the user asks to add, list, complete, delete or update tasks. "
            "For normal conversation, just respond normally. "
            "Always respond in a friendly and concise way."
        )
    }

    # LLM call
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct:free",  # free & fast model on OpenRouter
            messages=[system_prompt] + messages,
            tools=AGENT_TOOLS,
            temperature=0.7,
            max_tokens=512,
        )

        message = response.choices[0].message

        # Agar tool call aaya hai to handle karo
        if message.tool_calls:
            # Abhi simple response de rahe hain, baad mein actual tool execution add kar sakte ho
            tool_response = "Tool call received: " + message.tool_calls[0].function.name
            ans = tool_response
        else:
            ans = message.content.strip() or "Okay, noted!"

    except Exception as e:
        ans = f"Sorry, something went wrong with the AI: {str(e)}"

    # Assistant message save karo
    assistant_message = Message(
        conversation_id=conversation.id,
        sender="assistant",
        content=ans
    )
    session.add(assistant_message)
    session.commit()

    return ChatResponse(
        response=ans,
        conversation_id=conversation.id
    )