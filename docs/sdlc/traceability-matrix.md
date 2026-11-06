# Traceability Matrix

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start legend -->
Built from recorded links, not written by a model: requirement key → plan item (`source_stable_key`) → development ticket (`stable_key`) → the ticket's test steps → the last live deployment that started after the work finished. **AC tests** counts the story's acceptance criteria that have a test case, and those whose test cases all passed in the latest finished E2E run.
<!-- sdlc:auto:end legend -->

<!-- sdlc:auto:start matrix -->
| Requirement | Epic | Title | Plan items | Sprint | Design | Code | Commits | Ticket | Tests | AC tests | Deployed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US-001 | EPIC-001 | Register a new account | US-001 | 1 | POST /api/auth/register, api_backend, database, users, web_frontend | backend/app/__init__.py, backend/app/routes/api.py, backend/app/services/__init__.py, backend/app/services/auth_service.py, backend/tests/integration/__init__.py +10 more | d98c00a | delivered | not run | 3/3 tested · 3/3 passing | — |
| US-002 | EPIC-001 | Sign in to my account | US-002 | 1 | GET /api/auth/me, POST /api/auth/login, api_backend, users, web_frontend | — | d98c00a | delivered | not run | 2/2 tested · 2/2 passing | — |
| US-003 | EPIC-001 | Sign out of my account | US-003 | 1 | POST /api/auth/logout, api_backend, users, web_frontend | — | d98c00a | delivered | not run | 2/2 tested · 2/2 passing | — |
| US-004 | EPIC-002 | Create a note | US-004, US-004-T1, US-004-T2, US-004-T3 | 1 | POST /api/notes, api_backend, database, notes, web_frontend | backend/app/routes/web_frontend.py, backend/app/services/notes_service.py, backend/tests/integration/test_notes.py, frontend/e2e/notes.spec.ts, frontend/src/screens/Notes.svelte +1 more | 862860f | delivered | not run | 3/3 tested · 0/3 passing | — |
| US-005 | EPIC-002 | View a note | US-005 | 2 | GET /api/notes/{id}, api_backend, notes, web_frontend | backend/app/routes/web_frontend.py, backend/app/services/notes_service.py, backend/tests/integration/test_notes.py, frontend/src/App.svelte, frontend/src/lib/router.svelte.ts +3 more | 1aff12a | delivered | not run | 2/2 tested · 2/2 passing | — |
| US-006 | EPIC-002 | Edit a note | US-006 | 2 | PUT /api/notes/{id}, api_backend, notes, web_frontend | — | 1aff12a | delivered | not run | 2/2 tested · 2/2 passing | — |
| US-007 | EPIC-002 | Delete a note | US-007 | 2 | DELETE /api/notes/{id}, api_backend, notes, web_frontend | — | 1aff12a | delivered | not run | 2/2 tested · 2/2 passing | — |
| US-008 | EPIC-003 | Browse my notes list | US-008 | 2 | GET /api/notes, api_backend, notes, web_frontend | backend/app/routes/web_frontend.py, backend/app/services/notes_service.py, backend/tests/integration/test_notes.py, frontend/e2e/notes.spec.ts, frontend/src/screens/Notes.svelte +1 more | 1aff12a | delivered | not run | 2/2 tested · 0/2 passing | — |
| US-009 | EPIC-003 | Search my notes | US-009 | 2 | GET /api/notes, api_backend, database, notes, web_frontend | — | 1aff12a | delivered | not run | 3/3 tested · 1/3 passing | — |
| US-010 | EPIC-004 | Keep each user's notes private | US-010 | 3 | DELETE /api/notes/{id}, GET /api/notes, GET /api/notes/{id}, PUT /api/notes/{id}, api_backend, database, notes, users | backend/tests/integration/test_privacy.py, frontend/e2e/privacy.spec.ts | f5f5ab9 | delivered | not run | 2/2 tested · 0/2 passing | — |
| US-011 | EPIC-004 | Use the app free of charge | US-011 | 3 | api_backend, web_frontend | backend/tests/test_free_access.py, frontend/e2e/free-access.spec.ts, frontend/src/screens/Note.test.ts, frontend/src/screens/Notes.test.ts, frontend/src/screens/Register.test.ts +1 more | fc11232 | delivered | succeeded | 1/1 tested · 0/1 passing | — |
<!-- sdlc:auto:end matrix -->
