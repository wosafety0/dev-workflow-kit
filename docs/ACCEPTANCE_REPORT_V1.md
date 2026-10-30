# Redacted Acceptance Report (v1)

Status: deterministic metadata validator and report builder; not a test runner. Schema v1 remains the compatibility-mode format; the opt-in Git-bound runner emits schema v2.

## Required input (schema v1)

For compatibility-mode schema v1, the caller supplies exactly four fields:

- `commit_sha`: full 40-character Git commit SHA.
- `rules_pin`: lowercase SHA-256 content pin in the form `sha256:` followed by exactly 64 lowercase hexadecimal characters.
- `tool_version`: non-empty, trimmed toolkit version.
- `tests`: a non-empty object mapping test names to `passed`, `failed`, `skipped`, or `not_run`.

Example input:

```json
{
  "commit_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "rules_pin": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "tool_version": "dev-workflow-kit/0.1.0",
  "tests": {
    "offline-unit-tests": "passed",
    "policy-contract-tests": "passed"
  }
}
```

## CI integration

The GitHub Actions workflow supplies the actual workflow commit SHA, computes a SHA-256 content pin for `docs/STABLE_ACCEPTANCE_CONTRACT.md`, and identifies the tested toolkit revision as `dev-workflow-kit@<commit SHA>`. It records the offline contract-test step outcome, writes `artifacts/acceptance-report.json`, and uploads that file as the `acceptance-report` artifact for 14 days.

The test step uses `continue-on-error` only so the report can still be produced when tests fail. A final gate explicitly fails the job unless the test step outcome is `success`. The report is not a replacement for the job conclusion.

## Output and fail-closed behavior

A schema-v1 report contains only `schema_version`, `commit_sha`, `rules_pin`, `tool_version`, normalized `tests`, and overall `status`. Test names are sorted for deterministic output and the commit SHA is normalized to lowercase.

Overall status is `passed` only when every declared test status is exactly `passed`. A `failed`, `skipped`, or `not_run` test produces overall `failed`. Missing or malformed required data and unknown input keys are rejected. This strict allowlist prevents arbitrary input fields—including credentials, environment dumps, and raw logs—from being copied into the report.

## Schema v2 — optional Git-bound review

When the runner is invoked with both `--review-base` and `--review-head`, it emits schema version 2 and adds exactly one top-level field, `review_provenance`, containing:

- `base_sha`, `head_sha`, and `merge_base_sha`: full Git commit SHAs.
- `diff_sha256`: lowercase SHA-256 of the exact Git diff bytes supplied to the semantic reviewer.
- `changed_files`: sorted, unique repository-relative paths derived from Git.

The runner requires the requested head to equal the clean checked-out `HEAD` and derives the merge base, diff, and changed-file list from Git; caller-provided `diff` and `changed_files` are not trusted in this mode. The report formatter validates the provenance fields' structure but does not independently recompute Git ancestry or the diff digest. Without both strict-mode flags, schema v1 and caller-supplied review input remain supported.


## Boundaries

- The workflow supplies the current commit SHA, the content hash of the acceptance contract, the toolkit revision label, and the test step outcome. These values are traceable but do not constitute a cryptographic attestation of every runtime action.
- The module does not run tests, inspect repository state, or authenticate arbitrary caller-supplied test evidence.
- The report reflects the offline contract-test step only; it does not claim live model validation or complete defect detection.
- Never pass secrets, raw logs, or environment dumps as report metadata. Do not use this report as an authorization to write remotely or merge a pull request.
