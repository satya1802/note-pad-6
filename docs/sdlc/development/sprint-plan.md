# Sprint Plan

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start sprints -->
## Sprint 1: Sprint 1

Stand up accounts (register/sign-in/sign-out) and enable creating notes, including the users and notes schema

Capacity: 20 points · Committed: 20

| Key | Type | Title | Points | Role | Depends on |
|---|---|---|---|---|---|
| US-001 | Story | Register a new account | 5 | backend-agent | — |
| US-002 | Story | Sign in to my account | 5 | backend-agent | US-001 |
| US-003 | Story | Sign out of my account | 2 | backend-agent | US-002 |
| US-004 | Story | Create a note | 8 | backend-agent | US-002 |
| ↳ US-004-T1 | Task | Add notes table migration | — | backend-agent | — |
| ↳ US-004-T2 | Task | Implement POST /api/notes endpoint | — | backend-agent | — |
| ↳ US-004-T3 | Task | Build note creation screen | — | frontend-agent | — |

## Sprint 2: Sprint 2

Complete note CRUD (view, edit, delete), the personal notes list, and text search

Capacity: 20 points · Committed: 18

| Key | Type | Title | Points | Role | Depends on |
|---|---|---|---|---|---|
| US-005 | Story | View a note | 3 | frontend-agent | US-004 |
| US-006 | Story | Edit a note | 3 | frontend-agent | US-004 |
| US-007 | Story | Delete a note | 2 | frontend-agent | US-004 |
| US-008 | Story | Browse my notes list | 5 | frontend-agent | US-004 |
| US-009 | Story | Search my notes | 5 | backend-agent | US-008 |

## Sprint 3: Sprint 3

Harden per-user note privacy across all endpoints and confirm the app is free of any payment prompts

Capacity: 20 points · Committed: 4

| Key | Type | Title | Points | Role | Depends on |
|---|---|---|---|---|---|
| US-010 | Story | Keep each user's notes private | 3 | security-agent | US-002, US-004, US-005, US-006, US-007, US-008, US-009 |
| US-011 | Story | Use the app free of charge | 1 | qa-agent | US-001, US-002, US-004 |

## Unscheduled

_Nothing unscheduled._
<!-- sdlc:auto:end sprints -->
