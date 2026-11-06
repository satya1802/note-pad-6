<!-- sdlc:auto:start adr -->
# ADR-0004: Use AWS for Cloud

Status: Accepted  
Date: 2026-11-06

## Context and Problem Statement

Which Cloud technology does the project use? Decided in architecture v1.

## Considered Options

- AWS
- Render
- Fly.io

## Decision Outcome

Chosen option: AWS, because Approved stack. Managed app hosting plus RDS PostgreSQL run the free personal app on modest resources with TLS and encryption at rest.

## Consequences

More configuration surface than a single-click PaaS, but offers managed scaling headroom if usage grows.
<!-- sdlc:auto:end adr -->