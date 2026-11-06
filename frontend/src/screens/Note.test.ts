import { fireEvent, render, screen, waitFor } from "@testing-library/svelte";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import Note from "./Note.svelte";
import { ApiError, apiFetch } from "@/lib/api";
import { go, location } from "@/lib/router.svelte";
import { session } from "@/lib/session.svelte";

vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, apiFetch: vi.fn() };
});

vi.mock("@/lib/router.svelte", async () => {
  const actual = await vi.importActual<typeof import("@/lib/router.svelte")>("@/lib/router.svelte");
  return { ...actual, go: vi.fn() };
});

const mockedApiFetch = vi.mocked(apiFetch);

const NOTE = {
  id: "nt_1",
  title: "Grocery list",
  body: "Milk, eggs\nand bread",
  created_at: "2026-11-04T18:07:00+00:00",
  updated_at: "2026-11-06T08:42:00+00:00",
};

function setUser() {
  session.user = { id: "u_1", email: "satya.ganaraju@quorq.ai" };
  session.checked = true;
}

beforeEach(() => {
  setUser();
  location.path = "/note/nt_1";
});

afterEach(() => {
  vi.resetAllMocks();
});

describe("Note", () => {
  it("[AC-011] loads the note by id from GET /api/notes/{id} and shows title, body and timestamps", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);

    expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes/nt_1");
    expect(await screen.findByText("Grocery list")).toBeInTheDocument();
    expect(
      screen.getByText(
        (_, el) => el?.tagName === "P" && el.textContent === "Milk, eggs\nand bread",
      ),
    ).toBeInTheDocument();
    expect(screen.getByText(/Created 04 NOV 2026/)).toBeInTheDocument();
    expect(screen.getByText(/Updated 06 NOV 2026/)).toBeInTheDocument();
  });

  it("[AC-011] no seeded sample data remains", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);
    await screen.findByText("Grocery list");

    expect(screen.queryByText(/sourdough/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/rent increase/i)).not.toBeInTheDocument();
  });

  it("[AC-012] a 404 renders an access-denied state with no note content", async () => {
    mockedApiFetch.mockRejectedValueOnce(new ApiError(404, {}, "failed"));
    render(Note);

    expect(await screen.findByText(/isn't on your desk/i)).toBeInTheDocument();
    expect(screen.queryByText("Grocery list")).not.toBeInTheDocument();
  });

  it("[AC-012] a 403 renders an access-denied state with no note content", async () => {
    mockedApiFetch.mockRejectedValueOnce(new ApiError(403, {}, "failed"));
    render(Note);

    expect(await screen.findByText(/isn't on your desk/i)).toBeInTheDocument();
    expect(screen.queryByText("Grocery list")).not.toBeInTheDocument();
  });

  it("[AC-012] a 401 clears the session and routes to sign-in", async () => {
    mockedApiFetch.mockRejectedValueOnce(new ApiError(401, {}, "failed"));
    render(Note);

    await waitFor(() => expect(go).toHaveBeenCalledWith("/sign-in"));
    expect(session.user).toBeNull();
  });

  it("[AC-013] editing and saving issues PUT /api/notes/{id} and shows the new values and updated timestamp", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);
    await screen.findByText("Grocery list");

    await fireEvent.click(screen.getByRole("button", { name: /edit note/i }));

    const titleField = screen.getByLabelText(/title/i);
    await fireEvent.input(titleField, { target: { value: "Grocery list v2" } });

    mockedApiFetch.mockResolvedValueOnce({
      note: { ...NOTE, title: "Grocery list v2", updated_at: "2026-11-06T09:00:00+00:00" },
    });

    await fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    expect(mockedApiFetch).toHaveBeenCalledWith(
      "/api/notes/nt_1",
      expect.objectContaining({ method: "PUT" }),
    );
    expect(await screen.findByText("Grocery list v2")).toBeInTheDocument();
    expect(screen.getAllByText(/Updated 06 NOV 2026 · 09:00/).length).toBeGreaterThan(0);
  });

  it("[AC-014] saving with both title and body empty shows the backend's message", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);
    await screen.findByText("Grocery list");

    await fireEvent.click(screen.getByRole("button", { name: /edit note/i }));
    await fireEvent.input(screen.getByLabelText(/title/i), { target: { value: "" } });
    await fireEvent.input(screen.getByLabelText(/body/i), { target: { value: "" } });

    mockedApiFetch.mockRejectedValueOnce(
      new ApiError(
        422,
        { error: "empty_note", message: "Enter a title or some body text to save a note." },
        "failed",
      ),
    );

    await fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    expect(
      await screen.findByText("Enter a title or some body text to save a note."),
    ).toBeInTheDocument();
  });

  it("[AC-015] confirming delete calls DELETE /api/notes/{id} and returns to the notes list", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);
    await screen.findByText("Grocery list");

    await fireEvent.click(screen.getByRole("button", { name: /^delete$/i }));
    expect(await screen.findByRole("dialog")).toBeInTheDocument();

    mockedApiFetch.mockResolvedValueOnce(undefined);
    await fireEvent.click(screen.getByRole("button", { name: /delete permanently/i }));

    await waitFor(() =>
      expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes/nt_1", { method: "DELETE" }),
    );
    await waitFor(() => expect(go).toHaveBeenCalledWith("/notes"));
  });

  it("[AC-016] cancelling the confirmation with the button leaves the note unchanged and still displayed", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);
    await screen.findByText("Grocery list");

    await fireEvent.click(screen.getByRole("button", { name: /^delete$/i }));
    await screen.findByRole("dialog");

    await fireEvent.click(screen.getByRole("button", { name: /keep the note/i }));

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByText("Grocery list")).toBeInTheDocument();
    expect(mockedApiFetch).not.toHaveBeenCalledWith("/api/notes/nt_1", { method: "DELETE" });
  });

  it("[AC-016] cancelling the confirmation with Escape leaves the note unchanged and still displayed", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);
    await screen.findByText("Grocery list");

    await fireEvent.click(screen.getByRole("button", { name: /^delete$/i }));
    await screen.findByRole("dialog");

    await fireEvent.keyDown(window, { key: "Escape" });

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByText("Grocery list")).toBeInTheDocument();
  });

  it("[AC-024] viewing, editing and deleting a note never shows a payment or upgrade prompt", async () => {
    mockedApiFetch.mockResolvedValueOnce({ note: NOTE });
    render(Note);
    await screen.findByText("Grocery list");

    expect(screen.queryByLabelText(/card number/i)).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /subscribe|upgrade|add payment/i }),
    ).not.toBeInTheDocument();

    await fireEvent.click(screen.getByRole("button", { name: /edit note/i }));
    expect(screen.queryByText(/credit card|billing details|free trial/i)).not.toBeInTheDocument();
    await fireEvent.click(screen.getByRole("button", { name: /^cancel$/i }));

    await fireEvent.click(screen.getByRole("button", { name: /^delete$/i }));
    const dialog = await screen.findByRole("dialog");
    expect(dialog).not.toHaveTextContent(/payment|billing|subscription|upgrade/i);
  });
});
