/**
 * Unit tests for `apiFetch` and the session-token helpers it is built on. Nothing else
 * in this repository exercises `lib/api.ts` directly -- every screen test mocks the
 * module instead -- so the one thing every screen assumes (a stored session token is
 * sent as `Authorization: Bearer <token>` on every call, and a non-2xx response becomes
 * a catchable `ApiError`) had no test proving it actually works.
 */
import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiError, apiFetch, clearSessionToken, getSessionToken, setSessionToken } from "./api";

function stubFetch(response: { ok: boolean; status: number; json: () => Promise<unknown> }) {
  const fetchMock = vi.fn().mockResolvedValue(response);
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

afterEach(() => {
  clearSessionToken();
  vi.unstubAllGlobals();
});

describe("session token storage", () => {
  it("setSessionToken persists the token for getSessionToken to read back", () => {
    setSessionToken("abc-123");

    expect(getSessionToken()).toBe("abc-123");
  });

  it("clearSessionToken removes a previously stored token", () => {
    setSessionToken("abc-123");

    clearSessionToken();

    expect(getSessionToken()).toBeNull();
  });
});

describe("apiFetch", () => {
  it("sends a stored session token as 'Authorization: Bearer <token>' on every call", async () => {
    setSessionToken("the-session-token");
    const fetchMock = stubFetch({ ok: true, status: 200, json: async () => ({ user: {} }) });

    await apiFetch("/api/auth/me");

    const [, init] = fetchMock.mock.calls[0];
    expect(init.headers.Authorization).toBe("Bearer the-session-token");
  });

  it("sends credentials: 'include' so a same-origin fallback session cookie is still honoured", async () => {
    const fetchMock = stubFetch({ ok: true, status: 200, json: async () => ({}) });

    await apiFetch("/api/notes");

    const [, init] = fetchMock.mock.calls[0];
    expect(init.credentials).toBe("include");
  });

  it("sends no Authorization header at all when neither a session token nor a shared secret is configured", async () => {
    clearSessionToken();
    const fetchMock = stubFetch({ ok: true, status: 200, json: async () => ({}) });

    await apiFetch("/api/notes");

    const [, init] = fetchMock.mock.calls[0];
    expect(init.headers.Authorization).toBeUndefined();
  });

  it("joins the base URL and the path with exactly one slash", async () => {
    const fetchMock = stubFetch({ ok: true, status: 200, json: async () => ({}) });

    await apiFetch("/api/notes");

    const [url] = fetchMock.mock.calls[0];
    expect(url).not.toMatch(/[^:]\/\/api\/notes/);
    expect(url.endsWith("/api/notes")).toBe(true);
  });

  it("throws an ApiError carrying the status and the parsed JSON body on a non-2xx response", async () => {
    stubFetch({
      ok: false,
      status: 409,
      json: async () => ({ error: "email_in_use", message: "That email is already registered." }),
    });

    await expect(apiFetch("/api/auth/register", { method: "POST" })).rejects.toBeInstanceOf(
      ApiError,
    );

    stubFetch({
      ok: false,
      status: 409,
      json: async () => ({ error: "email_in_use", message: "That email is already registered." }),
    });

    try {
      await apiFetch("/api/auth/register", { method: "POST" });
      throw new Error("apiFetch should have thrown");
    } catch (err) {
      expect(err).toBeInstanceOf(ApiError);
      expect((err as ApiError).status).toBe(409);
      expect((err as ApiError).body).toEqual({
        error: "email_in_use",
        message: "That email is already registered.",
      });
    }
  });

  it("resolves to undefined on a 204 No Content, without attempting to parse a body", async () => {
    const jsonSpy = vi.fn();
    stubFetch({ ok: true, status: 204, json: jsonSpy });

    const result = await apiFetch("/api/notes/nt_1", { method: "DELETE" });

    expect(result).toBeUndefined();
    expect(jsonSpy).not.toHaveBeenCalled();
  });

  it("resolves with the parsed JSON body on a normal 2xx response", async () => {
    stubFetch({ ok: true, status: 200, json: async () => ({ user: { id: "u_1" } }) });

    const result = await apiFetch<{ user: { id: string } }>("/api/auth/me");

    expect(result).toEqual({ user: { id: "u_1" } });
  });
});
