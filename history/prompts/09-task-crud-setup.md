---
id: 09-task-crud-setup
title: Task CRUD API Implementation
stage: tasks
date: 2026-01-03
surface: cli
model: claude-sonnet-4-5-20250929
feature: 1-task-web-app
branch: 1-task-web-app
user: MWRIK
command: /sp.implement
labels: [crud, backend, tasks, security, jwt]
links:
  spec: specs/1-task-web-app/spec.md
  plan: specs/1-task-web-app/plan.md
  tasks: specs/1-task-web-app/tasks.md
files:
  - path: backend/routes/tasks.py
    action: created
  - path: backend/main.py
    action: modified
  - path: frontend/lib/generated/task_types.ts
    action: created
---

## Prompt

"Haan, Task CRUD APIs (Phase 4) shuru karo.

Backend Engineer Agent: backend/routes/tasks.py banao aur ye endpoints define karo:

POST /tasks: Naya task create karne ke liye.

GET /tasks: User ke apne saare tasks fetch karne ke liye.

PUT /tasks/{id}: Task update karne ke liye.

DELETE /tasks/{id}: Task remove karne ke liye.

Security & Ownership: Har endpoint par JWT verification middleware lazmi lagao. Ensure karo ke user sirf apne hi tasks access ya modify kar sake.

Skill Usage: api-generator skill ka istemal karo taake frontend ke liye task_types.ts generate ho jaye.

History: Result ko history/prompts/09-task-crud-setup.md mein record karo."

## Response snapshot

Implemented secure Task CRUD APIs in `backend/routes/tasks.py`. All endpoints require JWT authentication and enforce strict ownership—users can only see and modify their own tasks. Integrated the task router into the main FastAPI app and updated the `api-generator` skill to produce `task_types.ts` for the frontend. Verified the logic with a comprehensive lifecycle test script.

## Outcome

- ✅ Impact: Core business logic (Task Management) is now fully functional and secure.
- 🧪 Tests: `test_tasks.py` verified the full logic (Create -> Get -> Update -> Delete).
- 📁 Files: Added tasks routes and generated frontend types.
- 🔁 Next prompts: /sp.implement for Dashboard UI in frontend.
- 🧠 Reflection: Using `int(current_user_id)` casting for foreign key operations ensures type compatibility between the JWT payload and the database model.

## Evaluation notes (flywheel)

- Failure modes observed: Port 8000 was already occupied by a previous background process. Used `taskkill` or session management to handle.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
