# note pad 6 — SDLC Documentation

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start overview -->
build simple note pad

**Documentation version:** v10
<!-- sdlc:auto:end overview -->

## Contents

<!-- sdlc:auto:start contents -->
| Document | State |
|---|---|
| [Requirements](requirements/README.md) | v1 approved |
| [Architecture](architecture/README.md) | 7 entries |
| [Development](development/README.md) | 7 entries |
| [Testing](testing/README.md) | 2 entries |
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
| [Changelog](CHANGELOG.md) | 10 versions |
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

- Development run only reports delivery status for US-010 and US-011; no ticket/commit status is recorded for EPIC-001..EPIC-004 themselves, US-001 through US-009, or sub-tasks US-004-T1/T2/T3, despite the run being marked 'completed'.
- No development ticket or commit reported for US-001, US-002, or US-003 -- cannot confirm these were delivered despite the overall run being marked completed.
- No development ticket or commit reported for US-004 (or its sub-tasks), US-005, US-006, US-007, US-008, or US-009 -- cannot confirm delivery despite the run being marked completed.
- No test or deployment evidence yet confirms the privacy hardening behaves as intended in a running environment.
- No test or deployment evidence yet confirms the absence of payment prompts in a running environment.
- Discrepancy: run status says 'completed' but delivery evidence is only provided for 2 of 11 stories -- confirm whether the remaining 9 stories were actually completed and simply not reported, or genuinely not yet done.
- No commits or ticket statuses exist for US-001 through US-009 or their sub-tasks.

### Testing

- Detail does not name or categorize the 4 checks, so their scope/coverage cannot be confirmed.
- No date/timestamp given for when this check run occurred.
- AC-024 is not mapped to any of the known requirement keys (US-001 through US-011) in the provided input, so related_ids could not be set with confidence -- needs human confirmation of which user story this acceptance criterion belongs to.
- The input detail text is truncated mid-sentence ('a full browser walk (register, create/search/view/edit/delete a note,'), so the second Playwright spec and any remaining assertions in free-access.spec.ts are not fully documented.
- No date/timestamp provided for when this work was completed.

### Deployment

- No deployment recorded yet for this project.

### Maintenance

- No post-deployment/maintenance notes exist; project has not reached this phase.
<!-- sdlc:auto:end open-gaps -->
