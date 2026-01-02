---
id: 13-security-hardening
title: Security Hardening for Production
stage: tasks
date: 2026-01-03
surface: cli
model: claude-sonnet-4-5-20250929
feature: 1-task-web-app
branch: 1-task-web-app
user: MWRIK
command: custom
labels: [security, cors, secrets, hardening, production-ready]
links:
  spec: specs/1-task-web-app/spec.md
  plan: specs/1-task-web-app/plan.md
files:
  - path: backend/main.py
    action: modified
  - path: backend/core/config.py
    action: modified
  - path: .gitignore
    action: verified
---

## Prompt

Hardening security for production deployment

## Response snapshot

Implemented critical security hardening steps for production. Added `CORSMiddleware` to the FastAPI backend to restrict cross-origin access to authorized domains. Strictly enforced environment variable loading for `DATABASE_URL` and `JWT_SECRET` by making them non-optional in the settings config, ensuring the app fails fast if secrets are missing. Verified `.gitignore` to prevent sensitive `.env` files from being committed to the repository.

## Outcome

- ✅ Impact: Significantly reduced attack surface and data exposure risks.
- 🧪 Tests: Configuration validation ensures missing secrets block app startup.
- 📁 Files: Modified main.py and config.py.
- 🔁 Next prompts: Deployment execution.
- 🧠 Reflection: Forcing secrets to be non-optional is a best practice that prevents accidental fallback to insecure defaults in production.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
