# Reusable AI Development Harness — Architecture

## Status

Early 0.x development; not a stable release. The development branch currently contains a portable semantic-review module, offline contract tests, versioned configuration validation, deterministic acceptance-report generation, and a minimal reusable acceptance workflow. These capabilities are not a claim of live model validation or complete defect detection. Check the roadmap for implementation status and commit-specific CI evidence.

## Layers

1. **Rules and policy** — maintained by the user or organization. Consumers pin immutable commits and verify expected content hashes. Missing access or hash mismatch blocks strict gates.
2. **Harness core** — portable, project-independent validation utilities, contract checks, optional AI review, reports, and reusable workflow entry points.
3. **Project adapter** — kept in each consumer repository. It owns business rules, allowed validation commands, forbidden actions, authoritative archive paths, data-sharing policy, and approval boundaries.

The core must not infer project-specific paths, run arbitrary configured commands, or override project permissions.

## Implemented contracts

### Semantic review

The current `scripts/ai_semantic_review.py` accepts a JSON input containing the task, exact diff, changed-file paths, global rules, and project instructions. It sends the minimal supplied review context to an explicitly configured OpenAI-compatible endpoint and validates the response schema and evidence quotes.

Statuses: `PASS`, `NEEDS_CHANGES`, `INCONCLUSIVE`. Configuration, transport, response-format, or evidence-validation failures block the run. Structural checks do not establish reasoning correctness or complete defect detection.

### Configuration and acceptance report

The versioned configuration contract is validation-only and does not execute configured commands. The deterministic acceptance-report builder validates a strict metadata allowlist; it does not run tests or independently authenticate caller-supplied test evidence. The CI workflow supplies commit and contract metadata, records the offline test-step outcome, uploads a report, and applies a final fail-closed job gate. See `docs/HARNESS_CONFIG_V1.md` and `docs/ACCEPTANCE_REPORT_V1.md`.

### Reusable acceptance workflow

The reusable workflow runs an explicitly supplied consumer-owned acceptance command with read-only repository permissions. Consumers must review that command and pin the workflow to a reviewed full commit SHA. A successful run proves only that the supplied command exited successfully, not that the command is adequate.

## Security

- Secrets are environment-injected; source files and reports must never contain secret values.
- Private diffs are sent to a model only under an explicit provider/data policy.
- Reports should avoid raw diffs, rule bodies, credentials, and unredacted model responses.
- Deterministic tests remain independent from the model API.
- No automatic PR merge, deployment, or project business action is part of the core.

## Versioning and consumption

Until the contract stabilizes, use 0.x. Consumer repositories should pin the Harness to a tested commit SHA or protected release tag, not a floating branch. Changes to input/output contracts require tests and migration notes. The initial 0.x release remains gated on the roadmap acceptance criteria and a review of the exact release commit.

## Implementation status

See [ROADMAP.md](ROADMAP.md) for stage checklists, remaining consumer integration work, and the limits of available CI evidence. A successful run for a pull-request head does not by itself verify a later merge commit; verification claims must name the exact tested SHA and run.
