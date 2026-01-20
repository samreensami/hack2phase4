# Claude Code & Spec-Kit Plus Integration

This file serves as a placeholder for integrating with external AI development tools like Claude Code and Spec-Kit Plus in the monorepo structure.

## Purpose
- To define prompts, specifications, and instructions that can be used by AI assistants to understand and extend the project.
- To maintain a context for AI-driven development, ensuring consistency with the project's constitution.
- To provide guidance for AI assistants working with the monorepo structure.

## Monorepo Structure
This project follows a monorepo structure with the following key directories:

```
task-web-app/
├── backend/                 # FastAPI backend service
│   ├── core/               # Core configuration and utilities
│   ├── models/             # SQLModel/Pydantic models
│   ├── routes/             # API route handlers
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend unit tests
│   ├── main.py             # FastAPI application entry point
│   ├── pyproject.toml      # Python dependencies
│   └── Dockerfile          # Backend container config
├── frontend/               # Next.js frontend application
│   ├── app/                # Next.js app router pages
│   ├── components/         # Reusable React components
│   ├── lib/                # Utility functions and API services
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container config
├── tests/                  # Integration/E2E tests
├── specs/                  # Specifications and design documents
├── package.json            # Root workspace config with concurrent scripts
├── pyproject.toml          # Root Python config for testing
├── docker-compose.yml      # Multi-service deployment config
└── CONSTITUTION.md         # Project principles and guidelines
```

## Running the Project

### Development Mode (Concurrent)
```bash
# Install dependencies
npm install
cd backend && pip install -e .

# Run both frontend and backend simultaneously
npm run dev
```

### Individual Services
```bash
# Frontend only (port 3000)
npm run dev:frontend

# Backend only (port 8000)
npm run dev:backend
```

### Production Deployment
```bash
# Using Docker Compose
docker-compose up --build

# Or build individually
docker-compose build
docker-compose up -d
```

### Testing
```bash
# Run all tests
npm run test

# Backend tests only
npm run test:backend

# Or directly with pytest
cd backend && pytest
```

## Usage
When interacting with an AI, reference this file and the `CONSTITUTION.md` to provide the necessary context for generating code, documentation, or tests. The AI should be aware of the monorepo structure and place new components in the appropriate directories.

## Key Configuration Files
- `package.json` (root): npm workspaces, concurrent scripts for running both services
- `pyproject.toml` (root): pytest configuration for running tests
- `backend/pyproject.toml`: Python dependencies for FastAPI backend
- `frontend/package.json`: Node.js dependencies for Next.js frontend
- `docker-compose.yml`: Multi-container deployment configuration
