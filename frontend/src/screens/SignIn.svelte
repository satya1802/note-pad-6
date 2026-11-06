<script>
  import { Button, Checkbox, Icon, Input, Label } from "@/lib/ui";
  import { brand } from "@/lib/brand";
  import { useNavigate } from "@/lib/navigate";
  import { apiFetch } from "@/lib/api";
  import { session } from "@/lib/session.svelte";

  const navigate = useNavigate();

  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  let email = $state("");
  let password = $state("");
  let showPassword = $state(false);
  let remember = $state(true);

  // 'idle' | 'submitting' | 'success'
  let status = $state("idle");
  let formError = $state(null);
  let errorIn = $state(false);
  let fieldErrors = $state({ email: null, password: null });
  let sessionNotice = $state(true);
  let signedInEmail = $state("");

  const busy = $derived(status === "submitting" || status === "success");

  const timers = [];
  function later(fn, ms) {
    const id = setTimeout(fn, ms);
    timers.push(id);
    return id;
  }

  $effect(() => () => timers.forEach(clearTimeout));

  function raiseError(message) {
    formError = message;
    errorIn = false;
    later(() => (errorIn = true), 20);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (busy) return;

    const next = { email: null, password: null };
    const trimmed = email.trim();

    if (!trimmed) next.email = "Enter the email address on your account.";
    else if (!EMAIL_RE.test(trimmed)) next.email = "That is not a complete email address.";
    if (!password) next.password = "Enter your password.";

    fieldErrors = next;
    if (next.email || next.password) {
      formError = null;
      return;
    }

    formError = null;
    status = "submitting";

    try {
      const data = await apiFetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email: trimmed, password }),
      });
      session.user = data.user;
      session.checked = true;
      signedInEmail = data.user.email;
      status = "success";
      later(() => navigate("notes"), 600);
    } catch {
      status = "idle";
      password = "";
      // One generic message whichever credential was wrong: nothing here tells an
      // attacker which of the two was the mistake.
      raiseError("That email and password do not match an account.");
    }
  }

  const facts = [
    {
      n: "01",
      t: "Yours alone",
      d: "Every note is stored against your account. No shared folders, no one else reading over it.",
    },
    {
      n: "02",
      t: "Plain text, nothing else",
      d: "A title, a body, a created and an updated timestamp. No formatting to fight with.",
    },
    {
      n: "03",
      t: "Free, with no tier above it",
      d: "No card, no billing page, no upgrade prompt waiting three screens in.",
    },
  ];
</script>

<div
  class="min-h-screen w-full"
  style="background-color: {brand.backgroundColor}; color: {brand.primaryColor}; font-family: {brand.fontBody};"
>
  <!-- Masthead -->
  <header class="border-b-[3px] px-6 py-4 md:px-10" style="border-color: {brand.primaryColor};">
    <div class="mx-auto flex max-w-6xl flex-wrap items-baseline justify-between gap-x-8 gap-y-2">
      <p class="text-[11px] font-bold uppercase tracking-[0.3em]">Notepad&nbsp;6</p>
      <p
        class="text-[11px] uppercase tracking-[0.18em]"
        style="color: {brand.neutralColor}; font-variant-numeric: tabular-nums;"
      >
        Edition VI &middot; Friday 6 November 2026
      </p>
    </div>
  </header>

  <main class="mx-auto max-w-6xl px-6 py-12 md:px-10 md:py-16 lg:py-24">
    <div class="grid gap-14 lg:grid-cols-[1.05fr_minmax(0,460px)] lg:gap-20">
      <!-- Editorial column -->
      <section>
        <p
          class="text-[11px] font-bold uppercase tracking-[0.3em]"
          style="color: {brand.accentColor};"
        >
          &sect; 01 &mdash; Session
        </p>

        <h1
          class="mt-5 text-[56px] leading-[0.92] tracking-[-0.02em] sm:text-[76px] lg:text-[92px]"
          style="font-family: {brand.fontHeading};"
        >
          Sign in.
        </h1>

        <div class="mt-8 border-t-[3px] pt-6" style="border-color: {brand.primaryColor};">
          <p class="max-w-[58ch] text-[15px] leading-[1.6]" style="color: {brand.neutralColor};">
            Enter your email and password to start a new session.
          </p>
        </div>

        <!-- Signature: notepad margin rule down the facts list -->
        <ol class="mt-10 border-l-[3px] pl-6" style="border-color: {brand.accentColor};">
          {#each facts as fact, i (fact.n)}
            <li
              class="py-5 {i === 0 ? '' : 'border-t border-dashed'}"
              style="border-color: {brand.neutralColor};"
            >
              <div class="flex gap-5">
                <span
                  class="shrink-0 text-[11px] font-bold uppercase tracking-[0.2em]"
                  style="color: {brand.accentColor}; font-variant-numeric: tabular-nums;"
                  >{fact.n}</span
                >
                <div>
                  <h2 class="text-[20px] leading-tight" style="font-family: {brand.fontHeading};">
                    {fact.t}
                  </h2>
                  <p
                    class="mt-2 max-w-[52ch] text-[13px] leading-[1.6]"
                    style="color: {brand.neutralColor};"
                  >
                    {fact.d}
                  </p>
                </div>
              </div>
            </li>
          {/each}
        </ol>
      </section>

      <!-- Form column -->
      <section class="lg:pt-16">
        {#if sessionNotice && status !== "success"}
          <div
            class="mb-6 flex items-start gap-3 border-[3px] px-4 py-3"
            style="border-color: {brand.primaryColor}; background-color: {brand.backgroundColor};"
          >
            <Icon name="Clock" class="mt-[2px] h-4 w-4 shrink-0" aria-hidden="true" />
            <p class="flex-1 text-[12px] leading-[1.6]" style="color: {brand.neutralColor};">
              <span
                class="font-bold uppercase tracking-[0.18em]"
                style="color: {brand.primaryColor};">Session ended</span
              >
              <span class="block">Sign in again to reach your notes.</span>
            </p>
            <button
              type="button"
              aria-label="Dismiss session ended notice"
              class="-m-1 p-1 transition-opacity duration-150 hover:opacity-60 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2 motion-reduce:transition-none"
              style="outline-color: {brand.accentColor};"
              onclick={() => (sessionNotice = false)}
            >
              <Icon name="X" class="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        {/if}

        <div
          class="border-[3px] bg-white"
          style="border-color: {brand.primaryColor}; box-shadow: 6px 6px 0 0 {brand.primaryColor};"
        >
          {#if status === "success"}
            <div class="px-7 py-14 text-center md:px-10">
              <div
                class="mx-auto flex h-14 w-14 items-center justify-center border-[3px]"
                style="border-color: {brand.primaryColor}; background-color: {brand.accentColor};"
              >
                <Icon name="Check" class="h-7 w-7 text-white" aria-hidden="true" />
              </div>
              <h2 class="mt-6 text-[30px] leading-tight" style="font-family: {brand.fontHeading};">
                Session started
              </h2>
              <p class="mt-3 text-[13px] leading-[1.6]" style="color: {brand.neutralColor};">
                Signed in as {signedInEmail}. Opening your notes…
              </p>
              <div
                class="mx-auto mt-7 h-[3px] w-40 overflow-hidden"
                style="background-color: {brand.backgroundColor};"
              >
                <div
                  class="h-full w-full animate-pulse motion-reduce:animate-none"
                  style="background-color: {brand.accentColor};"
                ></div>
              </div>
              <button
                type="button"
                class="mt-7 text-[11px] font-bold uppercase tracking-[0.2em] underline underline-offset-4 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2"
                style="outline-color: {brand.accentColor};"
                onclick={() => navigate("notes")}
              >
                Go to my notes now
              </button>
            </div>
          {:else}
            <div
              class="border-b-[3px] px-7 py-5 md:px-8"
              style="border-color: {brand.primaryColor};"
            >
              <p
                class="text-[11px] font-bold uppercase tracking-[0.25em]"
                style="color: {brand.neutralColor};"
              >
                Returning reader
              </p>
              <h2 class="mt-1 text-[26px] leading-tight" style="font-family: {brand.fontHeading};">
                Enter your credentials
              </h2>
            </div>

            <form class="px-7 py-7 md:px-8" onsubmit={handleSubmit} novalidate>
              {#if formError}
                <div
                  role="alert"
                  class="mb-6 flex items-start gap-3 border-[3px] px-4 py-3 transition-all duration-300 motion-reduce:transition-none"
                  style="border-color: {brand.primaryColor}; background-color: {brand.backgroundColor}; opacity: {errorIn
                    ? 1
                    : 0}; transform: translateY({errorIn ? '0' : '-6px'});"
                >
                  <Icon name="AlertCircle" class="mt-[2px] h-4 w-4 shrink-0" aria-hidden="true" />
                  <div class="text-[12px] leading-[1.6]">
                    <p class="font-bold uppercase tracking-[0.18em]">Sign-in refused</p>
                    <p class="mt-1" style="color: {brand.neutralColor};">{formError}</p>
                  </div>
                </div>
              {/if}

              <div class="space-y-6">
                <div>
                  <Label
                    for="signin-email"
                    class="block text-[11px] font-bold uppercase tracking-[0.2em]"
                    >Email address</Label
                  >
                  <Input
                    id="signin-email"
                    type="email"
                    name="email"
                    autocomplete="email"
                    spellcheck="false"
                    placeholder="you@example.com"
                    bind:value={email}
                    disabled={busy}
                    aria-invalid={fieldErrors.email ? "true" : undefined}
                    aria-describedby={fieldErrors.email ? "signin-email-error" : undefined}
                    class="mt-2 w-full rounded-none border-[3px] bg-white px-4 py-3 text-[15px] disabled:opacity-50 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2"
                    style="border-color: {brand.primaryColor}; color: {brand.primaryColor}; outline-color: {brand.accentColor}; font-family: {brand.fontBody};"
                  />
                  {#if fieldErrors.email}
                    <p
                      id="signin-email-error"
                      class="mt-2 flex items-start gap-2 text-[12px] leading-[1.5]"
                    >
                      <Icon
                        name="AlertCircle"
                        class="mt-[1px] h-3.5 w-3.5 shrink-0"
                        aria-hidden="true"
                      />
                      <span>{fieldErrors.email}</span>
                    </p>
                  {/if}
                </div>

                <div>
                  <div class="flex items-baseline justify-between gap-4">
                    <Label
                      for="signin-password"
                      class="block text-[11px] font-bold uppercase tracking-[0.2em]">Password</Label
                    >
                    <button
                      type="button"
                      class="text-[11px] font-bold uppercase tracking-[0.18em] underline underline-offset-4 transition-opacity duration-150 hover:opacity-60 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2 motion-reduce:transition-none"
                      style="color: {brand.neutralColor}; outline-color: {brand.accentColor};"
                      aria-pressed={showPassword}
                      onclick={() => (showPassword = !showPassword)}
                    >
                      {showPassword ? "Hide" : "Show"}
                    </button>
                  </div>
                  <Input
                    id="signin-password"
                    type={showPassword ? "text" : "password"}
                    name="password"
                    autocomplete="current-password"
                    placeholder="••••••••••"
                    bind:value={password}
                    disabled={busy}
                    aria-invalid={fieldErrors.password ? "true" : undefined}
                    aria-describedby={fieldErrors.password ? "signin-password-error" : undefined}
                    class="mt-2 w-full rounded-none border-[3px] bg-white px-4 py-3 text-[15px] disabled:opacity-50 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2"
                    style="border-color: {brand.primaryColor}; color: {brand.primaryColor}; outline-color: {brand.accentColor}; font-family: {brand.fontBody};"
                  />
                  {#if fieldErrors.password}
                    <p
                      id="signin-password-error"
                      class="mt-2 flex items-start gap-2 text-[12px] leading-[1.5]"
                    >
                      <Icon
                        name="AlertCircle"
                        class="mt-[1px] h-3.5 w-3.5 shrink-0"
                        aria-hidden="true"
                      />
                      <span>{fieldErrors.password}</span>
                    </p>
                  {/if}
                </div>

                <div class="flex items-center gap-3 pt-1">
                  <Checkbox
                    id="signin-remember"
                    bind:checked={remember}
                    disabled={busy}
                    class="h-5 w-5 rounded-none border-[3px] focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2"
                    style="border-color: {brand.primaryColor}; accent-color: {brand.accentColor}; outline-color: {brand.accentColor};"
                  />
                  <Label
                    for="signin-remember"
                    class="text-[12px] leading-snug"
                    style="color: {brand.neutralColor};"
                  >
                    Keep this session open on this device
                  </Label>
                </div>
              </div>

              <Button
                type="submit"
                disabled={busy}
                class="mt-8 flex w-full items-center justify-center gap-3 rounded-none border-[3px] px-5 py-4 text-[12px] font-bold uppercase tracking-[0.25em] text-white transition-transform duration-150 hover:-translate-x-[1px] hover:-translate-y-[1px] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none disabled:cursor-not-allowed disabled:opacity-55 focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-[3px] motion-reduce:transition-none motion-reduce:transform-none"
                style="background-color: {brand.primaryColor}; border-color: {brand.primaryColor}; box-shadow: 4px 4px 0 0 {brand.accentColor}; outline-color: {brand.accentColor}; font-family: {brand.fontBody}; font-variant-numeric: tabular-nums;"
              >
                {#if status === "submitting"}
                  <span
                    class="inline-block h-2.5 w-2.5 animate-pulse motion-reduce:animate-none"
                    style="background-color: {brand.backgroundColor};"
                    aria-hidden="true"
                  ></span>
                  Checking credentials…
                {:else}
                  Sign in
                  <Icon name="ArrowRight" class="h-4 w-4" aria-hidden="true" />
                {/if}
              </Button>

              <p
                class="mt-4 text-center text-[11px] leading-[1.6]"
                style="color: {brand.neutralColor};"
              >
                No payment is ever asked for &mdash; not here, not later.
              </p>
            </form>
          {/if}
        </div>

        <div class="mt-8 border-t border-dashed pt-6" style="border-color: {brand.neutralColor};">
          <p class="text-[12px] leading-[1.6]" style="color: {brand.neutralColor};">
            Not registered yet? An account takes an email and a password, and nothing else.
          </p>
          <Button
            type="button"
            onclick={() => navigate("register")}
            class="mt-4 flex w-full items-center justify-center gap-3 rounded-none border-[3px] bg-transparent px-5 py-3.5 text-[12px] font-bold uppercase tracking-[0.2em] transition-transform duration-150 active:translate-x-[3px] active:translate-y-[3px] active:shadow-none focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-[3px] motion-reduce:transition-none motion-reduce:transform-none"
            style="border-color: {brand.primaryColor}; color: {brand.primaryColor}; box-shadow: 3px 3px 0 0 {brand.primaryColor}; outline-color: {brand.accentColor}; font-family: {brand.fontBody};"
          >
            <Icon name="Plus" class="h-4 w-4" aria-hidden="true" />
            Create an account
          </Button>
        </div>
      </section>
    </div>
  </main>

  <footer
    class="mt-8 border-t-[3px] px-6 py-6 md:px-10"
    style="border-color: {brand.primaryColor};"
  >
    <div
      class="mx-auto flex max-w-6xl flex-wrap items-baseline justify-between gap-x-8 gap-y-2 text-[11px] uppercase tracking-[0.18em]"
      style="color: {brand.neutralColor};"
    >
      <p>Notepad 6 &mdash; plain text, privately kept</p>
      <p style="font-variant-numeric: tabular-nums;">
        Free to use &middot; no billing &middot; set in Didot &amp; mono
      </p>
    </div>
  </footer>
</div>
