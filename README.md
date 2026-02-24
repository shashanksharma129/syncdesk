# School Communication & Helpdesk OS (V1)

Single-school communication and helpdesk system: structured, auditable communication replacing WhatsApp chaos. Parents submit tickets; staff (Director, Principal, VP, Teacher, Office, Transport) handle them with guardrails, internal notes, and one-way announcements.

## Stack

- **Backend:** FastAPI (Python 3.11), async SQLAlchemy, Alembic, PostgreSQL (Supabase-compatible)
- **Frontend:** Next.js (App Router, TypeScript), mobile-first PWA
- **Auth:** OTP + JWT (HTTP-only cookies)
- **Deploy:** Docker; backend suitable for Cloud Run; frontend for Vercel/Firebase

## Prerequisites

- [UV](https://docs.astral.sh/uv/) for Python
- Docker and Docker Compose
- Node.js 20+ (for frontend)
- WSL or Linux (tested on WSL2)

## Environment

- **Backend (Docker):** No `.env` needed for default `docker compose up`; compose sets `DATABASE_URL` and JWT secrets.
- **Backend (local UV):** Copy `backend/.env.example` to `backend/.env` and set `DATABASE_URL`, `JWT_ACCESS_SECRET`, `JWT_REFRESH_SECRET`.
- **Frontend:** Optional `frontend/.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`. See `frontend/.env.local.example`.

## Running the servers

**Full guide:** [docs/RUNNING.md](docs/RUNNING.md)

| What | Command (from repo root) | URL |
|------|---------------------------|-----|
| Backend + DB | `docker compose up --build` | API: http://localhost:8000 — Docs: http://localhost:8000/docs |
| Frontend | `cd frontend && npm install && npm run dev` | http://localhost:3000 |

Run backend first, then frontend in a second terminal. Always run `npm install` inside `frontend/` before `npm run dev`.

## Tests

- **Backend:** From `backend/`: `uv run pytest` (unit + integration). TDD; no mocks in production code paths.
- **Frontend:** From `frontend/`: `npm run test` (unit), `npm run test:e2e` (E2E when configured).
- **E2E:** Parent create ticket → staff resolve → parent satisfaction; see project spec.

## Project docs

- **[docs/RUNNING.md](docs/RUNNING.md)** — How to run backend and frontend (ports, troubleshooting)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) — Docker and Cloud Run deployment
- `spec.md` — Product and system specification
- `figma_ready_component_specs.md` — Design system and UI components
- `todo.md` — Backend checklist
- `todo_frontend.md` — Frontend checklist
- `prompt_plan.md` / `prompt_plan_frontend.md` — Build order

## CI (planned)

On push/PR: run backend tests (`cd backend && uv run pytest`), format check (`black --check`, `isort --check`), and lint (`ruff check`). Frontend: `npm run test` and `npm run lint`. No pipeline files in repo yet.

## License

Proprietary / internal use.
