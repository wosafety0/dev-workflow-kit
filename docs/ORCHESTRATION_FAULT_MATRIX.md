# Orchestration Fault Matrix

## Scope

This matrix covers the repository's offline CI orchestration only. It does not claim to test GitHub's hosted runner, artifact service, or live model providers directly.

The required CI stages are:

1. **Tests** — offline contract test step outcome.
2. **Report** — deterministic, allowlisted acceptance report generation.
3. **Artifact** — upload of the generated report.

The final gate opens only when all three stage outcomes are exactly `success`. GitHub job semantics also keep a failed required step visible as a failed job; the explicit gate makes the combined acceptance condition independently testable.

## Fault matrix

| Injected condition | Expected report behavior | Expected final gate |
|---|---|---|
| All required stages succeed | Report can be passed only when tests passed | Pass |
| Tests fail | Report records failed tests | Fail |
| Tests cancelled | Report records not_run | Fail |
| Tests skipped | Report records not_run | Fail |
| Test outcome missing or unknown | Report records not_run | Fail |
| Report generation fails | Artifact may fail because the file is absent | Fail |
| Artifact upload fails | Report may exist, but evidence was not uploaded | Fail |
| Any stage returns neutral, empty, differently cased, or unknown status | No status is treated as success | Fail |
| Required stage outcome is missing or extra arguments are supplied | Gate rejects the invocation | Fail |

## Offline coverage

`tests/test_ci_gate.py` injects each non-success outcome into each required stage, checks missing/extra stage inputs, verifies exact-success matching, and ensures diagnostics name failed stages without echoing raw outcome values.

The workflow passes the actual `steps.*.outcome` values for the test, report, and artifact steps into the final gate. Report generation and upload remain under `if: always()` so that diagnostics/evidence are attempted after earlier failures, without changing the final fail-closed decision.

## Limitations

- These unit tests validate the gate's decision logic; they do not simulate GitHub Actions expression evaluation or force a real artifact-service outage.
- The report builder validates caller-supplied metadata and does not independently authenticate it.
- A passing offline workflow is not evidence of live model quality or complete defect detection.
- Third-party Actions are still version-tag pinned in the workflow; immutable full-SHA pinning remains a separate hardening task.
