# Syncdesk — UI & flow bugs

From code review and expected behavior for **Parent** and **Staff** personas. Fix in order of severity where possible.

---

## Critical (data / security / wrong behavior)

### BUG-001: Satisfied flow does not call API — **FIXED**
- **Where:** `frontend/app/tickets/[id]/satisfied/page.tsx`
- **Expected:** On open, call `POST /tickets/{id}/satisfied` so the backend marks the ticket as satisfied.
- **Actual:** Page is mock-only; shows success message and links but never calls the API. Ticket remains unsatisfied in DB.
- **Persona:** Parent (resolved ticket).
- **Fix applied:** Added `markSatisfied(id)` in services/tickets; page calls it on mount (useEffect), shows loading/error/success.

### BUG-002: Reopen flow does not call API — **FIXED**
- **Where:** `frontend/app/tickets/[id]/reopen/page.tsx`
- **Expected:** On submit, call `POST /tickets/{id}/reopen` with `{ reason }`. Show backend errors (e.g. max reopen limit).
- **Actual:** Form submit is local only; no API call. Reopen request is never sent; backend reopen limits not enforced in UI.
- **Persona:** Parent (resolved ticket).
- **Fix applied:** Added `reopenTicket(id, reason)` in services/tickets; form submits via API, shows backend error message on 400.

### BUG-003: Staff route accessible to parents — **FIXED**
- **Where:** `frontend/components/AuthGuard.tsx`, `frontend/app/staff/*`
- **Expected:** `/staff` and `/staff/*` only for `user.role === "staff"`; parents redirected or shown “Access denied”.
- **Actual:** Any logged-in user can open `/staff`. Parent sees “Staff – Ticket inbox” with their own tickets (confusing and wrong persona).
- **Fix applied:** AuthGuard checks `isStaffPath` and `user.role !== "staff"`; redirects to `/` and returns null until redirect.

### BUG-004: Guardrails not wired — create ticket always allowed — **TODO**
- **Where:** `frontend/app/tickets/page.tsx`, `frontend/app/tickets/new/page.tsx`
- **Expected:** Before or on create, call backend for guardrail state and set `guardrail.blocked` / show GuardrailBanner for max open, cooldown, weekly cap. Disable “Create ticket” / “Continue” when blocked.
- **Actual:** `guardrail = { blocked: false }` is hardcoded on list page. User can always click Create ticket and submit; backend may return 400 but UX doesn’t preempt (no banner on list; BUG-010 fix shows banner on create after 400).
- **Persona:** Parent.
- **TODO:** Add backend GET (e.g. `/me/ticket-creation-status` or `/tickets/guardrail`) returning `{ blocked, reason?, block_until? }` and call it on tickets list and new page to show banner before submit.

---

## High (wrong or missing UX)

### BUG-005: Assigned role never shown on tickets — **FIXED**
- **Where:** `frontend/services/tickets.ts` (`toTicket`), ticket detail/card
- **Expected:** When a ticket is assigned, show “Assigned to: &lt;role or name&gt;” (or “Assigned” if role not in API).
- **Actual:** `assigned_role` was always undefined, so “Assigned to:” never appeared.
- **Fix applied:** `toTicket` sets `assigned_role: t.assigned_to_id != null ? "Assigned" : undefined`. Detail page already shows “Assigned to: {assigned_role}”.

### BUG-006: No Staff entry in main nav for staff — **FIXED**
- **Where:** `frontend/components/AppShell.tsx`
- **Expected:** For staff, main nav includes a “Staff” (or “Inbox”) link to `/staff`.
- **Fix applied:** AppShell uses `useAuth()`; when `user.role === "staff"`, nav includes “Staff” link to `/staff`. Nav items built from array; current route highlighted (BUG-013).

### BUG-007: Home page not role-aware — **FIXED**
- **Where:** `frontend/app/page.tsx`
- **Expected:** For staff, home can mention “or go to Staff inbox” / quick link to `/staff`.
- **Fix applied:** Home is client component using `useAuth()`; when staff, shows “Go to Staff inbox” link to `/staff`.

### BUG-008: Profile “Save changes” does not persist — **FIXED**
- **Where:** `frontend/app/profile/page.tsx`
- **Expected:** Name/email saved via API or show “Profile updates coming soon” and disable save.
- **Fix applied:** Backend has no PATCH /me. Name/email inputs are disabled; Alert says “Profile updates coming soon. Name and email are read-only for now.” Save button removed.

---

## Medium (inconsistency / edge cases)

### BUG-009: OTP validation message on staff login — **FIXED**
- **Where:** `frontend/app/login/otp/OtpForm.tsx`
- **Observed:** Sometimes “Please enter the 6-digit code” appeared even with 6 digits (stale state).
- **Fix applied:** Submit handler reads current value from form DOM (`input#otp` or `input[name="otp"]`) and validates `value.length === 6`; uses that value for `verifyOtp(phone, value)`.

### BUG-010: Create ticket — guardrail errors from API not shown as banner — **FIXED**
- **Where:** `frontend/app/tickets/new/page.tsx`
- **Expected:** If `POST /tickets` returns 400 with guardrail reason, show GuardrailBanner.
- **Fix applied:** On create failure, `guardrailReasonFromMessage(msg)` maps backend detail to `max_open`|`cooldown`|`weekly_cap`|`other`; set `guardrail` state and return to form step so GuardrailBanner is shown.

### BUG-011: Tickets list — no empty state when API returns [] — **FIXED**
- **Where:** `frontend/app/tickets/page.tsx`
- **Expected:** Clear empty state and CTA when no tickets.
- **Fix applied:** When `filtered.length === 0`, show “No tickets yet. Create one above when you need help.” when no filters; “No tickets match your filters. You can create a new ticket above.” when filters applied. Create ticket button already visible when not blocked.

### BUG-012: Announcement detail — mark read may fire before 3s on fast navigation — **VERIFIED**
- **Where:** `frontend/app/announcements/[id]/page.tsx`
- **Expected:** Mark as read only after ≥3 seconds; cancel if user leaves before 3s.
- **Status:** Effect cleanup already returns `() => clearTimeout(t)`, so when user navigates away the timeout is cleared and `markAnnouncementRead` is not called. No code change needed.

---

## Low / polish

### BUG-013: AppShell nav “current” page not dynamic — **FIXED**
- **Where:** `frontend/components/AppShell.tsx`
- **Expected:** Bottom nav highlights the current route.
- **Fix applied:** Nav built from array with `match(p)` per route; `usePathname()` used; `NavLink` gets `isCurrent={item.match(pathname)}` and sets `aria-current="page"` when true.

### BUG-014: Student display name is “Class 5A” not “Child A” — **TODO**
- **Where:** `frontend/services/students.ts` (`toStudent`), profile and ticket flows
- **Expected:** Spec/todo refers to “Child A, Child B”. Backend returns `class_name` + `section` (no display name).
- **TODO:** Product decision: align spec/copy with “Class 5A” style, or add display name to backend/seed and expose in API.

### BUG-015: Ticket detail — “Back to tickets” link when not found — **VERIFIED**
- **Where:** `frontend/app/tickets/[id]/page.tsx`, `frontend/app/staff/tickets/[id]/page.tsx`
- **Expected:** Parent: “Back to tickets” (/tickets); staff: “Back to inbox” (/staff).
- **Status:** Parent detail links to `/tickets`; staff detail links to `/staff` with “Back to inbox”. No change needed.

---

## Summary

| Severity | Count | Fixed | TODO / Verified |
|----------|--------|--------|------------------|
| Critical | 4     | 3     | 1 (BUG-004)      |
| High     | 4     | 4     | 0                |
| Medium   | 4     | 4     | 0                |
| Low      | 3     | 2     | 1 (BUG-014)      |

**Remaining TODO:** BUG-004 (preemptive guardrail API + list page banner), BUG-014 (student display name: backend/spec).

---

## Comprehensive review (post-fix)

**What was done in one pass:**

1. **BUG-001** — Satisfied page now calls `POST /tickets/{id}/satisfied` on mount; loading/error/success states.
2. **BUG-002** — Reopen page now calls `POST /tickets/{id}/reopen` with reason on submit; backend error shown on 400.
3. **BUG-003** — AuthGuard redirects non-staff from `/staff` to `/`.
4. **BUG-004** — Marked TODO: needs backend endpoint for guardrail status; create flow already shows banner after 400 (BUG-010).
5. **BUG-005** — `toTicket` sets `assigned_role: "Assigned"` when `assigned_to_id != null`.
6. **BUG-006** — AppShell shows “Staff” nav item for staff and uses pathname for current route (BUG-013).
7. **BUG-007** — Home shows “Go to Staff inbox” link for staff.
8. **BUG-008** — Profile name/email disabled with “Profile updates coming soon” (no PATCH /me).
9. **BUG-009** — OTP form validates from current input value (DOM) and uses it for verify call.
10. **BUG-010** — Create ticket 400 mapped to GuardrailBanner reason; user returned to form with banner.
11. **BUG-011** — Tickets list empty state: distinct copy for no tickets vs no matches.
12. **BUG-012** — Verified: effect cleanup clears timer; no change.
13. **BUG-013** — Nav current route from pathname (done with BUG-006).
14. **BUG-014** — Marked TODO: product/backend decision.
15. **BUG-015** — Verified: parent/staff back links correct; no change.

**Files touched:**  
`frontend/services/tickets.ts`, `frontend/app/tickets/[id]/satisfied/page.tsx`, `frontend/app/tickets/[id]/reopen/page.tsx`, `frontend/components/AuthGuard.tsx`, `frontend/services/tickets.ts` (assigned_role), `frontend/components/AppShell.tsx`, `frontend/app/page.tsx`, `frontend/app/profile/page.tsx`, `frontend/app/login/otp/OtpForm.tsx`, `frontend/app/tickets/new/page.tsx`, `frontend/app/tickets/page.tsx`, `bugs.md`.

**Ensuring bugs are fixed in the UI:**  
Run the Playwright E2E tests so the app is driven in a real browser and the fixes are verified there. Use a frontend build that includes the fixes (e.g. `npm run dev` in `frontend/`, or a rebuilt Docker image). Then:

```bash
cd frontend && PLAYWRIGHT_BASE_URL=http://localhost:3000 npm run test:e2e
```

See `frontend/e2e/README.md` for prerequisites (backend + frontend with latest code) and what each test asserts.

**Suggested next steps:** Implement BUG-004 (GET guardrail status) if preemptive blocking is required; decide BUG-014 (student display names). Run E2E and manual smoke (parent + staff flows).

---

## Testing note

Bugs are from code review and spec; browser UI was not exercised (MCP snapshot unavailable). Run manual smoke (parent + staff: login → tickets → create → announcements → profile → staff inbox; satisfied/reopen) or Playwright E2E to catch UI-only issues.
