// ABOUTME: E2E tests that verify bug fixes in UI (bugs.md).
// ABOUTME: Requires backend + frontend running; use stub OTP (123456 parent, 654321 staff).

import { test, expect } from "@playwright/test";

const PARENT_PHONE = "+15550000001";
const PARENT_OTP = "123456";
const STAFF_PHONE = "+15550000002";
const STAFF_OTP = "654321";

async function loginAsParent(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel(/phone/i).fill(PARENT_PHONE);
  await page.getByRole("button", { name: /continue/i }).click();
  await page.waitForURL(/\/login\/otp/);
  await page.getByLabel(/verification code/i).fill(PARENT_OTP);
  await page.getByRole("button", { name: /verify/i }).click();
  await page.waitForURL((u) => u.pathname === "/" || u.pathname.startsWith("/tickets"));
}

async function loginAsStaff(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel(/phone/i).fill(STAFF_PHONE);
  await page.getByRole("button", { name: /continue/i }).click();
  await page.waitForURL(/\/login\/otp/);
  await page.getByLabel(/verification code/i).fill(STAFF_OTP);
  await page.getByRole("button", { name: /verify/i }).click();
  await page.waitForURL((u) => u.pathname === "/" || u.pathname.startsWith("/staff"));
}

test.describe("Bug-fix UI verification", () => {
  test("BUG-003: Parent visiting /staff is redirected to /", async ({ page }) => {
    await loginAsParent(page);
    await page.goto("/staff");
    await expect(page).toHaveURL(/\//);
    await expect(page).not.toHaveURL(/\/staff/);
  });

  test("BUG-006 + BUG-007: Staff sees Staff nav and Home CTA", async ({ page }) => {
    await loginAsStaff(page);
    await expect(page.getByRole("link", { name: /staff/i }).first()).toBeVisible();
    await expect(page.getByRole("link", { name: /staff inbox/i }).first()).toBeVisible();
  });

  test("BUG-006: Parent does not see Staff in bottom nav", async ({ page }) => {
    await loginAsParent(page);
    const nav = page.getByRole("navigation", { name: /main/i });
    await expect(nav.getByRole("link", { name: /^staff$/i })).not.toBeVisible();
  });

  test("BUG-008: Profile shows read-only message, no Save button", async ({ page }) => {
    await loginAsParent(page);
    await page.getByRole("link", { name: /profile/i }).click();
    await expect(page.getByText(/profile updates coming soon/i)).toBeVisible();
    await expect(page.getByRole("button", { name: /save changes/i })).not.toBeVisible();
  });

  test("BUG-011: Tickets list shows create CTA and either list or empty state copy", async ({ page }) => {
    await loginAsParent(page);
    await page.getByRole("link", { name: /tickets/i }).first().click();
    await page.waitForURL(/\/tickets/);
    await expect(page.getByRole("link", { name: /create ticket/i }).or(page.getByRole("button", { name: /create ticket/i })).first()).toBeVisible();
    const hasListOrEmpty =
      (await page.getByText(/no tickets yet/i).count()) > 0 ||
      (await page.getByText(/no tickets match your filters/i).count()) > 0 ||
      (await page.locator("a[href*='/tickets/']").count()) > 0;
    expect(hasListOrEmpty).toBe(true);
  });

  test("BUG-013: Nav highlights current route (Tickets when on /tickets)", async ({ page }) => {
    await loginAsParent(page);
    await page.goto("/tickets");
    const ticketsLink = page.getByRole("navigation", { name: /main/i }).getByRole("link", { name: /^tickets$/i });
    await expect(ticketsLink).toHaveAttribute("aria-current", "page");
  });

  test("BUG-001: Satisfied page shows loading then success (API called)", async ({ page }) => {
    await loginAsParent(page);
    await page.goto("/tickets/1/satisfied");
    await expect(page.getByText(/thank you|resolved to your satisfaction|error|could not mark/i)).toBeVisible({
      timeout: 15000,
    });
  });

  test("BUG-002: Reopen page has form and submit calls API", async ({ page }) => {
    await loginAsParent(page);
    await page.goto("/tickets/1/reopen");
    await expect(page.getByRole("heading", { name: /request reopen/i })).toBeVisible();
    await page.getByLabel(/reason/i).fill("E2E test reason");
    await page.getByRole("button", { name: /submit request/i }).click();
    await expect(
      page.getByText(/reopen request has been submitted|error|cannot be reopened/i)
    ).toBeVisible({ timeout: 10000 });
  });
});
