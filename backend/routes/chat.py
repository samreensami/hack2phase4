from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import List
import json

from core.database import get_session
from core.security import get_current_user
from core.config import settings
from models import Conversation, Message
import tools

from openai import OpenAI

router = APIRouter(tags=["Chat"])


# -------------------------
# Schemas
# -------------------------

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: int


class LatestConversation(BaseModel):
    conversation_id: int | None = None


class MessageResponse(BaseModel):
    sender: str
    content: str


class MessagesResponse(BaseModel):
    messages: List[MessageResponse]


class NewConversationResponse(BaseModel):
    conversation_id: int


# -------------------------
# OpenRouter Client
# -------------------------

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


# -------------------------
# Tools mapping
# -------------------------

AVAILABLE_TOOLS = {
    "add_task": tools.add_task,
    "list_tasks": tools.list_tasks,
    "complete_task": tools.complete_task,
    "delete_task": tools.delete_task,
    "update_task": tools.update_task,
}


# -------------------------
# Chat Endpoint
# -------------------------

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
):

    if not settings.OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenRouter API key missing",
        )

    user_id = int(current_user_id)

    # -------------------------
    # Conversation
    # -------------------------

    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # -------------------------
    # Save user message
    # -------------------------

    user_message = Message(
        conversation_id=conversation.id,
        sender="user",
        content=request.message,
    )
    session.add(user_message)
    session.commit()

    # -------------------------
    # History
    # -------------------------

    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.desc())
        .limit(10)
    )

    history = list(reversed(session.exec(stmt).all()))

    messages = [{"role": m.sender, "content": m.content} for m in history]

    # -------------------------
    # System prompt
    # -------------------------

    system_prompt = """
You are an AI task management assistant.

Whenever the user talks about tasks, todos, reminders, or lists,
you MUST call one of the tools.

Never explain tools.
Never reply in plain text when a task action is required.

Available tools:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task
"""

    agent_messages = [{"role": "system", "content": system_prompt}] + messages

    # -------------------------
    # Tool schemas
    # -------------------------

    agent_tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "category": {"type": "string"},
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List user tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "status": {"type": "string"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Complete tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                        }
                    },
                    "required": ["task_ids"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                        }
                    },
                    "required": ["task_ids"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "category": {"type": "string"},
                        "status": {"type": "string"},
                    },
                    "required": ["task_id"],
                },
            },
        },
    ]

    # -------------------------
    # Agent loop
    # -------------------------

    max_iterations = 5
    assistant_response = None

    try:
        for _ in range(max_iterations):
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=agent_messages,
                tools=agent_tools,
                tool_choice="auto",
            )

            msg = response.choices[0].message

            if msg.tool_calls:
                agent_messages.append(msg)

                for call in msg.tool_calls:
                    fn_name = call.function.name
                    fn = AVAILABLE_TOOLS.get(fn_name)

                    if fn is None:
                        agent_messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": call.id,
                                "name": fn_name,
                                "content": json.dumps({"error": f"Unknown tool: {fn_name}"}),
                            }
                        )
                        continue

                    args = json.loads(call.function.arguments)
                    args["session"] = session
                    args["user_id"] = user_id

                    result = fn(**args)

                    agent_messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.id,
                            "name": fn_name,
                            "content": json.dumps(result),
                        }
                    )

            else:
                assistant_response = msg.content
                break

        if assistant_response is None:
            assistant_response = "I'm sorry, I couldn't complete the request. Please try again."

    except Exception as e:
        print(f"OpenRouter API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}",
        )

    # -------------------------
    # Save assistant message
    # -------------------------

    assistant_message = Message(
        conversation_id=conversation.id,
        sender="assistant",
        content=assistant_response,
    )

    session.add(assistant_message)
    session.commit()

    return ChatResponse(
        response=assistant_response,
        conversation_id=conversation.id,
    )


# -------------------------
# Extra endpoints
# -------------------------

@router.get("/conversations/latest", response_model=LatestConversation)
def get_latest_conversation(
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
):
    user_id = int(current_user_id)

    stmt = (
        select(Conversation.id)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(1)
    )

    return LatestConversation(conversation_id=session.exec(stmt).first())


@router.get("/conversations/{conv_id}/messages", response_model=MessagesResponse)
def get_messages(
    conv_id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
):
    user_id = int(current_user_id)

    convo = session.get(Conversation, conv_id)
    if not convo or convo.user_id != user_id:
        raise HTTPException(status_code=404)

    msgs = session.exec(
        select(Message)
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at.asc())
    ).all()

    return MessagesResponse(
        messages=[MessageResponse(sender=m.sender, content=m.content) for m in msgs]
    )


@router.post("/conversations/new", response_model=NewConversationResponse)
def new_conversation(
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
):
    convo = Conversation(user_id=int(current_user_id))
    session.add(convo)
    session.commit()
    session.refresh(convo)
    return NewConversationResponse(conversation_id=convo.id)
