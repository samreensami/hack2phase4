---
id: 06-db-connection
title: Neon DB Connection Setup
stage: misc
date: 2026-01-02
surface: cli
model: claude-sonnet-4-5-20250929
feature: 1-task-web-app
branch: 1-task-web-app
user: MWRIK
command: custom
labels: [database, neon, sqlmodel, connectivity]
links:
  spec: specs/1-task-web-app/spec.md
  plan: specs/1-task-web-app/plan.md
files:
  - path: .env
    action: created
  - path: backend/core/config.py
    action: modified
  - path: check_db.py
    action: created
  - path: .claude/skills/api-generator/generate.py
    action: modified
---

## Prompt

Ab Neon DB connection setup karo.

Environment Variable: Root mein .env file banao aur usme DATABASE_URL='postgresql://neondb_owner:npg_s4VuO6cESLil@ep-young-resonance-a4qdzk5n-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require' dalo.

Backend Config: backend/database.py mein SQLModel engine create karo jo is URL ko use kare.

Validation: Ek chota script chalao jo check kare ke connection 'Live' hai ya nahi.

Skill Usage: Is connection logic ko api-generator skill ka hissa banao.

History: Result ko history/prompts/06-db-connection.md mein save karo."

## Response snapshot

Successfully established a live connection to Neon PostgreSQL. Configured the root `.env` file and updated the backend settings to load it. Created a validation script `check_db.py` which confirmed the connection is "LIVE". Integrated the database connection logic into the `api-generator` skill scripts for future schema synchronization.

## Outcome

- ✅ Impact: Backend is now connected to a persistent, serverless production-ready database.
- 🧪 Tests: `check_db.py` executed successfully, returning "Database connection: LIVE".
- 📁 Files: Updated .env, config.py, generate.py, and created check_db.py.
- 🔁 Next prompts: /sp.implement for User models and migrations.
- 🧠 Reflection: Neon's pooler URL with SSL requirements works perfectly with SQLModel/SQLAlchemy after ensuring `pydantic-settings` points to the correct root `.env` path.

## Evaluation notes (flywheel)

- Failure modes observed: `sqlalchemy` was missing in the global environment; installed via pip to run the validation script.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
