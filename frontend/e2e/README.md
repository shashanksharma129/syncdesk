# E2E tests (Playwright)

These tests verify that bug fixes from bugs.md are present and working in the UI.

## Why run them

- Confirm fixes in a real browser, not just in code.
- Catch regressions after future changes.
- Document expected behaviour for parent vs staff.

## Prerequisites

1. Backend running (e.g. docker compose up or uvicorn from backend).
2. Frontend running with the latest code (npm run dev in frontend, or rebuilt Docker image).

If the frontend at http://localhost:3000 is an old Docker image built before the fixes, the E2E tests will not see the fixed UI.

## Run

From frontend directory:

  PLAYWRIGHT_BASE_URL=http://localhost:3000 npm run test:e2e

Or run without that env var so Playwright starts npm run dev and tests against it.

## What each test asserts

- BUG-003: Parent visiting /staff is redirected to /.
- BUG-006 + BUG-007: Staff sees Staff nav link and Staff inbox CTA on home.
- BUG-006: Parent bottom nav does not show Staff.
- BUG-008: Profile shows Profile updates coming soon, no Save button.
- BUG-011: Tickets page has Create CTA and either list or empty state copy.
- BUG-013: On /tickets, Tickets nav has aria-current=page.
- BUG-001: /tickets/1/satisfied shows thank-you or error (API called).
- BUG-002: Reopen form submit shows success or backend error.

Stub OTP: parent +15550000001 / 123456, staff +15550000002 / 654321.
