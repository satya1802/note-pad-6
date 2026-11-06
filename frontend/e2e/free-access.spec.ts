import { expect, test, type Page } from "@playwright/test";

const PASSWORD = "Sup3rSecret!1";

// Same fallback pattern as playwright.config.ts's webServer entry for the backend: no
// override given, so point at the locally-booted API on 127.0.0.1:8000.
const API_BASE_URL = process.env.E2E_API_URL ?? "http://127.0.0.1:8000";

// The exact word list from AC-024, matched whole-word and case-insensitively.
const PAYMENT_WORD_RE = /\b(payment|billing|card|subscription|upgrade|pricing|trial|plan)\b/gi;

// Known, deliberate reassurance copy the product is expected to show (e.g. "no card",
// "no billing", "no upgrade prompt"). Stripped out of a screen's visible text before the
// keyword scan runs below, so a real prompt anywhere else on the same screen is still
// caught. "free" is never special-cased because it is not one of the eight listed words,
// so bare "Free, always" / "Free to use" copy never needs an exclusion of its own.
const ALLOWED_COPY: RegExp[] = [
  /no\s+card\b/gi,
  /no\s+billing\b/gi,
  /no\s+upgrade\s+prompt\b/gi,
  /no\s+payment\s+is\s+ever\s+asked\s+for\b/gi,
  /free,?\s*always\s*(—|-)?\s*no\s+card/gi,
  /free\s*to\s*use/gi,
  /free,?\s*with\s+no\s+tier\s+above\s+it/gi,
  /free\s*(—|-)\s*no\s+billing,?\s*ever/gi,
];

// Domains a real payment gateway would send the browser to. The flow below must never
// cause a request (fetch, redirect, or an opened popup) toward any of them.
const PAYMENT_PROVIDER_RE =
  /stripe\.com|paypal\.com|braintreegateway\.com|checkout\.com|adyen\.com|squareup\.com|razorpay\.com/i;

function stripAllowedCopy(text: string): string {
  let out = text;
  for (const re of ALLOWED_COPY) out = out.replace(re, " ");
  return out;
}

async function assertNoPaymentPrompt(page: Page): Promise<void> {
  const text = await page.locator("body").innerText();
  const matches = stripAllowedCopy(text).match(PAYMENT_WORD_RE) ?? [];
  expect(matches, `unexpected payment-shaped words on screen: ${matches.join(", ")}`).toHaveLength(
    0,
  );
}

async function assertNoCardOrBillingFields(page: Page): Promise<void> {
  const count = await page
    .locator(
      [
        'input[type="card" i]',
        'input[type="billing" i]',
        'input[name*="card" i]',
        'input[name*="billing" i]',
        'input[autocomplete*="cc-" i]',
      ].join(", "),
    )
    .count();
  expect(count).toBe(0);
}

function uniqueEmail(tag: string): string {
  return `qa-free-${tag}-${Date.now()}-${Math.floor(Math.random() * 100000)}@example.com`;
}

/** Registers a brand-new account, exercises create/search/open/edit/delete on a note,
 * signs out and back in, and checks every screen traversed along the way for a payment
 * prompt, a card/billing form field, or an outbound hop to a payment provider. */
async function runFreeAccessFlow(page: Page, tag: string): Promise<void> {
  const outboundRequests: string[] = [];
  page.on("request", (req) => outboundRequests.push(req.url()));
  page.on("popup", (popup) => outboundRequests.push(popup.url()));

  const email = uniqueEmail(tag);

  // --- Registration ---
  await page.goto("/register");
  await assertNoPaymentPrompt(page);
  await assertNoCardOrBillingFields(page);
  await page.locator("#ed-email").fill(email);
  await page.locator("#ed-password").fill(PASSWORD);
  await page.getByRole("button", { name: "Create my account →" }).click();
  await expect(page.getByRole("status")).toContainText("Account opened", { timeout: 15_000 });
  await assertNoPaymentPrompt(page);

  await page.getByRole("button", { name: "Write my first note →" }).click();
  await expect(page).toHaveURL(/\/notes$/);
  await expect(page.getByRole("heading", { name: "My notes", level: 1 })).toBeVisible();
  await assertNoPaymentPrompt(page);
  await assertNoCardOrBillingFields(page);

  // --- Create ---
  await page.getByRole("button", { name: "Write a new note" }).click();
  await page.locator("#note-title").fill("Grocery run");
  await page.locator("#note-body").fill("Milk, eggs, bread");
  await assertNoPaymentPrompt(page);
  await assertNoCardOrBillingFields(page);
  await page.getByRole("button", { name: "Save note" }).click();
  await expect(page.getByRole("status")).toContainText("Saved", { timeout: 10_000 });
  await assertNoPaymentPrompt(page);

  // --- Search ---
  await page.locator("#note-search").fill("grocery");
  await expect(page.getByRole("button", { name: "Grocery run" })).toBeVisible({ timeout: 10_000 });
  await assertNoPaymentPrompt(page);

  // --- Open ---
  await page.getByRole("button", { name: "Grocery run" }).click();
  await expect(page.getByRole("heading", { name: "Grocery run" })).toBeVisible();
  await assertNoPaymentPrompt(page);

  // --- Edit ---
  await page.getByRole("button", { name: "Edit note" }).click();
  await page.locator("#note-body").fill("Milk, eggs, bread, butter");
  await assertNoPaymentPrompt(page);
  await assertNoCardOrBillingFields(page);
  await page.getByRole("button", { name: "Save changes" }).click();
  await expect(page.getByRole("status")).toContainText("Saved", { timeout: 10_000 });

  // --- Delete ---
  await page.getByRole("button", { name: "Delete", exact: true }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  const dialogText = stripAllowedCopy(await dialog.innerText());
  expect(dialogText.match(PAYMENT_WORD_RE) ?? []).toHaveLength(0);
  await assertNoCardOrBillingFields(page);
  await dialog.getByRole("button", { name: "Delete permanently" }).click();
  await expect(page).toHaveURL(/\/notes$/, { timeout: 10_000 });

  // --- Sign out, sign back in ---
  await page.getByRole("button", { name: /Sign out/ }).click();
  await expect(page).toHaveURL(/\/sign-in$/);
  await assertNoPaymentPrompt(page);
  await assertNoCardOrBillingFields(page);

  await page.locator("#signin-email").fill(email);
  await page.locator("#signin-password").fill(PASSWORD);
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/notes$/, { timeout: 15_000 });
  await assertNoPaymentPrompt(page);

  // The route table itself never grows a billing/checkout/upgrade screen to navigate to.
  await expect(page).not.toHaveURL(/billing|checkout|upgrade|subscribe|payment/i);

  const toProvider = outboundRequests.filter((url) => PAYMENT_PROVIDER_RE.test(url));
  expect(toProvider, `unexpected outbound navigation to a payment provider: ${toProvider.join(", ")}`).toHaveLength(
    0,
  );
}

test("[AC-024] registration, sign-in and every note feature never ask for payment — mobile viewport", async ({
  page,
}) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await runFreeAccessFlow(page, "mobile");
});

test("[AC-024] registration, sign-in and every note feature never ask for payment — desktop viewport", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await runFreeAccessFlow(page, "desktop");
});

test("[AC-024] the API contract never returns a payment-required status or billing-shaped fields", async ({
  request,
}) => {
  const email = uniqueEmail("api");

  const register = await request.post(`${API_BASE_URL}/api/auth/register`, {
    data: { email, password: PASSWORD },
  });
  expect(register.status()).toBe(201);
  expect(register.status()).not.toBe(402);
  const registerBody = await register.json();
  expect(JSON.stringify(registerBody).toLowerCase()).not.toMatch(
    /billing|subscription|payment|upgrade|stripe|checkout/,
  );

  const cookie = register.headers()["set-cookie"];
  const extraHeaders = cookie ? { Cookie: cookie.split(";")[0] } : {};

  const createNote = await request.post(`${API_BASE_URL}/api/notes`, {
    headers: extraHeaders,
    data: { title: "Free to use", body: "no card on file" },
  });
  expect(createNote.status()).toBe(201);
  const note = (await createNote.json()).note;
  expect(JSON.stringify(note).toLowerCase()).not.toMatch(/billing|subscription|payment|plan/);

  const list = await request.get(`${API_BASE_URL}/api/notes`, { headers: extraHeaders });
  expect(list.status()).toBe(200);

  const update = await request.put(`${API_BASE_URL}/api/notes/${note.id}`, {
    headers: extraHeaders,
    data: { title: "Free to use", body: "still no card" },
  });
  expect(update.status()).toBe(200);
  expect(update.status()).not.toBe(402);

  const remove = await request.delete(`${API_BASE_URL}/api/notes/${note.id}`, {
    headers: extraHeaders,
  });
  expect([200, 204]).toContain(remove.status());

  // No billing-style route exists to be gated behind in the first place.
  for (const path of ["/api/billing", "/api/subscription", "/api/payment", "/api/checkout"]) {
    const response = await request.get(`${API_BASE_URL}${path}`, { headers: extraHeaders });
    expect(response.status()).toBe(404);
  }
});
