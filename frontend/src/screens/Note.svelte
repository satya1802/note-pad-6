<script>
  /* eslint-disable @typescript-eslint/no-unused-vars -- generated imports, matched generously */
  import { Button, Empty, Icon, Input, Label, Textarea } from "@/lib/ui";
  import { brand } from "@/lib/brand";
  import { useNavigate } from "@/lib/navigate";

  const navigate = useNavigate();

  const owner = { id: 'u_9f21', email: 'satya.ganaraju@quorq.ai' };

  let notes = $state([
    {
      id: 'N-0137',
      user_id: 'u_9f21',
      title: 'Rent increase — reply to Marwood & Co',
      body: `Letter arrived Tuesday. They want £1,480 from 1 Feb, up from £1,315.

Points for the reply:
— The boiler was out for nine days in March (emails 12–21 Mar).
— Two flats on the same stair went to £1,390 in September.
— Offer £1,380 on a 24-month term so neither of us does this again next year.

Call Dana first, she handled the Thistle Street one.`,
      created_at: '2026-11-04 18:07',
      updated_at: '2026-11-06 08:42',
      sync: 'pending'
    },
    {
      id: 'N-0136',
      user_id: 'u_9f21',
      title: 'Standup — Tue 3 Nov',
      body: `Aurora migration: read replicas cut over at 04:10, no errors in the hour after.
Priya is blocked on the staging secrets — ask Ops for a rotation window.
Customer ticket #55120 still open, waiting on the insurer.
Next: dry run of the failover Thursday 06:00.`,
      created_at: '2026-11-03 09:12',
      updated_at: '2026-11-03 09:48',
      sync: 'synced'
    },
    {
      id: 'N-0134',
      user_id: 'u_9f21',
      title: 'Sourdough — 68% hydration log',
      body: `Flour 400g Shipton Mill white, 100g wholemeal.
Water 340g (68%). Salt 10g. Levain 100g, fed 06:00.

Bulk 4h 20m at 23°C, four coil folds on the half hour.
Shaped 11:50, fridge overnight.
Baked 07:05 — 20 min lid on at 250°C, 22 min off at 220°C.

Verdict: better ear than last week. Next time hold the final proof to 14 hours.`,
      created_at: '2026-11-02 07:30',
      updated_at: '2026-11-02 19:05',
      sync: 'synced'
    },
    {
      id: 'N-0131',
      user_id: 'u_9f21',
      title: 'Books to find at Daunt',
      body: `— Jan Morris, Trieste and the Meaning of Nowhere
— Rebecca Solnit, A Field Guide to Getting Lost
— Something by Natalia Ginzburg, ask at the desk
— Paperback of The Peregrine for Tom's birthday (22 Nov)`,
      created_at: '2026-10-31 12:40',
      updated_at: '2026-10-31 12:40',
      sync: 'synced'
    },
    {
      id: 'N-0128',
      user_id: 'u_9f21',
      title: 'Insurance claim AX-55120 — what they asked for',
      body: `Claim AX-55120, Hartfield Mutual, opened 28 Oct.

They want, by 14 Nov:
1. Photographs of the hallway and the airing cupboard
2. The plumber's invoice (Keane & Sons, £412.90)
3. The dates the flat was unoccupied

Assessor: Robert Enright, 0131 496 0122. Call back after 10:00.`,
      created_at: '2026-10-28 15:02',
      updated_at: '2026-11-05 16:20',
      sync: 'synced'
    },
    {
      id: 'N-0122',
      user_id: 'u_9f21',
      title: 'Pitch outline — getting off the spreadsheet',
      body: `Working title: getting off the spreadsheet.

1. The 14-tab workbook that three people edit at once
2. What breaks — the September reconciliation took nine days
3. What we would replace it with, in one sentence
4. Cost, honestly, including the migration month
5. Ask: two engineers until February

Run it past Dana before it goes to the board on 19 Nov.`,
      created_at: '2026-10-27 08:25',
      updated_at: '2026-10-29 14:55',
      sync: 'synced'
    }
  ]);

  let currentId = $state('N-0137');
  let mode = $state('read'); // read | edit | new
  let status = $state('ready'); // ready | loading | denied
  let openingId = $state('');
  let deniedId = $state('');

  let draftTitle = $state('');
  let draftBody = $state('');
  let formError = $state('');
  let saving = $state(false);

  let flash = $state('');
  let flashIn = $state(false);

  let confirmOpen = $state(false);
  let dialogIn = $state(false);
  let cancelEl = $state(null);

  let lookup = $state('');
  let lookupError = $state('');

  let connection = $state('offline'); // offline | retrying | online
  let connectionError = $state('');
  let retries = $state(0);
  let lastSynced = $state('2026-11-06 08:05');

  let clock = $state(9 * 60 + 41);

  let timer = null;
  function later(fn, ms) {
    clearTimeout(timer);
    timer = setTimeout(fn, ms);
  }
  $effect(() => () => clearTimeout(timer));

  function now() {
    const hh = String(Math.floor(clock / 60)).padStart(2, '0');
    const mm = String(clock % 60).padStart(2, '0');
    return `2026-11-06 ${hh}:${mm}`;
  }

  const current = $derived(notes.find((n) => n.id === currentId) || null);
  const ordered = $derived([...notes].sort((a, b) => b.updated_at.localeCompare(a.updated_at)));
  const liveBody = $derived(mode === 'read' ? (current ? current.body : '') : draftBody);
  const words = $derived(liveBody.trim() ? liveBody.trim().split(/\s+/).length : 0);
  const chars = $derived(liveBody.length);
  const pendingCount = $derived(notes.filter((n) => n.sync === 'pending').length);

  function firstLine(text) {
    const line = text.split('\n').map((s) => s.trim()).find((s) => s.length > 0);
    return (line || 'Untitled entry').slice(0, 80);
  }

  function nextId() {
    const max = notes.reduce((acc, n) => Math.max(acc, Number(n.id.slice(2))), 0);
    return 'N-' + String(max + 1).padStart(4, '0');
  }

  function startEdit() {
    if (!current) return;
    draftTitle = current.title;
    draftBody = current.body;
    formError = '';
    flash = '';
    mode = 'edit';
  }

  function startNew() {
    draftTitle = '';
    draftBody = '';
    formError = '';
    flash = '';
    status = 'ready';
    mode = 'new';
  }

  function cancelEdit() {
    formError = '';
    saving = false;
    mode = 'read';
    if (!current && ordered.length) currentId = ordered[0].id;
  }

  function save() {
    const t = draftTitle.trim();
    const b = draftBody.trim();
    if (!t && !b) {
      formError = "There's nothing to save yet. Give the entry a title or a line of body text, then save.";
      return;
    }
    formError = '';
    saving = true;
    later(() => {
      saving = false;
      clock += 3;
      const stamp = now();
      const title = t || firstLine(draftBody);
      const sync = connection === 'online' ? 'synced' : 'pending';
      if (mode === 'new') {
        const id = nextId();
        notes = [
          { id, user_id: owner.id, title, body: draftBody, created_at: stamp, updated_at: stamp, sync },
          ...notes
        ];
        currentId = id;
        flash =
          connection === 'online'
            ? `Entry ${id} filed to your account at ${stamp.slice(11)}.`
            : `Entry ${id} saved on this device at ${stamp.slice(11)}. It syncs the moment you're back online.`;
      } else {
        notes = notes.map((n) =>
          n.id === currentId ? { ...n, title, body: draftBody, updated_at: stamp, sync } : n
        );
        flash =
          connection === 'online'
            ? `Saved. ${currentId} updated at ${stamp.slice(11)}.`
            : `Saved on this device at ${stamp.slice(11)} — queued to sync.`;
      }
      mode = 'read';
    }, 650);
  }

  function openEntry(id) {
    if (id === currentId && status === 'ready' && mode === 'read') return;
    flash = '';
    formError = '';
    mode = 'read';
    status = 'loading';
    openingId = id;
    later(() => {
      currentId = id;
      status = 'ready';
      openingId = '';
    }, 420);
  }

  function goToEntry(event) {
    event.preventDefault();
    const q = lookup.trim().toUpperCase().replace(/^#/, '');
    if (!q) {
      lookupError = 'Type an entry ID, for example N-0134.';
      return;
    }
    lookupError = '';
    const found = notes.find((n) => n.id === q);
    if (found) {
      lookup = '';
      openEntry(found.id);
    } else {
      deniedId = q;
      lookup = '';
      mode = 'read';
      status = 'denied';
    }
  }

  function retryConnection() {
    connection = 'retrying';
    connectionError = '';
    later(() => {
      if (retries === 0) {
        retries = 1;
        connection = 'offline';
        connectionError =
          'Still no answer from api.notepad6.app — the DNS lookup failed. Nothing is lost; every entry is held on this device.';
      } else {
        const queued = pendingCount;
        connection = 'online';
        connectionError = '';
        clock += 2;
        lastSynced = now();
        notes = notes.map((n) => ({ ...n, sync: 'synced' }));
        flash = queued
          ? `Back online. ${queued} ${queued === 1 ? 'entry' : 'entries'} sent to your account.`
          : 'Back online. Everything was already up to date.';
      }
    }, 950);
  }

  function askDelete() {
    if (!current) return;
    confirmOpen = true;
  }

  function closeDialog() {
    confirmOpen = false;
  }

  function reallyDelete() {
    const gone = current;
    notes = notes.filter((n) => n.id !== gone.id);
    confirmOpen = false;
    mode = 'read';
    status = 'ready';
    const rest = [...notes].sort((a, b) => b.updated_at.localeCompare(a.updated_at));
    currentId = rest.length ? rest[0].id : '';
    flash = `Deleted ${gone.id} — “${gone.title}”. That one is gone for good.`;
  }

  function onKeydown(event) {
    if (event.key === 'Escape' && confirmOpen) {
      event.preventDefault();
      closeDialog();
    }
  }

  $effect(() => {
    if (flash) {
      flashIn = false;
      const t = setTimeout(() => (flashIn = true), 20);
      return () => clearTimeout(t);
    }
  });

  $effect(() => {
    if (confirmOpen) {
      dialogIn = false;
      const t = setTimeout(() => {
        dialogIn = true;
        if (cancelEl) cancelEl.focus();
      }, 20);
      return () => clearTimeout(t);
    }
  });

  const hair = $derived(brand.neutralColor + '33');
  const primaryBtn = 'inline-flex items-center justify-center gap-2 border-[3px] px-5 py-3 text-[11px] uppercase tracking-[0.2em] transition-transform duration-150 hover:-translate-x-[2px] hover:-translate-y-[2px] active:translate-x-0 active:translate-y-0 motion-reduce:transform-none focus-visible:outline-2 focus-visible:outline-offset-[3px] disabled:opacity-60 disabled:hover:translate-x-0 disabled:hover:translate-y-0';
  const ghostBtn = 'inline-flex items-center justify-center gap-2 border-[3px] bg-transparent px-5 py-3 text-[11px] uppercase tracking-[0.2em] transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-[3px]';
</script>

<svelte:window onkeydown={onKeydown} />

<div
  class="min-h-screen w-full"
  style="background-color:{brand.backgroundColor}; color:{brand.primaryColor}; font-family:{brand.fontBody};"
>
  <div class="mx-auto max-w-[1180px] px-5 py-8 sm:px-8 lg:px-12 lg:py-12">

    <!-- masthead -->
    <div
      class="flex flex-wrap items-end justify-between gap-x-6 gap-y-2 border-b-[3px] pb-2"
      style="border-color:{brand.primaryColor}"
    >
      <p class="text-[11px] uppercase tracking-[0.32em]" style="color:{brand.neutralColor}">
        Notepad 6 · the desk
      </p>
      <p class="text-[11px] uppercase tracking-[0.32em] tabular-nums" style="color:{brand.neutralColor}">
        {owner.email} · {notes.length} entries on file
      </p>
    </div>
    <div class="mt-[3px] h-px w-full" style="background-color:{brand.primaryColor}"></div>

    <!-- connection strip -->
    <div class="mt-3 flex flex-wrap items-center justify-between gap-3">
      <p class="flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] tabular-nums" style="color:{brand.neutralColor}">
        {#if connection === 'online'}
          <Icon name="CheckCircle" class="h-[14px] w-[14px]" aria-hidden="true" />
          Synced {lastSynced}
        {:else if connection === 'retrying'}
          <Icon name="Clock" class="h-[14px] w-[14px] animate-spin motion-reduce:animate-none" aria-hidden="true" />
          Reaching the server…
        {:else}
          <Icon name="AlertCircle" class="h-[14px] w-[14px]" aria-hidden="true" />
          Working offline · last synced {lastSynced}{pendingCount ? ` · ${pendingCount} waiting` : ''}
        {/if}
      </p>
      {#if connection !== 'online'}
        <button
          type="button"
          onclick={retryConnection}
          disabled={connection === 'retrying'}
          class="border-b-[3px] text-[11px] uppercase tracking-[0.22em] transition-opacity hover:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50"
          style="border-color:{brand.primaryColor}; outline-color:{brand.accentColor}"
        >
          {connection === 'retrying' ? 'Trying…' : 'Retry connection'}
        </button>
      {/if}
    </div>

    {#if connectionError}
      <p
        class="mt-3 border-[3px] px-4 py-3 text-[12px] leading-relaxed"
        style="border-color:{brand.primaryColor}; background-color:#fff"
        role="status"
      >
        {connectionError}
      </p>
    {/if}

    <!-- action bar -->
    <div class="mt-8 flex flex-wrap items-center justify-between gap-4">
      <Button
        onclick={() => navigate('notes')}
        class="inline-flex items-center gap-2 bg-transparent px-0 py-2 text-[11px] uppercase tracking-[0.22em] transition-opacity hover:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-2"
        style="color:{brand.neutralColor}; outline-color:{brand.accentColor}"
      >
        <Icon name="ArrowLeft" class="h-4 w-4" aria-hidden="true" />
        All notes
      </Button>

      <div class="flex flex-wrap items-center gap-3">
        {#if mode === 'read' && current && status === 'ready'}
          <Button
            onclick={startNew}
            class={ghostBtn}
            style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
          >
            <Icon name="Plus" class="h-4 w-4" aria-hidden="true" />
            New entry
          </Button>
          <Button
            onclick={askDelete}
            class={ghostBtn}
            style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
          >
            <Icon name="Trash" class="h-4 w-4" aria-hidden="true" />
            Delete
          </Button>
          <Button
            onclick={startEdit}
            class={primaryBtn}
            style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
          >
            <Icon name="Edit" class="h-4 w-4" aria-hidden="true" />
            Edit entry
          </Button>
        {:else if mode === 'read'}
          <Button
            onclick={startNew}
            class={primaryBtn}
            style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
          >
            <Icon name="Plus" class="h-4 w-4" aria-hidden="true" />
            New entry
          </Button>
        {/if}
      </div>
    </div>

    {#if flash}
      <p
        role="status"
        class="mt-6 flex items-start gap-3 border-[3px] border-l-[10px] px-4 py-3 text-[12px] leading-relaxed transition-all duration-300 motion-reduce:transition-none {flashIn ? 'translate-y-0 opacity-100' : '-translate-y-1 opacity-0'}"
        style="border-color:{brand.primaryColor}; border-left-color:{brand.accentColor}; background-color:#fff"
      >
        <Icon name="CheckCircle" class="mt-[2px] h-4 w-4 shrink-0" aria-hidden="true" />
        <span>{flash}</span>
      </p>
    {/if}

    <div class="mt-8 grid grid-cols-1 gap-10 lg:grid-cols-[minmax(0,1fr)_300px] lg:gap-14">

      <!-- ============ main column ============ -->
      <section aria-labelledby="entry-heading">

        {#if status === 'denied'}
          <h1 id="entry-heading" class="sr-only">Entry {deniedId} is not available</h1>
          <div
            class="border-[3px] bg-white p-7 sm:p-10"
            style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
          >
            <p class="text-[11px] uppercase tracking-[0.3em] tabular-nums" style="color:{brand.neutralColor}">
              403 · not your entry
            </p>
            <h2
              class="mt-5 text-3xl leading-[1.08] sm:text-4xl"
              style="font-family:{brand.fontHeading}"
            >
              Entry {deniedId} isn’t on your desk
            </h2>
            <p class="mt-5 max-w-[60ch] text-[14px] leading-[1.6]">
              Entries belong to the account that wrote them. Having the ID doesn’t open it — Notepad 6 checks
              the owner on every read, so nobody opens yours either.
            </p>
            <p class="mt-3 text-[12px] tabular-nums" style="color:{brand.neutralColor}">
              Signed in as {owner.email} (user {owner.id}). If a friend wants you to read their note, ask them
              to paste the text; there is no shared access.
            </p>
            <div class="mt-8 flex flex-wrap gap-3">
              <Button
                onclick={() => { status = 'ready'; deniedId = ''; }}
                class={primaryBtn}
                style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
              >
                Back to {current ? current.id : 'my entries'}
              </Button>
              <Button
                onclick={() => navigate('notes')}
                class={ghostBtn}
                style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
              >
                Open my notes list
              </Button>
            </div>
          </div>

        {:else if status === 'loading'}
          <h1 id="entry-heading" class="sr-only">Opening entry {openingId}</h1>
          <div
            class="border-[3px] bg-white p-7 sm:p-10"
            style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
            aria-busy="true"
          >
            <p class="text-[11px] uppercase tracking-[0.3em] tabular-nums" style="color:{brand.neutralColor}">
              Fetching entry {openingId}…
            </p>
            <div class="mt-6 animate-pulse space-y-4 motion-reduce:animate-none">
              <div class="h-10 w-4/5" style="background-color:{brand.neutralColor}22"></div>
              <div class="h-px w-full" style="background-color:{hair}"></div>
              <div class="h-3 w-full" style="background-color:{brand.neutralColor}22"></div>
              <div class="h-3 w-11/12" style="background-color:{brand.neutralColor}22"></div>
              <div class="h-3 w-3/5" style="background-color:{brand.neutralColor}22"></div>
              <div class="h-3 w-10/12" style="background-color:{brand.neutralColor}22"></div>
            </div>
          </div>

        {:else if mode === 'read' && !current}
          <h1 id="entry-heading" class="sr-only">No entries yet</h1>
          <div
            class="border-[3px] bg-white p-7 sm:p-10"
            style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
          >
            <Empty
              title="The desk is clear"
              description="Nothing is filed under this account right now. Start an entry — Notepad 6 stamps it with a created and an updated time and keeps it private to you."
            >
              {#snippet action()}
                <Button
                  onclick={startNew}
                  class={primaryBtn}
                  style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
                >
                  <Icon name="Plus" class="h-4 w-4" aria-hidden="true" />
                  Write the first entry
                </Button>
              {/snippet}
            </Empty>
          </div>

        {:else if mode === 'read'}
          <p class="text-[11px] uppercase tracking-[0.3em] tabular-nums" style="color:{brand.neutralColor}">
            Entry {current.id}
          </p>
          <h1
            id="entry-heading"
            class="mt-3 text-[34px] leading-[1.04] sm:text-[46px] lg:text-[54px]"
            style="font-family:{brand.fontHeading}"
          >
            {current.title}
          </h1>

          <div class="mt-5 flex flex-wrap items-center gap-x-6 gap-y-2 border-t-[3px] pt-3 text-[11px] uppercase tracking-[0.2em] tabular-nums"
               style="border-color:{brand.primaryColor}; color:{brand.neutralColor}">
            <span>Created {current.created_at}</span>
            <span>Updated {current.updated_at}</span>
            <span class="inline-flex items-center gap-2" style="color:{brand.primaryColor}">
              {#if current.sync === 'pending'}
                <Icon name="Clock" class="h-[14px] w-[14px]" aria-hidden="true" />
                Pending sync
              {:else}
                <Icon name="Check" class="h-[14px] w-[14px]" aria-hidden="true" />
                Saved to account
              {/if}
            </span>
          </div>

          <article
            class="mt-7 border-[3px] bg-white p-6 sm:p-9"
            style="border-color:{brand.primaryColor}; box-shadow:6px 6px 0 {brand.primaryColor}"
          >
            <p class="whitespace-pre-wrap text-[15px] leading-[1.75]">{current.body}</p>
            <div class="mt-8 h-px w-full" style="background-color:{hair}"></div>
            <p class="mt-3 text-[11px] uppercase tracking-[0.2em] tabular-nums" style="color:{brand.neutralColor}">
              {words} words · {chars} characters · plain text only
            </p>
          </article>

        {:else}
          <h1 id="entry-heading" class="sr-only">
            {mode === 'new' ? 'Write a new entry' : `Editing entry ${current ? current.id : ''}`}
          </h1>
          <p class="text-[11px] uppercase tracking-[0.3em] tabular-nums" style="color:{brand.neutralColor}">
            {mode === 'new' ? 'New entry · not filed yet' : `Editing entry ${current.id}`}
          </p>

          <form onsubmit={(e) => { e.preventDefault(); save(); }} class="mt-4">
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
                placeholder="Untitled entry"
                class="mt-3 w-full rounded-none border-0 border-b-[3px] bg-transparent px-0 pb-3 text-[26px] leading-tight sm:text-[34px] focus-visible:outline-2 focus-visible:outline-offset-4"
                style="font-family:{brand.fontHeading}; border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
              />
              <p class="mt-3 text-[12px] leading-relaxed" style="color:{brand.neutralColor}">
                Leave this blank and the first line of the body becomes the title.
              </p>

              <Label
                for="note-body"
                class="mt-8 block text-[11px] uppercase tracking-[0.3em]"
                style="color:{brand.neutralColor}"
              >
                Body
              </Label>
              <Textarea
                id="note-body"
                rows="14"
                bind:value={draftBody}
                placeholder="Type the entry. Plain text — no formatting, no attachments."
                class="mt-3 w-full rounded-none border-[3px] bg-transparent p-4 text-[15px] leading-[1.75] focus-visible:outline-2 focus-visible:outline-offset-[3px]"
                style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}; font-family:{brand.fontBody}"
              ></Textarea>

              <div class="mt-4 flex flex-wrap items-center justify-between gap-3 text-[11px] uppercase tracking-[0.2em] tabular-nums"
                   style="color:{brand.neutralColor}">
                <span>{words} words · {chars} characters</span>
                <span>
                  {mode === 'new' ? 'Created stamp set on save' : `Created ${current.created_at}`}
                </span>
              </div>
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
              <Button
                type="submit"
                disabled={saving}
                class={primaryBtn}
                style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
              >
                {#if saving}
                  <Icon name="Clock" class="h-4 w-4 animate-spin motion-reduce:animate-none" aria-hidden="true" />
                  Saving…
                {:else}
                  <Icon name="Check" class="h-4 w-4" aria-hidden="true" />
                  {mode === 'new' ? 'File this entry' : 'Save changes'}
                {/if}
              </Button>
              <Button
                type="button"
                onclick={cancelEdit}
                class={ghostBtn}
                style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
              >
                <Icon name="X" class="h-4 w-4" aria-hidden="true" />
                Cancel
              </Button>
              {#if connection !== 'online'}
                <span class="text-[11px] uppercase tracking-[0.2em]" style="color:{brand.neutralColor}">
                  Offline — this saves here and syncs later
                </span>
              {/if}
            </div>
          </form>
        {/if}
      </section>

      <!-- ============ folio sidebar ============ -->
      <aside class="space-y-8">

        <!-- 01 folio -->
        <section
          class="border-[3px] bg-white p-5"
          style="border-color:{brand.primaryColor}"
          aria-labelledby="folio-heading"
        >
          <h2 id="folio-heading" class="text-[11px] uppercase tracking-[0.3em]" style="color:{brand.neutralColor}">
            01 / Folio
          </h2>
          <div class="mt-4">
            {#if current && mode !== 'new' && status === 'ready'}
              <dl class="text-[12px] tabular-nums">
                <div class="flex items-baseline justify-between gap-4 py-2">
                  <dt class="uppercase tracking-[0.16em]" style="color:{brand.neutralColor}">Entry ID</dt>
                  <dd>{current.id}</dd>
                </div>
                <div class="h-px w-full" style="background-color:{hair}"></div>
                <div class="flex items-baseline justify-between gap-4 py-2">
                  <dt class="uppercase tracking-[0.16em]" style="color:{brand.neutralColor}">Owner</dt>
                  <dd class="truncate">{owner.id}</dd>
                </div>
                <div class="h-px w-full" style="background-color:{hair}"></div>
                <div class="flex items-baseline justify-between gap-4 py-2">
                  <dt class="uppercase tracking-[0.16em]" style="color:{brand.neutralColor}">Created</dt>
                  <dd>{current.created_at}</dd>
                </div>
                <div class="h-px w-full" style="background-color:{hair}"></div>
                <div class="flex items-baseline justify-between gap-4 py-2">
                  <dt class="uppercase tracking-[0.16em]" style="color:{brand.neutralColor}">Updated</dt>
                  <dd>{current.updated_at}</dd>
                </div>
                <div class="h-px w-full" style="background-color:{hair}"></div>
                <div class="flex items-baseline justify-between gap-4 py-2">
                  <dt class="uppercase tracking-[0.16em]" style="color:{brand.neutralColor}">Words</dt>
                  <dd>{words}</dd>
                </div>
                <div class="h-px w-full" style="background-color:{hair}"></div>
                <div class="flex items-baseline justify-between gap-4 py-2">
                  <dt class="uppercase tracking-[0.16em]" style="color:{brand.neutralColor}">Storage</dt>
                  <dd>Private</dd>
                </div>
              </dl>
            {:else if mode === 'new'}
              <p class="text-[12px] leading-relaxed" style="color:{brand.neutralColor}">
                This entry has no ID yet. Notepad 6 assigns {nextId()} and stamps both timestamps the moment
                you file it.
              </p>
            {:else}
              <p class="text-[12px] leading-relaxed" style="color:{brand.neutralColor}">
                No entry is open. Pick one from the recent list below.
              </p>
            {/if}
          </div>
        </section>

        <!-- 02 open another -->
        <section
          class="border-[3px] bg-white p-5"
          style="border-color:{brand.primaryColor}"
          aria-labelledby="goto-heading"
        >
          <h2 id="goto-heading" class="text-[11px] uppercase tracking-[0.3em]" style="color:{brand.neutralColor}">
            02 / Go to entry
          </h2>
          <form onsubmit={goToEntry} class="mt-4">
            <Label for="entry-lookup" class="block text-[11px] uppercase tracking-[0.16em]" style="color:{brand.neutralColor}">
              Entry ID
            </Label>
            <div class="mt-2 flex gap-2">
              <Input
                id="entry-lookup"
                bind:value={lookup}
                placeholder="N-0134"
                class="w-full rounded-none border-[3px] bg-transparent px-3 py-2 text-[13px] tabular-nums focus-visible:outline-2 focus-visible:outline-offset-[3px]"
                style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}; font-family:{brand.fontBody}"
              />
              <Button
                type="submit"
                aria-label="Open that entry"
                class="inline-flex shrink-0 items-center justify-center border-[3px] px-3 transition-transform duration-150 hover:-translate-y-[2px] motion-reduce:transform-none focus-visible:outline-2 focus-visible:outline-offset-[3px]"
                style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; outline-color:{brand.accentColor}"
              >
                <Icon name="Search" class="h-4 w-4" aria-hidden="true" />
              </Button>
            </div>
            {#if lookupError}
              <p role="alert" class="mt-2 text-[12px]" style="color:{brand.primaryColor}">{lookupError}</p>
            {/if}
          </form>
        </section>

        <!-- 03 recent -->
        <section
          class="border-[3px] bg-white p-5"
          style="border-color:{brand.primaryColor}"
          aria-labelledby="recent-heading"
        >
          <h2 id="recent-heading" class="text-[11px] uppercase tracking-[0.3em]" style="color:{brand.neutralColor}">
            03 / Recently updated
          </h2>
          {#if ordered.length === 0}
            <p class="mt-4 text-[12px] leading-relaxed" style="color:{brand.neutralColor}">
              Nothing filed yet. Your entries will list here, newest change first.
            </p>
          {:else}
            <ul class="mt-4">
              {#each ordered.slice(0, 6) as note (note.id)}
                <li>
                  <button
                    type="button"
                    onclick={() => openEntry(note.id)}
                    aria-current={note.id === currentId && status === 'ready' ? 'true' : undefined}
                    class="group flex w-full items-start gap-3 border-l-[6px] py-3 pl-3 pr-1 text-left transition-colors duration-150 hover:bg-black/[0.04] focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none"
                    style="border-left-color:{note.id === currentId && status === 'ready' ? brand.accentColor : 'transparent'}; outline-color:{brand.accentColor}"
                  >
                    <span class="min-w-0 flex-1">
                      <span class="block truncate text-[13px] leading-snug">{note.title}</span>
                      <span class="mt-1 block text-[11px] uppercase tracking-[0.14em] tabular-nums" style="color:{brand.neutralColor}">
                        {note.id} · {note.updated_at}{note.id === currentId && status === 'ready' ? ' · reading' : ''}
                      </span>
                    </span>
                    <Icon name="ChevronRight" class="mt-[2px] h-4 w-4 shrink-0 opacity-40 transition-opacity group-hover:opacity-100" aria-hidden="true" />
                  </button>
                  <div class="h-px w-full" style="background-color:{hair}"></div>
                </li>
              {/each}
            </ul>
            <Button
              onclick={() => navigate('notes')}
              class="mt-4 inline-flex items-center gap-2 bg-transparent px-0 py-2 text-[11px] uppercase tracking-[0.2em] transition-opacity hover:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-2"
              style="color:{brand.primaryColor}; outline-color:{brand.accentColor}"
            >
              See all {notes.length} entries
              <Icon name="ArrowRight" class="h-4 w-4" aria-hidden="true" />
            </Button>
          {/if}
        </section>
      </aside>
    </div>

    <p class="mt-14 border-t-[3px] pt-3 text-[11px] uppercase tracking-[0.3em]"
       style="border-color:{brand.primaryColor}; color:{brand.neutralColor}">
      Notepad 6 · free to use, no billing, ever · entries are visible to {owner.email} alone
    </p>
  </div>
</div>

{#if confirmOpen && current}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-5 transition-opacity duration-200 motion-reduce:transition-none {dialogIn ? 'opacity-100' : 'opacity-0'}"
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
      class="relative w-full max-w-md border-[3px] bg-white p-7 transition-transform duration-200 motion-reduce:transition-none {dialogIn ? 'translate-y-0' : 'translate-y-2'}"
      style="border-color:{brand.primaryColor}; box-shadow:8px 8px 0 {brand.primaryColor}"
    >
      <p class="text-[11px] uppercase tracking-[0.3em] tabular-nums" style="color:{brand.neutralColor}">
        Confirm · entry {current.id}
      </p>
      <h2 id="delete-heading" class="mt-4 text-[28px] leading-[1.1]" style="font-family:{brand.fontHeading}">
        Delete this entry?
      </h2>
      <p id="delete-copy" class="mt-4 text-[13px] leading-[1.65]">
        “{current.title}” leaves your account for good. There is no bin to pull it back from, and the text
        isn’t kept anywhere else.
      </p>
      <p class="mt-3 text-[11px] uppercase tracking-[0.18em] tabular-nums" style="color:{brand.neutralColor}">
        Created {current.created_at} · updated {current.updated_at}
      </p>
      <div class="mt-7 flex flex-wrap justify-end gap-3">
        <Button
          bind:ref={cancelEl}
          onclick={closeDialog}
          class={ghostBtn}
          style="border-color:{brand.primaryColor}; color:{brand.primaryColor}; outline-color:{brand.accentColor}"
        >
          Keep the entry
        </Button>
        <Button
          onclick={reallyDelete}
          class={primaryBtn}
          style="border-color:{brand.primaryColor}; background-color:{brand.primaryColor}; color:{brand.backgroundColor}; box-shadow:5px 5px 0 {brand.accentColor}; outline-color:{brand.accentColor}"
        >
          <Icon name="Trash" class="h-4 w-4" aria-hidden="true" />
          Delete permanently
        </Button>
      </div>
    </div>
  </div>
{/if}
