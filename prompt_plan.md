Below is a **carefully structured, end‑to‑end build blueprint** followed by **multiple rounds of decomposition**, ending in a **sequence of right‑sized, test‑driven prompts for a code‑generation LLM**.

This is designed so that:
- Each step is **safe**, **testable**, and **incremental**
- There are **no big jumps in complexity**
- Every piece is **wired into the system immediately**
- A junior dev + LLM or a senior dev alone could follow this

---

# PART 1: HIGH‑LEVEL BUILD BLUEPRINT

At the highest level, the system must be built in this order:

1. **Foundation**
   - Repo setup, tooling, CI mindset
   - FastAPI app skeleton
   - Database connection + migrations
   - Health checks

2. **Auth & Identity**
   - User model
   - OTP generation & verification
   - JWT sessions
   - Role enforcement

3. **Core Domain Models**
   - School, Student
   - Class‑Teacher mappings
   - Guardrail primitives (cooldowns, counters)

4. **Ticketing Core**
   - Ticket model & lifecycle
   - Guardrails
   - Routing logic
   - Replies & internal notes

5. **Announcements**
   - One‑way announcements
   - Targeting & read tracking

6. **Notifications**
   - Notification abstraction
   - WhatsApp + SMS hooks (mocked first)

7. **Operational Controls**
   - Abuse flags
   - Soft SLAs
   - Metrics & exports

8. **System Hardening**
   - Error handling
   - Audit logging
   - Background jobs

Each layer **must be usable before the next begins**.

---

# PART 2: FIRST DECOMPOSITION (FEATURE CHUNKS)

We now break the blueprint into **implementation chunks** that each:
- Deliver working functionality
- Can be tested independently
- Are deployable

### Chunk A: Backend Foundation
- FastAPI app
- Settings
- DB connection
- Health check

### Chunk B: Auth & Users
- User table
- OTP flow
- JWT sessions
- Role middleware

### Chunk C: Students & School Context
- Student model
- Parent ↔ student linking
- `school_id` enforcement

### Chunk D: Ticket Core
- Ticket model
- Status transitions
- Replies
- Internal notes

### Chunk E: Ticket Guardrails & Routing
- Limits
- Cooldowns
- Category routing

### Chunk F: Announcements
- Announcement model
- Targeting
- Read tracking

### Chunk G: Notifications (Abstracted)
- Notification service
- Mock WhatsApp/SMS

### Chunk H: Admin Controls & Metrics
- Abuse flags
- Metrics queries
- Weekly report logic

---

# PART 3: SECOND DECOMPOSITION (ENGINEERING‑SIZED STEPS)

Now we break each chunk into **small, safe steps** suitable for TDD.

I’ll show this for the **entire system**, then we’ll convert it into prompts.

---

## CHUNK A: BACKEND FOUNDATION

A1. Create FastAPI app skeleton  
A2. Environment & settings management  
A3. Database connection (SQLAlchemy)  
A4. Alembic migrations  
A5. Health check endpoint  

✅ Result: Deployed backend that responds to `/health`

---

## CHUNK B: AUTH & USERS

B1. User SQLAlchemy model  
B2. OTP model & hashing  
B3. OTP request endpoint  
B4. OTP verification endpoint  
B5. JWT issuance & refresh  
B6. Auth dependency + role checking  

✅ Result: Logged‑in users with roles

---

## CHUNK C: STUDENTS & SCHOOL CONTEXT

C1. Student model  
C2. Parent‑student linking table  
C3. Fetch parent’s students API  
C4. Admin correction APIs  

✅ Result: Parents see their children

---

## CHUNK D: TICKET CORE

D1. Ticket model  
D2. Ticket status enum & transitions  
D3. Create ticket endpoint (no guardrails yet)  
D4. Ticket reply endpoint  
D5. Internal notes (staff‑only)  

✅ Result: Tickets work end‑to‑end

---

## CHUNK E: GUARDRAILS & ROUTING

E1. Open ticket count enforcement  
E2. Cooldown enforcement  
E3. Weekly cap enforcement  
E4. Reopen limit enforcement  
E5. Category‑based routing  

✅ Result: Abuse‑resistant ticketing

---

## CHUNK F: ANNOUNCEMENTS

F1. Announcement model  
F2. Create announcement API  
F3. Targeting logic  
F4. Read tracking logic  

✅ Result: One‑way announcements working

---

## CHUNK G: NOTIFICATIONS

G1. Notification interface  
G2. Web notification persistence  
G3. Mock WhatsApp sender  
G4. Retry & fallback logic  

✅ Result: Notifications observable & testable

---

## CHUNK H: ADMIN & OPS

H1. Abuse flagging  
H2. Metrics queries  
H3. Weekly report job  
H4. Export logic  

✅ Result: Operational visibility

---

# PART 4: FINAL DECOMPOSITION → LLM PROMPTS

Below is the **final output you asked for**:  
a **series of prompts**, each:
- Small enough to implement safely
- Test‑driven
- Building on previous prompts
- Fully wired (no orphan code)

Each prompt is wrapped in **code tags** as requested.

---

## PROMPT 1: Project Skeleton & Health Check

```text
You are building the backend for a School Communication & Helpdesk OS using FastAPI.

Task:
1. Create a FastAPI project skeleton with:
   - app/main.py
   - app/core/config.py (Pydantic BaseSettings)
   - app/core/logging.py
2. Add a /health endpoint that returns {"status": "ok"}
3. Add pytest setup and write a test that asserts /health returns 200 and correct JSON.

Constraints:
- Use FastAPI
- No database yet
- Code must be runnable
- Tests must pass

Output:
- All necessary files
- Tests included
```

---

## PROMPT 2: Database Setup & Migrations

```text
Extend the existing FastAPI project.

Task:
1. Add SQLAlchemy async setup with PostgreSQL
2. Add Alembic configuration
3. Create a base declarative model
4. Add a startup hook that checks DB connectivity
5. Write a test that verifies the app starts with a test database

Constraints:
- Use SQLAlchemy 2.x style
- No models yet
- Migrations must run

Do not modify unrelated files.
```

---

## PROMPT 3: User & OTP Models

```text
Add authentication data models.

Task:
1. Create User model with:
   - id
   - phone
   - role
   - school_id
2. Create OTP model with:
   - phone
   - hashed_code
   - expires_at
3. Add Alembic migration
4. Write unit tests for model constraints

Constraints:
- No endpoints yet
- Password/OTP must be hashed
```

---

## PROMPT 4: OTP Auth Flow

```text
Implement OTP authentication.

Task:
1. POST /auth/request-otp
2. POST /auth/verify-otp
3. Generate single-use OTP expiring in 5 minutes
4. Issue JWT on success
5. Write tests for:
   - OTP expiry
   - Invalid OTP
   - Successful login

Constraints:
- No external SMS calls
- Stub OTP sending
```

---

## PROMPT 5: Role‑Based Access Control

```text
Add authorization.

Task:
1. Create auth dependency that extracts user from JWT
2. Add role-based guard (e.g., require_role)
3. Write tests for forbidden access

Do not add new endpoints.
```

---

## PROMPT 6: Student & Parent Linking

```text
Add student context.

Task:
1. Create Student model
2. Create parent_student linking table
3. GET /me/students endpoint
4. Tests:
   - Parent sees own students
   - Cannot see others

Constraints:
- Enforce school_id
```

---

## PROMPT 7: Ticket Core

```text
Implement ticket basics.

Task:
1. Ticket model with status enum
2. POST /tickets
3. GET /tickets/{id}
4. POST /tickets/{id}/reply
5. Tests for full ticket lifecycle

Constraints:
- No guardrails yet
```

---

## PROMPT 8: Guardrails & Routing

```text
Add ticket guardrails.

Task:
1. Enforce max open tickets
2. Enforce cooldown
3. Enforce weekly cap
4. Implement category routing
5. Tests for each rule

Constraints:
- Errors must be user-friendly
```

---

## PROMPT 9: Internal Notes & Reopen Logic

```text
Extend ticketing.

Task:
1. Internal notes (staff-only)
2. Reopen request flow
3. Enforce reopen limits
4. Tests for visibility & limits
```

---

## PROMPT 10: Announcements

```text
Implement announcement engine.

Task:
1. Announcement model
2. POST /announcements
3. GET /announcements (targeted)
4. Read tracking logic
5. Tests for targeting & reads
```

---

## PROMPT 11: Notifications Abstraction

```text
Add notifications.

Task:
1. Notification interface
2. Web notification persistence
3. Mock WhatsApp sender
4. Retry & fallback logic
5. Tests using mocks
```

---

## PROMPT 12: Metrics & Ops

```text
Add admin operations.

Task:
1. Abuse flagging
2. Metrics queries
3. Weekly report generator (callable function)
4. Tests for metrics correctness
```

---
