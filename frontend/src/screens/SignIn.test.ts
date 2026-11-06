import { fireEvent, render, screen } from "@testing-library/svelte";
import { afterEach, describe, expect, it, vi } from "vitest";

import SignIn from "./SignIn.svelte";
import { apiFetch } from "@/lib/api";

vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, apiFetch: vi.fn() };
});

vi.mock("@/lib/router.svelte", async () => {
  const actual = await vi.importActual<typeof import("@/lib/router.svelte")>("@/lib/router.svelte");
  return { ...actual, go: vi.fn() };
});

const mockedApiFetch = vi.mocked(apiFetch);

afterEach(() => {
  vi.clearAllMocks();
});

async function fillAndSubmit(email: string, password: string) {
  await fireEvent.input(screen.getByLabelText(/email address/i), { target: { value: email } });
  await fireEvent.input(screen.getByLabelText(/^password$/i), { target: { value: password } });
  await fireEvent.click(screen.getByRole("button", { name: /sign in/i }));
}

describe("SignIn", () => {
  it("[AC-004] submits to the login endpoint and navigates to the notes list on success", async () => {
    mockedApiFetch.mockResolvedValueOnce({ user: { id: "u_1", email: "reader@example.com" } });
    render(SignIn);

    await fillAndSubmit("reader@example.com", "correct-horse");

    expect(mockedApiFetch).toHaveBeenCalledWith(
      "/api/auth/login",
      expect.objectContaining({ method: "POST" }),
    );
    expect(await screen.findByText(/session started/i)).toBeInTheDocument();
  });

  it("[AC-005, NFR-002] shows one generic error for wrong credentials, naming no field, with no demo-account shortcut", async () => {
    mockedApiFetch.mockRejectedValueOnce(new Error("401"));
    render(SignIn);

    await fillAndSubmit("reader@example.com", "wrong-password");

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("That email and password do not match an account.");
    expect(alert.textContent?.toLowerCase()).not.toMatch(
      /email is wrong|password is wrong|no such user/,
    );
    expect(screen.queryByText(/demo account/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/fill these in for me/i)).not.toBeInTheDocument();
  });
});
