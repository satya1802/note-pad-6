# Development

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start narrative -->
### DEV-PLAN-001 · approved · source: plan

Development plan version 1, approved, organizes the project into 3 sprints of capacity 20 each, spanning 4 epics and 11 user stories.

Plan status: approved, version 1. Sprint 1 goal: stand up accounts (register/sign-in/sign-out) and enable creating notes, including users and notes schema. Sprint 2 goal: complete note CRUD (view, edit, delete), the personal notes list, and text search. Sprint 3 goal: harden per-user note privacy across all endpoints and confirm the app is free of any payment prompts. Each sprint has capacity 20 points.

**Related:** US-001, US-002, US-003, US-004, US-005, US-006, US-007, US-008, US-009, US-010, US-011

- ⚠ Input does not explicitly map individual backlog items to a specific sprint number -- sprint-to-item assignment above is inferred only from sprint goal wording, not stated directly.

### DEV-EPIC-001 · draft · source: plan:EPIC-001

Epic covering account registration and authentication: register, sign in, sign out.

EPIC-001 'Account Registration and Authentication' (role unassigned) contains: US-001 Register a new account (5 pts, backend-agent); US-002 Sign in to my account (5 pts, backend-agent); US-003 Sign out of my account (2 pts, backend-agent). Aligns with Sprint 1 goal of standing up accounts.

**Related:** US-001, US-002, US-003

- ⚠ No development ticket/commit recorded for US-001, US-002, or US-003 -- delivery status unknown.

### DEV-EPIC-002 · draft · source: plan:EPIC-002

Epic covering note creation, viewing, editing, and deletion.

EPIC-002 'Note Creation, Editing, Viewing and Deletion' (role unassigned) contains: US-004 Create a note (8 pts, backend-agent), broken into US-004-T1 Add notes table migration (backend-agent), US-004-T2 Implement POST /api/notes endpoint (backend-agent), and US-004-T3 Build note creation screen (frontend-agent); US-005 View a note (3 pts, frontend-agent); US-006 Edit a note (3 pts, frontend-agent); US-007 Delete a note (2 pts, frontend-agent). Aligns with Sprint 1 (creation) and Sprint 2 (view/edit/delete) goals.

**Related:** US-004, US-005, US-006, US-007

- ⚠ No development ticket/commit recorded for US-004 (or its sub-tasks US-004-T1/T2/T3), US-005, US-006, or US-007 -- delivery status unknown.

### DEV-EPIC-003 · draft · source: plan:EPIC-003

Epic covering the personal notes list and text search.

EPIC-003 'Notes List and Search' (role unassigned) contains: US-008 Browse my notes list (5 pts, frontend-agent); US-009 Search my notes (5 pts, backend-agent). Aligns with Sprint 2 goal of completing the personal notes list and text search.

**Related:** US-008, US-009

- ⚠ No development ticket/commit recorded for US-008 or US-009 -- delivery status unknown.

### DEV-EPIC-004 · draft · source: plan:EPIC-004

Epic covering private per-user note storage and free access to the app.

EPIC-004 'Private Per-User Storage and Free Access' (role unassigned) contains: US-010 Keep each user's notes private (3 pts, security-agent); US-011 Use the app free of charge (1 pt, qa-agent). Aligns with Sprint 3 goal of hardening per-user note privacy and confirming the app is free of payment prompts.

**Related:** US-010, US-011

### DEV-TICKET-US-010 · approved · source: dev:US-010

Ticket for keeping each user's notes private was delivered.

Ticket US-010 'Keep each user's notes private' - status: delivered, commit f5f5ab9300cedecab56c646377603cda06163265.

**Related:** US-010, EPIC-004

### DEV-TICKET-US-011 · approved · source: dev:US-011

Ticket for free-of-charge app usage was delivered.

Ticket US-011 'Use the app free of charge' - status: delivered, commit fc11232e8c204a3042c07e8ccd83c8e680f2590b.

**Related:** US-011, EPIC-004

### DEV-GAPS-001 · draft · source: dev:run-status

Development run is marked 'completed', but only 2 of the 11 planned stories have recorded ticket evidence.

The development run status is reported as 'completed', yet only tickets for US-010 and US-011 (both from Sprint 3's epic) are listed with status and commit. No ticket records were provided for US-001 through US-009 or for sub-tasks US-004-T1, US-004-T2, US-004-T3, all of which were planned in Sprints 1 and 2.

**Related:** US-001, US-002, US-003, US-004, US-005, US-006, US-007, US-008, US-009

- ⚠ Discrepancy: run status says 'completed' but 9 of 11 stories (US-001-US-009) and 3 sub-tasks (US-004-T1, US-004-T2, US-004-T3) have no delivery/ticket record -- unclear if they were actually built, not yet reported, or completed under untracked tickets.
- ⚠ Cannot confirm whether account registration/sign-in/sign-out (US-001-003), note creation/view/edit/delete (US-004-007), or notes list/search (US-008-009) were implemented.
<!-- sdlc:auto:end narrative -->
