# Task Web App (Phase 2 - Production Ready)

A full-stack, production-ready To-Do list application built with a modern monorepo architecture.

## 🚀 Tech Stack

- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.12, SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Auth**: JWT (JSON Web Tokens) with secure password hashing
- **Migrations**: Alembic
- **Tooling**: Claude Code, Spec-Kit Plus

## ✨ Key Features

- **Secure Authentication**: User registration and login with JWT issuance.
- **Task Management**: Full CRUD (Create, Read, Update, Delete) operations.
- **Ownership Protection**: Users can only access and modify their own tasks.
- **Task Categorization**: Organize tasks by labels (Work, Personal, etc.).
- **Type Safety**: End-to-end type synchronization between backend models and frontend clients.
- **Modern UI**: Clean, responsive interface with real-time state updates.

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- Neon DB Account (PostgreSQL)

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL='your-neon-db-url'
JWT_SECRET='your-secret-key'
JWT_ALGORITHM='HS256'
NEXT_PUBLIC_API_URL='http://localhost:8000'
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt # Or use uv sync
alembic upgrade head
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📂 Project Structure

- `backend/`: FastAPI application server and database models.
- `frontend/`: Next.js web application.
- `specs/`: Detailed technical specifications and implementation plans.
- `history/`: Prompt History Records (PHR) for development traceability.
- `.claude/`: Custom AI skills (api-generator).

## 📄 License
MIT
# hack2phase3
