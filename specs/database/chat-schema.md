# Data Model: Chat Schema

## Entities

### Conversation
Represents a single chat session between a user and the AI assistant.
- **id**: Integer (Primary Key)
- **user_id**: Integer (Foreign Key -> User.id, On Delete Cascade)
- **created_at**: DateTime (Auto-generated)

### Message
Represents a single message within a conversation.
- **id**: Integer (Primary Key)
- **conversation_id**: Integer (Foreign Key -> Conversation.id, On Delete Cascade)
- **sender**: String (Enum: 'user', 'assistant')
- **content**: Text (The actual message content)
- **created_at**: DateTime (Auto-generated)

## Relationships
- **User -> Conversation**: One-to-Many (A user can have many conversations)
- **Conversation -> Message**: One-to-Many (A conversation can have many messages)

## Database Schema (SQLModel/PostgreSQL)

```sql
CREATE TABLE "conversation" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE "message" (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES "conversation"(id) ON DELETE CASCADE,
    sender VARCHAR NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```
