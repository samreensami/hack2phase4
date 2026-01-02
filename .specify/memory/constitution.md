# SDD-RI AI Development Constitution (Phase 2)

## Core Principles

### I. Next.js Frontend Excellence
The frontend must be built using Next.js (App Router). All UI components should be modular, typed with TypeScript, and follow modern accessibility standards.

### II. FastAPI Backend Architecture
The backend services are powered by FastAPI. APIs must be RESTful, documented with OpenAPI (Swagger), and utilize Pydantic for data validation.

### III. Neon DB & Database integrity
Neon (Serverless Postgres) is the primary database. Use clear schemas, migrations for all changes, and follow security best practices for data storage and retrieval.

### IV. Type Safety (End-to-End)
Strict TypeScript on the frontend and Pydantic/Type Hints on the backend. No `any` types allowed unless strictly justified.

### V. Test-Driven Development (TDD)
Tests must accompany every feature. Integration tests between Next.js and FastAPI are mandatory before any major release.

## Technology Stack

- **Frontend**: Next.js (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.12, Pydantic
- **Database**: Neon (PostgreSQL)
- **Tooling**: Spec-Kit Plus, Claude Code

## Governance
This constitution supersedes all previous phase definitions. All architectural decisions must align with these principles.

**Version**: 2.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
