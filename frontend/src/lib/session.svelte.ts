/**
 * The signed-in user, as the app shell knows it. Loaded once from `GET /api/auth/me` and
 * kept here so a protected route can tell, without calling the API itself, whether to
 * render or send the visitor to sign in.
 */
import { apiFetch } from "./api";

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

/** Forget the signed-in user on this client, e.g. after sign-out. */
export function clearSession(): void {
  session.user = null;
  session.checked = true;
}
