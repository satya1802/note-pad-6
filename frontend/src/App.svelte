<script module lang="ts">
  import type { Component } from "svelte";

  import Register from "./screens/Register.svelte";
  import SignIn from "./screens/SignIn.svelte";
  import Notes from "./screens/Notes.svelte";
  import Note from "./screens/Note.svelte";

  // Screens marked bare (shown before sign-in, or hidden from the menu) render on their own.
  export const routes: Array<{ path: string; component: Component; bare?: boolean }> = [
    { path: "/register", component: Register, bare: true },
    { path: "/sign-in", component: SignIn, bare: true },
    { path: "/notes", component: Notes },
    { path: "/note/:id", component: Note },
  ];
  // Where an unknown path lands.
  export const fallback = "/sign-in";
</script>

<script lang="ts">
  import { go, location, matches } from "./lib/router.svelte";
  import { session, refreshSession } from "./lib/session.svelte";

  const current = $derived(routes.find((route) => matches(route.path, location.path)));

  $effect(() => {
    if (!current) go(fallback, true);
  });

  $effect(() => {
    refreshSession();
  });

  // Protected routes (anything not marked `bare`) require an active session: once the
  // one-time /api/auth/me check comes back without a user, send the visitor to sign in.
  $effect(() => {
    if (session.checked && !session.user && current && !current.bare) {
      go(fallback, true);
    }
  });

  function linkClass(path: string): string {
    const active = path === "/" ? location.path === "/" : location.path.startsWith(path);
    return [
      "flex items-center gap-2 rounded-[var(--brand-radius)] px-3 py-2 text-sm font-medium transition-colors",
      active ? "bg-[var(--brand-hover)] text-[var(--brand-fg)]" : "text-[var(--brand-fg-muted)]",
    ].join(" ");
  }

  function follow(event: MouseEvent, path: string): void {
    event.preventDefault();
    go(path);
  }
</script>

{#if current?.bare}
  <current.component />
{:else if current && session.checked && session.user}
  <div class="flex min-h-screen">
    <aside
      class="w-56 shrink-0 border-r p-4"
      style="background-color: var(--brand-surface); border-color: var(--brand-border)"
    >
      <p class="mb-4 px-3 text-sm font-semibold" style="font-family: var(--brand-font-heading)">
        note pad 6
      </p>
      <nav aria-label="App menu" class="flex flex-col gap-1">
        <a href="/notes" class={linkClass("/notes")} onclick={(event) => follow(event, "/notes")}>
          My notes
        </a>
      </nav>
    </aside>
    <main class="flex-1 overflow-auto">
      <current.component />
    </main>
  </div>
{/if}
