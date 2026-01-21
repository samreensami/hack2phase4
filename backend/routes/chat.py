from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from core.security import get_current_user
import os, json
from openai import OpenAI
import tools
from models import Conversation, Message, MessageResponse, ChatRequest, ChatResponse

router = APIRouter(tags=["Chat"])

# IMPORTANT: Ensure your core/config.py has OPENROUTER_API_KEY
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

AVAILABLE_TOOLS = {
    "add_task": tools.add_task,
    "list_tasks": tools.list_tasks,
    "complete_task": tools.complete_task,
    "delete_task": tools.delete_task,
    "update_task": tools.update_task,
}

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, session: Session = Depends(get_session), current_user_id: str = Depends(get_current_user)):
    user_id = int(current_user_id)
    
    # Conversation logic
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation); session.commit(); session.refresh(conversation)

    # Save user message
    session.add(Message(conversation_id=conversation.id, sender="user", content=request.message))
    session.commit()

    # Get history
    stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())
    history = session.exec(stmt).all()
    messages = [{"role": m.sender, "content": m.content} for m in history]

    # Agent Loop
    agent_tools = [
        {"type": "function", "function": {"name": "add_task", "description": "Add task", "parameters": {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}}},
        {"type": "function", "function": {"name": "list_tasks", "description": "List tasks", "parameters": {"type": "object", "properties": {}}}},
    ]

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct", # OpenRouter ka fast model
        messages=[{"role": "system", "content": "You are a task assistant. Use tools for any task actions."}] + messages,
        tools=agent_tools
    )

    ans = response.choices[0].message.content or "Task processed!"
    
    # Save assistant message
    session.add(Message(conversation_id=conversation.id, sender="assistant", content=ans))
    session.commit()

    return ChatResponse(response=ans, conversation_id=conversation.id)