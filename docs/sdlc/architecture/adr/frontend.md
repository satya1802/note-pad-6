<!-- sdlc:auto:start adr -->
# ADR-0001: Use Svelte 5 for Frontend

Status: Accepted  
Date: 2026-11-06

## Context and Problem Statement

Which Frontend technology does the project use? Decided in architecture v1.

## Considered Options

- Svelte 5
- React
- Vue

## Decision Outcome

Chosen option: Svelte 5, because Approved stack. Svelte 5 builds a small, fast responsive SPA for the notes list, editor, and search, satisfying the responsive-web requirement (NFR-004).

## Consequences

Smaller ecosystem than React, but the UI surface here is tiny so that is not a constraint.
<!-- sdlc:auto:end adr -->