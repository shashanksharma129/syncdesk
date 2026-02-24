Below is a **thorough, production‑ready `frontend/todo.md`**, designed to pair cleanly with your backend todo and the frozen V1 spec.

It is:
- Ordered for **safe, incremental frontend development**
- Explicit about **state management, auth wiring, and UX guardrails**
- Written so a dev (or you + LLM) always knows *what to build next*
- Focused on **mobile‑first web (PWA‑ready)**

You can drop this into `frontend/todo.md`.

---

```markdown
# School Communication & Helpdesk OS — Frontend V1 TODO

This checklist follows the frozen V1 spec and backend architecture.
Frontend is a **responsive web app** built with **Next.js (React)**.

Rule:
✅ Do NOT build UI ahead of backend readiness  
✅ Every screen must be wired to real APIs or mocks  
✅ Mobile UX > Desktop polish

---

## ✅ 0. Frontend Repo & Tooling

- [ ] Initialize Next.js app (App Router)
- [ ] Choose TypeScript (mandatory)
- [ ] Set up folder structure:
  - [ ] `/app`
  - [ ] `/components`
  - [ ] `/lib`
  - [ ] `/services`
  - [ ] `/styles`
- [ ] Configure ESLint + Prettier
- [ ] Configure absolute imports
- [ ] Add `.env.local.example`
- [ ] Add `frontend/todo.md`
- [ ] Basic README (how to run frontend)

---

## ✅ 1. Design Foundations (Before Screens)

- [ ] Define color palette (professional, neutral)
- [ ] Define typography scale
- [ ] Define spacing scale
- [ ] Define status colors:
  - [ ] Pending
  - [ ] In Progress
  - [ ] Resolved
  - [ ] Urgent
- [ ] Create reusable UI primitives:
  - [ ] Button
  - [ ] Input
  - [ ] Select
  - [ ] Textarea
  - [ ] Modal
  - [ ] Badge
  - [ ] Alert / Banner
- [ ] Mobile-first breakpoints

---

## ✅ 2. App Shell & Layout

- [ ] App layout component
- [ ] Top header (school name + role)
- [ ] Bottom navigation (mobile-first)
  - [ ] Home
  - [ ] Tickets
  - [ ] Announcements
  - [ ] Profile
- [ ] Desktop sidebar variant (optional)
- [ ] Loading & skeleton states
- [ ] Global error boundary

---

## ✅ 3. Authentication Flow (Critical)

- [ ] Login screen (phone number input)
- [ ] OTP verification screen
- [ ] Magic-link handling (auto-login)
- [ ] Session persistence handling
- [ ] Auto-logout UX (inactivity)
- [ ] Logout button (visible)
- [ ] Auth guard for protected routes
- [ ] Role-aware routing (parent vs staff)
- [ ] Friendly auth error messages

---

## ✅ 4. Parent Profile & Context

- [ ] Profile screen
- [ ] Show parent name & phone
- [ ] Editable fields:
  - [ ] Name
  - [ ] Email
- [ ] Read-only fields:
  - [ ] Linked students
- [ ] Banner:
  > “Some student details are maintained by the school.”
- [ ] Logout action

---

## ✅ 5. Student Context Handling

- [ ] Fetch `/me/students`
- [ ] Student selector component
- [ ] Multi-student selection support
- [ ] Confirmation UI before ticket creation:
  > “This ticket is about: Child A, Child B”
- [ ] Handle zero-student edge case gracefully

---

## ✅ 6. Ticket List (Parent)

- [ ] Ticket list screen
- [ ] Filter by:
  - [ ] Status
  - [ ] Child
- [ ] Ticket card component:
  - [ ] Category
  - [ ] Status
  - [ ] Last updated
- [ ] Empty state messaging
- [ ] Pagination / lazy loading
- [ ] Visual indicator for urgent tickets

---

## ✅ 7. Ticket Detail View

- [ ] Ticket header:
  - [ ] Category
  - [ ] Status
  - [ ] Assigned role
- [ ] Message thread (chronological)
- [ ] Attachments preview/download
- [ ] Status change visibility
- [ ] Internal notes hidden from parents
- [ ] Clear visual separation between parent/staff messages

---

## ✅ 8. Create Ticket Flow (Parent)

- [ ] “Create Ticket” CTA
- [ ] Category selection
- [ ] UX hint for Academic categories:
  > “Policy or promotion concerns go to school administration.”
- [ ] Child selection (mandatory)
- [ ] Title + description
- [ ] Attachment upload (type/size validation)
- [ ] Urgency selector (restricted)
- [ ] Guardrail error handling:
  - [ ] Max open tickets
  - [ ] Cooldown
  - [ ] Weekly cap
- [ ] Success confirmation screen

---

## ✅ 9. Ticket Guardrail UX

- [ ] Friendly error banners:
  - [ ] “You already have 3 open tickets”
  - [ ] “Please wait 30 minutes before creating another request”
- [ ] Disabled submit states when blocked
- [ ] Countdown indicator for cooldown

---

## ✅ 10. Reopen & Satisfaction Flow

- [ ] Satisfaction prompt on resolved ticket
- [ ] “Yes, resolved” flow
- [ ] “Request reopen” flow
- [ ] Reopen reason input
- [ ] Reopen limit error messaging
- [ ] Clear status updates after reopen

---

## ✅ 11. Announcements (Parent)

- [ ] Announcements list screen
- [ ] Announcement card:
  - [ ] Title
  - [ ] Date
  - [ ] Attachment indicator
- [ ] Announcement detail view
- [ ] Attachment download
- [ ] Auto-mark read after ≥3 seconds
- [ ] Archive handling (older announcements)
- [ ] Empty state

---

## ✅ 12. Staff Dashboard (Shared Base)

- [ ] Role-aware dashboard shell
- [ ] Ticket inbox (assigned tickets only)
- [ ] Status filter
- [ ] Priority / urgency indicators
- [ ] Empty states

---

## ✅ 13. Staff Ticket Detail View

- [ ] Full ticket context
- [ ] Parent message thread
- [ ] Reply box
- [ ] Status update control
- [ ] Internal notes panel
- [ ] Warning text:
  > “Internal notes are part of permanent records.”
- [ ] Prompt:
  > “Do you want to update the parent?”

---

## ✅ 14. Transport-Specific UI

- [ ] Known issue indicator
- [ ] Broadcast update form
- [ ] Route selection
- [ ] Broadcast rate-limit messaging
- [ ] Footer auto-display:
  > “No action required from parents.”

---

## ✅ 15. Abuse & Safety UI (Admin)

- [ ] Abuse flag indicator
- [ ] Admin-only warning banner
- [ ] Parent restriction controls
- [ ] Lock/unlock ticket creation UI
- [ ] Clear audit visibility

---

## ✅ 16. Response Guidelines UX (Staff)

- [ ] Soft response timer display (internal only)
- [ ] Reminder indicator (non-alarming)
- [ ] Escalation visibility (VP only)
- [ ] Snooze escalation control

---

## ✅ 17. Office Hours UX

- [ ] Office hours banner on ticket creation
- [ ] Category-specific display
- [ ] Non-blocking informational tone

---

## ✅ 18. Notifications (Web)

- [ ] Web notification inbox
- [ ] Unread indicators
- [ ] Click-through to relevant screen
- [ ] Graceful handling when notifications disabled

---

## ✅ 19. Error Handling & Resilience

- [ ] Global API error handler
- [ ] Network failure UI
- [ ] Retry affordances
- [ ] Friendly, non-technical copy
- [ ] No raw error messages shown

---

## ✅ 20. Accessibility & UX Polish

- [ ] Keyboard navigation
- [ ] Accessible form labels
- [ ] Touch-friendly tap targets
- [ ] Loading indicators everywhere
- [ ] No action without feedback

---

## ✅ 21. End-to-End Frontend Testing

- [ ] Auth flow (login → dashboard)
- [ ] Parent ticket creation
- [ ] Guardrail enforcement UX
- [ ] Staff reply & resolve flow
- [ ] Announcement read tracking
- [ ] Abuse handling visibility

---

## ✅ 22. PWA & Deployment Prep

- [ ] PWA manifest
- [ ] Add-to-home-screen prompt
- [ ] Basic offline fallback
- [ ] Environment-based API config
- [ ] Production build test

---

## ✅ 23. Launch Readiness

- [ ] Mobile testing (Android Chrome)
- [ ] Low-bandwidth testing
- [ ] Content tone review
- [ ] Admin walkthrough
- [ ] Parent walkthrough checklist

---

✅ **Do not move ahead until the current section is complete.**
✅ **Mobile UX correctness > feature speed.**
```

---
