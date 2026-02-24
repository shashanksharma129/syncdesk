# Backend deployment (GCP / Docker)

## Docker (local or any host)

- Build: `docker compose build`
- Run: `docker compose up` (Postgres + backend)
- Backend listens on port 8000; ensure `DATABASE_URL`, `JWT_ACCESS_SECRET`, `JWT_REFRESH_SECRET` are set (see `backend/.env.example`).

## Cloud Run (GCP)

- Build and push image to Artifact Registry (or use Cloud Build).
- Deploy with:
  - Min instances: 0
  - Max instances: 10
  - Set env vars from Secret Manager or env: `DATABASE_URL`, `JWT_ACCESS_SECRET`, `JWT_REFRESH_SECRET`, `DEFAULT_SCHOOL_ID`, optional `OFFICE_HOURS_*`, `SENTRY_DSN`, etc.
- Use a VPC connector if DB is in VPC; or allow Cloud SQL public IP and set `DATABASE_URL` accordingly.

## Secret management

- Do not commit `.env`. Use Cloud Run env vars or Secret Manager for production.
- Required: `JWT_ACCESS_SECRET`, `JWT_REFRESH_SECRET`, `DATABASE_URL`.

## Rollout checklist

- Run migrations: `alembic upgrade head` (in job or before app start).
- Seed test users/students if needed (see seed script or admin).
- Verify health: `GET /health` returns 200.
