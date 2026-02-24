# School Communication & Helpdesk OS — V1 TODO

This checklist follows the frozen V1 spec.
Do not skip steps. Each section should be complete before moving on.

---

## ✅ 0. Repo & Tooling Setup

- [x] Initialize Git repository
- [x] Add `.gitignore` (Python, Node, env files)
- [x] Add `README.md` (high-level project overview)
- [x] Add `todo.md` (this file)
- [x] Choose Python version (3.11 recommended)
- [x] Set up virtualenv (UV)
- [x] Add `.env.example`
- [x] Configure formatting: black, isort, ruff
- [x] Configure testing: pytest, pytest-asyncio
- [x] Basic CI plan (even if not implemented yet)
- [x] Docker (Dockerfile + docker-compose for DB + backend)

---

## ✅ 1. Backend Foundation (FastAPI)

- [x] Create FastAPI app skeleton (app/main.py, api/, core/, models/, services/)
- [x] Add configuration system (Pydantic BaseSettings)
- [x] Add structured logging
- [x] Add `/health` endpoint
- [x] Write test for `/health`
- [x] Run app locally and verify health check

---

## ✅ 2. Database & Migrations

- [x] Set up async SQLAlchemy
- [x] Set up Alembic
- [x] Create declarative base model
- [x] Add DB session dependency
- [x] Add startup DB connectivity check
- [x] Create test database configuration
- [x] Write test verifying DB connection

---

## ✅ 3. Core Identity Models

- [x] Create `User` model (id, phone, role, school_id, created_at, name, email, restricted_to_admin_until, ticket_creation_blocked_until)
- [x] Create `OTP` model (phone, hashed_code, expires_at, used)
- [x] Add Alembic migration
- [x] Unit tests for model constraints

---

## ✅ 4. OTP Authentication Flow

- [x] OTP generator utility
- [x] OTP hashing & verification (SHA256)
- [x] POST `/auth/request-otp`
- [x] POST `/auth/verify-otp`
- [x] OTP expiry enforcement (5 minutes)
- [x] Single-use OTP enforcement
- [x] Stub OTP delivery (log/console)
- [x] Tests: invalid OTP, expired OTP, successful login

---

## ✅ 5. Session & Authorization

- [x] JWT access token generation (15 min)
- [x] JWT refresh secret in config (7–30 days ready)
- [x] Auth dependency (`get_current_user`)
- [x] Role-based access decorator (`require_roles`)
- [x] GET `/me`
- [x] Tests for role enforcement

---

## ✅ 6. Student & Parent Linking

- [x] Create `Student` model
- [x] Create parent-student linking table
- [x] Enforce `school_id` everywhere
- [x] GET `/me/students`
- [ ] Admin APIs for silent corrections (deferred)
- [x] Tests: parent sees own students

---

## ✅ 7. Ticket Core Models

- [x] Create `Ticket` model (category, status, urgency, assigned_to, school_id, known_issue, abuse_flagged, escalation_snoozed_until, deleted_at, satisfied_at)
- [x] Create `TicketMessage` model
- [x] Create `InternalNote` model
- [x] Create `TicketReopen` model
- [x] Alembic migrations
- [x] Unit tests for status transitions

---

## ✅ 8. Ticket Core APIs

- [x] POST `/tickets`
- [x] GET `/tickets`, GET `/tickets/{id}`
- [x] POST `/tickets/{id}/reply`
- [x] Staff-only internal notes endpoint
- [x] Auto-move status to In Progress on staff reply
- [x] PATCH `/tickets/{id}/status`, POST `/tickets/{id}/reopen`, POST `/tickets/{id}/satisfied`
- [x] PATCH `/tickets/{id}/known-issue` (transport)
- [x] Tests: parent ticket creation, staff reply, visibility rules

---

## ✅ 9. Ticket Guardrails (Critical)

- [x] Max 3 open tickets enforcement
- [x] 30-minute cooldown enforcement
- [x] Max 5 tickets / 7-day rolling window
- [x] Max 1 open "Other" ticket
- [x] Max 2 reopen requests per ticket
- [x] Urgent only Transport/Health & Safety, 1/week
- [x] User-friendly error messages
- [x] Tests for each guardrail

---

## ✅ 10. Ticket Routing & Urgency

- [x] Category → role routing rules (routing.py)
- [x] Urgent ticket restrictions (in guardrails)
- [ ] Default assignee logic (deferred)
- [ ] Manual reassignment (admin) (deferred)

---

## ✅ 11. Reopen & Satisfaction Flow

- [x] Satisfaction confirmation after resolve (POST `/tickets/{id}/satisfied`)
- [x] Reopen request endpoint
- [x] Reopen limit enforcement
- [x] Staff PATCH status to resolved
- [ ] Escalation on excessive reopens (deferred)

---

## ✅ 12. Announcements Engine

- [x] Create `Announcement` and `AnnouncementRead` models
- [x] POST `/announcements`, GET `/announcements`
- [x] Targeting (audience: parents/staff/both)
- [x] Read tracking (POST `/announcements/{id}/read`)
- [ ] Rate limit 2/day/role (deferred)
- [x] Tests for targeting & reads

---

## ✅ 13. Notifications System

- [x] Notification interface (NotificationSender)
- [x] Stub sender (log only)
- [ ] Web notification persistence (deferred)
- [ ] Real WhatsApp/SMS when env set (documented in .env.example)

---

## ✅ 14. Transport-Specific Features

- [x] Known issue flag on ticket
- [x] PATCH `/tickets/{id}/known-issue`
- [x] TransportBroadcast model for rate limiting
- [x] Footer auto-append ("No action required from parents.")
- [ ] Route broadcast API (deferred)

---

## ✅ 15. Abuse & Safety Controls

- [x] Abuse flag on ticket (POST `/tickets/{id}/flag-abuse`)
- [x] GET `/admin/abuse-flagged` (Director)
- [x] Admin-only parent restriction (POST `/admin/users/{id}/restrict`)
- [x] Temporary ticket lock (POST `/admin/users/{id}/block-tickets`)
- [x] Audit log on abuse flag

---

## ✅ 16. Response Guidelines (Soft SLA)

- [ ] Category-based response targets (config only; no reminder job yet)
- [ ] Reminder scheduling logic (deferred)
- [x] Ticket.escalation_snoozed_until (model ready)
- [ ] VP snooze API (deferred)

---

## ✅ 17. Office Hours Handling

- [x] Office hours configuration (config)
- [x] GET `/config/office-hours` (banner for off-hours)
- [ ] Category-based enforcement (deferred)

---

## ✅ 18. Data Retention & Exports

- [x] Soft delete only (Ticket.deleted_at)
- [x] GET `/admin/export/tickets` (watermark)
- [ ] Logical archive after 2 years (deferred)
- [ ] Password-protected ZIP (deferred)

---

## ✅ 19. Metrics & System Health

- [x] GET `/admin/metrics` (tickets, resolved, reopens, announcement reads)
- [ ] Weekly director report generator (deferred)

---

## ✅ 20. File Storage (GCS)

- [ ] GCS bucket setup (deferred)
- [ ] Signed upload/download URLs (deferred)
- [x] Documented in .env.example

---

## ✅ 21. Error Handling & Logging

- [x] Centralized exception handling (global handler in main)
- [x] User-safe error messages
- [x] Structured logging
- [x] Audit logs (AuditLog model + log_audit on abuse flag)

---

## ✅ 22. End-to-End Testing

- [x] Parent ticket flow (create → staff resolve → parent satisfied)
- [ ] Announcement visibility E2E (deferred)
- [ ] Abuse escalation E2E (deferred)

---

## E2E / Stub login (testing)

- [x] Stub OTP for parent (123456) — doc in RUNNING.md
- [x] Stub OTP for staff (654321) — creates/upgrades user to teacher; doc in RUNNING.md and .env.example
- [ ] Optional: seed script or second phone for staff E2E without upgrading same phone

---

## ✅ 23. Deployment Prep (GCP)

- [x] Dockerfile
- [x] docker-compose (DB + backend)
- [x] Environment variables (.env.example)
- [x] docs/DEPLOYMENT.md (Cloud Run, secrets)
- [ ] Manual deploy test (user)

---

## ✅ 24. Rollout Readiness

- [ ] Seed test data (optional script)
- [ ] Pilot class setup
- [ ] Admin walkthrough
- [ ] Go-live checklist

---

**Next:** Frontend (see `todo_frontend.md` and `prompt_plan_frontend.md`).

✅ **Only move to the next section when all items in the current section are complete.**
