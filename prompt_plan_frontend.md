Excellent — this is the right moment to do this.  
Below is a **carefully sequenced set of frontend LLM build prompts**, modeled **exactly like the backend prompts**, but adapted for **Next.js (App Router), TypeScript, mobile‑first UX, and strict wiring to the backend APIs**.

Key properties of these prompts:

- ✅ Incremental, safe steps  
- ✅ Testable UI at every stage  
- ✅ No orphan components  
- ✅ Each prompt **builds on previous prompts**
- ✅ Forces good UX + guardrails
- ✅ LLM‑friendly and human‑reviewable

You can paste **each prompt one by one** into a code‑generation LLM.

---

# FRONTEND LLM BUILD PROMPTS  
**School Communication & Helpdesk OS – V1**

---

## PROMPT 1: Next.js Project Skeleton & App Shell

```text
You are building the frontend for a School Communication & Helpdesk OS.

Task:
1. Create a Next.js 14 project using App Router and TypeScript.
2. Set up the following folders:
   - /app
   - /components
   - /lib
   - /services
   - /styles
3. Create a basic App Shell with:
   - Mobile-first layout
   - Top header placeholder
   - Bottom navigation placeholder
4. Add a global layout and a basic home page.
5. Add minimal CSS for spacing and typography.

Constraints:
- Use functional components only
- Mobile-first (no desktop-only assumptions)
- No backend calls yet

Output:
- Project structure
- Running app with visible shell
```

---

## PROMPT 2: Design System & UI Primitives

```text
Extend the existing Next.js project.

Task:
1. Create reusable UI primitives:
   - Button
   - Input
   - Select
   - Textarea
   - Badge
   - Alert/Banner
2. Define a basic design system:
   - Color palette (neutral, professional)
   - Status colors (Pending, In Progress, Resolved, Urgent)
   - Spacing scale
3. Ensure all components are accessible (labels, focus states).
4. Demonstrate each component on a temporary /ui-preview page.

Constraints:
- No external UI libraries
- Mobile-friendly touch targets
- Components must be reusable

Do not add business logic yet.
```

---

## PROMPT 3: Authentication Screens (UI Only)

```text
Add authentication UI screens.

Task:
1. Create Login screen:
   - Phone number input
   - Continue button
2. Create OTP Verification screen:
   - OTP input
   - Verify button
3. Add client-side form validation.
4. Add loading and error states (UI only).
5. Add routing between login and OTP screens.

Constraints:
- No real API calls yet
- Use mock success/failure flows
- Friendly, non-technical copy

Ensure mobile-first UX.
```

---

## PROMPT 4: Auth State & Route Protection

```text
Implement frontend authentication state management.

Task:
1. Add an auth context/provider.
2. Track:
   - logged-in state
   - user role (mocked)
3. Implement protected routes:
   - Redirect unauthenticated users to login
4. Add logout button and logout behavior.
5. Add auto-logout UX placeholder (no timers yet).

Constraints:
- Auth state may be mocked
- No backend dependency yet
- Must be easy to replace with real API later
```

---

## PROMPT 5: Parent Profile & Student Context UI

```text
Add parent profile and student context UI.

Task:
1. Create Profile screen:
   - Show name, phone
   - Editable name and email
2. Show read-only linked students list.
3. Display banner:
   “Some student details are maintained by the school.”
4. Add a reusable StudentSelector component:
   - Supports multi-select
5. Add confirmation UI:
   “This ticket is about: Child A, Child B”

Constraints:
- Use mocked student data
- No API calls yet
- Mobile-first layout
```

---

## PROMPT 6: Ticket List (Parent View)

```text
Implement parent ticket list UI.

Task:
1. Create Ticket List screen.
2. Display ticket cards with:
   - Category
   - Status
   - Last updated time
3. Add filters:
   - Status
   - Child
4. Add empty state UI.
5. Add visual indicator for urgent tickets.

Constraints:
- Use mocked ticket data
- No backend calls
- Ensure smooth scrolling on mobile
```

---

## PROMPT 7: Ticket Detail View (Parent)

```text
Implement ticket detail UI for parents.

Task:
1. Create Ticket Detail screen.
2. Display:
   - Category
   - Status
   - Assigned role
3. Show message thread (chronological).
4. Show attachments (preview/download UI).
5. Hide internal notes completely.
6. Clearly separate parent vs staff messages visually.

Constraints:
- Use mocked data
- No status changes allowed here yet
```

---

## PROMPT 8: Create Ticket Flow (Parent)

```text
Implement create ticket flow.

Task:
1. Add “Create Ticket” CTA.
2. Create ticket form:
   - Category selector
   - Child selector (mandatory)
   - Title + description
   - Attachment upload UI
   - Urgency selector (restricted)
3. Add UX hint for Academic category:
   “Policy or promotion concerns go to school administration.”
4. Add confirmation step before submit.
5. Add success screen.

Constraints:
- Use mocked submission
- Validate required fields
- Mobile-friendly form layout
```

---

## PROMPT 9: Ticket Guardrail UX

```text
Add ticket guardrail user experience.

Task:
1. Display friendly error banners for:
   - Max open tickets
   - Cooldown active
   - Weekly cap reached
2. Disable submit button when blocked.
3. Add cooldown countdown indicator.

Constraints:
- Guardrail data mocked
- Copy must be calm and respectful
```

---

## PROMPT 10: Reopen & Satisfaction Flow (Parent)

```text
Add satisfaction and reopen UX.

Task:
1. Show satisfaction prompt on resolved tickets.
2. Implement:
   - “Yes, resolved” flow
   - “Request reopen” flow
3. Add reopen reason input.
4. Handle reopen limit errors gracefully.
5. Update ticket status UI accordingly.

Constraints:
- Use mocked backend responses
```

---

## PROMPT 11: Announcements (Parent)

```text
Implement announcements UI.

Task:
1. Announcement list screen.
2. Announcement card with:
   - Title
   - Date
   - Attachment indicator
3. Announcement detail view.
4. Auto-mark announcement as read after 3 seconds.
5. Handle archived announcements.

Constraints:
- Use mocked announcements
- No reply UI allowed
```

---

## PROMPT 12: Staff Dashboard & Ticket Inbox

```text
Implement staff dashboard UI.

Task:
1. Role-aware dashboard shell.
2. Ticket inbox showing assigned tickets only.
3. Filters by status and urgency.
4. Empty states.

Constraints:
- Mock staff role
- No cross-ticket visibility
```

---

## PROMPT 13: Staff Ticket Detail & Internal Notes

```text
Extend ticket detail UI for staff.

Task:
1. Add reply box for staff.
2. Add status update control.
3. Add internal notes panel.
4. Show warning:
   “Internal notes are part of permanent records.”
5. Prompt:
   “Do you want to update the parent?”

Constraints:
- Internal notes must never render for parents
```

---

## PROMPT 14: Transport-Specific UI

```text
Add transport-specific ticket UI.

Task:
1. Known issue indicator.
2. Broadcast update form.
3. Route selector.
4. Rate-limit messaging.
5. Footer:
   “No action required from parents.”

Constraints:
- Staff-only visibility
```

---

## PROMPT 15: Notifications UI

```text
Implement web notifications UI.

Task:
1. Notification inbox screen.
2. Unread indicators.
3. Click-through navigation.
4. Graceful handling if notifications disabled.

Constraints:
- Use mocked notifications
```

---

## PROMPT 16: Office Hours & Soft SLA UX

```text
Add operational UX elements.

Task:
1. Office-hours banner on ticket creation.
2. Soft response guideline indicators (staff-only).
3. Reminder indicators (non-alarming).
4. Escalation visibility (VP only).

Constraints:
- Informational only, no pressure language
```

---

## PROMPT 17: Error Handling & Resilience

```text
Add global error handling.

Task:
1. Global API error handler.
2. Network failure UI.
3. Retry affordances.
4. Ensure no raw error messages are shown.

Constraints:
- Friendly, non-technical copy
```

---

## PROMPT 18: API Wiring & Real Backend Integration

```text
Wire frontend to real backend APIs.

Task:
1. Replace mocks with real API calls.
2. Centralize API client logic.
3. Handle auth cookies and session expiry.
4. Ensure all flows still work end-to-end.

Constraints:
- No UI regressions
- All previous flows must remain functional
```

---

## PROMPT 19: PWA & Launch Prep

```text
Prepare frontend for production.

Task:
1. Add PWA manifest.
2. Add add-to-home-screen prompt.
3. Basic offline fallback.
4. Production build verification.

Constraints:
- Mobile-first testing
```

---
