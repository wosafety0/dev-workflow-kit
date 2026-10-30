# Reusable Acceptance Workflow

## Status and scope

This is an early 0.x reusable workflow. It provides a small, fail-closed execution gate for a consuming repository's explicitly declared acceptance command. It does not replace project instructions, review rules, tests, safety constraints, or archive requirements.

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
      python-version: "3.12"
      test-command: "python -m unittest discover -s tests -v"
```

Replace the placeholder with a real, reviewed commit SHA from this repository. Do not commit the placeholder. Do not use a moving branch or tag as the production pin. The consumer's tests and command remain consumer-owned.

## Upgrade procedure

1. Select a candidate toolkit commit and inspect its diff, workflow, and acceptance contract.
2. Verify that commit's own CI run completed with conclusion `success`; record the exact 40-character SHA and run URL.
3. Update the consumer's `uses:` reference to that SHA in a separate PR.
4. Review the consumer-specific command, permissions, tests, safety boundaries, and archive paths.
5. Confirm the consumer PR's checks pass on the exact resulting commit before any separately authorized merge.
6. Keep the prior SHA and evidence in the consumer's change history so rollback is a pin revert.

## Security boundaries

- The reusable workflow has only `contents: read` permissions and does not receive secrets by default.
- `test-command` is executable shell supplied by the consuming repository. Treat it as code, review it, and do not populate it from untrusted PR text, issue comments, model output, or other untrusted data.
- This workflow checks out and executes code from the consuming repository. Use it only for repositories and events where executing that code is appropriate.
- The reusable workflow does not install project dependencies, access model-provider APIs, publish artifacts, merge PRs, or perform project business actions.
- The reusable workflow is intended to be pinned by consumers to a reviewed full commit SHA. The third-party actions invoked inside this workflow are also pinned to full commit SHAs in the workflow source; verify those pins during upgrades.
- A green run establishes only that the consumer-provided command exited successfully. It does not prove the quality or completeness of the command itself.
