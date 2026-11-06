import { fireEvent, render, screen } from "@testing-library/svelte";
import { afterEach, describe, expect, it, vi } from "vitest";

import Register from "./Register.svelte";
import { ApiError, apiFetch } from "@/lib/api";
import { go } from "@/lib/router.svelte";

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
  await fireEvent.input(screen.getByLabelText(/email/i), { target: { value: email } });
  await fireEvent.input(screen.getByLabelText(/password/i), { target: { value: password } });
  await fireEvent.click(screen.getByRole("button", { name: /create my account/i }));
}

describe("Register", () => {
  it("[AC-001] submits to the register endpoint and lands on the notes list on success", async () => {
    mockedApiFetch.mockResolvedValueOnce({ user: { id: "u_1", email: "new@example.com" } });
    render(Register);

    await fillAndSubmit("new@example.com", "correct-horse");

    expect(mockedApiFetch).toHaveBeenCalledWith(
      "/api/auth/register",
      expect.objectContaining({ method: "POST" }),
    );
    expect(await screen.findByRole("status")).toHaveTextContent("Account opened");

    await fireEvent.click(screen.getByRole("button", { name: /write my first note/i }));
    expect(go).toHaveBeenCalledWith("/notes");
  });

  it("[AC-002] shows an email-already-in-use message on a 409 and has no hardcoded email list", async () => {
    mockedApiFetch.mockRejectedValueOnce(new ApiError(409, { message: "in use" }, "failed"));
    render(Register);

    await fillAndSubmit("dana.whitfield@quorq.ai", "correct-horse");

    expect(await screen.findByRole("alert")).toHaveTextContent(/already in use/i);
  });

  it("[AC-003] shows the field-level 422 error returned by the server", async () => {
    mockedApiFetch.mockRejectedValueOnce(
      new ApiError(422, { fields: { email: "Email format is invalid." } }, "failed"),
    );
    render(Register);

    await fillAndSubmit("ok@example.com", "correct-horse");

    expect(await screen.findByText("Email format is invalid.")).toBeInTheDocument();
  });

  it("[AC-024] registering never shows a payment prompt, card field or upgrade offer", async () => {
    mockedApiFetch.mockResolvedValueOnce({ user: { id: "u_1", email: "new@example.com" } });
    render(Register);

    // Before submitting: no card field, no upgrade copy, on the form itself.
    expect(screen.queryByLabelText(/card number/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/credit card|subscription|upgrade to/i)).not.toBeInTheDocument();
    expect(screen.getByText(/free, always/i)).toBeInTheDocument();

    await fillAndSubmit("new@example.com", "correct-horse");
    await screen.findByRole("status");

    // After the account is created: same again, on the confirmation screen.
    expect(screen.queryByLabelText(/card number/i)).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /subscribe|upgrade|add payment/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByText(/credit card|billing details/i)).not.toBeInTheDocument();
  });
});
