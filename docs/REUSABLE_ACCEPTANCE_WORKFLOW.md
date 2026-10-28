# Reusable Acceptance Workflow

## Status and scope

This is an early 0.x reusable workflow. It provisions an explicitly selected Python or Node.js runtime, runs a consuming repository's declared acceptance command, writes a small redacted status report, uploads that report, and fails closed unless the test, report, and artifact stages all succeed. It does not replace project instructions, review rules, tests, safety constraints, or archive requirements.

## Immutable SHA pinning

Call this workflow from a consumer workflow using the full 40-character commit SHA reviewed for that version:

```yaml
name: Consumer Acceptance

on:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  acceptance:
    uses: wosafety0/dev-workflow-kit/.github/workflows/reusable-acceptance.yml@REPLACE_WITH_REVIEWED_40_CHAR_SHA
    with:
      runtime: "python"
      python-version: "3.12"
      test-command: "python -m unittest discover -s tests -v"
```

For a Node.js consumer, select Node explicitly and provide its existing test/check command:

```yaml
jobs:
  acceptance:
    uses: wosafety0/dev-workflow-kit/.github/workflows/reusable-acceptance.yml@REPLACE_WITH_REVIEWED_40_CHAR_SHA
    with:
      runtime: "node"
      node-version: "26"
      test-command: "npm ci && npm test"
```

Replace each placeholder with a real, reviewed commit SHA from this repository. Do not commit a placeholder. Do not use a moving branch or tag as the production pin. The consumer's tests and command remain consumer-owned. Runtime values are allowlisted to `python` or `node`; unsupported values fail closed.

## Behavior and report

- The workflow uses immutable commit SHAs for checkout, Python setup, Node setup, and artifact upload.
- The test command runs with `bash -euo pipefail` and its outcome is recorded even when it fails.
- The workflow attempts to create `artifacts/consumer-acceptance-report.json` after the test step. The report contains only a schema version, consumer commit SHA, caller workflow reference/SHA, test status, and overall status. It does not copy test output, environment variables, credentials, or arbitrary command text.
- The report is uploaded as the `consumer-acceptance-report` artifact for 14 days.
- The final gate opens only when the test, report-generation, and artifact-upload steps each have the exact outcome `success`. A failed or skipped required stage closes the gate.
- If checkout or runtime setup fails, later `always()` steps still attempt to run; the report/artifact/gate path must not turn that earlier failure into success.
- The report is a concise consumer-command status record. It is not the semantic-review report produced by `scripts/acceptance_report.py`, and a passing command does not establish review quality or full policy compliance.

## Upgrade procedure

1. Select a candidate toolkit commit and inspect its diff, workflow, and acceptance contract.
2. Verify that commit's own CI run completed with conclusion `success`; record the exact 40-character SHA and run URL.
3. Update the consumer's `uses:` reference to that SHA in a separate PR.
4. Review the consumer-specific runtime, command, permissions, tests, safety boundaries, and archive paths.
5. Confirm the consumer PR's checks pass on the exact resulting commit before any separately authorized merge.
6. Keep the prior SHA and evidence in the consumer's change history so rollback is a pin revert.

## Security boundaries

- The reusable workflow has only `contents: read` permissions and does not receive secrets by default.
- `test-command` is executable shell supplied by the consuming repository. Treat it as code, review it, and do not populate it from untrusted PR text, issue comments, model output, or other untrusted data.
- This workflow checks out and executes code from the consuming repository. Use it only for repositories and events where executing that code is appropriate.
- Node package-manager caching is disabled in the setup step; consumers may explicitly add reviewed cache behavior in a future version if needed.
- A green run establishes only that the consumer-provided command exited successfully and the status report was uploaded. It does not prove the quality or completeness of the command itself.
- No merge, release, deployment, model-provider call, or project business action is performed.
