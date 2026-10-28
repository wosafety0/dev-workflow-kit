# Reusable AI Development Harness — Architecture

## Status

Initial implementation proposal, not a stable release. The repository currently contains the first portable semantic-review module and offline contract tests; broader orchestration and configuration support remain roadmap items.

## Layers

1. **Rules and policy** — maintained by the user or organization. Consumers pin immutable commits and verify expected content hashes. Missing access or hash mismatch blocks strict gates.
2. **Harness core** — portable, project-independent validation utilities, contract checks, optional AI review, reports, and reusable workflow entry points.
3. **Project adapter** — kept in each consumer repository. It owns business rules, allowed validation commands, forbidden actions, authoritative archive paths, data-sharing policy, and approval boundaries.

The core must not infer project-specific paths, run arbitrary configured commands, or override project permissions.

## Semantic review contract

The current `scripts/ai_semantic_review.py` accepts a JSON input containing the task, exact diff, changed-file paths, global rules, and project instructions. It sends the minimal supplied review context to an explicitly configured OpenAI-compatible endpoint and validates the response schema and evidence quotes.

Statuses: `PASS`, `NEEDS_CHANGES`, `INCONCLUSIVE`. Configuration, transport, response-format, or evidence-validation failures block the run. Structural checks do not establish reasoning correctness or complete defect detection.

## Security

- Secrets are environment-injected; source files and reports must never contain secret values.
- Private diffs are sent to a model only under an explicit provider/data policy.
- Reports should avoid raw diffs, rule bodies, credentials, and unredacted model responses.
- Deterministic tests remain independent from the model API.
- No automatic PR merge, deployment, or project business action is part of the core.

## Versioning and consumption

Until the contract stabilizes, use 0.x. Consumer repositories should pin the Harness to a tested commit SHA or protected release tag, not a floating branch. Changes to input/output contracts require tests and migration notes.

## Implementation stages

See [ROADMAP.md](ROADMAP.md). The current increment is limited to moving the reviewed semantic-review prototype and its offline tests into this repository. No release is made until independent CI, failure-path tests, configuration validation, and consumer integration are verified.
