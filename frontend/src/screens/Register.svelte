<script>
  import { Icon } from "@/lib/ui";
  import { brand } from "@/lib/brand";
  import { useNavigate } from "@/lib/navigate";
  import { apiFetch, ApiError } from "@/lib/api";
  import { session } from "@/lib/session.svelte";

  const navigate = useNavigate();

  const PRODUCT = "note pad 6";
  const SCREEN = "Create account";
  const MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace';

  const MIN_PASSWORD = 8;

  let email = $state("");
  let password = $state("");
  let emailError = $state("");
  let passwordError = $state("");
  let formError = $state("");
  let submitting = $state(false);
  let done = $state(false);
  let createdAt = $state("");
  let focusedField = $state("");

  function stamp() {
    const d = new Date();
    const p = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (submitting) return;
    formError = "";
    emailError = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())
      ? ""
      : "Enter an email address in the form you@example.com";
    passwordError =
      password.length >= MIN_PASSWORD
        ? ""
        : `Use at least ${MIN_PASSWORD} characters — you typed ${password.length}`;
    if (emailError || passwordError) return;

    submitting = true;
    try {
      const data = await apiFetch("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({ email: email.trim(), password }),
      });
      session.user = data.user;
      session.checked = true;
      createdAt = stamp();
      done = true;
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        formError = "That email is already in use. Sign in instead, or register another address.";
      } else if (err instanceof ApiError && err.status === 422) {
        const fields = err.body && err.body.fields ? err.body.fields : {};
        emailError = fields.email || "";
        passwordError = fields.password || "";
        if (!fields.email && !fields.password) {
          formError = "Something about that form isn't right. Check the fields and try again.";
        }
      } else {
        formError = "Could not reach the server to create your account. Try again.";
      }
    } finally {
      submitting = false;
    }
  }

  const thick = `3px solid ${brand.primaryColor}`;
  const hard = `8px 8px 0 ${brand.primaryColor}`;
  const field = {
    border: thick,
    borderRadius: brand.radius,
    height: 48,
    backgroundColor: "transparent",
    fontFamily: MONO,
  };
  const fieldStyle = (name) =>
    `border: ${field.border}; border-radius: ${field.borderRadius}; height: ${field.height}px; background-color: ${field.backgroundColor}; font-family: ${field.fontFamily}; box-shadow: ${focusedField === name ? `4px 4px 0 ${brand.accentColor}` : "none"};`;
</script>

<div
  class="flex min-h-screen flex-col px-12 py-8"
  style="color: {brand.primaryColor}; font-family: {brand.fontBody}; background-color: {brand.backgroundColor};"
>
  <header
    class="flex items-center justify-between pb-4"
    style="border-bottom: {thick}; font-family: {MONO};"
  >
    <p class="text-sm font-bold uppercase tracking-[0.25em]">{PRODUCT}</p>
    <p class="text-xs uppercase" style="font-variant-numeric: tabular-nums;">
      Vol. 01 — No. 11 — 06 Nov 2026
    </p>
  </header>

  <div class="grid flex-1 grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)] items-center gap-14 py-10">
    <h1
      class="text-[120px] font-bold leading-[0.85] tracking-tight"
      style="font-family: {brand.fontHeading};"
    >
      {SCREEN}<span style="color: {brand.accentColor};">.</span>
    </h1>

    <main
      class="p-8"
      style="border: {thick}; box-shadow: {hard}; border-radius: {brand.radius}; background-color: {brand.backgroundColor};"
    >
      {#if done}
        <p role="status" class="text-2xl font-bold" style="font-family: {brand.fontHeading};">
          Account opened. The notebook is yours alone.
        </p>
        <dl
          class="mt-6 space-y-2 text-xs uppercase"
          style="font-family: {MONO}; font-variant-numeric: tabular-nums;"
        >
          <div
            class="flex justify-between gap-4 pb-2"
            style="border-bottom: 1px dashed {brand.neutralColor};"
          >
            <dt class="font-bold tracking-[0.2em]">Email</dt>
            <dd class="truncate normal-case">{email}</dd>
          </div>
          <div
            class="flex justify-between gap-4 pb-2"
            style="border-bottom: 1px dashed {brand.neutralColor};"
          >
            <dt class="font-bold tracking-[0.2em]">Created at</dt>
            <dd>{createdAt}</dd>
          </div>
          <div class="flex justify-between gap-4">
            <dt class="font-bold tracking-[0.2em]">Notes on file</dt>
            <dd>0</dd>
          </div>
        </dl>
        <button
          type="button"
          onclick={() => navigate("notes")}
          class="mt-6 h-14 w-full text-sm font-bold uppercase tracking-[0.25em] transition-transform active:translate-x-1 active:translate-y-1 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4"
          style="background-color: {brand.primaryColor}; color: {brand.backgroundColor}; border: {thick}; border-radius: {brand.radius}; box-shadow: 4px 4px 0 {brand.accentColor}; font-family: {MONO}; outline-color: {brand.accentColor};"
        >
          Write my first note →
        </button>
      {:else}
        <form class="space-y-6" onsubmit={handleSubmit} novalidate>
          {#if formError}
            <p
              role="alert"
              class="flex items-start gap-2 p-3 text-xs font-bold uppercase leading-relaxed tracking-[0.1em]"
              style="border: 1px dashed {brand.primaryColor}; font-family: {MONO};"
            >
              <Icon name="AlertCircle" class="h-4 w-4 shrink-0" aria-hidden="true" />
              <span>{formError}</span>
            </p>
          {/if}

          <div class="space-y-2">
            <label
              for="ed-email"
              class="block text-xs font-bold uppercase tracking-[0.2em]"
              style="font-family: {MONO};">01 / Email</label
            >
            <input
              id="ed-email"
              type="email"
              autocomplete="email"
              placeholder="you@example.com"
              bind:value={email}
              onfocus={() => (focusedField = "email")}
              onblur={() => (focusedField = "")}
              aria-invalid={emailError ? "true" : undefined}
              aria-describedby={emailError ? "ed-email-error" : undefined}
              class="w-full px-3 text-sm outline-none"
              style={fieldStyle("email")}
            />
            {#if emailError}
              <p
                id="ed-email-error"
                class="flex items-start gap-2 text-xs font-bold uppercase tracking-[0.1em]"
                style="font-family: {MONO};"
              >
                <Icon name="AlertCircle" class="h-4 w-4 shrink-0" aria-hidden="true" />
                <span>{emailError}</span>
              </p>
            {/if}
          </div>

          <div class="space-y-2">
            <label
              for="ed-password"
              class="block text-xs font-bold uppercase tracking-[0.2em]"
              style="font-family: {MONO};">02 / Password</label
            >
            <input
              id="ed-password"
              type="password"
              autocomplete="new-password"
              bind:value={password}
              onfocus={() => (focusedField = "password")}
              onblur={() => (focusedField = "")}
              aria-invalid={passwordError ? "true" : undefined}
              aria-describedby={passwordError
                ? "ed-password-error ed-password-hint"
                : "ed-password-hint"}
              class="w-full px-3 text-sm outline-none"
              style={fieldStyle("password")}
            />
            <p
              id="ed-password-hint"
              class="text-xs uppercase tracking-[0.1em]"
              style="font-family: {MONO}; color: {brand.neutralColor}; font-variant-numeric: tabular-nums;"
            >
              {MIN_PASSWORD} characters minimum
            </p>
            {#if passwordError}
              <p
                id="ed-password-error"
                class="flex items-start gap-2 text-xs font-bold uppercase tracking-[0.1em]"
                style="font-family: {MONO}; font-variant-numeric: tabular-nums;"
              >
                <Icon name="AlertCircle" class="h-4 w-4 shrink-0" aria-hidden="true" />
                <span>{passwordError}</span>
              </p>
            {/if}
          </div>

          <button
            type="submit"
            disabled={submitting}
            class="h-14 w-full text-sm font-bold uppercase tracking-[0.25em] transition-transform active:translate-x-1 active:translate-y-1 disabled:opacity-70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4"
            style="background-color: {brand.primaryColor}; color: {brand.backgroundColor}; border: {thick}; border-radius: {brand.radius}; box-shadow: 4px 4px 0 {brand.accentColor}; font-family: {MONO}; outline-color: {brand.accentColor};"
          >
            {submitting ? "Opening your notebook…" : "Create my account →"}
          </button>
        </form>
      {/if}
      <p class="mt-6 text-xs uppercase" style="font-family: {MONO};">
        Free, always — no card.
        <button
          type="button"
          onclick={() => navigate("sign-in")}
          class="font-bold underline underline-offset-4 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
          style="outline-color: {brand.accentColor};">Already registered? Sign in</button
        >
      </p>
    </main>
  </div>

  <footer
    class="flex justify-between pt-3 text-xs uppercase"
    style="border-top: {thick}; font-family: {MONO};"
  >
    <span>© {PRODUCT}</span>
    <span>Plain text · Private to you · No billing</span>
  </footer>
</div>
