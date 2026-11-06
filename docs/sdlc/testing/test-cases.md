# Tests

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start summary -->
33 tests · Passed 27 · Failed 0 · Skipped 0 · Not run 6

Acceptance criteria covered: 10/24 · passing: 7/24
<!-- sdlc:auto:end summary -->

<!-- sdlc:auto:start tests -->
## Sprint 1

### US-001: Register a new account

| Criteria | Test | Level | Result | File |
|---|---|---|---|---|
| AC-007 | App > [AC-007] redirects to sign-in when /api/auth/me reports no active session | Unit | Passed | `frontend/src/App.test.ts` |
| AC-007 | App > [AC-007] renders a protected screen inside the app shell once a session is confirmed | Unit | Passed | `frontend/src/App.test.ts` |
| AC-001 | Register > [AC-001] submits to the register endpoint and lands on the notes list on success | Unit | Passed | `frontend/src/screens/Register.test.ts` |
| AC-002 | Register > [AC-002] shows an email-already-in-use message on a 409 and has no hardcoded email list | Unit | Passed | `frontend/src/screens/Register.test.ts` |
| AC-003 | Register > [AC-003] shows the field-level 422 error returned by the server | Unit | Passed | `frontend/src/screens/Register.test.ts` |
| AC-004 | SignIn > [AC-004] submits to the login endpoint and navigates to the notes list on success | Unit | Passed | `frontend/src/screens/SignIn.test.ts` |
| AC-005 | SignIn > [AC-005, NFR-002] shows one generic error for wrong credentials, naming no field, with no demo-account shortcut | Unit | Passed | `frontend/src/screens/SignIn.test.ts` |
| AC-001 | test_ac001_register_creates_account_and_active_session | Integration | Passed | `backend/tests/integration/test_auth.py` |
| AC-002 | test_ac002_register_duplicate_email_returns_409 | Integration | Passed | `backend/tests/integration/test_auth.py` |
| AC-003 | test_ac003_register_invalid_email_and_short_password_returns_422 | Integration | Passed | `backend/tests/integration/test_auth.py` |
| AC-004 | test_ac004_login_with_correct_credentials_starts_session | Integration | Passed | `backend/tests/integration/test_auth.py` |
| AC-005 | test_ac005_login_wrong_credentials_returns_single_generic_401 | Integration | Passed | `backend/tests/integration/test_auth.py` |
| AC-006 | test_ac006_logout_ends_session | Integration | Passed | `backend/tests/integration/test_auth.py` |
| AC-007 | test_ac007_me_returns_401_without_active_session | Integration | Passed | `backend/tests/integration/test_auth.py` |

### US-004: Create a note

| Criteria | Test | Level | Result | File |
|---|---|---|---|---|
| AC-008 | Notes > [AC-008] loads the list from GET /api/notes on mount and shows a saved note's stored timestamps after POST | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| AC-009 | Notes > [AC-009] saving with a blank title shows the title the API derived from the first body line | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| AC-010 | Notes > [AC-010] a 422 for no title and no body prompts the user with the API's message | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| — | Notes > [AC] redirects to sign-in on a 401 from GET /api/notes | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| — | Notes > the seeded sample notes and the offline toggle are gone | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| AC-008 | test_ac008_create_and_list_notes_scoped_to_session_user | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-008 | test_ac008_newest_first_and_other_users_never_returned | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-009 | test_ac009_blank_title_derives_from_first_body_line | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-010 | test_ac010_rejects_note_with_no_title_and_no_body | Integration | Passed | `backend/tests/integration/test_notes.py` |
| — | test_ac_get_notes_requires_session | Integration | Passed | `backend/tests/integration/test_notes.py` |
| — | test_ac_post_notes_requires_session | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-008 | [AC-008] creating a note with a title and body shows it at the top of the list | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| AC-009 | [AC-009] creating a note with body only derives the title from the first line | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| AC-010 | [AC-010] attempting an empty save shows a prompt to enter content | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| — | [AC-sign-in] signing in with a registered account reaches the notes list | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| — | [NFR-004] the notes list renders without horizontal overflow at mobile and desktop widths | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |

## Project setup

| Criteria | Test | Level | Result | File |
|---|---|---|---|---|
| — | test_every_generated_route_is_registered | Unit | Passed | `backend/tests/test_health.py` |
| — | test_health_reports_ok | Unit | Passed | `backend/tests/test_health.py` |
| — | the app loads | E2E | Not run yet | `frontend/e2e/example.spec.ts` |
<!-- sdlc:auto:end tests -->
