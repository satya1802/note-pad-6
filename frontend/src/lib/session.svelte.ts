/**
 * The signed-in user, as the app shell knows it. Loaded once from `GET /api/auth/me` and
 * kept here so a protected route can tell, without calling the API itself, whether to
 * render or send the visitor to sign in.
 */
import { apiFetch, clearSessionToken } from "./api";

export type SessionUser = { id: string; email: string };

export const session = $state<{ user: SessionUser | null; checked: boolean }>({
  user: null,
  checked: false,
});

/** Ask the API who, if anyone, is signed in. Never throws. */
export async function refreshSession(): Promise<void> {
  try {
    const data = await apiFetch<{ user: SessionUser }>("/api/auth/me");
    session.user = data.user;
  } catch {
    session.user = null;
  } finally {
    session.checked = true;
  }
}

/**
 * Forget the signed-in user on this client, e.g. after sign-out or a 401 from the API.
 * Also drops the stored bearer token: without this, `apiFetch` would keep sending a
 * token for an account the UI claims to have left, and a later `refreshSession()` would
 * silently sign the visitor back in.
 */
export function clearSession(): void {
  session.user = null;
  session.checked = true;
  clearSessionToken();
}
