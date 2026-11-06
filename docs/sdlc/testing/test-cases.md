# Tests

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start summary -->
63 tests · Passed 54 · Failed 0 · Skipped 0 · Not run 9

Acceptance criteria covered: 21/24 · passing: 14/24
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
| AC-017 | Notes > [AC-017] shows notes in the order the API returned them, without re-sorting client-side | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| AC-018 | Notes > [AC-018] with no notes at all shows an empty-state message inviting the first note | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| AC-019 | Notes > [AC-019] typing in the search box queries GET /api/notes?q=<text> debounced and shows only what the API returns | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| AC-020 | Notes > [AC-020] a search with no matches shows a 'no results' message distinct from the empty state | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| — | Notes > [AC] redirects to sign-in on a 401 from GET /api/notes | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| — | Notes > [AC] redirects to sign-in on a 401 returned from a search request | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| — | Notes > the seeded sample notes and the offline toggle are gone | Unit | Passed | `frontend/src/screens/Notes.test.ts` |
| AC-008 | test_ac008_create_and_list_notes_scoped_to_session_user | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-008 | test_ac008_newest_first_and_other_users_never_returned | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-009 | test_ac009_blank_title_derives_from_first_body_line | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-010 | test_ac010_rejects_note_with_no_title_and_no_body | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-011 | test_ac011_get_note_returns_full_shape_for_owner | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-012 | test_ac012_get_put_delete_require_session | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-012 | test_ac012_non_owned_note_rejected_without_leaking_content | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-013 | test_ac013_put_persists_changes_and_updates_timestamp | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-014 | test_ac014_put_with_blank_title_and_body_returns_422_and_persists_nothing | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-015 | test_ac015_delete_removes_note_permanently | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-017 | test_ac017_list_orders_by_updated_at_desc | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-018 | test_ac018_empty_list_returns_200_empty_array | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-019 | test_ac019_search_matches_title_or_body_case_insensitively | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-020 | test_ac020_search_no_matches_returns_empty_array | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-021 | test_ac021_search_never_returns_other_users_notes | Integration | Passed | `backend/tests/integration/test_notes.py` |
| — | test_ac_blank_q_behaves_as_unfiltered_list | Integration | Passed | `backend/tests/integration/test_notes.py` |
| — | test_ac_get_notes_requires_session | Integration | Passed | `backend/tests/integration/test_notes.py` |
| — | test_ac_post_notes_requires_session | Integration | Passed | `backend/tests/integration/test_notes.py` |
| AC-008 | [AC-008] creating a note with a title and body shows it at the top of the list | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| AC-009 | [AC-009] creating a note with body only derives the title from the first line | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| AC-010 | [AC-010] attempting an empty save shows a prompt to enter content | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| AC-017 | [AC-017] notes appear newest-updated first, each with a title and timestamps, at a mobile viewport | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| AC-018 | [AC-018] a brand-new account sees the empty-state invitation | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| AC-019, AC-020 | [AC-019][AC-020] searching a word filters the list; a nonsense query shows the no-results message | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| — | [AC-sign-in] signing in with a registered account reaches the notes list | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |
| — | [NFR-004] the notes list renders without horizontal overflow at mobile and desktop widths | E2E | Not run yet | `frontend/e2e/notes.spec.ts` |

## Sprint 2

### US-005: View a note

| Criteria | Test | Level | Result | File |
|---|---|---|---|---|
| AC-011 | Note > [AC-011] loads the note by id from GET /api/notes/{id} and shows title, body and timestamps | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-011 | Note > [AC-011] no seeded sample data remains | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-012 | Note > [AC-012] a 401 clears the session and routes to sign-in | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-012 | Note > [AC-012] a 403 renders an access-denied state with no note content | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-012 | Note > [AC-012] a 404 renders an access-denied state with no note content | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-013 | Note > [AC-013] editing and saving issues PUT /api/notes/{id} and shows the new values and updated timestamp | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-014 | Note > [AC-014] saving with both title and body empty shows the backend's message | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-015 | Note > [AC-015] confirming delete calls DELETE /api/notes/{id} and returns to the notes list | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-016 | Note > [AC-016] cancelling the confirmation with Escape leaves the note unchanged and still displayed | Unit | Passed | `frontend/src/screens/Note.test.ts` |
| AC-016 | Note > [AC-016] cancelling the confirmation with the button leaves the note unchanged and still displayed | Unit | Passed | `frontend/src/screens/Note.test.ts` |

## Project setup

| Criteria | Test | Level | Result | File |
|---|---|---|---|---|
| — | test_every_generated_route_is_registered | Unit | Passed | `backend/tests/test_health.py` |
| — | test_health_reports_ok | Unit | Passed | `backend/tests/test_health.py` |
| — | the app loads | E2E | Not run yet | `frontend/e2e/example.spec.ts` |
<!-- sdlc:auto:end tests -->
