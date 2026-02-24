You are building the **School Communication & Helpdesk OS (V1)** in a single, full run. Your job is to produce a working application (backend + frontend) by following the project's specification and step-by-step plans, and by using the todo checklists as the source of truth.

---

## 1. Project summary

Single-school communication and helpdesk system: replace WhatsApp chaos with structured, auditable communication. Stack: **FastAPI (Python)** backend, **Next.js (App Router, TypeScript)** frontend, **PostgreSQL** (Supabase-compatible), OTP + JWT auth, ticketing with guardrails, one-way announcements, role-based access (Director, Principal, VP, Teacher, Office, Transport, Parent). Full product and technical details are in **spec.md** — read and follow it.

---

## 2. Document map (read these files)

| File | Role |
|------|------|
| **spec.md** | Authoritative product and system spec. Implement exactly this. |
| **figma_ready_component_specs.md** | Design system: colors, typography, components, mobile-first (360×800). Build all UI to this. |
| **prompt_plan.md** | Backend build order (chunks A–H, steps A1–H4). Follow this sequence. |
| **prompt_plan_frontend.md** | Frontend build order (Prompts 1–19). Follow this sequence. |
| **todo.md** | Backend checklist (sections 0–24). Complete in order; use as progress source of truth. |
| **todo_frontend.md** | Frontend checklist (sections 0–23). Complete in order; use as progress source of truth. |

---

## 3. Environment and tooling (mandatory)

- **Environment variables**: The user will provide a **.env** file (and, for the frontend, **.env.local** if needed) with all required keys and values. You must:
  - **Assume .env exists** and that the app runs with these variables set.
  - **Document** every required variable in **.env.example** (and frontend equivalent) with short comments. No hardcoded secrets; read everything from env.
- **Python**: Use **UV** for virtual environment creation and dependency management (install deps with `uv`, run commands in the UV-managed environment). This is a WSL environment; use UV as the standard way to manage the backend Python environment.
- **Running the project**: Use **Docker** to run the application (e.g. backend, PostgreSQL, and optionally frontend). Provide a way to run the full stack via Docker (e.g. `docker compose up` or equivalent). The app should be buildable and runnable in WSL using Docker and UV.

---

## 4. Build order (do not reorder)

1. **Repo and tooling**  
   Initialize repo, .gitignore, README, **.env.example** (and frontend env example). Set up **UV** for the backend. Set up **Docker** (e.g. Dockerfile for backend, docker-compose for DB + backend + optional frontend). Configure formatting (black, isort, ruff) and pytest (+ pytest-asyncio). Match **todo.md** section 0.

2. **Backend (full)**  
   Implement the backend strictly in the order of **prompt_plan.md** (Chunks A → H) and **todo.md** (sections 1–24):  
   Foundation (FastAPI skeleton, config, health) → DB + migrations (SQLAlchemy async, Alembic) → User & OTP models → OTP auth flow → RBAC → Students & parent linking → Ticket core (model, APIs, replies, internal notes) → Guardrails & routing → Reopen & satisfaction → Announcements → Notifications (interface + real integrations when env is set; document env vars) → Admin/ops (abuse, metrics, weekly report).  
   Every step must be test-driven; add unit and integration tests as you go. Mark progress in **todo.md** if you update it.

3. **Frontend (full)**  
   Implement the frontend strictly in the order of **prompt_plan_frontend.md** (Prompts 1–19) and **todo_frontend.md** (sections 0–23):  
   Next.js skeleton, app shell, layout → Design system and UI primitives per **figma_ready_component_specs.md** → Auth screens (login, OTP) → Auth state and route protection → Parent profile and student context → Ticket list and detail → Create ticket flow → Guardrail UX → Reopen and satisfaction → Announcements → Staff dashboard and inbox → Staff ticket detail and internal notes → Transport-specific UI → Notifications UI → Office hours and soft SLA UX → Error handling and resilience → **Wire all flows to the real backend APIs** → PWA and launch prep.  
   Use the design system (colors, typography, components, status badges, empty states) from **figma_ready_component_specs.md**. Mobile-first everywhere. Mark progress in **todo_frontend.md** if you update it.

4. **Integration and launch**  
   Ensure frontend uses the real backend (no mocks). Add E2E tests (e.g. parent creates ticket, staff resolves, parent satisfaction). Verify Docker-based run and document in README how to run with UV and Docker in WSL.

---

## 5. Design and UX

- Follow **figma_ready_component_specs.md** for all UI: color palette, typography (e.g. Inter), spacing (8px), components (Button, Input, Select, Textarea, Badge, Alert, TicketCard, MessageBubble, etc.), status colors (Pending, In Progress, Resolved, Urgent).
- Mobile-first; touch targets ≥44px; calm, professional language; no blame in guardrail messages.
- Copy from the spec: e.g. "This ticket is about: Child A, Child B", "Some student details are maintained by the school", "Internal notes are part of permanent records", "No action required from parents" (transport), etc.

---

## 6. Testing (non-negotiable)

- **TDD**: Write failing tests first, then implementation; refactor with tests green.
- **Unit tests**: Guardrails, permissions, status transitions, OTP logic, model constraints.
- **Integration tests**: Auth flow, routing, notifications, DB.
- **End-to-end tests**: Parent creates ticket → staff resolves → parent confirms; announcement visibility; abuse escalation where applicable.
- **Test output**: Must be pristine; no marking test types as "not applicable". If something is not implemented yet, implement it so tests exist and pass.

---

## 7. What "done" looks like

- Backend: FastAPI app with health, auth (OTP + JWT), students, tickets (with guardrails, routing, internal notes, reopen), announcements (with targeting and read tracking), notifications (real when env set), and admin/ops features. All runnable with UV and Docker.
- Frontend: Next.js app with auth, parent and staff flows, ticket list/detail/create, guardrail UX, announcements, staff inbox and internal notes, transport UI, notifications, error handling, wired to backend. PWA-ready.
- **.env.example** (and frontend env example) listing every required variable with brief comments.
- README with: how to set up .env, how to use UV for backend, how to run the stack with Docker in WSL, and how to run tests.
- No mocks in production code paths; use real APIs and real integrations when the user supplies env vars (document which vars are needed for OTP, SMS, WhatsApp, DB, etc.).
