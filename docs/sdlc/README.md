# note pad 6 — SDLC Documentation

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start overview -->
build simple note pad

**Documentation version:** v6
<!-- sdlc:auto:end overview -->

## Contents

<!-- sdlc:auto:start contents -->
| Document | State |
|---|---|
| [Requirements](requirements/README.md) | v1 approved |
| [Architecture](architecture/README.md) | 7 entries |
| [Development](development/README.md) | 7 entries |
| [Testing](testing/README.md) | 1 entry |
| [Deployment](deployment/README.md) | 1 entry |
| [Maintenance](maintenance/README.md) | 1 entry |
| [Data model](architecture/data-model.md) | generated |
| [API (OpenAPI)](architecture/api/openapi.yaml) | generated |
| [Decisions (ADRs)](architecture/adr/README.md) | 4 decisions |
| [Sprint plan](development/sprint-plan.md) | 3 sprints |
| [Developer guide](development/developer-guide.md) | generated |
| [API reference](development/api-reference.md) | 10 routes |
| [Test report](testing/test-report.md) | not run yet |
| [Tests](testing/test-cases.md) | 63 tests |
| [Deployment guide](deployment/deployment-guide.md) | not deployed yet |
| [Runbook](deployment/runbook.md) | not deployed yet |
| [Release notes](deployment/release-notes.md) | 0 releases |
| [Traceability matrix](traceability-matrix.md) | 11 requirements |
| [Changelog](CHANGELOG.md) | 6 versions |
<!-- sdlc:auto:end contents -->

## Open gaps

<!-- sdlc:auto:start open-gaps -->
### Requirements

- Minimum password requirements (length/complexity) are not specified.
- No specific credential-handling standard (e.g. hashing algorithm) was specified.

### Architecture

- Input does not map these critical paths to specific requirement IDs (US-001..US-011), so explicit traceability links could not be made.
- Choice between Amplify/S3+CloudFront for the static site and between App Runner/Elastic Beanstalk for the API is left open (both alternatives listed without a final pick).
- NFR-004 is referenced by the architecture input but is not among the known requirement keys (US-001..US-011) provided for this project, so its traceability back to a formal requirement record could not be confirmed.

### Development

- No approver name or date recorded for the plan approval.
- No delivery status recorded for US-001 (Register a new account).
- No delivery status recorded for US-002 (Sign in to my account).
- No delivery status recorded for US-003 (Sign out of my account).
- No delivery status recorded for US-004 (Create a note) or its tasks US-004-T1, US-004-T2, US-004-T3.
- No delivery status recorded for US-010 (Keep each user's notes private) -- a privacy/security-critical story.
- No delivery status recorded for US-011 (Use the app free of charge).
- Discrepancy: overall dev run status is 'completed' but ticket coverage is only 5 of 11 planned stories -- needs confirmation of whether the remaining stories were actually built, skipped, or simply not reported.

### Testing

- No ticket ID associated with this check run, so it cannot be linked to a specific development item.
- No breakdown of what the 4 checks actually verified (e.g. unit, integration, UI) -- only an aggregate pass count was given.
- No mapping provided between these checks and any of the known requirements (US-001 through US-011), so requirement-level test coverage cannot be confirmed or documented.
- No test plan or test case documentation was supplied for this phase.

### Deployment

- No deployment recorded yet for this project.

### Maintenance

- No post-deployment/maintenance notes exist; project has not reached this phase.
<!-- sdlc:auto:end open-gaps -->
