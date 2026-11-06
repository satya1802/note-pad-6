<script>
  import { Icon, Input, Label, Stat, Textarea } from "@/lib/ui";
  import { brand } from "@/lib/brand";
  import { useNavigate } from "@/lib/navigate";
  import { apiFetch, ApiError } from "@/lib/api";
  import { session, clearSession } from "@/lib/session.svelte";

  const navigate = useNavigate();

  const MONTHS = [
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
  ];

  let notes = $state([]);

  let query = $state("");
  let composerOpen = $state(false);
  let composerIn = $state(false);
  let composerEl = $state(null);
  let draftTitle = $state("");
  let draftBody = $state("");
  let formError = $state("");
  let saving = $state(false);
  let flash = $state(null);
  let loading = $state(true);
  let listError = $state("");
  let signingOut = $state(false);
  let newId = $state(null);

  const q = $derived(query.trim().toLowerCase());
  const sorted = $derived([...notes].sort((a, b) => b.created_at.localeCompare(a.created_at)));
  const results = $derived(
    q ? sorted.filter((n) => (n.title + " " + n.body).toLowerCase().includes(q)) : sorted,
  );
  const totalWords = $derived(
    notes.reduce((sum, n) => sum + n.body.trim().split(/\s+/).filter(Boolean).length, 0),
  );
  const draftWords = $derived(draftBody.trim().split(/\s+/).filter(Boolean).length);

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function stamp(iso) {
    const [d, t] = iso.split("T");
    const [y, m, day] = d.split("-");
    return day + " " + MONTHS[Number(m) - 1] + " " + y + " · " + t.slice(0, 5);
  }

  function snippet(note, needle) {
    const body = note.body.replace(/\s+/g, " ").trim();
    if (!body) return "No body text.";
    if (!needle) return body.length > 165 ? body.slice(0, 165) + "…" : body;
    const idx = body.toLowerCase().indexOf(needle);
    if (idx === -1) return body.length > 165 ? body.slice(0, 165) + "…" : body;
    const start = Math.max(0, idx - 55);
    const end = Math.min(body.length, start + 175);
    return (start > 0 ? "…" : "") + body.slice(start, end) + (end < body.length ? "…" : "");
  }

  function parts(text, needle) {
    if (!needle) return [{ t: text, hit: false }];
    const out = [];
    const lower = text.toLowerCase();
    let i = 0;
    while (i <= text.length) {
      const idx = lower.indexOf(needle, i);
      if (idx === -1) {
        out.push({ t: text.slice(i), hit: false });
        break;
      }
      out.push({ t: text.slice(i, idx), hit: false });
      out.push({ t: text.slice(idx, idx + needle.length), hit: true });
      i = idx + needle.length;
    }
    return out.filter((p) => p.t.length > 0);
  }

  function openComposer() {
    composerOpen = true;
    formError = "";
  }

  function closeComposer() {
    composerOpen = false;
    formError = "";
  }

  /** A 401 on any notes call means the session is gone: forget it and send the
   * visitor back to sign in, same as a deliberate sign-out. */
  function handleUnauthorized() {
    clearSession();
    navigate("sign-in");
  }

  async function loadNotes() {
    loading = true;
    listError = "";
    try {
      const data = await apiFetch("/api/notes");
      notes = Array.isArray(data?.notes) ? data.notes : [];
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        handleUnauthorized();
        return;
      }
      listError = "Could not reach the notes server. Try again.";
    } finally {
      loading = false;
    }
  }

  async function saveNote(event) {
    event.preventDefault();
    if (saving) return;
    formError = "";
    saving = true;
    try {
      const data = await apiFetch("/api/notes", {
        method: "POST",
        body: JSON.stringify({ title: draftTitle.trim(), body: draftBody.trim() }),
      });
      notes = [data.note, ...notes];
      newId = data.note.id;
      composerOpen = false;
      draftTitle = "";
      draftBody = "";
      query = "";
      flash = {
        kind: "success",
        text: "Saved. “" + data.note.title + "” is at the top of your list.",
      };
      setTimeout(() => {
        if (newId === data.note.id) newId = null;
      }, 2400);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        handleUnauthorized();
        return;
      }
      if (err instanceof ApiError && err.status === 422) {
        formError =
          (err.body && err.body.message) ||
          "Enter a title or some body text to save a note.";
      } else {
        formError = "Could not save the note. Try again.";
      }
    } finally {
      saving = false;
    }
  }

  async function signOut() {
    if (signingOut) return;
    signingOut = true;
    try {
      await apiFetch("/api/auth/logout", { method: "POST" });
    } catch {
      // The user's intent is to leave regardless; clear local state and go anyway.
    }
    clearSession();
    navigate("sign-in");
  }

  function openNote() {
    navigate("note");
  }

  function onKey(event) {
    if (event.key !== "Escape") return;
    if (composerOpen && !saving) {
      closeComposer();
    } else if (query) {
      query = "";
    }
  }

  $effect(() => {
    loadNotes();
  });

  $effect(() => {
    if (composerOpen) {
      composerIn = false;
      requestAnimationFrame(() => {
        composerIn = true;
      });
      if (composerEl) {
        const field = composerEl.querySelector("#note-title");
        if (field) field.focus();
      }
    } else {
      composerIn = false;
    }
  });


</script>

<svelte:window onkeydown={onKey} />

<div
  class="min-h-screen w-full"
  style="--ink: {brand.primaryColor}; --paper: {brand.backgroundColor}; --accent: {brand.accentColor}; --muted: {brand.neutralColor}; background-color: {brand.backgroundColor}; color: {brand.primaryColor}; font-family: {brand.fontBody}; font-variant-numeric: tabular-nums;"
>
  <div class="mx-auto w-full max-w-6xl px-5 py-10 sm:px-8 lg:px-12 lg:py-14">
    <!-- Masthead -->
    <header class="border-b-[3px] pb-6" style="border-color: {brand.primaryColor}">
      <div class="flex flex-wrap items-end justify-between gap-6">
        <div class="min-w-0">
          <p class="text-[11px] uppercase tracking-[0.34em]" style="color: {brand.neutralColor}">
            Notepad 6 · Private edition
          </p>
          <h1
            class="mt-3 text-[2.75rem] leading-[0.95] sm:text-6xl"
            style="font-family: {brand.fontHeading}; letter-spacing: -0.01em;"
          >
            My notes
          </h1>
        </div>
        <div class="flex items-center gap-4">
          <div class="text-right text-[11px] uppercase leading-5 tracking-[0.18em]">
            <p style="color: {brand.neutralColor}">Signed in as</p>
            <p class="break-all">{session.user ? session.user.email : ""}</p>
          </div>
          <button
            type="button"
            onclick={signOut}
            disabled={signingOut}
            class="inline-flex min-h-[44px] items-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] transition-all duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-60 motion-reduce:transition-none"
            style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
          >
            <Icon name="ArrowLeft" class="h-4 w-4" aria-hidden="true" />
            {signingOut ? "Signing out…" : "Sign out"}
          </button>
        </div>
      </div>

      <dl
        class="mt-6 flex flex-wrap items-baseline gap-x-8 gap-y-2 text-[11px] uppercase tracking-[0.18em]"
      >
        <div class="flex gap-2">
          <dt style="color: {brand.neutralColor}">Notes</dt>
          <dd>{pad(notes.length)}</dd>
        </div>
        <div class="flex gap-2">
          <dt style="color: {brand.neutralColor}">Words</dt>
          <dd>{totalWords.toLocaleString("en-GB")}</dd>
        </div>
        <div class="flex gap-2">
          <dt style="color: {brand.neutralColor}">Account</dt>
          <dd>Free — no billing, ever</dd>
        </div>
      </dl>
    </header>

    <div class="mt-10 grid gap-10 lg:grid-cols-3 lg:gap-12">
      <!-- Main column -->
      <div class="lg:col-span-2">
        <!-- Section 01: search + new note -->
        <section aria-labelledby="sec-search">
          <h2
            id="sec-search"
            class="text-[11px] uppercase tracking-[0.3em]"
            style="color: {brand.neutralColor}"
          >
            § 01 — Find or write
          </h2>

          <div class="mt-4 flex flex-col gap-4 sm:flex-row sm:items-end">
            <form
              role="search"
              aria-label="Search your notes"
              class="min-w-0 flex-1"
              onsubmit={(e) => e.preventDefault()}
            >
              <Label for="note-search" class="block text-[11px] uppercase tracking-[0.2em]">
                Search titles and body text
              </Label>
              <div
                class="mt-2 flex items-center gap-3 border-[3px] bg-white px-4"
                style="border-color: {brand.primaryColor}"
              >
                <Icon name="Search" class="h-4 w-4 shrink-0" aria-hidden="true" />
                <Input
                  id="note-search"
                  type="search"
                  bind:value={query}
                  placeholder="lease, Reykjavík, cambelt…"
                  class="h-12 w-full border-0 bg-transparent px-0 text-sm focus:outline-none"
                  style="font-family: {brand.fontBody}; color: {brand.primaryColor}; border-radius: 0;"
                />
                {#if query}
                  <button
                    type="button"
                    aria-label="Clear the search box"
                    onclick={() => (query = "")}
                    class="inline-flex h-9 w-9 items-center justify-center border-[3px] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                    style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
                  >
                    <Icon name="X" class="h-3.5 w-3.5" aria-hidden="true" />
                  </button>
                {/if}
              </div>
            </form>

            <button
              type="button"
              onclick={openComposer}
              aria-expanded={composerOpen}
              aria-controls="composer"
              class="inline-flex min-h-[52px] items-center justify-center gap-3 border-[3px] px-6 py-3 text-xs uppercase tracking-[0.22em] text-white transition-transform duration-150 motion-safe:hover:-translate-x-0.5 motion-safe:hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
              style="background-color: {brand.accentColor}; border-color: {brand.primaryColor}; box-shadow: 6px 6px 0 {brand.primaryColor}; outline-color: {brand.primaryColor};"
            >
              <Icon name="Plus" class="h-4 w-4" aria-hidden="true" />
              Write a new note
            </button>
          </div>

          <p
            aria-live="polite"
            class="mt-3 text-[11px] uppercase tracking-[0.18em]"
            style="color: {brand.neutralColor}"
          >
            {#if q}
              Showing {pad(results.length)} of {pad(notes.length)} — matching “{query.trim()}”
            {:else}
              Showing all {pad(notes.length)} of your notes, newest first
            {/if}
          </p>
        </section>

        <!-- Composer -->
        {#if composerOpen}
          <section
            id="composer"
            aria-labelledby="composer-heading"
            bind:this={composerEl}
            class="mt-6 border-[3px] bg-white transition-all duration-300 ease-out motion-reduce:transition-none {composerIn
              ? 'translate-y-0 opacity-100'
              : '-translate-y-2 opacity-0'}"
            style="border-color: {brand.primaryColor}; box-shadow: 8px 8px 0 {brand.primaryColor};"
          >
            <div
              class="flex items-center justify-between border-b-[3px] px-6 py-4"
              style="border-color: {brand.primaryColor}"
            >
              <h3 id="composer-heading" class="text-2xl" style="font-family: {brand.fontHeading}">
                New note
              </h3>
              <span
                class="text-[11px] uppercase tracking-[0.2em]"
                style="color: {brand.neutralColor}"
              >
                {draftWords} words · {draftBody.length} chars
              </span>
            </div>

            <form class="px-6 py-6" onsubmit={saveNote} novalidate>
              <div>
                <Label for="note-title" class="block text-[11px] uppercase tracking-[0.2em]"
                  >Title — optional</Label
                >
                <Input
                  id="note-title"
                  bind:value={draftTitle}
                  placeholder="Leave blank to use the first line"
                  class="mt-2 h-12 w-full border-[3px] px-4 text-base focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                  style="border-color: {brand.primaryColor}; border-radius: 0; font-family: {brand.fontBody}; outline-color: {brand.accentColor};"
                />
              </div>

              <div class="mt-6">
                <Label for="note-body" class="block text-[11px] uppercase tracking-[0.2em]"
                  >Note</Label
                >
                <Textarea
                  id="note-body"
                  rows="7"
                  bind:value={draftBody}
                  placeholder="Plain text only. Line breaks are kept exactly as you type them."
                  class="mt-2 w-full border-[3px] p-4 text-sm leading-relaxed focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                  style="border-color: {brand.primaryColor}; border-radius: 0; font-family: {brand.fontBody}; outline-color: {brand.accentColor};"
                />
              </div>

              <div aria-live="assertive">
                {#if formError}
                  <p
                    class="mt-4 flex items-start gap-3 border-[3px] px-4 py-3 text-sm leading-relaxed"
                    style="border-color: {brand.primaryColor}; background-color: {brand.backgroundColor};"
                  >
                    <Icon name="AlertCircle" class="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span>{formError}</span>
                  </p>
                {/if}
              </div>

              <div
                class="mt-6 flex flex-wrap items-center gap-4 border-t-[3px] pt-5"
                style="border-color: {brand.primaryColor}"
              >
                <button
                  type="submit"
                  disabled={saving}
                  class="inline-flex min-h-[48px] items-center gap-3 border-[3px] px-6 py-3 text-xs uppercase tracking-[0.22em] text-white transition-transform duration-150 motion-safe:hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-70 motion-reduce:transition-none"
                  style="background-color: {brand.accentColor}; border-color: {brand.primaryColor}; box-shadow: 5px 5px 0 {brand.primaryColor}; outline-color: {brand.primaryColor};"
                >
                  {#if saving}
                    <Icon
                      name="Clock"
                      class="h-4 w-4 motion-safe:animate-spin"
                      aria-hidden="true"
                    />
                    Saving…
                  {:else}
                    <Icon name="Check" class="h-4 w-4" aria-hidden="true" />
                    Save note
                  {/if}
                </button>

                <button
                  type="button"
                  onclick={closeComposer}
                  class="inline-flex min-h-[48px] items-center px-2 text-xs uppercase tracking-[0.22em] underline underline-offset-4 transition-colors duration-150 hover:text-[color:var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                  style="color: {brand.neutralColor}; outline-color: {brand.accentColor};"
                >
                  Cancel — keeps your draft
                </button>

                <span
                  class="ml-auto text-[11px] uppercase tracking-[0.18em]"
                  style="color: {brand.neutralColor}"
                >
                  Saves to your account
                </span>
              </div>
            </form>
          </section>
        {/if}

        <!-- Flash -->
        {#if flash}
          <div
            role="status"
            class="mt-6 flex items-start gap-3 border-[3px] px-4 py-3"
            style="border-color: {brand.primaryColor}; background-color: {flash.kind === 'success'
              ? '#ffffff'
              : brand.backgroundColor};"
          >
            <Icon
              name={flash.kind === "success" ? "CheckCircle" : "AlertCircle"}
              class="mt-0.5 h-4 w-4 shrink-0"
              aria-hidden="true"
            />
            <p class="flex-1 text-sm leading-relaxed">{flash.text}</p>
            <button
              type="button"
              aria-label="Dismiss this message"
              onclick={() => (flash = null)}
              class="inline-flex h-8 w-8 items-center justify-center border-[3px] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
              style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
            >
              <Icon name="X" class="h-3.5 w-3.5" aria-hidden="true" />
            </button>
          </div>
        {/if}

        <!-- Section 02: the list -->
        <section aria-labelledby="sec-notes" class="mt-12">
          <div class="flex flex-wrap items-baseline justify-between gap-4">
            <h2
              id="sec-notes"
              class="text-[11px] uppercase tracking-[0.3em]"
              style="color: {brand.neutralColor}"
            >
              § 02 — Your notes
            </h2>
            <p class="text-[11px] uppercase tracking-[0.18em]" style="color: {brand.neutralColor}">
              Ordered newest first
            </p>
          </div>

          {#if listError}
            <div
              class="mt-4 border-[3px] bg-white p-6"
              style="border-color: {brand.primaryColor}; box-shadow: 6px 6px 0 {brand.primaryColor};"
            >
              <h3 class="flex items-center gap-3 text-[11px] uppercase tracking-[0.2em]">
                <Icon name="AlertCircle" class="h-4 w-4" aria-hidden="true" />
                Could not load your notes
              </h3>
              <p
                class="mt-3 max-w-[66ch] text-sm leading-relaxed"
                style="color: {brand.neutralColor}"
              >
                {listError}
              </p>
              <button
                type="button"
                onclick={loadNotes}
                class="mt-5 inline-flex min-h-[44px] items-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
              >
                <Icon name="Upload" class="h-4 w-4" aria-hidden="true" />
                Try again
              </button>
            </div>
          {/if}

          {#if loading}
            <div
              class="mt-4 border-[3px] bg-white"
              style="border-color: {brand.primaryColor}; box-shadow: 6px 6px 0 {brand.primaryColor};"
              aria-live="polite"
            >
              <p
                class="border-b-[3px] px-6 py-3 text-[11px] uppercase tracking-[0.2em]"
                style="border-color: {brand.primaryColor}"
              >
                Fetching your notes…
              </p>
              {#each [0, 1, 2] as row (row)}
                <div
                  class="flex gap-6 border-b-[3px] p-6 last:border-b-0"
                  style="border-color: {brand.primaryColor}"
                >
                  <div
                    class="h-3 w-8 motion-safe:animate-pulse"
                    style="background-color: {brand.neutralColor}; opacity: 0.25;"
                  ></div>
                  <div class="flex-1 space-y-3">
                    <div
                      class="h-5 w-2/3 motion-safe:animate-pulse"
                      style="background-color: {brand.neutralColor}; opacity: 0.25;"
                    ></div>
                    <div
                      class="h-3 w-full motion-safe:animate-pulse"
                      style="background-color: {brand.neutralColor}; opacity: 0.18;"
                    ></div>
                    <div
                      class="h-3 w-5/6 motion-safe:animate-pulse"
                      style="background-color: {brand.neutralColor}; opacity: 0.18;"
                    ></div>
                  </div>
                </div>
              {/each}
            </div>
          {:else if notes.length === 0}
            <div
              class="mt-4 border-[3px] bg-white px-8 py-14 text-center"
              style="border-color: {brand.primaryColor}; box-shadow: 8px 8px 0 {brand.primaryColor};"
            >
              <p class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">
                Blank page
              </p>
              <h3 class="mt-4 text-4xl" style="font-family: {brand.fontHeading}">
                Nothing filed yet
              </h3>
              <p
                class="mx-auto mt-4 max-w-[52ch] text-sm leading-relaxed"
                style="color: {brand.neutralColor}"
              >
                This is your own notepad — a shopping list, a half-written reply, the thing you will
                forget by Thursday. Only you can read what you put here.
              </p>
              <button
                type="button"
                onclick={openComposer}
                class="mt-7 inline-flex min-h-[48px] items-center gap-3 border-[3px] px-6 py-3 text-xs uppercase tracking-[0.22em] text-white transition-transform duration-150 motion-safe:hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                style="background-color: {brand.accentColor}; border-color: {brand.primaryColor}; box-shadow: 6px 6px 0 {brand.primaryColor}; outline-color: {brand.primaryColor};"
              >
                <Icon name="Plus" class="h-4 w-4" aria-hidden="true" />
                Write your first note
              </button>
            </div>
          {:else if results.length === 0}
            <div
              class="mt-4 border-[3px] bg-white px-8 py-12"
              style="border-color: {brand.primaryColor}; box-shadow: 8px 8px 0 {brand.primaryColor};"
            >
              <p class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">
                No match
              </p>
              <h3 class="mt-4 text-3xl" style="font-family: {brand.fontHeading}">
                Nothing of yours says “{query.trim()}”
              </h3>
              <p
                class="mt-4 max-w-[60ch] text-sm leading-relaxed"
                style="color: {brand.neutralColor}"
              >
                Search reads the title and body of all {notes.length} of your notes, and nothing outside
                your account. Try a shorter word, or clear the box to see the whole list again.
              </p>
              <div class="mt-7 flex flex-wrap gap-4">
                <button
                  type="button"
                  onclick={() => (query = "")}
                  class="inline-flex min-h-[44px] items-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                  style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
                >
                  <Icon name="X" class="h-4 w-4" aria-hidden="true" />
                  Clear the search
                </button>
                <button
                  type="button"
                  onclick={() => {
                    draftTitle = query.trim();
                    openComposer();
                  }}
                  class="inline-flex min-h-[44px] items-center gap-2 px-2 text-[11px] uppercase tracking-[0.2em] underline underline-offset-4 transition-colors duration-150 hover:text-[color:var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                  style="color: {brand.neutralColor}; outline-color: {brand.accentColor};"
                >
                  Start a note called “{query.trim()}”
                </button>
              </div>
            </div>
          {:else}
            <ol
              class="mt-4 border-[3px] bg-white"
              style="border-color: {brand.primaryColor}; box-shadow: 8px 8px 0 {brand.primaryColor};"
            >
              {#each results as note, i (note.id)}
                <li
                  class="border-b-[3px] transition-colors duration-700 last:border-b-0 motion-reduce:transition-none"
                  style="border-color: {brand.primaryColor}; border-left: {note.id === newId
                    ? '8px solid ' + brand.accentColor
                    : '0'};"
                >
                  <div class="flex flex-col gap-4 p-6 sm:flex-row sm:items-start sm:gap-6">
                    <span
                      class="pt-1 text-[11px] uppercase tracking-[0.2em]"
                      style="color: {brand.neutralColor}"
                    >
                      {pad(i + 1)}
                    </span>

                    <div class="min-w-0 flex-1">
                      <h3 class="text-2xl leading-tight" style="font-family: {brand.fontHeading}">
                        <button
                          type="button"
                          onclick={() => openNote(note.id)}
                          class="text-left underline-offset-[6px] transition-colors duration-150 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 motion-reduce:transition-none"
                          style="outline-color: {brand.accentColor};"
                        >
                          {#each parts(note.title, q) as piece, pi (pi)}
                            {#if piece.hit}
                              <mark
                                style="background-color: {brand.accentColor}; color: #ffffff; padding: 0 2px;"
                                >{piece.t}</mark
                              >
                            {:else}{piece.t}{/if}
                          {/each}
                        </button>
                      </h3>

                      <p
                        class="mt-2 max-w-[72ch] text-sm leading-relaxed"
                        style="color: {brand.neutralColor}"
                      >
                        {#each parts(snippet(note, q), q) as piece, pi (pi)}
                          {#if piece.hit}
                            <mark
                              style="background-color: {brand.accentColor}; color: #ffffff; padding: 0 2px;"
                              >{piece.t}</mark
                            >
                          {:else}{piece.t}{/if}
                        {/each}
                      </p>

                      <p
                        class="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-[11px] uppercase tracking-[0.18em]"
                      >
                        <span style="color: {brand.neutralColor}">Updated</span>
                        <span>{stamp(note.updated_at)}</span>
                        <span aria-hidden="true" style="color: {brand.neutralColor}">/</span>
                        <span style="color: {brand.neutralColor}"
                          >Created {stamp(note.created_at)}</span
                        >
                      </p>
                    </div>

                    <div class="flex shrink-0 items-center gap-3">
                      <button
                        type="button"
                        onclick={() => openNote(note.id)}
                        class="inline-flex min-h-[44px] items-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                        style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
                      >
                        Open
                        <Icon name="ChevronRight" class="h-4 w-4" aria-hidden="true" />
                      </button>
                    </div>
                  </div>
                </li>
              {/each}
            </ol>
          {/if}
        </section>
      </div>

      <!-- Aside -->
      <aside class="lg:col-span-1">
        <h2 class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">
          § 03 — This account
        </h2>

        <div class="mt-4 border-[3px] bg-white" style="border-color: {brand.primaryColor}">
          <div class="border-b-[3px] p-5" style="border-color: {brand.primaryColor}">
            <Stat label="Notes kept" value={pad(notes.length)} hint="All saved to your account" />
          </div>
          <div class="p-5">
            <Stat
              label="Words written"
              value={totalWords.toLocaleString("en-GB")}
              hint="Across every note"
            />
          </div>
        </div>

        <div class="mt-6 border-[3px] p-5" style="border-color: {brand.primaryColor}">
          <h3 class="flex items-center gap-2 text-[11px] uppercase tracking-[0.2em]">
            <Icon name="User" class="h-4 w-4" aria-hidden="true" />
            Private to you
          </h3>
          <p class="mt-3 text-sm leading-relaxed" style="color: {brand.neutralColor}">
            Every note here is stored against <span style="color: {brand.primaryColor}"
              >{session.user ? session.user.email : ""}</span
            >. Listing, searching and opening all run inside your account — nobody else’s notes can
            appear in your results, and yours never appear in theirs.
          </p>
        </div>

        <div class="mt-6 border-[3px] p-5" style="border-color: {brand.primaryColor}">
          <h3 class="text-[11px] uppercase tracking-[0.2em]">Connection</h3>
          <button
            type="button"
            onclick={loadNotes}
            disabled={loading}
            class="mt-4 inline-flex min-h-[44px] w-full items-center justify-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-60 motion-reduce:transition-none"
            style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
          >
            <Icon name="Upload" class="h-4 w-4" aria-hidden="true" />
            {loading ? "Checking…" : "Check for updates"}
          </button>
        </div>

        <p
          class="mt-6 border-t-[3px] pt-4 text-[11px] uppercase leading-5 tracking-[0.18em]"
          style="border-color: {brand.primaryColor}; color: {brand.neutralColor}"
        >
          Esc clears the search and closes the editor.
        </p>
      </aside>
    </div>
  </div>
</div>
