# note pad 6 — SDLC Documentation

> Maintained by QuorQ AI SDLC. Text between `sdlc:auto` markers is regenerated; anything outside them is yours and is kept.

<!-- sdlc:auto:start overview -->
build simple note pad

**Documentation version:** v3
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
| [API reference](development/api-reference.md) | 1 route |
| [Test report](testing/test-report.md) | not run yet |
| [Tests](testing/test-cases.md) | 0 tests |
| [Deployment guide](deployment/deployment-guide.md) | not deployed yet |
| [Runbook](deployment/runbook.md) | not deployed yet |
| [Release notes](deployment/release-notes.md) | 0 releases |
| [Traceability matrix](traceability-matrix.md) | 11 requirements |
| [Changelog](CHANGELOG.md) | 3 versions |
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

- No sprint start/end dates provided.
- No execution status (in-progress/done, commits, PRs, test results) provided for any backlog item -- only the approved plan and backlog assignments are known.
- Input does not explicitly map backlog items to sprints; mapping used in sprint entries below is inferred from matching sprint goal text and point totals to item titles, and should be confirmed.
- Item-to-sprint assignment is inferred from goal wording and point-total match, not explicitly stated in the input.
- No status reported on whether these items were completed within the sprint.
- Item-to-sprint assignment is inferred from goal wording, not explicitly stated in the input.
- Point total (18) does not fully match the 20-point capacity; unclear whether unlisted work fills the remainder or this is planned slack.
- No status reported on completion of these items.
- Point total (4) is far below the 20-point capacity; unclear if additional hardening work (not itemized in the input) is planned to fill this sprint.
- No acceptance criteria, design, or implementation detail provided beyond story titles, points, and assigned role.
- No completion status reported for any child story.
- Task-level point estimates not provided for US-004-T1/T2/T3.
- No completion status, code artifacts, or test results reported for any item in this epic.
- No completion status reported for either story.
- No detail on search implementation (e.g. scope, indexing, match behavior) beyond the story title.
- No completion status, security review findings, or QA test results reported despite security-agent and qa-agent role assignments.
- No detail on what 'per-user privacy across all endpoints' or 'free of any payment prompts' specifically entails beyond the Sprint 3 goal statement.

### Testing

- Testing phase has not started; no test plan, execution, or results exist to document.

### Deployment

- No deployment recorded yet for this project.

### Maintenance

- No post-deployment/maintenance notes exist; project has not reached this phase.
<!-- sdlc:auto:end open-gaps -->
