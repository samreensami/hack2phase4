# API Specification: Task Web App REST Endpoints

**Feature Branch**: `1-task-web-app`
**Status**: Draft
**Base URL**: `/api/v1`

## Authentication (Better Auth / JWT)

All protected endpoints require the header: `Authorization: Bearer <JWT_TOKEN>`

### Authentication Endpoints

- **POST /auth/register**: Register a new user.
  - Body: `{ email, password }`
  - Response: 201 Created `{ user_id, email }`
- **POST /auth/login**: Login and receive a token.
  - Body: `{ email, password }`
  - Response: 200 OK `{ access_token, token_type: "bearer" }`

---

## Task Management Endpoints

### GET /tasks
List all tasks for the authenticated user.
- **Query Params**: `category` (optional)
- **Response**: 200 OK `[{ id, title, description, status, category, created_at }]`

### POST /tasks
Create a new task.
- **Body**: `{ title, description?, category? }`
- **Response**: 201 Created `{ id, title, description, status: false, category, created_at }`

### GET /tasks/{id}
Get details for a specific task.
- **Response**: 200 OK `{ id, title, description, status, category, created_at }`
- **Error**: 404 Not Found if id doesn't belong to user.

### PUT /tasks/{id}
Update an existing task.
- **Body**: `{ title?, description?, status?, category? }`
- **Response**: 200 OK Updated task object.

### DELETE /tasks/{id}
Delete a task.
- **Response**: 204 No Content.

---

## Technical Constraints

- **Language**: Python (FastAPI).
- **Validation**: Pydantic models for all request bodies.
- **Auth**: JWT verification middleware on all `/tasks/*` routes.
- **Database**: Neon (Postgres) via SQLAlchemy/SQLModel.
