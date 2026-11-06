# note pad 6 — SDLC Documentation

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start overview -->
build simple note pad

**Documentation version:** v8
<!-- sdlc:auto:end overview -->

## Contents

<!-- sdlc:auto:start contents -->
| Document | State |
|---|---|
| [Requirements](requirements/README.md) | v1 approved |
| [Architecture](architecture/README.md) | 7 entries |
| [Development](development/README.md) | 8 entries |
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
| [Tests](testing/test-cases.md) | 79 tests |
| [Deployment guide](deployment/deployment-guide.md) | not deployed yet |
| [Runbook](deployment/runbook.md) | not deployed yet |
| [Release notes](deployment/release-notes.md) | 0 releases |
| [Traceability matrix](traceability-matrix.md) | 11 requirements |
| [Changelog](CHANGELOG.md) | 8 versions |
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

- Input does not explicitly map individual backlog items to a specific sprint number -- sprint-to-item assignment above is inferred only from sprint goal wording, not stated directly.
- No development ticket/commit recorded for US-001, US-002, or US-003 -- delivery status unknown.
- No development ticket/commit recorded for US-004 (or its sub-tasks US-004-T1/T2/T3), US-005, US-006, or US-007 -- delivery status unknown.
- No development ticket/commit recorded for US-008 or US-009 -- delivery status unknown.
- Discrepancy: run status says 'completed' but 9 of 11 stories (US-001-US-009) and 3 sub-tasks (US-004-T1, US-004-T2, US-004-T3) have no delivery/ticket record -- unclear if they were actually built, not yet reported, or completed under untracked tickets.
- Cannot confirm whether account registration/sign-in/sign-out (US-001-003), note creation/view/edit/delete (US-004-007), or notes list/search (US-008-009) were implemented.

### Testing

- Testing phase has not started, or its records were not provided -- no test plan, test cases, execution results, or defect data available.
- Cannot trace test coverage back to requirements US-001 through US-011 due to absence of testing input.
- No QA sign-off or approval status is available for this phase.

### Deployment

- No deployment recorded yet for this project.

### Maintenance

- No post-deployment/maintenance notes exist; project has not reached this phase.
<!-- sdlc:auto:end open-gaps -->
