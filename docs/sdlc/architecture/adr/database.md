<!-- sdlc:auto:start adr -->
# ADR-0003: Use PostgreSQL 16 for Database

Status: Accepted  
Date: 2026-11-06

## Context and Problem Statement

Which Database technology does the project use? Decided in architecture v1.

## Considered Options

- PostgreSQL 16
- SQLite
- MySQL

## Decision Outcome

Chosen option: PostgreSQL 16, because Approved stack. Stores accounts and notes reliably and provides built-in full-text search (tsvector/GIN) for 'search across my own notes' with no extra search system.

## Consequences

Heavier than SQLite for a single-user feel, but gives managed hosting, strong indexing, and room to grow.
<!-- sdlc:auto:end adr -->