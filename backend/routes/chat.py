from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import List
import json

from core.database import get_session
from core.security import get_current_user
from models import (
    Conversation,
    Message,
    MessageCreate,
    ConversationCreate,
    User,
    MessageRead
)
import tools
from openai import OpenAI
from core.config import settings

router = APIRouter(prefix="/api", tags=["Chat"])

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

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# A mapping from tool name to the actual function
AVAILABLE_TOOLS = {
    "add_task": tools.add_task,
    "list_tasks": tools.list_tasks,
    "complete_task": tools.complete_task,
    "delete_task": tools.delete_task,
    "update_task": tools.update_task,
}

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
):
    """
    Handles a chat message from the user, processes it through the AI agent,
    and returns the agent's response.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key is not configured."
        )

    user_id = int(current_user_id)
    
    # 1. Get or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # 2. Add user message to DB
    user_message = Message(
        conversation_id=conversation.id,
        sender="user",
        content=request.message,
    )
    session.add(user_message)
    session.commit()
    session.refresh(user_message)
    
    # 3. Fetch conversation history
    history_statement = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.desc()).limit(10)
    history = session.exec(history_statement).all()
    # Reverse the history to be in chronological order
    history.reverse()
    messages = [{"role": msg.sender, "content": msg.content} for msg in history]

    # 4. Call the agent with tools
    system_prompt = "You are a helpful assistant that can manage a user's tasks. Use the available tools to add, list, complete, delete, or update tasks. Be concise and professional."
    agent_messages = [{"role": "system", "content": system_prompt}] + messages
    
    # Define tools for the OpenAI client
    agent_tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task to the user's list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the task."},
                        "description": {"type": "string", "description": "A longer description of the task."},
                        "category": {"type": "string", "description": "A category to assign to the task."},
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Lists all tasks for the current user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Filters tasks by a specific category."},
                        "status": {"type": "string", "description": "Filters tasks by status (e.g., 'complete', 'incomplete')."},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Marks one or more tasks as complete.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_ids": {"type": "array", "items": {"type": "integer"}, "description": "A list of task IDs to mark as complete."},
                    },
                    "required": ["task_ids"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Deletes one or more tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_ids": {"type": "array", "items": {"type": "integer"}, "description": "A list of task IDs to delete."},
                    },
                    "required": ["task_ids"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Updates the details of a single task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to update."},
                        "title": {"type": "string", "description": "The new title for the task."},
                        "description": {"type": "string", "description": "The new description for the task."},
                        "category": {"type": "string", "description": "The new category for the task."},
                        "status": {"type": "string", "description": "The new status for the task ('complete' or 'incomplete')."},
                    },
                    "required": ["task_id"],
                },
            },
        },
    ]

    # Agent loop
    while True:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=agent_messages,
            tools=agent_tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message

        if response_message.tool_calls:
            agent_messages.append(response_message)
            tool_calls = response_message.tool_calls
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = AVAILABLE_TOOLS[function_name]
                function_args = json.loads(tool_call.function.arguments)
                
                # Add session and user_id to the arguments
                function_args["session"] = session
                function_args["user_id"] = user_id

                try:
                    function_response = function_to_call(**function_args)
                    agent_messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(function_response),
                        }
                    )
                except Exception as e:
                     agent_messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": f'{{"error": "An error occurred: {str(e)}"}}',
                        }
                    )
        else:
            assistant_response_content = response_message.content
            break

    # 5. Save assistant response to DB
    assistant_message = Message(
        conversation_id=conversation.id,
        sender="assistant",
        content=assistant_response_content,
    )
    session.add(assistant_message)
    session.commit()

    return ChatResponse(response=assistant_response_content, conversation_id=conversation.id)


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
    latest_id = session.exec(stmt).first()
    return LatestConversation(conversation_id=latest_id)


@router.get("/conversations/{conv_id}/messages", response_model=MessagesResponse)
def get_conversation_messages(
    conv_id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
):
    user_id = int(current_user_id)
    conversation = session.get(Conversation, conv_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    stmt = (
        select(Message)
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at.asc())
    )
    messages = session.exec(stmt).all()

    msg_list = [
        MessageResponse(sender=m.sender, content=m.content)
        for m in messages
    ]
    return MessagesResponse(messages=msg_list)

@router.post("/conversations/new", response_model=NewConversationResponse)
def create_new_conversation(
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user),
):
    user_id = int(current_user_id)
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return NewConversationResponse(conversation_id=conversation.id)
