# Skill: API Generator

## Purpose
Automate the synchronization of data models and API clients between the FastAPI backend and Next.js frontend in the monorepo.

## Logic
1. **Source**: FastAPI automatically generates an `openapi.json` at `/openapi.json` (or `/api/v1/openapi.json`).
2. **Action**: Fetch this JSON schema.
3. **Generation**: Parse the schema to generate TypeScript interfaces and a typed API fetch client.
4. **Destination**: Write generated files to `frontend/lib/generated/`.

## Usage
Run after any change to backend models:
`claude skill api-generator`

## Implementation Details
- Uses `datamodel-code-generator` or custom Jinja2 templates (as researched).
- Ensures `frontend` stays in sync with `backend` without manual type duplication.
