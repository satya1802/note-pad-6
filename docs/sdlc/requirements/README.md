# Product Requirements

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start narrative -->
## Summary

### REQ-STACK · approved · source: requirements:stack

Product owner approved technology stack: Flask 3.0 backend, Svelte 5 frontend, PostgreSQL 16 database, hosted on AWS.

Stack is fixed and must not be substituted. Rationale given: AWS runs a small free personal app cheaply with room to grow and offers managed hosting plus managed PostgreSQL without server management. PostgreSQL chosen because notes/accounts/timestamps are simple structured records, per-user privacy is enforced via ownership ties, and built-in full-text search covers the in-scope 'search my own notes' need without an extra system. Delivery scope is 'lightweight'; requirements version 1. Image/file attachment to notes is explicitly out of scope.

### REQ-US-001 · approved · source: requirements:EPIC-001/US-001

New visitors can register an account with email and password to get a private note space.

Critical priority. AC-001: valid unused email + password meeting minimum requirements creates the account and signs the user in (or routes to sign-in). AC-002: already-registered email is rejected with a message that the email is in use. AC-003: invalid email format or password not meeting minimum requirements is rejected with the specific invalid field shown. Assumption stated: authentication is email/password with sessions managed by the web application; no social login, SSO, or MFA included at this scope. Standard secure handling of account data assumed (no specific regulatory requirement given).

**Related:** EPIC-001, AC-001, AC-002, AC-003, NFR-002

- ⚠ Minimum password requirements (length/complexity) are not specified.

### REQ-US-002 · approved · source: requirements:EPIC-001/US-002

Registered users can sign in with email and password to reach their private notes.

Critical priority. AC-004: correct email/password authenticates, starts a web-managed session, and lands on the notes list. AC-005: incorrect email/password combination is refused with a generic error that does not reveal which field was wrong.

**Related:** EPIC-001, AC-004, AC-005, NFR-002, NFR-003

### REQ-US-003 · approved · source: requirements:EPIC-001/US-003

Signed-in users can sign out to protect their notes on shared devices.

High priority. AC-006: choosing sign out ends the session and returns the user to the sign-in page. AC-007: after sign-out, attempting to open an authenticated page redirects to sign-in.

**Related:** EPIC-001, AC-006, AC-007, NFR-003

### REQ-US-004 · approved · source: requirements:EPIC-002/US-004

Signed-in users can create a plain-text note with title and body.

Critical priority. AC-008: saving a note with body text stores it against the account with a created timestamp and initial updated timestamp, and it appears in the notes list. AC-009: if title is left blank, the first line of the body becomes the title. AC-010: a note with no title and no body cannot be saved; the system prompts for content. Notes are plain text only -- no rich-text formatting, folders, or tags. Attaching images/files is out of scope.

**Related:** EPIC-002, AC-008, AC-009, AC-010

### REQ-US-005 · approved · source: requirements:EPIC-002/US-005

Signed-in users can open and read one of their notes in full.

Critical priority. AC-011: opening a note from the list displays its title, full body, and created/updated timestamps. AC-012: attempting to open a note belonging to another account is denied and no content is shown.

**Related:** EPIC-002, AC-011, AC-012, NFR-001

### REQ-US-006 · approved · source: requirements:EPIC-002/US-006

Signed-in users can edit the title and body of an existing note.

Critical priority. AC-013: saving a changed title or body persists the change and sets the updated timestamp to the edit time. AC-014: clearing both title and body prevents saving and prompts the user to keep some content.

**Related:** EPIC-002, AC-013, AC-014

### REQ-US-007 · approved · source: requirements:EPIC-002/US-007

Signed-in users can delete a note they no longer need, with confirmation.

High priority. AC-015: confirming deletion permanently removes the note from the account and the notes list. AC-016: cancelling the confirmation leaves the note unchanged.

**Related:** EPIC-002, AC-015, AC-016

### REQ-US-008 · approved · source: requirements:EPIC-003/US-008

Signed-in users see a personal list of all their notes, most recently updated first.

Critical priority. AC-017: the list shows only the signed-in user's own notes, each with title (or first line) and a timestamp, ordered most-recently-updated first. AC-018: a user with no notes sees an empty-state message inviting them to create their first note.

**Related:** EPIC-003, AC-017, AC-018

### REQ-US-009 · approved · source: requirements:EPIC-003/US-009

Signed-in users can search their own notes by text in title or body.

High priority. AC-019: entering a search word shows only the user's notes whose title or body contains that text. AC-020: no matches shows a clear 'no results' message. AC-021: other users' matching notes never appear in the results. Search is plain text across the signed-in user's own notes only; no folders, tags, or advanced filtering at this scope.

**Related:** EPIC-003, AC-019, AC-020, AC-021, NFR-001

### REQ-US-010 · approved · source: requirements:EPIC-004/US-010

Each user's notes are stored privately; no other user can read, edit, or delete them.

Critical priority. AC-022: when one of two users is signed in and lists, searches, views, or edits notes, only their own notes are accessible; the other user's notes are never exposed. AC-023: a request for a note is rejected if the requesting session does not own it, regardless of how the note identifier was obtained.

**Related:** EPIC-004, AC-022, AC-023, NFR-001

### REQ-US-011 · approved · source: requirements:EPIC-004/US-011

The app is free to use with no payments, billing, or subscriptions.

Medium priority. AC-024: using registration, sign-in, or any note feature never prompts for payment, billing details, or a subscription upgrade.

**Related:** EPIC-004, AC-024

### REQ-NFR-001 · approved · source: requirements:NFR-001

Privacy: notes are strictly scoped to their owning account.

Every note is tied to its creating account; a signed-in user can only list, view, search, edit, or delete their own notes. Requests for notes not owned by the current session are rejected regardless of how the identifier was obtained.

**Related:** US-010, US-005, US-009

### REQ-NFR-002 · approved · source: requirements:NFR-002

Security: account credentials handled with standard secure practices; generic failed sign-in error.

Account email and password data is handled using standard secure practices. A failed sign-in shows a generic error that does not reveal whether the email or password was wrong.

**Related:** US-001, US-002

- ⚠ No specific credential-handling standard (e.g. hashing algorithm) was specified.

### REQ-NFR-003 · approved · source: requirements:NFR-003

Session control: authentication required for notes access; sign-out ends session and protects pages.

Access to notes requires an active web-managed session. Signing out ends the session, and any attempt to open an authenticated page afterward redirects to the sign-in page.

**Related:** US-002, US-003

### REQ-NFR-004 · approved · source: requirements:NFR-004

Compatibility: delivered as a responsive web app across screen sizes, no native app.

The product is a responsive web application that works in a browser across different screen sizes. No native mobile or desktop app is provided.

### REQ-NFR-005 · approved · source: requirements:NFR-005

Performance: accepted risk -- sized for modest personal use, no specific targets.

The app is sized for individual personal use at modest scale. No specific performance, throughput, or response-time target was set at this scope. Marked as an accepted risk by the requirements input.

### REQ-NFR-006 · approved · source: requirements:NFR-006

Compliance: accepted risk -- no specific regulatory requirement identified.

No specific regulatory or regional compliance requirement was identified for this app; only standard secure handling of account data applies. Marked as an accepted risk by the requirements input. No industry or domain compliance skill was supplied for this project, so no regulation-specific traceability could be performed.
<!-- sdlc:auto:end narrative -->

<!-- sdlc:auto:start summary -->
**Requirements version:** v1  
**Delivery scope:** lightweight  
**Approved:** 2026-11-06

**Capabilities in scope:** Account registration and sign-in, Create a note, Edit a note, View a note, Delete a note, Personal notes list, Text search across your own notes, Private per-user note storage with created/updated timestamps, Free to use with no payments or billing

**Approved technology stack:**

| Layer | Choice | Rationale |
|---|---|---|
| backend | Flask | — |
| cloud | AWS | AWS is the platform target and comfortably runs a small, free personal web app on modest, inexpensive resources, with room to grow if the user base ever expands. It gives you managed hosting for the app and a managed PostgreSQL database without having to run servers yourself. |
| database | PostgreSQL | Notes, accounts and timestamps are simple structured records, and strict per-user privacy is enforced naturally by tying every note to its owner's account. PostgreSQL stores this reliably and its built-in full-text search covers your 'simple text search across my own notes' without adding any extra system, keeping the whole app in one dependable store. |
| frontend | Svelte | — |
<!-- sdlc:auto:end summary -->

<!-- sdlc:auto:start epics -->
## EPIC-001: Account Registration and Authentication

Individuals can create a personal account and sign in to access only their own notes. Assumption: authentication is email/password with sessions managed by the web application. No social login, SSO, or multi-factor authentication was discussed and none is included at this scope. Account data is handled with standard secure practices (no specific regulatory requirement was given).

### US-001: Register a new account

**Priority:** critical

> As a new visitor, I want to register for an account using my email address and a password, so that I can have my own private space to keep notes.

| ID | Given | When | Then |
|---|---|---|---|
| AC-001 | I am on the registration page and not signed in | I submit a valid, unused email address and a password that meets the minimum requirements | my account is created and I am signed in (or directed to sign in) |
| AC-002 | I am on the registration page | I submit an email address that is already registered | registration is rejected and I am told the email is already in use |
| AC-003 | I am on the registration page | I submit an invalid email format or a password that does not meet the minimum requirements | registration is rejected and I am shown which field is invalid |

### US-002: Sign in to my account

**Priority:** critical

> As a registered user, I want to sign in with my email and password, so that I can access my own private notes.

| ID | Given | When | Then |
|---|---|---|---|
| AC-004 | I have a registered account and am on the sign-in page | I submit my correct email and password | I am authenticated, a web-managed session is started, and I am taken to my notes list |
| AC-005 | I am on the sign-in page | I submit an email/password combination that is incorrect | sign-in is refused and I am shown a generic error without revealing which field was wrong |

### US-003: Sign out of my account

**Priority:** high

> As a signed-in user, I want to sign out, so that my notes are not accessible to anyone else using the same device.

| ID | Given | When | Then |
|---|---|---|---|
| AC-006 | I am signed in with an active session | I choose to sign out | my session is ended and I am returned to the sign-in page |
| AC-007 | my session has ended | I try to open a page that requires authentication | I am redirected to the sign-in page |

## EPIC-002: Note Creation, Editing, Viewing and Deletion

Users have full CRUD over their own plain-text notes. Assumption: each note has a title (or first line) and body text, with created and updated timestamps. Notes are plain text only — no rich-text formatting, folders, or tags. Attaching images or files to notes is explicitly out of scope.

### US-004: Create a note

**Priority:** critical

> As a signed-in user, I want to create a new plain-text note with a title and body, so that I can capture information I want to keep.

| ID | Given | When | Then |
|---|---|---|---|
| AC-008 | I am signed in | I create a note and save it with body text | the note is stored against my account with a created timestamp and an initial updated timestamp, and it appears in my notes list |
| AC-009 | I am creating a note and leave the title blank | I save the note | the first line of the body is used as the note's title |
| AC-010 | I am creating a note | I save it with no title and no body text | the system prevents saving an empty note and prompts me to enter content |

### US-005: View a note

**Priority:** critical

> As a signed-in user, I want to open and read a note, so that I can see its full content.

| ID | Given | When | Then |
|---|---|---|---|
| AC-011 | I have at least one note | I open a note from my notes list | its title, full body text, and created/updated timestamps are displayed |
| AC-012 | I am signed in | I attempt to open a note that does not belong to my account | access is denied and the note content is not shown |

### US-006: Edit a note

**Priority:** critical

> As a signed-in user, I want to edit the title and body of an existing note, so that I can keep its content up to date.

| ID | Given | When | Then |
|---|---|---|---|
| AC-013 | I am viewing one of my notes | I change its title or body and save | the changes are persisted and the note's updated timestamp is set to the time of the edit |
| AC-014 | I am editing a note | I clear all content so both title and body are empty and attempt to save | saving is prevented and I am prompted to keep some content |

### US-007: Delete a note

**Priority:** high

> As a signed-in user, I want to delete a note I no longer need, so that my notes list stays relevant.

| ID | Given | When | Then |
|---|---|---|---|
| AC-015 | I am viewing or selecting one of my notes | I choose to delete it and confirm | the note is permanently removed from my account and no longer appears in my notes list |
| AC-016 | I choose to delete a note | I cancel the confirmation | the note is retained unchanged |

## EPIC-003: Notes List and Search

Users find their notes through a personal notes list and a simple text search. Assumption: search is a plain text search across only the signed-in user's own notes (matching title and body). No folders, tags, or advanced filtering are included at this scope.

### US-008: Browse my notes list

**Priority:** critical

> As a signed-in user, I want to see a list of all my notes, so that I can find and open the one I need.

| ID | Given | When | Then |
|---|---|---|---|
| AC-017 | I am signed in and have one or more notes | I open my notes list | I see only my own notes, each showing its title (or first line) and a timestamp, ordered with the most recently updated first |
| AC-018 | I am signed in and have no notes yet | I open my notes list | I see an empty-state message inviting me to create my first note |

### US-009: Search my notes

**Priority:** high

> As a signed-in user, I want to search my notes by text, so that I can quickly find a note without scrolling the whole list.

| ID | Given | When | Then |
|---|---|---|---|
| AC-019 | I am signed in and have notes containing a given word | I enter that word in the search | the list shows only my notes whose title or body contains the search text |
| AC-020 | I perform a search | no note of mine matches the search text | I am shown a clear 'no results' message |
| AC-021 | another user has notes matching my search text | I run a search | their notes never appear in my results |

## EPIC-004: Private Per-User Storage and Free Access

Notes are stored securely so that one user can never see another user's notes, and the application is free to use. Assumption: the app is free with no payments, billing, or subscription tiers. Standard secure handling of account data is assumed; no specific regulatory requirement was given. Delivered as a responsive web application (no native mobile/desktop app).

### US-010: Keep each user's notes private

**Priority:** critical

> As a user, I want my notes to be stored privately against my account, so that no other user can read, edit, or delete my notes.

| ID | Given | When | Then |
|---|---|---|---|
| AC-022 | two different users each have their own notes | one user is signed in and lists, searches, views, or edits notes | only that user's own notes are accessible and the other user's notes are never exposed |
| AC-023 | a request is made for a note | the requesting session does not own that note | the request is rejected regardless of how the note identifier was obtained |

### US-011: Use the app free of charge

**Priority:** medium

> As a user, I want to use all note-taking features without any payment, so that I can take notes without cost or subscription.

| ID | Given | When | Then |
|---|---|---|---|
| AC-024 | I have a registered account | I use registration, sign-in, and any note feature | I am never asked for payment, billing details, or to upgrade a subscription |
<!-- sdlc:auto:end epics -->
