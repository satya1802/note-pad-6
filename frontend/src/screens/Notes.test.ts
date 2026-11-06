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

  it("[AC-017] shows notes in the order the API returned them, without re-sorting client-side", async () => {
    setUser();
    const newer = {
      id: "nt_b",
      title: "Newer",
      body: "edited most recently",
      created_at: "2026-10-01T00:00:00+00:00",
      updated_at: "2026-11-05T00:00:00+00:00",
    };
    const older = {
      id: "nt_a",
      title: "Older",
      body: "edited first",
      created_at: "2026-11-01T00:00:00+00:00",
      updated_at: "2026-11-01T00:00:00+00:00",
    };
    // `newer`'s created_at is earlier than `older`'s: if the screen re-sorted by
    // created_at client-side it would come out second, not first.
    mockedApiFetch.mockResolvedValueOnce({ notes: [newer, older] });
    render(Notes);

    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));
    const firstTitle = await screen.findByText("Newer");
    const secondTitle = await screen.findByText("Older");
    expect(
      firstTitle.compareDocumentPosition(secondTitle) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it("[AC-018] with no notes at all shows an empty-state message inviting the first note", async () => {
    setUser();
    mockedApiFetch.mockResolvedValueOnce({ notes: [] });
    render(Notes);

    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));
    expect(await screen.findByText(/nothing filed yet/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /write your first note/i })).toBeInTheDocument();
  });

  it("[AC-019] typing in the search box queries GET /api/notes?q=<text> debounced and shows only what the API returns", async () => {
    setUser();
    const unrelated = {
      id: "nt_1",
      title: "Shopping list",
      body: "milk, eggs",
      created_at: "2026-11-01T00:00:00+00:00",
      updated_at: "2026-11-01T00:00:00+00:00",
    };
    mockedApiFetch.mockResolvedValueOnce({ notes: [unrelated] });
    render(Notes);
    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));
    await screen.findByText("Shopping list");

    // Server-returned note that does not itself contain "lease" -- proves the result
    // comes from the server, not a client-side filter of the stale list.
    const serverMatch = {
      id: "nt_2",
      title: "Flat renewal",
      body: "talk to the landlord",
      created_at: "2026-11-02T00:00:00+00:00",
      updated_at: "2026-11-06T00:00:00+00:00",
    };
    mockedApiFetch.mockResolvedValueOnce({ notes: [serverMatch] });

    await fireEvent.input(screen.getByLabelText(/search titles and body text/i), {
      target: { value: "lease" },
    });

    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes?q=lease"));
    expect(await screen.findByText("Flat renewal")).toBeInTheDocument();
    expect(screen.queryByText("Shopping list")).not.toBeInTheDocument();
  });

  it("[AC-020] a search with no matches shows a 'no results' message distinct from the empty state", async () => {
    setUser();
    const note = {
      id: "nt_1",
      title: "Shopping list",
      body: "milk, eggs",
      created_at: "2026-11-01T00:00:00+00:00",
      updated_at: "2026-11-01T00:00:00+00:00",
    };
    mockedApiFetch.mockResolvedValueOnce({ notes: [note] });
    render(Notes);
    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));
    await screen.findByText("Shopping list");

    mockedApiFetch.mockResolvedValueOnce({ notes: [] });
    await fireEvent.input(screen.getByLabelText(/search titles and body text/i), {
      target: { value: "zzz" },
    });

    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes?q=zzz"));
    expect(await screen.findByText(/no match/i)).toBeInTheDocument();
    expect(screen.queryByText(/nothing filed yet/i)).not.toBeInTheDocument();
  });

  it("[AC] redirects to sign-in on a 401 returned from a search request", async () => {
    setUser();
    const note = {
      id: "nt_1",
      title: "Shopping list",
      body: "milk, eggs",
      created_at: "2026-11-01T00:00:00+00:00",
      updated_at: "2026-11-01T00:00:00+00:00",
    };
    mockedApiFetch.mockResolvedValueOnce({ notes: [note] });
    render(Notes);
    await waitFor(() => expect(mockedApiFetch).toHaveBeenCalledWith("/api/notes"));
    await screen.findByText("Shopping list");

    mockedApiFetch.mockRejectedValueOnce(new ApiError(401, {}, "failed"));
    await fireEvent.input(screen.getByLabelText(/search titles and body text/i), {
      target: { value: "x" },
    });

    await waitFor(() => expect(go).toHaveBeenCalledWith("/sign-in"));
  });
});
