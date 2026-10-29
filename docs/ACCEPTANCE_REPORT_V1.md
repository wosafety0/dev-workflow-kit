# Redacted Acceptance Report (v1)

Status: deterministic metadata validator and report builder; not a test runner.

## Required input

The caller supplies exactly four fields:

- `commit_sha`: full 40-character Git commit SHA.
- `rules_pin`: non-empty, trimmed identifier for the reviewed rules revision.
- `tool_version`: non-empty, trimmed toolkit version.
- `tests`: a non-empty object mapping test names to `passed`, `failed`, `skipped`, or `not_run`.

Example input:

```json
{
  "commit_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "rules_pin": "sha256:rules-v1",
  "tool_version": "dev-workflow-kit/0.1.0",
  "tests": {
    "offline-unit-tests": "passed",
    "policy-contract-tests": "passed"
  }
}
```

## CI integration

The GitHub Actions workflow supplies the actual workflow commit SHA, computes a SHA-256 content pin for `docs/STABLE_ACCEPTANCE_CONTRACT.md`, and identifies the tested toolkit revision as `dev-workflow-kit@<commit SHA>`, matching the strict verifier's identity contract. It records the offline contract-test step outcome, writes `artifacts/acceptance-report.json`, and uploads that file as the `acceptance-report` artifact for 14 days.

The test step uses `continue-on-error` only so the report can still be produced when tests fail. A final gate explicitly fails the job unless the test step outcome is `success`. The report is not a replacement for the job conclusion.

## Output and fail-closed behavior

The report contains only `schema_version`, `commit_sha`, `rules_pin`, `tool_version`, normalized `tests`, and overall `status`. Test names are sorted for deterministic output and the commit SHA is normalized to lowercase.

Overall status is `passed` only when every declared test status is exactly `passed`. A `failed`, `skipped`, or `not_run` test produces overall `failed`. Missing or malformed required data and unknown input keys are rejected. This strict allowlist prevents arbitrary input fields—including credentials, environment dumps, and raw logs—from being copied into the report.

## Boundaries

- The workflow supplies the current commit SHA, the content hash of the acceptance contract, the toolkit revision label, and the test step outcome. These values are traceable but do not constitute a cryptographic attestation of every runtime action.
- The module does not run tests, inspect repository state, or authenticate arbitrary caller-supplied test evidence.
- The report reflects the offline contract-test step only; it does not claim live model validation or complete defect detection.
- Never pass secrets, raw logs, or environment dumps as report metadata. Do not use this report as an authorization to write remotely or merge a pull request.
