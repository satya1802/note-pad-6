<!-- sdlc:auto:start adr -->
# ADR-0002: Use Flask 3.0 for Backend

Status: Accepted  
Date: 2026-11-06

## Context and Problem Statement

Which Backend technology does the project use? Decided in architecture v1.

## Considered Options

- Flask 3.0
- Django
- FastAPI

## Decision Outcome

Chosen option: Flask 3.0, because Approved stack. Flask 3.0 hosts the JSON API, session-based auth, ownership enforcement, and CRUD against PostgreSQL with minimal moving parts.

## Consequences

Fewer batteries-included features than Django (auth, admin) mean those are assembled from small libraries, which suits this lightweight scope.
<!-- sdlc:auto:end adr -->