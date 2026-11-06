import { expect, test, type Page } from "@playwright/test";

const PASSWORD = "correct-horse-battery";

function uniqueEmail(tag: string): string {
  return `qa-${tag}-${Date.now()}-${Math.floor(Math.random() * 100000)}@example.com`;
}

/** Fills the registration form and waits for the account-created confirmation. Leaves the
 * visitor on /register with an active session (same effect as signing in for a fresh user). */
async function registerAndLand(page: Page, email: string, password = PASSWORD): Promise<void> {
  await page.goto("/register");
  await page.locator("#ed-email").fill(email);
  await page.locator("#ed-password").fill(password);
  await page.getByRole("button", { name: "Create my account →" }).click();
  await expect(page.getByRole("status")).toContainText("Account opened", { timeout: 15_000 });
}

async function goToNotesFromRegisterSuccess(page: Page): Promise<void> {
  await page.getByRole("button", { name: "Write my first note →" }).click();
  await expect(page).toHaveURL(/\/notes$/);
  await expect(page.getByRole("heading", { name: "My notes", level: 1 })).toBeVisible();
}

async function openComposer(page: Page): Promise<void> {
  await page.getByRole("button", { name: "Write a new note" }).click();
  await expect(page.locator("#note-title")).toBeVisible();
}

test("[AC-sign-in] signing in with a registered account reaches the notes list", async ({
  page,
}) => {
  const email = uniqueEmail("signin");
  await registerAndLand(page, email);
  await goToNotesFromRegisterSuccess(page);

  await page.getByRole("button", { name: /Sign out/ }).click();
  await expect(page).toHaveURL(/\/sign-in$/);

  await page.locator("#signin-email").fill(email);
  await page.locator("#signin-password").fill(PASSWORD);
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(page.getByText("Session started")).toBeVisible({ timeout: 15_000 });
  await expect(page).toHaveURL(/\/notes$/, { timeout: 15_000 });
  await expect(page.getByText(email, { exact: false }).first()).toBeVisible();
});

test("[AC-008] creating a note with a title and body shows it at the top of the list", async ({
  page,
}) => {
  const email = uniqueEmail("create-both");
  await registerAndLand(page, email);
  await goToNotesFromRegisterSuccess(page);

  await openComposer(page);
  await page.locator("#note-title").fill("Shopping list");
  await page.locator("#note-body").fill("Milk\nEggs\nBread");
  await page.getByRole("button", { name: "Save note" }).click();

  await expect(page.getByRole("status")).toContainText("Saved", { timeout: 10_000 });
  await expect(page.getByRole("button", { name: "Shopping list" })).toBeVisible();
  await expect(page.getByText("Milk Eggs Bread", { exact: false })).toBeVisible();
});

test("[AC-009] creating a note with body only derives the title from the first line", async ({
  page,
}) => {
  const email = uniqueEmail("create-body-only");
  await registerAndLand(page, email);
  await goToNotesFromRegisterSuccess(page);

  await openComposer(page);
  await page.locator("#note-body").fill("Call the landlord about the boiler\nAsk about the lease too");
  await page.getByRole("button", { name: "Save note" }).click();

  await expect(page.getByRole("status")).toContainText("Saved", { timeout: 10_000 });
  await expect(
    page.getByRole("button", { name: "Call the landlord about the boiler" }),
  ).toBeVisible();
});

test("[AC-010] attempting an empty save shows a prompt to enter content", async ({ page }) => {
  const email = uniqueEmail("empty-save");
  await registerAndLand(page, email);
  await goToNotesFromRegisterSuccess(page);

  await openComposer(page);
  await page.getByRole("button", { name: "Save note" }).click();

  await expect(
    page.getByText("Enter a title or some body text to save a note.", { exact: false }),
  ).toBeVisible({ timeout: 10_000 });
  // The failed attempt created nothing: the empty-state copy is still showing.
  await expect(page.getByText("Nothing filed yet")).toBeVisible();
});

test("[NFR-004] the notes list renders without horizontal overflow at mobile and desktop widths", async ({
  page,
}) => {
  const email = uniqueEmail("responsive");
  await registerAndLand(page, email);
  await goToNotesFromRegisterSuccess(page);

  await page.setViewportSize({ width: 375, height: 667 });
  await page.waitForTimeout(100);
  let overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(overflow).toBe(false);

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.waitForTimeout(100);
  overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(overflow).toBe(false);
});
