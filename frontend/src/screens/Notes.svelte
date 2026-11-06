<script>
  /* eslint-disable @typescript-eslint/no-unused-vars -- generated imports, matched generously */
  import { Icon, Input, Label, Stat, Textarea } from "@/lib/ui";
  import { brand } from "@/lib/brand";
  import { useNavigate } from "@/lib/navigate";

  const navigate = useNavigate();

  const MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

  const user = {
    id: 'u_8821',
    email: 'satya.ganaraju@quorq.ai',
    created_at: '2026-04-18T10:02:00'
  };

  let notes = $state([
    {
      id: 'nt_1041',
      user_id: 'u_8821',
      title: 'Q4 board pack — pricing walkthrough',
      body: 'Three slides maximum on the price change. Open with churn at 2.1%, not the ARR number — Priya will ask for the cohort split either way. Marcus wants the migration plan for the 14 legacy accounts before anything is published.\n\nDeck to Priya by Friday 13 Nov.',
      created_at: '2026-10-29T08:14:00',
      updated_at: '2026-11-06T09:12:00',
      sync: 'synced'
    },
    {
      id: 'nt_1039',
      user_id: 'u_8821',
      title: 'Dentist — Dr Okafor, 18 Nov 14:30',
      body: 'Marchmont Dental, 42 Warrender Park Road. Ask about the night guard quote (£180?) and whether the hygienist visit is covered this year. Bring the referral letter from Dr Iyer.',
      created_at: '2026-11-05T19:40:00',
      updated_at: '2026-11-05T19:48:00',
      sync: 'synced'
    },
    {
      id: 'nt_1012',
      user_id: 'u_8821',
      title: 'Sourdough — 70% hydration timings',
      body: 'Levain 09:00, 1:4:4. Autolyse 11:30 for 45 minutes. Four sets of coil folds, 30 minutes apart. Bulk until 50% rise, about 5 hours at 23°C. Shape 17:00, cold retard overnight. Bake 250°C lid on for 20 min, 230°C lid off for 22.',
      created_at: '2026-09-02T18:20:00',
      updated_at: '2026-11-05T07:55:00',
      sync: 'synced'
    },
    {
      id: 'nt_1036',
      user_id: 'u_8821',
      title: 'Standup blockers — week of 2 Nov',
      body: 'Mon: staging migration stuck behind the pg_dump restore. Tue: cleared. Wed: waiting on Hana for the search index rebuild — the tsvector column is still null on 312 rows. Thu: nothing blocking, shipped the export fix.',
      created_at: '2026-11-02T09:05:00',
      updated_at: '2026-11-04T16:21:00',
      sync: 'queued'
    },
    {
      id: 'nt_1034',
      user_id: 'u_8821',
      title: 'Reply to Marguerite about the lease',
      body: 'Draft — do not send yet.\n\nMarguerite, thank you for the revised terms. I can agree to the three-year break clause, but not the service charge uplift at 6%. RPI-linked is the most I can sign off. Could we talk Thursday morning?',
      created_at: '2026-11-03T21:12:00',
      updated_at: '2026-11-04T11:03:00',
      sync: 'synced'
    },
    {
      id: 'nt_1030',
      user_id: 'u_8821',
      title: 'Packing — Reykjavík, 21–26 Nov',
      body: 'Thermals x3, waterproof shell, swim shorts for the Sky Lagoon, type F adaptor, crampons from Dad. Passport runs to 2029 so that is fine. Book the airport transfer before the 14th — the price doubles after that.',
      created_at: '2026-10-30T22:10:00',
      updated_at: '2026-11-03T20:39:00',
      sync: 'synced'
    },
    {
      id: 'nt_1028',
      user_id: 'u_8821',
      title: 'Car service quotes — comparison',
      body: 'Kwik Fit Gorgie: £264 full service plus MOT, 18 Nov. Halfords Newhaven Road: £229 but no courtesy car. The independent on Jane Street quoted £198 with a two-week wait. Cambelt due at 80k, currently on 71,340.',
      created_at: '2026-11-02T13:10:00',
      updated_at: '2026-11-02T13:27:00',
      sync: 'synced'
    },
    {
      id: 'nt_1021',
      user_id: 'u_8821',
      title: 'Reading list after Lisbon',
      body: 'The Book of Disquiet — Pessoa, finish part two. Lisbon: War in the Shadows — Lochery. Night Train to Lisbon — Mercier, borrowed from Tomás, give it back. Also the Saramago one with the elephant.',
      created_at: '2026-10-28T09:44:00',
      updated_at: '2026-10-31T18:02:00',
      sync: 'synced'
    },
    {
      id: 'nt_1018',
      user_id: 'u_8821',
      title: "Mum's 60th — gift ideas",
      body: 'Shortlist: the Orkney wool blanket (£140), a year of the Hidcote seed club, or National Trust life membership. Dad says no more picture frames. Decide by 12 Dec, the party is on the 20th.',
      created_at: '2026-10-26T20:30:00',
      updated_at: '2026-10-30T12:15:00',
      sync: 'synced'
    }
  ]);

  let query = $state('');
  let composerOpen = $state(false);
  let composerIn = $state(false);
  let composerEl = $state(null);
  let draftTitle = $state('');
  let draftBody = $state('');
  let formError = $state('');
  let saving = $state(false);
  let confirmId = $state(null);
  let flash = $state(null);
  let offline = $state(false);
  let loading = $state(false);
  let listError = $state('');
  let deniedNotice = $state(true);
  let signingOut = $state(false);
  let newId = $state(null);
  let lastSynced = $state('06 NOV 2026 · 09:41');
  let nextId = $state(1042);

  const q = $derived(query.trim().toLowerCase());
  const sorted = $derived([...notes].sort((a, b) => b.updated_at.localeCompare(a.updated_at)));
  const results = $derived(
    q ? sorted.filter((n) => (n.title + ' ' + n.body).toLowerCase().includes(q)) : sorted
  );
  const totalWords = $derived(
    notes.reduce((sum, n) => sum + n.body.trim().split(/\s+/).filter(Boolean).length, 0)
  );
  const queuedCount = $derived(notes.filter((n) => n.sync === 'queued').length);
  const draftWords = $derived(draftBody.trim().split(/\s+/).filter(Boolean).length);

  function pad(n) {
    return String(n).padStart(2, '0');
  }

  function stamp(iso) {
    const [d, t] = iso.split('T');
    const [y, m, day] = d.split('-');
    return day + ' ' + MONTHS[Number(m) - 1] + ' ' + y + ' · ' + t.slice(0, 5);
  }

  function localIso(d) {
    return (
      d.getFullYear() +
      '-' + pad(d.getMonth() + 1) +
      '-' + pad(d.getDate()) +
      'T' + pad(d.getHours()) +
      ':' + pad(d.getMinutes()) +
      ':' + pad(d.getSeconds())
    );
  }

  function snippet(note, needle) {
    const body = note.body.replace(/\s+/g, ' ').trim();
    if (!body) return 'No body text.';
    if (!needle) return body.length > 165 ? body.slice(0, 165) + '…' : body;
    const idx = body.toLowerCase().indexOf(needle);
    if (idx === -1) return body.length > 165 ? body.slice(0, 165) + '…' : body;
    const start = Math.max(0, idx - 55);
    const end = Math.min(body.length, start + 175);
    return (start > 0 ? '…' : '') + body.slice(start, end) + (end < body.length ? '…' : '');
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
    formError = '';
  }

  function closeComposer() {
    composerOpen = false;
    formError = '';
  }

  function saveNote(event) {
    event.preventDefault();
    const title = draftTitle.trim();
    const body = draftBody.trim();
    if (!title && !body) {
      formError = 'A note needs something in it. Type a title, or a first line of body text.';
      return;
    }
    saving = true;
    formError = '';
    setTimeout(() => {
      const now = new Date();
      const iso = localIso(now);
      const firstLine = body.split('\n')[0].trim();
      const finalTitle = title || (firstLine.length > 62 ? firstLine.slice(0, 62) + '…' : firstLine);
      const note = {
        id: 'nt_' + nextId,
        user_id: user.id,
        title: finalTitle,
        body: body,
        created_at: iso,
        updated_at: iso,
        sync: offline ? 'queued' : 'synced'
      };
      nextId = nextId + 1;
      notes = [note, ...notes];
      newId = note.id;
      saving = false;
      composerOpen = false;
      draftTitle = '';
      draftBody = '';
      query = '';
      flash = {
        kind: 'success',
        text: offline
          ? 'Saved on this device. “' + finalTitle + '” uploads as soon as you reconnect.'
          : 'Saved. “' + finalTitle + '” is at the top of your list.'
      };
      setTimeout(() => {
        if (newId === note.id) newId = null;
      }, 2400);
    }, 520);
  }

  function askDelete(id) {
    confirmId = id;
    flash = null;
  }

  function cancelDelete() {
    const kept = notes.find((n) => n.id === confirmId);
    confirmId = null;
    if (kept) flash = { kind: 'info', text: 'Kept “' + kept.title + '”. Nothing was changed.' };
  }

  function confirmDelete(id) {
    const gone = notes.find((n) => n.id === id);
    notes = notes.filter((n) => n.id !== id);
    confirmId = null;
    flash = { kind: 'success', text: 'Deleted “' + gone.title + '”. It is gone from your account for good.' };
  }

  function reload() {
    if (loading) return;
    loading = true;
    listError = '';
    flash = null;
    setTimeout(() => {
      loading = false;
      if (offline) {
        listError =
          'Could not reach the notes server — you have offline mode switched on. Everything below is the copy saved on this device.';
      } else {
        lastSynced = stamp(localIso(new Date()));
        notes = notes.map((n) => ({ ...n, sync: 'synced' }));
        flash = { kind: 'success', text: 'List refreshed. This device matches the server.' };
      }
    }, 750);
  }

  function toggleOffline() {
    offline = !offline;
    listError = '';
    flash = {
      kind: 'info',
      text: offline
        ? 'Offline mode on. New notes queue on this device until you switch it back.'
        : 'Back online. Queued notes upload on the next refresh.'
    };
  }

  function signOut() {
    if (signingOut) return;
    signingOut = true;
    setTimeout(() => navigate('sign-in'), 480);
  }

  function openNote(id) {
    navigate('note');
  }

  function onKey(event) {
    if (event.key !== 'Escape') return;
    if (confirmId) {
      cancelDelete();
    } else if (composerOpen && !saving) {
      closeComposer();
    } else if (query) {
      query = '';
    }
  }

  $effect(() => {
    if (composerOpen) {
      composerIn = false;
      requestAnimationFrame(() => {
        composerIn = true;
      });
      if (composerEl) {
        const field = composerEl.querySelector('#note-title');
        if (field) field.focus();
      }
    } else {
      composerIn = false;
    }
  });

  $effect(() => {
    if (confirmId) {
      const target = document.querySelector('[data-confirm-delete="' + confirmId + '"]');
      if (target) target.focus();
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
            <p class="break-all">{user.email}</p>
          </div>
          <button
            type="button"
            onclick={signOut}
            disabled={signingOut}
            class="inline-flex min-h-[44px] items-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] transition-all duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-60 motion-reduce:transition-none"
            style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
          >
            <Icon name="ArrowLeft" class="h-4 w-4" aria-hidden="true" />
            {signingOut ? 'Signing out…' : 'Sign out'}
          </button>
        </div>
      </div>

      <dl class="mt-6 flex flex-wrap items-baseline gap-x-8 gap-y-2 text-[11px] uppercase tracking-[0.18em]">
        <div class="flex gap-2">
          <dt style="color: {brand.neutralColor}">Today</dt>
          <dd>06 NOV 2026</dd>
        </div>
        <div class="flex gap-2">
          <dt style="color: {brand.neutralColor}">Notes</dt>
          <dd>{pad(notes.length)}</dd>
        </div>
        <div class="flex gap-2">
          <dt style="color: {brand.neutralColor}">Words</dt>
          <dd>{totalWords.toLocaleString('en-GB')}</dd>
        </div>
        <div class="flex gap-2">
          <dt style="color: {brand.neutralColor}">Account</dt>
          <dd>Free — no billing, ever</dd>
        </div>
      </dl>
    </header>

    <!-- Permission denied notice -->
    {#if deniedNotice}
      <div
        role="status"
        class="mt-8 flex items-start gap-4 border-[3px] bg-white p-5"
        style="border-color: {brand.primaryColor}; box-shadow: 6px 6px 0 {brand.primaryColor};"
      >
        <Icon name="AlertCircle" class="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true" />
        <div class="min-w-0 flex-1">
          <h2 class="text-[11px] uppercase tracking-[0.2em]">Note not opened — it isn’t yours</h2>
          <p class="mt-2 max-w-[66ch] text-sm leading-relaxed" style="color: {brand.neutralColor}">
            The link you followed points at note <span style="color: {brand.primaryColor}">nt_7730</span>, which is
            stored against another account. Only its owner can open, edit or delete it. Ask them to paste the text to
            you if you need it.
          </p>
        </div>
        <button
          type="button"
          aria-label="Dismiss the note access notice"
          onclick={() => (deniedNotice = false)}
          class="inline-flex h-11 w-11 shrink-0 items-center justify-center border-[3px] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
          style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
        >
          <Icon name="X" class="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    {/if}

    <!-- Stale / offline bar -->
    {#if offline}
      <p
        class="mt-8 flex flex-wrap items-center gap-x-3 gap-y-1 border-y-[3px] px-1 py-3 text-[11px] uppercase tracking-[0.18em]"
        style="border-color: {brand.primaryColor}"
      >
        <Icon name="Clock" class="h-4 w-4" aria-hidden="true" />
        <span>Offline copy</span>
        <span aria-hidden="true" style="color: {brand.neutralColor}">/</span>
        <span style="color: {brand.neutralColor}">Last synced {lastSynced}</span>
        <span aria-hidden="true" style="color: {brand.neutralColor}">/</span>
        <span style="color: {brand.neutralColor}">{queuedCount} waiting to upload</span>
      </p>
    {/if}

    <div class="mt-10 grid gap-10 lg:grid-cols-3 lg:gap-12">

      <!-- Main column -->
      <div class="lg:col-span-2">

        <!-- Section 01: search + new note -->
        <section aria-labelledby="sec-search">
          <h2 id="sec-search" class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">
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
              <div class="mt-2 flex items-center gap-3 border-[3px] bg-white px-4" style="border-color: {brand.primaryColor}">
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
                    onclick={() => (query = '')}
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

          <p aria-live="polite" class="mt-3 text-[11px] uppercase tracking-[0.18em]" style="color: {brand.neutralColor}">
            {#if q}
              Showing {pad(results.length)} of {pad(notes.length)} — matching “{query.trim()}”
            {:else}
              Showing all {pad(notes.length)} of your notes, newest edit first
            {/if}
          </p>
        </section>

        <!-- Composer -->
        {#if composerOpen}
          <section
            id="composer"
            aria-labelledby="composer-heading"
            bind:this={composerEl}
            class="mt-6 border-[3px] bg-white transition-all duration-300 ease-out motion-reduce:transition-none {composerIn ? 'translate-y-0 opacity-100' : '-translate-y-2 opacity-0'}"
            style="border-color: {brand.primaryColor}; box-shadow: 8px 8px 0 {brand.primaryColor};"
          >
            <div class="flex items-center justify-between border-b-[3px] px-6 py-4" style="border-color: {brand.primaryColor}">
              <h3 id="composer-heading" class="text-2xl" style="font-family: {brand.fontHeading}">New note</h3>
              <span class="text-[11px] uppercase tracking-[0.2em]" style="color: {brand.neutralColor}">
                {draftWords} words · {draftBody.length} chars
              </span>
            </div>

            <form class="px-6 py-6" onsubmit={saveNote} novalidate>
              <div>
                <Label for="note-title" class="block text-[11px] uppercase tracking-[0.2em]">Title — optional</Label>
                <Input
                  id="note-title"
                  bind:value={draftTitle}
                  placeholder="Leave blank to use the first line"
                  class="mt-2 h-12 w-full border-[3px] px-4 text-base focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                  style="border-color: {brand.primaryColor}; border-radius: 0; font-family: {brand.fontBody}; outline-color: {brand.accentColor};"
                />
              </div>

              <div class="mt-6">
                <Label for="note-body" class="block text-[11px] uppercase tracking-[0.2em]">Note</Label>
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

              <div class="mt-6 flex flex-wrap items-center gap-4 border-t-[3px] pt-5" style="border-color: {brand.primaryColor}">
                <button
                  type="submit"
                  disabled={saving}
                  class="inline-flex min-h-[48px] items-center gap-3 border-[3px] px-6 py-3 text-xs uppercase tracking-[0.22em] text-white transition-transform duration-150 motion-safe:hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-70 motion-reduce:transition-none"
                  style="background-color: {brand.accentColor}; border-color: {brand.primaryColor}; box-shadow: 5px 5px 0 {brand.primaryColor}; outline-color: {brand.primaryColor};"
                >
                  {#if saving}
                    <Icon name="Clock" class="h-4 w-4 motion-safe:animate-spin" aria-hidden="true" />
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

                <span class="ml-auto text-[11px] uppercase tracking-[0.18em]" style="color: {brand.neutralColor}">
                  {offline ? 'Will queue on this device' : 'Saves to your account only'}
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
            style="border-color: {brand.primaryColor}; background-color: {flash.kind === 'success' ? '#ffffff' : brand.backgroundColor};"
          >
            <Icon
              name={flash.kind === 'success' ? 'CheckCircle' : 'AlertCircle'}
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
            <h2 id="sec-notes" class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">
              § 02 — Your notes
            </h2>
            <p class="text-[11px] uppercase tracking-[0.18em]" style="color: {brand.neutralColor}">
              Ordered by last edit
            </p>
          </div>

          {#if listError}
            <div
              class="mt-4 border-[3px] bg-white p-6"
              style="border-color: {brand.primaryColor}; box-shadow: 6px 6px 0 {brand.primaryColor};"
            >
              <h3 class="flex items-center gap-3 text-[11px] uppercase tracking-[0.2em]">
                <Icon name="AlertCircle" class="h-4 w-4" aria-hidden="true" />
                Refresh failed
              </h3>
              <p class="mt-3 max-w-[66ch] text-sm leading-relaxed" style="color: {brand.neutralColor}">{listError}</p>
              <button
                type="button"
                onclick={reload}
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
              <p class="border-b-[3px] px-6 py-3 text-[11px] uppercase tracking-[0.2em]" style="border-color: {brand.primaryColor}">
                Fetching your notes…
              </p>
              {#each [0, 1, 2] as row (row)}
                <div class="flex gap-6 border-b-[3px] p-6 last:border-b-0" style="border-color: {brand.primaryColor}">
                  <div class="h-3 w-8 motion-safe:animate-pulse" style="background-color: {brand.neutralColor}; opacity: 0.25;"></div>
                  <div class="flex-1 space-y-3">
                    <div class="h-5 w-2/3 motion-safe:animate-pulse" style="background-color: {brand.neutralColor}; opacity: 0.25;"></div>
                    <div class="h-3 w-full motion-safe:animate-pulse" style="background-color: {brand.neutralColor}; opacity: 0.18;"></div>
                    <div class="h-3 w-5/6 motion-safe:animate-pulse" style="background-color: {brand.neutralColor}; opacity: 0.18;"></div>
                  </div>
                </div>
              {/each}
            </div>

          {:else if notes.length === 0}
            <div
              class="mt-4 border-[3px] bg-white px-8 py-14 text-center"
              style="border-color: {brand.primaryColor}; box-shadow: 8px 8px 0 {brand.primaryColor};"
            >
              <p class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">Blank page</p>
              <h3 class="mt-4 text-4xl" style="font-family: {brand.fontHeading}">Nothing filed yet</h3>
              <p class="mx-auto mt-4 max-w-[52ch] text-sm leading-relaxed" style="color: {brand.neutralColor}">
                This is your own notepad — a shopping list, a half-written reply, the thing you will forget by Thursday.
                Only you can read what you put here.
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
              <p class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">No match</p>
              <h3 class="mt-4 text-3xl" style="font-family: {brand.fontHeading}">
                Nothing of yours says “{query.trim()}”
              </h3>
              <p class="mt-4 max-w-[60ch] text-sm leading-relaxed" style="color: {brand.neutralColor}">
                Search reads the title and body of all {notes.length} of your notes, and nothing outside your account.
                Try a shorter word, or clear the box to see the whole list again.
              </p>
              <div class="mt-7 flex flex-wrap gap-4">
                <button
                  type="button"
                  onclick={() => (query = '')}
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
                  style="border-color: {brand.primaryColor}; border-left: {note.id === newId ? '8px solid ' + brand.accentColor : '0'};"
                >
                  <div class="flex flex-col gap-4 p-6 sm:flex-row sm:items-start sm:gap-6">
                    <span class="pt-1 text-[11px] uppercase tracking-[0.2em]" style="color: {brand.neutralColor}">
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
                          {#each parts(note.title, q) as piece}
                            {#if piece.hit}
                              <mark style="background-color: {brand.accentColor}; color: #ffffff; padding: 0 2px;">{piece.t}</mark>
                            {:else}{piece.t}{/if}
                          {/each}
                        </button>
                      </h3>

                      <p class="mt-2 max-w-[72ch] text-sm leading-relaxed" style="color: {brand.neutralColor}">
                        {#each parts(snippet(note, q), q) as piece}
                          {#if piece.hit}
                            <mark style="background-color: {brand.accentColor}; color: #ffffff; padding: 0 2px;">{piece.t}</mark>
                          {:else}{piece.t}{/if}
                        {/each}
                      </p>

                      <p class="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-[11px] uppercase tracking-[0.18em]">
                        <span style="color: {brand.neutralColor}">Updated</span>
                        <span>{stamp(note.updated_at)}</span>
                        <span aria-hidden="true" style="color: {brand.neutralColor}">/</span>
                        <span style="color: {brand.neutralColor}">Created {stamp(note.created_at)}</span>
                        <span
                          class="inline-flex items-center gap-1.5 border-[3px] px-2 py-1"
                          style="border-color: {brand.primaryColor}"
                        >
                          <Icon name={note.sync === 'queued' ? 'Clock' : 'Check'} class="h-3 w-3" aria-hidden="true" />
                          {note.sync === 'queued' ? 'Queued' : 'Synced'}
                        </span>
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
                      <button
                        type="button"
                        aria-label={'Delete note: ' + note.title}
                        title={'Delete note: ' + note.title}
                        onclick={() => askDelete(note.id)}
                        class="inline-flex h-11 w-11 items-center justify-center border-[3px] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                        style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
                      >
                        <Icon name="Trash" class="h-4 w-4" aria-hidden="true" />
                      </button>
                    </div>
                  </div>

                  {#if confirmId === note.id}
                    <div
                      role="alertdialog"
                      aria-label={'Confirm deleting ' + note.title}
                      class="flex flex-col gap-4 px-6 py-5 sm:flex-row sm:items-center sm:justify-between"
                      style="background-color: {brand.primaryColor}; color: {brand.backgroundColor};"
                    >
                      <p class="max-w-[60ch] text-sm leading-relaxed">
                        Delete “{note.title}” for good? The text and both timestamps go with it, and there is no undo.
                      </p>
                      <div class="flex shrink-0 flex-wrap gap-3">
                        <button
                          type="button"
                          data-confirm-delete={note.id}
                          onclick={() => confirmDelete(note.id)}
                          class="inline-flex min-h-[44px] items-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                          style="border-color: {brand.backgroundColor}; background-color: {brand.backgroundColor}; color: {brand.primaryColor}; outline-color: {brand.backgroundColor};"
                        >
                          <Icon name="Trash" class="h-4 w-4" aria-hidden="true" />
                          Delete permanently
                        </button>
                        <button
                          type="button"
                          onclick={cancelDelete}
                          class="inline-flex min-h-[44px] items-center px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] underline underline-offset-4 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                          style="color: {brand.backgroundColor}; outline-color: {brand.backgroundColor};"
                        >
                          Keep it
                        </button>
                      </div>
                    </div>
                  {/if}
                </li>
              {/each}
            </ol>
          {/if}
        </section>
      </div>

      <!-- Aside -->
      <aside class="lg:col-span-1">
        <h2 class="text-[11px] uppercase tracking-[0.3em]" style="color: {brand.neutralColor}">§ 03 — This account</h2>

        <div class="mt-4 border-[3px] bg-white" style="border-color: {brand.primaryColor}">
          <div class="border-b-[3px] p-5" style="border-color: {brand.primaryColor}">
            <Stat
              label="Notes kept"
              value={pad(notes.length)}
              hint={queuedCount > 0 ? queuedCount + ' waiting to upload' : 'All uploaded'}
              class="[&_*]:tracking-normal"
            />
          </div>
          <div class="border-b-[3px] p-5" style="border-color: {brand.primaryColor}">
            <Stat label="Words written" value={totalWords.toLocaleString('en-GB')} hint="Across every note" />
          </div>
          <div class="p-5">
            <Stat label="Last synced" value={lastSynced} hint={offline ? 'Offline mode is on' : 'Up to date'} />
          </div>
        </div>

        <div class="mt-6 border-[3px] p-5" style="border-color: {brand.primaryColor}">
          <h3 class="flex items-center gap-2 text-[11px] uppercase tracking-[0.2em]">
            <Icon name="User" class="h-4 w-4" aria-hidden="true" />
            Private to you
          </h3>
          <p class="mt-3 text-sm leading-relaxed" style="color: {brand.neutralColor}">
            Every note here is stored against <span style="color: {brand.primaryColor}">{user.email}</span>. Listing,
            searching and opening all run inside your account — nobody else’s notes can appear in your results, and
            yours never appear in theirs.
          </p>
          <p class="mt-4 text-[11px] uppercase tracking-[0.18em]" style="color: {brand.neutralColor}">
            Member since {stamp(user.created_at).slice(0, 11)}
          </p>
        </div>

        <div class="mt-6 border-[3px] p-5" style="border-color: {brand.primaryColor}">
          <h3 class="text-[11px] uppercase tracking-[0.2em]">Connection</h3>
          <div class="mt-4 flex items-center justify-between gap-4">
            <span class="text-sm" style="color: {brand.neutralColor}">Work offline</span>
            <button
              type="button"
              role="switch"
              aria-checked={offline}
              onclick={toggleOffline}
              class="inline-flex min-h-[44px] items-center gap-2 border-[3px] px-3 py-2 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
              style="border-color: {brand.primaryColor}; background-color: {offline ? brand.primaryColor : 'transparent'}; color: {offline ? brand.backgroundColor : brand.primaryColor}; outline-color: {brand.accentColor};"
            >
              <Icon name={offline ? 'Check' : 'X'} class="h-3.5 w-3.5" aria-hidden="true" />
              {offline ? 'On' : 'Off'}
            </button>
          </div>
          <button
            type="button"
            onclick={reload}
            disabled={loading}
            class="mt-5 inline-flex min-h-[44px] w-full items-center justify-center gap-2 border-[3px] px-4 py-2.5 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 hover:bg-[var(--ink)] hover:text-[var(--paper)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-60 motion-reduce:transition-none"
            style="border-color: {brand.primaryColor}; outline-color: {brand.accentColor};"
          >
            <Icon name="Upload" class="h-4 w-4" aria-hidden="true" />
            {loading ? 'Checking…' : 'Check for updates'}
          </button>
        </div>

        <p class="mt-6 border-t-[3px] pt-4 text-[11px] uppercase leading-5 tracking-[0.18em]" style="border-color: {brand.primaryColor}; color: {brand.neutralColor}">
          Esc clears the search, closes the editor and cancels a delete.
        </p>
      </aside>
    </div>
  </div>
</div>
