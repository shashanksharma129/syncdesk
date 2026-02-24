# Syncdesk — UI & flow bugs

From code review and expected behavior for **Parent** and **Staff** personas. Fix in order of severity where possible.

---

## Critical (data / security / wrong behavior)

### BUG-001: Satisfied flow does not call API
- **Where:** `frontend/app/tickets/[id]/satisfied/page.tsx`
- **Expected:** On open, call `POST /tickets/{id}/satisfied` so the backend marks the ticket as satisfied.
- **Actual:** Page is mock-only; shows success message and links but never calls the API. Ticket remains unsatisfied in DB.
- **Persona:** Parent (resolved ticket).

### BUG-002: Reopen flow does not call API
- **Where:** `frontend/app/tickets/[id]/reopen/page.tsx`
- **Expected:** On submit, call `POST /tickets/{id}/reopen` with `{ reason }`. Show backend errors (e.g. max reopen limit).
- **Actual:** Form submit is local only; no API call. Reopen request is never sent; backend reopen limits not enforced in UI.
- **Persona:** Parent (resolved ticket).

### BUG-003: Staff route accessible to parents
- **Where:** `frontend/components/AuthGuard.tsx`, `frontend/app/staff/*`
- **Expected:** `/staff` and `/staff/*` only for `user.role === "staff"`; parents redirected or shown “Access denied”.
- **Actual:** Any logged-in user can open `/staff`. Parent sees “Staff – Ticket inbox” with their own tickets (confusing and wrong persona).
- **Fix:** Add role check: if `user.role !== "staff"` and path starts with `/staff`, redirect to `/` or show an “Access denied” message.

### BUG-004: Guardrails not wired — create ticket always allowed
- **Where:** `frontend/app/tickets/page.tsx`, `frontend/app/tickets/new/page.tsx`
- **Expected:** Before or on create, call backend for guardrail state and set `guardrail.blocked` / show GuardrailBanner for max open, cooldown, weekly cap. Disable “Create ticket” / “Continue” when blocked.
- **Actual:** `guardrail = { blocked: false }` is hardcoded. User can always click Create ticket and submit; backend may return 400 but UX doesn’t preempt (no banner, no countdown).
- **Persona:** Parent.

---

## High (wrong or missing UX)

### BUG-005: Assigned role never shown on tickets
- **Where:** `frontend/services/tickets.ts` (`toTicket`), ticket detail/card
- **Expected:** When a ticket is assigned, show “Assigned to: &lt;role or name&gt;” (or “Assigned” if role not in API).
- **Actual:** `assigned_role: t.assigned_to_id != null ? undefined : undefined` — always undefined, so “Assigned to:” never appears even when ticket is assigned.
- **Fix:** Either backend adds `assigned_role` (or user name) to ticket response, or frontend shows “Assigned” when `assigned_to_id != null`.

### BUG-006: No Staff entry in main nav for staff
- **Where:** `frontend/components/AppShell.tsx`
- **Expected:** For staff, main nav includes a “Staff” (or “Inbox”) link to `/staff` so they don’t have to open Profile first.
- **Actual:** Nav is same for everyone: Home, Tickets, Announcements, Profile. Staff must open Profile and click “Staff inbox” to reach `/staff`.
- **Fix:** When `user.role === "staff"`, add a nav item to `/staff` (e.g. “Staff” or “Inbox”). Requires AppShell to consume auth (e.g. from context).

### BUG-007: Home page not role-aware
- **Where:** `frontend/app/page.tsx`
- **Expected:** For staff, home can mention “or go to Staff inbox” / quick link to `/staff`. For parent, current copy is fine.
- **Actual:** Same “Welcome” and “Use the menu below…” for all roles; no staff-specific CTA.
- **Persona:** Staff (and optionally parent clarity).

### BUG-008: Profile “Save changes” does not persist
- **Where:** `frontend/app/profile/page.tsx`
- **Expected:** Name/email saved via API (e.g. PATCH /me or similar) and reflected after reload.
- **Actual:** Save only sets local state and shows “Saved.”; no API call. Data is lost on refresh. Backend may have no PATCH /me yet — if so, either add API or show “Profile updates coming soon” and disable save.

---

## Medium (inconsistency / edge cases)

### BUG-009: OTP validation message on staff login
- **Where:** `frontend/app/login/otp/OtpForm.tsx`
- **Observed:** When entering staff stub OTP (654321), sometimes “Please enter the 6-digit code we sent you” appears even with 6 digits (e.g. timing or validation run before state update). Second submit often works.
- **Fix:** Ensure validation uses current input value (e.g. validate in submit handler from state, not from a stale ref), and/or avoid showing the alert when `code.length === 6`.

### BUG-010: Create ticket — guardrail errors from API not shown as banner
- **Where:** `frontend/app/tickets/new/page.tsx`
- **Expected:** If `POST /tickets` returns 400 with a guardrail reason (max open, cooldown, weekly cap), show GuardrailBanner (or equivalent) and optionally prefill `guardrail` state so list page can show banner too.
- **Actual:** API errors are shown as generic `setError(...)`. No mapping of backend message to GuardrailBanner or `blockUntil` for countdown.
- **Persona:** Parent.

### BUG-011: Tickets list — no empty state when API returns []
- **Where:** `frontend/app/tickets/page.tsx`
- **Expected:** When `tickets.length === 0` and no filters (or filters applied), show a clear empty state (“No tickets yet” / “No tickets match your filters”) and CTA to create ticket when allowed.
- **Actual:** Empty state exists for filtered list; ensure copy is clear and create CTA is visible when not blocked.

### BUG-012: Announcement detail — mark read may fire before 3s on fast navigation
- **Where:** `frontend/app/announcements/[id]/page.tsx`
- **Expected:** Mark as read only after viewing for ≥3 seconds (per spec). If user navigates away before 3s, don’t mark read (or cancel timer).
- **Actual:** Timer is 3s; effect cleanup must clear it so `markAnnouncementRead` is not called if user leaves before 3s.

---

## Low / polish

### BUG-013: AppShell nav “current” page not dynamic
- **Where:** `frontend/components/AppShell.tsx`
- **Expected:** Bottom nav highlights the current route (e.g. Tickets when on `/tickets` or `/tickets/123`).
- **Actual:** `aria-current="page"` is hardcoded on Home link. Other routes (Tickets, Announcements, Profile) are never marked current.
- **Fix:** Use `usePathname()` and set `aria-current="page"` (and any “active” class) on the matching nav item.

### BUG-014: Student display name is “Class 5A” not “Child A”
- **Where:** `frontend/services/students.ts` (`toStudent`), profile and ticket flows
- **Expected:** Spec/todo often refers to “Child A, Child B”. Backend returns `class_name` + `section` (no display name). If product wants “Child A”, backend or seed needs a name; otherwise “Class 5A” is consistent but may not match copy elsewhere.
- **Action:** Align spec/copy with backend (Class/section) or add display name to API/seed.

### BUG-015: Ticket detail — “Back to tickets” link when not found
- **Where:** `frontend/app/tickets/[id]/page.tsx`
- **Expected:** On “Ticket not found”, link back to list. Parent: “Back to tickets” (/tickets); staff: “Back to inbox” (/staff).
- **Actual:** Parent links to `/tickets`; staff detail already uses “Back to inbox”. Consistency check only.

---

## Summary

| Severity | Count |
|----------|--------|
| Critical | 4 |
| High     | 4 |
| Medium   | 4 |
| Low      | 3 |

**Recommended order to fix:** BUG-001, BUG-002 (satisfied/reopen API), then BUG-003 (staff route protection), then BUG-004 (guardrails), then BUG-005–BUG-008, then medium/low.

---

## Testing note

Bugs are from code review and spec; browser UI was not exercised (MCP snapshot unavailable). Run manual smoke (parent + staff: login → tickets → create → announcements → profile → staff inbox; satisfied/reopen) or Playwright E2E to catch UI-only issues.
