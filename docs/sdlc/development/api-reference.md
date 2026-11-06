# API Reference

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start endpoints -->
| Method | Path | Handler | Source | Summary |
|---|---|---|---|---|
| GET | /health | health | `backend/app/__init__.py:79` | Liveness probe, and the only view here that is not a stub. |
| POST | /api/auth/login | post_api_auth_login | `backend/app/routes/api.py:45` | Authenticate email and password and start a web-managed session. |
| POST | /api/auth/logout | post_api_auth_logout | `backend/app/routes/api.py:65` | End the current session. |
| GET | /api/auth/me | get_api_auth_me | `backend/app/routes/api.py:73` | Return the current signed-in user or unauthenticated. |
| POST | /api/auth/register | post_api_auth_register | `backend/app/routes/api.py:22` | Create an account from email and password, validating format/uniqueness, then start |
| GET | /api/notes | get_api_notes | `backend/app/routes/web_frontend.py:42` | List the current user's notes ordered by created_at desc; when q is present, |
| POST | /api/notes | post_api_notes | `backend/app/routes/web_frontend.py:53` | Create a note for the current user; derive title from first body line if |
| DELETE | /api/notes/{id} | delete_api_notes_by_id | `backend/app/routes/web_frontend.py:101` | Permanently delete the user's own note. |
| GET | /api/notes/{id} | get_api_notes_by_id | `backend/app/routes/web_frontend.py:71` | Return a single note with full body and timestamps only if it belongs to the current user. |
| PUT | /api/notes/{id} | put_api_notes_by_id | `backend/app/routes/web_frontend.py:82` | Update title/body of the user's own note and set updated_at; reject if both become empty. |
<!-- sdlc:auto:end endpoints -->

<!-- sdlc:auto:start drift -->
_Code matches the designed API._
<!-- sdlc:auto:end drift -->

<!-- sdlc:auto:start source -->
Generated from commit `edfbfbf`
<!-- sdlc:auto:end source -->
