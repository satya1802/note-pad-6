import { expect, test, type Page } from "@playwright/test";

const PASSWORD = "correct-horse";

function uniqueEmail(tag: string): string {
  return `qa-privacy-${tag}-${Date.now()}-${Math.floor(Math.random() * 100000)}@example.com`;
}

async function register(page: Page, email: string): Promise<void> {
  await page.goto("/register");
  await page.locator("#ed-email").fill(email);
  await page.locator("#ed-password").fill(PASSWORD);
  await page.getByRole("button", { name: "Create my account →" }).click();
  await expect(page.getByRole("status")).toContainText("Account opened", { timeout: 15_000 });
  await page.getByRole("button", { name: "Write my first note →" }).click();
  await expect(page).toHaveURL(/\/notes$/);
}

async function signOut(page: Page): Promise<void> {
  await page.getByRole("button", { name: /Sign out/ }).click();
  await expect(page).toHaveURL(/\/sign-in$/);
}

/** [AC-022][AC-023] User A's note is invisible to user B, both in the list and when
 * user B navigates straight to the note's URL. */
async function runIsolationFlow(page: Page, tag: string): Promise<void> {
  const emailA = uniqueEmail(`${tag}-a`);
  const emailB = uniqueEmail(`${tag}-b`);
  const secretTitle = `Private note ${tag} ${Date.now()}`;

  // --- User A creates a note and captures its direct URL ---
  await register(page, emailA);
  await page.getByRole("button", { name: "Write a new note" }).click();
  await page.locator("#note-title").fill(secretTitle);
  await page.locator("#note-body").fill("Only user A should ever see this body text.");
  await page.getByRole("button", { name: "Save note" }).click();
  await expect(page.getByRole("status")).toContainText("Saved", { timeout: 10_000 });

  await page.getByRole("button", { name: secretTitle }).click();
  await expect(page.getByRole("heading", { name: secretTitle })).toBeVisible();
  const noteUrl = page.url();

  await signOut(page);

  // --- User B signs in and should see none of it ---
  await register(page, emailB);
  await expect(page.getByText(secretTitle)).not.toBeVisible();

  await page.goto(noteUrl);
  await expect(page.getByText("This note isn't on your desk")).toBeVisible({ timeout: 10_000 });
  const bodyText = await page.locator("body").innerText();
  expect(bodyText).not.toContain(secretTitle);
  expect(bodyText).not.toContain("Only user A should ever see this body text.");
}

test("[AC-022][AC-023] user B never sees user A's note in the list or via direct URL — mobile viewport", async ({
  page,
}) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await runIsolationFlow(page, "mobile");
});

test("[AC-022][AC-023] user B never sees user A's note in the list or via direct URL — desktop viewport", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await runIsolationFlow(page, "desktop");
});
