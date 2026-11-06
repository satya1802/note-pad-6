import { render } from "@testing-library/svelte";
import { tick } from "svelte";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App.svelte";
import { go } from "./lib/router.svelte";

function stubMe(ok: boolean) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok,
      status: ok ? 200 : 401,
      json: async () => (ok ? { user: { id: "u_1", email: "reader@example.com" } } : { error: "unauthorized" }),
    }),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("App", () => {
  it("[AC-007] renders a protected screen inside the app shell once a session is confirmed", async () => {
    stubMe(true);
    go("/notes");
    const { container } = render(App);
    await tick();
    await tick();
    await tick();
    expect(container.textContent).toContain("My notes");
  });

  it("[AC-007] redirects to sign-in when /api/auth/me reports no active session", async () => {
    stubMe(false);
    go("/notes");
    render(App);
    await tick();
    await tick();
    await tick();
    expect(window.location.pathname).toBe("/sign-in");
  });
});
