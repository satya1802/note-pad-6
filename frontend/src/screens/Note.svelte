<script>
  import { Icon, Input, Label, Textarea } from "@/lib/ui";
  import { brand } from "@/lib/brand";
  import { useNavigate } from "@/lib/navigate";
  import { apiFetch, ApiError } from "@/lib/api";
  import { session, clearSession } from "@/lib/session.svelte";
  import { location, param, go } from "@/lib/router.svelte";

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

  const noteId = $derived(param("/note/:id", location.path, "id"));

  let note = $state(null);
  let status = $state("loading"); // loading | ready | denied | error
  let mode = $state("read"); // read | edit
  let draftTitle = $state("");
  let draftBody = $state("");
  let formError = $state("");
  let saving = $state(false);
  let flash = $state("");

  let confirmOpen = $state(false);
  let deleting = $state(false);
  let deleteError = $state("");
  let cancelEl = $state(null);

  function stamp(iso) {
    if (!iso) return "";
    const [d, t] = iso.split("T");
    const [y, m, day] = (d || "").split("-");
    if (!y || !m || !day) return iso;
    return day + " " + MONTHS[Number(m) - 1] + " " + y + " · " + (t ? t.slice(0, 5) : "");
  }

  function handleUnauthorized() {
    clearSession();
    navigate("sign-in");
  }

  async function loadNote() {
    if (!noteId) return;
    status = "loading";
    mode = "read";
    formError = "";
    flash = "";
    try {
      const data = await apiFetch(`/api/notes/${noteId}`);
      note = data.note;
      status = "ready";
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        handleUnauthorized();
        return;
      }
      if (err instanceof ApiError && (err.status === 403 || err.status === 404)) {
        note = null;
        status = "denied";
        return;
      }
      status = "error";
    }
  }

  function startEdit() {
    if (!note) return;
    draftTitle = note.title;
    draftBody = note.body;
    formError = "";
    flash = "";
    mode = "edit";
  }

  function cancelEdit() {
    formError = "";
    mode = "read";
  }

  async function save() {
    if (saving || !noteId) return;
    formError = "";
    saving = true;
    try {
      const data = await apiFetch(`/api/notes/${noteId}`, {
        method: "PUT",
        body: JSON.stringify({ title: draftTitle.trim(), body: draftBody.trim() }),
      });
      note = data.note;
      mode = "read";
      flash = `Saved. Updated ${stamp(note.updated_at)}.`;
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        handleUnauthorized();
        return;
      }
      if (err instanceof ApiError && err.status === 422) {
        formError =
          (err.body && err.body.message) || "Enter a title or some body text to save a note.";
      } else {
        formError = "Could not save the note. Try again.";
      }
    } finally {
      saving = false;
    }
  }

  function askDelete() {
    if (!note) return;
    deleteError = "";
    confirmOpen = true;
  }

  function closeDialog() {
    confirmOpen = false;
  }

  async function confirmDelete() {
    if (deleting || !noteId) return;
    deleting = true;
    deleteError = "";
    try {
      await apiFetch(`/api/notes/${noteId}`, { method: "DELETE" });
      go("/notes");
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        handleUnauthorized();
        return;
      }
      deleteError = "Could not delete the note. Try again.";
    } finally {
      deleting = false;
    }
  }

  function onKeydown(event) {
    if (event.key === "Escape" && confirmOpen) {
      event.preventDefault();
      closeDialog();
    }
  }

  $effect(() => {
    // Re-run whenever the id in the path changes (e.g. opening a different note).
    loadNote();
  });

  $effect(() => {
    if (confirmOpen && cancelEl) cancelEl.focus();
  });

  const words = $derived(
    mode === "edit"
      ? draftBody.trim()
        ? draftBody.trim().split(/\s+/).length
        : 0
      : note && note.body.trim()
        ? note.body.trim().split(/\s+/).length
        : 0,
  );

  const primaryBtn =
    "inline-flex min-h-[44px] items-center justify-center gap-2 border-[3px] px-5 py-3 text-[11px] uppercase tracking-[0.2em] transition-transform duration-150 motion-safe:hover:-translate-x-[2px] motion-safe:hover:-translate-y-[2px] focus-visible:outline-2 focus-visible:outline-offset-[3px] disabled:opacity-60 motion-reduce:transition-none";
  const ghostBtn =
    "inline-flex min-h-[44px] items-center justify-center gap-2 border-[3px] bg-transparent px-5 py-3 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-[3px]";
</script>

<svelte:window onkeydown={onKeydown} />

<div
  class="min-h-screen w-full"
  style="background-color:{brand.backgroundColor}; color:{brand.primaryColor}; font-family:{brand.fontBody};"
>
  <div class="mx-auto max-w-3xl px-5 py-8 sm:px-8 lg:px-12 lg:py-12">
    <!-- masthead -->
    <div
      class="flex flex-wrap items-end justify-between gap-x-6 gap-y-2 border-b-[3px] pb-2"
      style="border-color:{brand.primaryColor}"
    >
      <button
        type="button"
        onclick={() => navigate("notes")}
        class="inline-flex items-center gap-2 bg-transparent px-0 py-1 text-[11px] uppercase tracking-[0.22em] transition-opacity hover:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-2"
        style="color:{brand.neutralColor}; outline-color:{brand.accentColor}"
      >
        <Icon name="ArrowLeft" class="h-4 w-4" aria-hidden="true" />
        All notes
      </button>
      <p
        class="text-[11px] uppercase tracking-[0.32em] break-all"
        style="color:{brand.neutralColor}"
      >
        {session.user ? session.user.email : ""}
      </p>
    </div>

    {#if flash}
      <p
        role="status"
        class="mt-6 flex items-start gap-3 border-[3px] border-l-[10px] bg-white px-4 py-3 text-[12px] leading-relaxed"
        style="border-color:{brand.primaryColor}; border-left-color:{brand.accentColor}"
      >
        <Icon name="CheckCircle" class="mt-[2px] h-4 w-4 shrink-0" aria-hidden="true" />
        <span>{flash}</span>
      </p>
    {/if}

    <div class="mt-8">
      {#if status === "denied"}
        <div
          class="border-[3px] bg-white p-7 sm:p-10"
          style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
        >
          <p
            class="text-[11px] uppercase tracking-[0.3em]"
            style="color:{brand.neutralColor}"
          >
            Access denied
          </p>
          <h1 class="mt-5 text-3xl leading-[1.08] sm:text-4xl" style="font-family:{brand.fontHeading}">
            This note isn't on your desk
          </h1>
          <p class="mt-5 max-w-[60ch] text-[14px] leading-[1.6]">
            Notes belong to the account that wrote them. Notepad 6 checks the owner on every read, so
            nobody else can open yours either.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <button
              type="button"
              onclick={() => navigate("notes")}
              class={primaryBtn}
              style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
            >
              Open my notes list
            </button>
          </div>
        </div>
      {:else if status === "loading"}
        <div
          class="border-[3px] bg-white p-7 sm:p-10"
          style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
          aria-busy="true"
          aria-live="polite"
        >
          <p class="text-[11px] uppercase tracking-[0.3em]" style="color:{brand.neutralColor}">
            Fetching your note…
          </p>
          <div class="mt-6 animate-pulse space-y-4 motion-reduce:animate-none">
            <div class="h-10 w-4/5" style="background-color:{brand.neutralColor}22"></div>
            <div class="h-3 w-full" style="background-color:{brand.neutralColor}22"></div>
            <div class="h-3 w-11/12" style="background-color:{brand.neutralColor}22"></div>
            <div class="h-3 w-3/5" style="background-color:{brand.neutralColor}22"></div>
          </div>
        </div>
      {:else if status === "error"}
        <div
          class="border-[3px] bg-white p-7 sm:p-10"
          style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
        >
          <h1 class="flex items-center gap-3 text-[11px] uppercase tracking-[0.2em]">
            <Icon name="AlertCircle" class="h-4 w-4" aria-hidden="true" />
            Could not load this note
          </h1>
          <p class="mt-4 max-w-[60ch] text-sm leading-relaxed" style="color:{brand.neutralColor}">
            Something went wrong reaching the notes server. Try again.
          </p>
          <button
            type="button"
            onclick={loadNote}
            class="mt-6 {ghostBtn}"
            style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
          >
            <Icon name="Upload" class="h-4 w-4" aria-hidden="true" />
            Try again
          </button>
        </div>
      {:else if mode === "read" && note}
        <h1
          class="text-[30px] leading-[1.08] sm:text-[42px] lg:text-[48px]"
          style="font-family:{brand.fontHeading}"
        >
          {note.title}
        </h1>

        <div
          class="mt-5 flex flex-wrap items-center gap-x-6 gap-y-2 border-t-[3px] pt-3 text-[11px] uppercase tracking-[0.2em]"
          style="border-color:{brand.primaryColor}; color:{brand.neutralColor}"
        >
          <span>Created {stamp(note.created_at)}</span>
          <span>Updated {stamp(note.updated_at)}</span>
        </div>

        <article
          class="mt-7 border-[3px] bg-white p-6 sm:p-9"
          style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
        >
          <p class="whitespace-pre-wrap text-[15px] leading-[1.75]">{note.body}</p>
        </article>

        <div class="mt-7 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onclick={startEdit}
            class={primaryBtn}
            style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
          >
            <Icon name="Edit" class="h-4 w-4" aria-hidden="true" />
            Edit note
          </button>
          <button
            type="button"
            onclick={askDelete}
            class={ghostBtn}
            style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
          >
            <Icon name="Trash" class="h-4 w-4" aria-hidden="true" />
            Delete
          </button>
        </div>
      {:else if mode === "edit" && note}
        <h1 class="text-[11px] uppercase tracking-[0.3em]" style="color:{brand.neutralColor}">
          Editing note
        </h1>

        <form
          onsubmit={(e) => {
            e.preventDefault();
            save();
          }}
          class="mt-4"
        >
          <div
            class="border-[3px] bg-white p-6 sm:p-9"
            style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
          >
            <Label
              for="note-title"
              class="block text-[11px] uppercase tracking-[0.3em]"
              style="color:{brand.neutralColor}"
            >
              Title
            </Label>
            <Input
              id="note-title"
              bind:value={draftTitle}
              placeholder="Untitled note"
              class="mt-3 w-full rounded-none border-0 border-b-[3px] bg-transparent px-0 pb-3 text-[24px] leading-tight sm:text-[30px] focus-visible:outline-2 focus-visible:outline-offset-4"
              style="font-family:{brand.fontHeading}; border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
            />

            <Label
              for="note-body"
              class="mt-8 block text-[11px] uppercase tracking-[0.3em]"
              style="color:{brand.neutralColor}"
            >
              Body
            </Label>
            <Textarea
              id="note-body"
              rows="12"
              bind:value={draftBody}
              placeholder="Plain text — no formatting, no attachments."
              class="mt-3 w-full rounded-none border-[3px] bg-transparent p-4 text-[15px] leading-[1.75] focus-visible:outline-2 focus-visible:outline-offset-[3px]"
              style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}; font-family:{brand.fontBody}"
            ></Textarea>

            <p
              class="mt-4 text-[11px] uppercase tracking-[0.2em]"
              style="color:{brand.neutralColor}"
            >
              {words} words
            </p>
          </div>

          {#if formError}
            <p
              role="alert"
              class="mt-5 flex items-start gap-3 border-[3px] border-l-[10px] bg-white px-4 py-3 text-[13px] leading-relaxed"
              style="border-color:{brand.primaryColor}; border-left-color:{brand.primaryColor}"
            >
              <Icon name="AlertCircle" class="mt-[2px] h-4 w-4 shrink-0" aria-hidden="true" />
              <span>{formError}</span>
            </p>
          {/if}

          <div class="mt-7 flex flex-wrap items-center gap-3">
            <button
              type="submit"
              disabled={saving}
              class={primaryBtn}
              style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
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
                Save changes
              {/if}
            </button>
            <button
              type="button"
              onclick={cancelEdit}
              class={ghostBtn}
              style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
            >
              <Icon name="X" class="h-4 w-4" aria-hidden="true" />
              Cancel
            </button>
          </div>
        </form>
      {/if}
    </div>
  </div>
</div>

{#if confirmOpen && note}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-5"
    style="background-color:#0a0a0a99"
  >
    <button
      type="button"
      aria-label="Close without deleting"
      onclick={closeDialog}
      class="absolute inset-0 h-full w-full cursor-default focus-visible:outline-2 focus-visible:outline-offset-[-4px]"
      style="outline-color:{brand.accentColor}"
    ></button>

    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="delete-heading"
      aria-describedby="delete-copy"
      class="relative w-full max-w-md border-[3px] bg-white p-7"
      style="border-color:{brand.primaryColor}; box-shadow:8px 8px 0 {brand.primaryColor}"
    >
      <h2 id="delete-heading" class="text-[28px] leading-[1.1]" style="font-family:{brand.fontHeading}">
        Delete this note?
      </h2>
      <p id="delete-copy" class="mt-4 text-[13px] leading-[1.65]">
        “{note.title}” leaves your account for good. There is no bin to pull it back from.
      </p>

      {#if deleteError}
        <p role="alert" class="mt-4 text-[13px]" style="color:{brand.primaryColor}">
          {deleteError}
        </p>
      {/if}

      <div class="mt-7 flex flex-wrap justify-end gap-3">
        <button
          bind:this={cancelEl}
          type="button"
          onclick={closeDialog}
          class={ghostBtn}
          style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
        >
          Keep the note
        </button>
        <button
          type="button"
          onclick={confirmDelete}
          disabled={deleting}
          class={primaryBtn}
          style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
        >
          <Icon name="Trash" class="h-4 w-4" aria-hidden="true" />
          {deleting ? "Deleting…" : "Delete permanently"}
        </button>
      </div>
    </div>
  </div>
{/if}
