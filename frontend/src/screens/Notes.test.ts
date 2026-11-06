import { fireEvent, render, screen, waitFor } from "@testing-library/svelte";
import { afterEach, describe, expect, it, vi } from "vitest";

import Notes from "./Notes.svelte";
import { ApiError, apiFetch } from "@/lib/api";
import { go } from "@/lib/router.svelte";
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

afterEach(() => {
  vi.resetAllMocks();
});

function setUser() {
  session.user = { id: "u_1", email: "satya.ganaraju@quorq.ai" };
  session.checked = true;
}

async function openComposerAndFill(title: string, body: string) {
  await fireEvent.click(screen.getByRole("button", { name: /write a new note/i }));
  if (title) {
    await fireEvent.input(screen.getByLabelText(/^title/i), { target: { value: title } });
  }
  if (body) {
    await fireEvent.input(screen.getByLabelText(/^note$/i), { target: { value: body } });
  }
  await fireEvent.click(screen.getByRole("button", { name: /save note/i }));
}

describe("Notes", () => {
  it("[AC-008] loads the list from GET /api/notes on mount and shows a saved note's stored timestamps after POST", async () => {
    setUser();
    mockedApiFetch.mockResolvedValueOnce({ notes: [] });
    render(Notes);

    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));

    mockedApiFetch.mockResolvedValueOnce({
      note: {
        id: "nt_1",
        title: "Grocery list",
        body: "Milk, eggs, bread",
        created_at: "2026-11-06T09:12:00+00:00",
        updated_at: "2026-11-06T09:12:00+00:00",
      },
    });

    await openComposerAndFill("Grocery list", "Milk, eggs, bread");

    expect(mockedApiFetch).toHaveBeenCalledWith(
      "/api/notes",
      expect.objectContaining({ method: "POST" }),
    );
    expect(await screen.findByText("Grocery list")).toBeInTheDocument();
    expect(screen.getAllByText(/06 NOV 2026/).length).toBeGreaterThan(0);
  });

  it("[AC-009] saving with a blank title shows the title the API derived from the first body line", async () => {
    setUser();
    mockedApiFetch.mockResolvedValueOnce({ notes: [] });
    render(Notes);
    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));

    mockedApiFetch.mockResolvedValueOnce({
      note: {
        id: "nt_2",
        title: "First line of the body",
        body: "First line of the body\nmore text",
        created_at: "2026-11-06T09:00:00+00:00",
        updated_at: "2026-11-06T09:00:00+00:00",
      },
    });

    await openComposerAndFill("", "First line of the body\nmore text");

    expect(mockedApiFetch).toHaveBeenCalledWith(
      "/api/notes",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ title: "", body: "First line of the body\nmore text" }),
      }),
    );
    expect(await screen.findByText("First line of the body")).toBeInTheDocument();
  });

  it("[AC-010] a 422 for no title and no body prompts the user with the API's message", async () => {
    setUser();
    mockedApiFetch.mockResolvedValueOnce({ notes: [] });
    render(Notes);
    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));

    mockedApiFetch.mockRejectedValueOnce(
      new ApiError(
        422,
        { error: "empty_note", message: "Enter a title or some body text to save a note." },
        "failed",
      ),
    );

    await openComposerAndFill("", "");

    expect(
      await screen.findByText("Enter a title or some body text to save a note."),
    ).toBeInTheDocument();
  });

  it("the seeded sample notes and the offline toggle are gone", async () => {
    setUser();
    mockedApiFetch.mockResolvedValueOnce({ notes: [] });
    render(Notes);
    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));

    expect(screen.queryByText(/sourdough/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/work offline/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("switch")).not.toBeInTheDocument();
  });

  it("[AC] redirects to sign-in on a 401 from GET /api/notes", async () => {
    setUser();
    mockedApiFetch.mockRejectedValueOnce(new ApiError(401, {}, "failed"));
    render(Notes);

    await waitFor(() => expect(go).toHaveBeenCalledWith("/sign-in"));
  });
});
