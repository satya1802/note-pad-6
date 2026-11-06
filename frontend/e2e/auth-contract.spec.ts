import { expect, test } from "@playwright/test";

// Same fallback pattern as the other API-contract specs: no override given, so point at
// the locally-booted API on 127.0.0.1:8000.
const API_BASE_URL = process.env.E2E_API_URL ?? "http://127.0.0.1:8000";
const PASSWORD = "correct-horse-battery";

function uniqueEmail(tag: string): string {
  return `qa-auth-contract-${tag}-${Date.now()}-${Math.floor(Math.random() * 100000)}@example.com`;
}

/**
 * The deployed frontend and this API sit on different origins, so a session cookie is
 * not something a cross-origin browser reliably keeps sending -- the token
 * `/api/auth/register` and `/api/auth/login` hand back in the JSON body is what actually
 * has to authenticate every later call, sent as `Authorization: Bearer <token>`. Every
 * other spec in this suite drives the app through the browser (which does send cookies)
 * or reuses one Playwright `request` context across a whole flow (which also keeps
 * cookies) -- so nothing else proves the token alone, with no cookie in play at all, is
 * sufficient. These tests use a disposable context to obtain the token and a second,
 * never-cookied context to use it, so there is no cookie jar left to fall back on.
 */
test("[AC-session-token] a token from /api/auth/register authenticates later calls with no cookie present", async ({
  playwright,
}) => {
  const setup = await playwright.request.newContext({ baseURL: API_BASE_URL });
  const email = uniqueEmail("register");
  const register = await setup.post("/api/auth/register", {
    data: { email, password: PASSWORD },
  });
  expect(register.status()).toBe(201);
  const registerBody = await register.json();
  expect(typeof registerBody.token).toBe("string");
  expect(registerBody.token.length).toBeGreaterThan(10);
  const token = registerBody.token as string;
  await setup.dispose();

  // Never received a Set-Cookie from this API: only the Authorization header below can
  // be what authenticates it.
  const bearerOnly = await playwright.request.newContext({ baseURL: API_BASE_URL });

  const me = await bearerOnly.get("/api/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(me.status()).toBe(200);
  expect((await me.json()).user.email).toBe(email);

  const created = await bearerOnly.post("/api/notes", {
    headers: { Authorization: `Bearer ${token}` },
    data: { title: "Bearer-only note", body: "created with no cookie in play" },
  });
  expect(created.status()).toBe(201);
  const note = (await created.json()).note;

  const list = await bearerOnly.get("/api/notes", {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(list.status()).toBe(200);
  expect((await list.json()).notes.some((n: { id: string }) => n.id === note.id)).toBe(true);

  const removed = await bearerOnly.delete(`/api/notes/${note.id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect([200, 204]).toContain(removed.status());

  await bearerOnly.dispose();
});

test("[AC-session-token] a token from /api/auth/login works the same way after the registration session ends", async ({
  playwright,
}) => {
  const setup = await playwright.request.newContext({ baseURL: API_BASE_URL });
  const email = uniqueEmail("login");
  await setup.post("/api/auth/register", { data: { email, password: PASSWORD } });
  await setup.post("/api/auth/logout");

  const login = await setup.post("/api/auth/login", { data: { email, password: PASSWORD } });
  expect(login.status()).toBe(200);
  const token = (await login.json()).token as string;
  expect(typeof token).toBe("string");
  await setup.dispose();

  const bearerOnly = await playwright.request.newContext({ baseURL: API_BASE_URL });
  const me = await bearerOnly.get("/api/auth/me", { headers: { Authorization: `Bearer ${token}` } });

  expect(me.status()).toBe(200);
  expect((await me.json()).user.email).toBe(email);

  await bearerOnly.dispose();
});

test("[AC-session-token] no Authorization header, or a tampered one, is rejected with 401", async ({
  playwright,
}) => {
  const ctx = await playwright.request.newContext({ baseURL: API_BASE_URL });

  const noAuth = await ctx.get("/api/notes");
  expect(noAuth.status()).toBe(401);

  const tampered = await ctx.get("/api/notes", {
    headers: { Authorization: "Bearer not-a-real-token" },
  });
  expect(tampered.status()).toBe(401);

  const me = await ctx.get("/api/auth/me");
  expect(me.status()).toBe(401);

  await ctx.dispose();
});
