Below is the **final, frozen, developer‑ready V1 specification**, updated to **Python + FastAPI + GCP (free‑tier optimized)** and incorporating **all product decisions and all hole‑poking fixes**.

This is the version you can **hand to a developer and start building immediately**.

---

# School Communication & Helpdesk OS  
**V1 — FINAL DEVELOPER SPEC (Python + GCP)**

**School Context**
- Single English‑medium school
- Etawah, Uttar Pradesh
- Nursery → Class 8
- ~1500 students
- Goal: Replace WhatsApp chaos with structured, auditable communication

---

## 1. Product Principles (NON‑NEGOTIABLE)

1. No free‑form chat
2. Teachers are protected from noise
3. Parents feel heard but cannot spam
4. Everything is auditable
5. Mobile‑first UX
6. Behavioral guardrails are first‑class features

---

## 2. Platform Scope (V1)

### Platforms
- ✅ Responsive Web Portal (Parents)
- ✅ Responsive Web Dashboard (Staff/Admin)

### Out of Scope
- Native Android / iOS apps
- AI routing or auto‑responses

---

## 3. Architecture Overview

### Frontend
- **Next.js (React)**
- Mobile‑first, PWA‑ready
- Hosted on **Vercel (Free)** or **Firebase Hosting**

### Backend
- **FastAPI (Python)**
- Containerized & deployed on **Google Cloud Run**
- Async, API‑first design

### Database
- **PostgreSQL**
  - **Supabase Free Tier** (V1)
  - Cloud SQL Postgres later (drop‑in)

### Cache / Rate Limiting
- No Redis (cost‑optimized)
- In‑memory TTL cache + Postgres tables

### File Storage
- **Google Cloud Storage (Free Tier)**
- Signed URLs for uploads/downloads

### Auth
- OTP + JWT
- HTTP‑only cookies
- Magic‑link login

### Integrations
- WhatsApp Business API
- SMS Gateway (OTP + fallback)

### Logging & Monitoring
- GCP Cloud Logging (Free)
- Optional Sentry (Free)

### Future‑Proofing
- `school_id` in all tables
- Versioned class‑teacher mappings
- Routing rules engine isolated

---

## 4. Authentication & Session Management

### Login
- Mobile number + OTP
- **OTP magic link**
  - Single‑use
  - Expires in 5 minutes
  - Soft‑bound to device/IP

### Sessions
- JWT access token (15 min)
- Refresh token (7–30 days)
- Auto‑logout after 7 days inactivity
- Max session length: 30 days
- Visible logout button
- Optional PIN for ticket creation

---

## 5. User Roles & Permissions

| Role | Access |
|---|---|
| Director | Full visibility, exports |
| Principal | Fees, transport, escalations |
| Vice Principal | Discipline, safety |
| Teacher | Assigned tickets only |
| Office Staff | Infra, documents |
| Transport Manager | Transport tickets |
| Parent | Own tickets only |

---

## 6. Parent Onboarding & Profile

### Onboarding
- Parent‑first self signup
- Auto‑link student on match
- Immediate access
- Admin silent corrections allowed

### Editable Fields
**Parent**
- Name
- Email (optional)

**Admin only**
- Phone
- Linked students
- Admission details

Banner:
> “Some student details are maintained by the school.”

---

## 7. Announcement Engine (One‑Way)

### Capabilities
- Read‑only
- No replies/reactions

### Permissions
- Director
- Principal
- Vice Principal

### Targeting
- School / Grade / Class
- Parents / Staff / Both

### Content
- Plain text + basic formatting
- Max 1 attachment (PDF/image ≤5MB)

### Read Tracking
- Count as read if visible ≥3 seconds
- Admin sees aggregate %
- Parents never see read receipts

### Rate Limit
- Max 2 announcements/day/role
- Emergency override

### Archival
- Auto‑archive after 30 days
- Optional expiry date

---

## 8. Ticketing System (Core)

### Ticket Creation (Parent)

**Mandatory**
- Child / children (confirmation required)
- Category

**Optional**
- Title
- Description
- Attachment
- Urgency (restricted)

Confirmation:
> “This ticket is about: Child A, Child B”

---

## 9. Ticket Guardrails (STRICT)

- Max **3 open tickets**
- **30‑minute cooldown**
- Max **1 open ‘Other’ ticket**
- Max **5 tickets per parent per 7‑day rolling window**
- Max **2 reopen requests per ticket**

---

## 10. Ticket Categories & Routing

| Category | Routing |
|---|---|
| Academic – Teaching/Homework | Teacher |
| Academic – Exam/Policy | Vice Principal |
| Discipline | Vice Principal |
| Attendance / Leave | Teacher / Office |
| Fee & Accounts | Principal / Office |
| Transport | Transport Manager |
| Health & Safety | Vice Principal |
| Cleanliness / Infra | Office |
| Documents | Office |
| Other | Principal |

UX Hint:
> “Policy or promotion concerns go to school administration.”

---

## 11. Urgency Rules

- Urgent allowed only for:
  - Transport
  - Health & Safety
- Max 1 urgent ticket per parent per week

---

## 12. Ticket Lifecycle & Automation

```
Pending → In Progress → Resolved
```

### Controls
- Director, Principal, Vice Principal
- Assigned staff only

### Automation
- Staff reply → auto In Progress
- Prompt if reply without status change
- Reminder if no activity
- Escalation only if untouched
- VP can snooze escalation

---

## 13. Parent Satisfaction & Reopen

After resolution:
- ✅ Resolved
- ❌ Request reopen (reason required)

Reopen limits enforced.

---

## 14. Internal Notes (Staff‑Only)

- Permanent
- Never visible to parents

Warnings:
> “Internal notes are part of permanent records.”

Prompt:
> “Do you want to update the parent?”

---

## 15. Transport‑Specific Handling

- Known issue tagging
- Route‑wise broadcast
- Max 1 broadcast/route/2 hours
- Footer:
> “No action required from parents.”

---

## 16. Notifications

### Channels
1. Web notifications
2. WhatsApp (transactional only)
3. SMS fallback

### WhatsApp Rules
- Pre‑approved templates only
- No replies
- Magic login deep links

---

## 17. Soft Response Guidelines (Internal Only)

| Category | Target |
|---|---|
| Health & Safety | 1 hour |
| Transport | 4 hours |
| Academic | 24 hours |

Language: “Reminder”, not “Overdue”

---

## 18. Office Hours Handling

Auto banner for off‑hours:
> “School office hours are ___. Requests will be addressed next working day.”

---

## 19. Abuse Handling

- Staff flag ticket as inappropriate
- Director notified
- Director actions:
  - Restrict parent to admin‑only routing
  - Temporarily block ticket creation

---

## 20. Data Retention & Audit

- Permanent storage
- Logical archive after 2 years
- Soft delete only
- Export:
  - Watermarked
  - Password‑protected ZIP

---

## 21. Metrics (Admin‑Only)

- Avg response time by category
- % reopened tickets
- Announcement view rate
- Ticket volume per class

No per‑teacher leaderboards.

---

## 22. System Health Visibility

Weekly auto‑email to Director:
- Tickets created
- Tickets resolved
- Avg response time

---

## 23. Core Data Models (Simplified)

```text
User(id, role, phone, school_id)
Student(id, class, section, school_id)
Ticket(id, category, status, urgency, assigned_to, school_id)
TicketMessage(id, ticket_id, sender_role)
InternalNote(ticket_id, note)
Announcement(id, content, targeting)
OTP(id, phone, hash, expires_at)
```

---

## 24. Error Handling

### User Errors
- Clear, polite, non‑technical

### System Errors
- Generic UI message
- Detailed logs

### Notification Failures
- WhatsApp → SMS fallback
- Retry with logging

---

## 25. Testing Plan

### Unit Tests
- Guardrails
- Permissions
- Status transitions
- OTP logic

### Integration Tests
- Routing
- Notifications
- Auth flow

### End‑to‑End Tests
- Parent creates ticket
- Staff resolves
- Parent confirms satisfaction

### UAT
- 5–10 parents
- 3 teachers
- Office staff
- Transport manager

---

## 26. Rollout Plan

1. Internal staff testing
2. Pilot classes
3. Full school rollout

---
