# Running the servers (local development)

Clear steps to run the backend and frontend. Use this when setting up or when something fails to start.

---

## Prerequisites

- **Docker and Docker Compose** — for backend + database
- **Node.js 20+** and **npm** — for frontend
- **UV** (optional) — only if you run the backend locally without Docker

---

## 1. Run everything with Docker (recommended)

From the **repository root**:

```bash
docker compose up --build -d
```

- **Backend:** http://localhost:8000 — API docs: http://localhost:8000/docs  
- **Frontend:** http://localhost:3000  

Database migrations run automatically when the backend container starts (`alembic upgrade head` then uvicorn). No manual migration step is needed when using Docker.

**Stub OTP (testing):** With `APP_ENV=development` and stub codes set in docker-compose:
- **Parent:** Request OTP for any phone, then enter **123456** on the verify screen.
- **Staff:** Request OTP (same or different phone), then enter **654321** to log in as staff (teacher). Using **654321** on an existing parent account upgrades that account to staff for testing.

**Seeded data (E2E):** On first backend start, seed creates a parent and a staff user with sample tickets and announcements. To see them:
- **Parent with data:** phone **+15550000001**, OTP **123456** — 2 linked students, 3 tickets, 2 announcements.
- **Staff with data:** phone **+15550000002**, OTP **654321** — same tickets in staff inbox.

---

## 1b. Backend only (API + database)

From the **repository root**:

```bash
docker compose up --build
```

- **First run:** `--build` builds the backend and frontend images. Use `docker compose up -d` to run in background.
- **API base URL:** http://localhost:8000  
- **Health check:** http://localhost:8000/health  
- **API docs (Swagger):** http://localhost:8000/docs  

PostgreSQL runs in a container; the backend connects via `DATABASE_URL` set in `docker-compose.yml`. No local `.env` is required for this default setup.

---

## 2. Frontend (Next.js)

**Option A — with Docker:** Already running if you used `docker compose up --build -d`. Open http://localhost:3000.

**Option B — local npm:** From the **repository root**:

```bash
cd frontend
npm install
npm run dev
```

- **First run:** Always run `npm install` before `npm run dev` so dependencies are installed.
- **App URL:** http://localhost:3000  

The frontend talks to the backend at http://localhost:8000. To override, set `NEXT_PUBLIC_API_URL` in `frontend/.env.local`.

**Stop (npm):** `Ctrl+C` in the terminal where `npm run dev` is running.

---

## 3. Run both together

- **Docker:** `docker compose up --build -d` — then open http://localhost:3000 (frontend) and http://localhost:8000/docs (API).
- **Mixed:** Terminal 1: `docker compose up --build` (backend + DB). Terminal 2: `cd frontend && npm install && npm run dev`. Open http://localhost:3000.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| Backend shows only `/` and `/health` in Swagger | Rebuild with no cache: `docker compose build --no-cache backend` then `docker compose up`. |
| Frontend: `next: not found` or command not found | Run `npm install` inside `frontend/` so `node_modules/.bin/next` exists. Use `npm run dev`, not `npx next dev` (npx may pull a different Next version). |
| Frontend: port 3000 in use | Stop the process using 3000, or set `PORT=3001 npm run dev` to use another port. |
| Backend: DB connection failed | Ensure the `db` service is healthy. Run `docker compose up` and wait for "db is healthy" before the backend starts. |

---

## Optional: Backend without Docker

If you have PostgreSQL and UV installed locally:

```bash
cd backend
cp .env.example .env   # edit .env with your DATABASE_URL and JWT secrets
uv sync
uv run uvicorn app.main:app --reload
```

API will be at http://localhost:8000. Database must be running and migrations applied (`uv run alembic upgrade head`).
