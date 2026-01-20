# Phase 2 Implementation Guide - Complete Prompt Collection

## Pre-Phase 2: Infrastructure Setup

### Prompt 1: Initialize Phase 2 Foundation
```
Phase 2 shuru karo. Pehle ye infrastructure setup karo:

Constitution Update: .specify/memory/constitution.md ko Phase 2 ke tech stack (Next.js, FastAPI, Neon DB) ke liye update karo.

History Folder: Root mein history/prompts/ directory banao.

Agent Memory: .specify/memory/agents/ folder banao aur wahan wo 5 agents (spec-writer.md, architecture-planner.md, etc.) create karo jo humne discuss kiye hain.

Project Structure: Ensure karo frontend/ aur backend/ folders ready hain.
```

## Phase 2.1: Specification Writing

### Prompt 2: Write Full-Stack Specifications
```
/sp.specify using the spec-writer agent.

Task: specs/features/task-web-app.md aur specs/api/rest-endpoints.md likho.

Rules (From Article):

Quality Criteria: Har feature ke liye 'Acceptance Criteria' lazmi dalo.

Process: Pehle user stories likho, phir technical constraints (Next.js 16+, FastAPI, Neon DB).

API Design: Better Auth JWT integration ke mutabiq saare endpoints define karo.

Save context to: history/prompts/02-specifications.md.
```

## Phase 2.2: Architecture Planning

### Prompt 3: Design System Architecture
```
/sp.plan using the architecture-planner agent.

Task: specs/1-task-web-app/plan.md generate karo jo in cheezon ko cover kare:

Monorepo Structure: Frontend aur Backend folders ke darmiyan shared types aur environment variables (.env) kaise handle honge.

Auth Flow: Better Auth frontend par aur JWT verification backend par kaise link hogi.

Database: Neon PostgreSQL connection string aur SQLModel migrations ka setup.

Skill Link: .claude/skills/api-generator skill ko use karne ka logic dalo.

History: Is plan ka record history/prompts/03-planning.md mein save karo.
```

## Phase 2.3: Task Generation

### Prompt 4: Break Down Into Atomic Tasks
```
/sp.tasks using the task-generator agent.

Goal: Plan ko implementable tasks mein convert karo.

Backend Tasks: Setup FastAPI, SQLModel models, aur Neon DB connection.

Auth Tasks: Better Auth configuration aur JWT verification middleware.

Frontend Tasks: Next.js UI components aur API client integration.

History: Tasks list ko history/prompts/04-task-breakdown.md mein record karo.
```

## Phase 2.4: Infrastructure Implementation

### Prompt 5: Setup Foundation
```
/sp.implement using the implementation-agent.

Focus: Phase 1 (Monorepo Setup) aur Phase 2 (Foundational Infrastructure) ke tasks mukammal karo.

Skill Integration: Coding shuru karne se pehle .claude/skills/api-generator/SKILL.md banao jaisa article mein bataya gaya hai.

Backend: FastAPI aur SQLModel ki basic configuration backend/ folder mein setup karo.

Frontend: Next.js ka folder structure aur basic layout frontend/ mein initialize karo.

QA Check: Har task ke baad qa-agent ko bula kar verify karwao.

History: Progress ko history/prompts/05-implementation-start.md mein save karo.
```

## Phase 2.5: Database Connection

### Prompt 6: Connect Neon DB
```
Ab Neon DB connection setup karo.

Environment Variable: Root mein .env file banao aur usme DATABASE_URL='your-neon-connection-string' dalo.

Backend Config: backend/database.py mein SQLModel engine create karo jo is URL ko use kare.

Validation: Ek chota script chalao jo check kare ke connection 'Live' hai ya nahi.

Skill Usage: Is connection logic ko api-generator skill ka hissa banao.

History: Result ko history/prompts/06-db-connection.md mein save karo.
```

## Phase 2.6: Models & Migrations

### Prompt 7: Setup Data Models
```
Ab User models aur migrations setup karo.

Models: backend/models/ mein User aur Task ke SQLModel classes banao.

Alembic: Migration framework initialize karo aur pehli revision generate karo.

Apply: Alembic migration ko Neon DB par run karke tables create karo.

Verification: Check karo ke Neon dashboard par tables nazar aa rahi hain.

History: Progress ko history/prompts/07-models-migrations.md mein save karo.
```

## Phase 2.7: Authentication Setup

### Prompt 8: Implement Auth APIs
```
Haan, Authentication APIs shuru karo.

Backend Engineer Agent: backend/routes/auth.py banao aur wahan Register aur Login ke endpoints define karo.

Security: Password hashing ke liye passlib use karo aur JWT token generate karne ka mechanism dalo.

Integration Tester Agent: Ensure karo ke user registration ke baad data sahi tarah Neon DB mein save ho raha hai.

Skill Usage: api-generator skill ko use karo taake auth responses (tokens) frontend ke liye standard hon.

History: Result ko history/prompts/08-auth-api-setup.md mein record karo.
```

## Phase 2.8: Task CRUD Operations

### Prompt 9: Build Core Functionality
```
Haan, Task CRUD APIs (Phase 4) shuru karo.

Backend Engineer Agent: backend/routes/tasks.py banao aur ye endpoints define karo:

POST /tasks: Naya task create karne ke liye.

GET /tasks: User ke apne saare tasks fetch karne ke liye.

PUT /tasks/{id}: Task update karne ke liye.

DELETE /tasks/{id}: Task remove karne ke liye.

Security & Ownership: Har endpoint par JWT verification middleware lazmi lagao. Ensure karo ke user sirf apne hi tasks access ya modify kar sake.

Skill Usage: api-generator skill ka istemal karo taake frontend ke liye task_types.ts generate ho jaye.

History: Result ko history/prompts/09-task-crud-setup.md mein record karo.
```

## Phase 2.9: Frontend UI

### Prompt 10: Build User Interface
```
Ab Frontend Dashboard aur Auth UI (Phase 3 & 4) shuru karo.

Frontend Engineer Agent: Next.js mein ye components aur pages banao:

Auth Pages: /login aur /register pages jahan user login kar sake.

Dashboard: Aik main page jahan user apne tasks ki list dekh sake aur naye tasks add kar sake.

State Management: Authentication token (JWT) ko handle karne ke liye local storage ya cookies ka istemal karo.

API Integration: Pehle se generated auth_types.ts aur task_types.ts ko use karte hue backend endpoints ko call karo.

Skill Usage: ui-generator skill (agar mojud hai) ko use karo taake Tailwind CSS ke sath ek saaf aur modern interface bane.

History: Is progress ko history/prompts/10-frontend-ui-setup.md mein record karo.
```

## Phase 2.10: Advanced Features

### Prompt 11: Add Categorization
```
Ab Phase 5 (US3: Task Categorization) shuru karo.

Architecture Planner Agent: Category ka naya model design karo aur Task model ke sath uska relationship (Foreign Key) define karo.

Backend Engineer Agent:

Backend models mein category field add karo.

Alembic migration run karke database schema update karo.

Tasks CRUD endpoints ko update karo taake wo category support karein.

Frontend Engineer Agent: Dashboard par category filter aur task creation form mein category dropdown add karo.

Skill Usage: api-generator skill ko dubara chalao taake naye schema ki types frontend mein update ho jayein.

History: Progress ko history/prompts/11-task-categorization.md mein record karo.
```

## Phase 2.11: Polish & Verification

### Prompt 12: Final Polish
```
Ab Phase 6 (Polish & Deployment Verification) shuru karo.

Code Polishing: Poore codebase mein unused imports aur console logs ko saaf karo.

README Update: Project ki main README file likho jisme setup instructions, tech stack (Next.js, FastAPI, Neon DB), aur features ka zikr ho.

Deployment Prep:

Frontend ke liye vercel.json ya zaroori build scripts check karo.

Backend ke liye Dockerfile ya Render deployment ki requirements verify karo.

Final QA: qa-agent ko active karo taake wo ek akhri baar poore flow (Register -> Login -> Create Task -> Filter by Category) ko verify kare.

History: Final status ko history/prompts/12-final-polish.md mein record karo.
```

## Phase 2.12: Security Hardening

### Prompt 13: Production Security
```
Hardening security for production deployment.

JWT Secret: .env mein cryptographically secure JWT_SECRET generate karo (openssl rand -base64 32).

CORS Lockdown: backend/main.py mein CORSMiddleware ko strict production domains par set karo.

Environment Validation: Ensure karo ke app start na ho agar zaroori env variables missing hon.

Security Headers: X-Content-Type-Options, HSTS jaise headers add karo.

Skill Update: security-hardener skill ko Intelligence Library mein add karo.

History: Final security audit ko history/prompts/13-security-hardening.md mein save karo.
```

## Phase 2.13: Deployment

### Prompt 14: Deploy to Production
```
Ab project ko GitHub par push karo taake hum deployment shuru kar saken.

Safety First (.gitignore): Ensure karo ke .env, __pycache__, .pytest_cache, aur node_modules jaisi files git mein shamil NA hon.

Git Initialization: Agar repo initialize nahi hai toh git init karo.

Remote Setup: Is repository ko remote origin ke taur par add karo: https://github.com/samreensami/hack2-phase2.git.

Final Commit: Saare hardened files ko add karo aur commit message likho: 'feat: complete hardened full-stack task app with neon db'.

Push: Code ko main branch par push karo.

History: Is push ka record history/prompts/14-github-push.md mein save karo.
```

## Expert Tips

1. **Agent Memory**: Har agent ki memory file (.specify/memory/agents/*.md) mein uska specific role, quality criteria, aur process steps clearly defined hain.

2. **Skills Library**: .claude/skills/ folder mein reusable logic hai jo future phases mein bhi kaam aayegi.

3. **No Manual Coding**: Poora implementation agents ke zariye hoga, jo "Designing Reusable Intelligence" framework ka core principle hai.

4. **History Tracking**: Har step ka prompt history/prompts/ mein save hoga taake aapka kaam scannable aur auditable ho.

## Checkpoint Sequence
- [ ] Infrastructure ready (agents, folders, constitution)
- [ ] Specification written (/sp.specify)
- [ ] Architecture planned (/sp.plan)
- [ ] Tasks generated (/sp.tasks)
- [ ] Foundation implemented (DB, Auth)
- [ ] CRUD APIs working
- [ ] Frontend UI functional
- [ ] Categories & filters added
- [ ] Code polished
- [ ] Security hardened
- [ ] Deployed to production

**Current Status**: Ready to start Phase 2 infrastructure setup.
