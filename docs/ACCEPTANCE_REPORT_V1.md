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

## Output and fail-closed behavior

The report contains only `schema_version`, `commit_sha`, `rules_pin`, `tool_version`, normalized `tests`, and overall `status`. Test names are sorted for deterministic output and the commit SHA is normalized to lowercase.

Overall status is `passed` only when every declared test status is exactly `passed`. A `failed`, `skipped`, or `not_run` test produces overall `failed`. Missing or malformed required data and unknown input keys are rejected. This strict allowlist prevents arbitrary input fields—including credentials, environment dumps, and raw logs—from being copied into the report.

## Boundaries

- The module does not discover the commit SHA, rules pin, tool version, or test results itself; the calling workflow must provide verified values.
- It does not run tests, inspect repository state, verify that a rules pin actually refers to the intended policy, or authenticate the evidence.
- A syntactically valid report is not proof that its supplied test statuses are true.
- Never pass secrets, raw logs, or environment dumps as report metadata. Do not use this report as an authorization to write remotely or merge a pull request.
