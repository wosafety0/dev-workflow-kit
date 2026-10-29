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
- The reusable workflow does not install project dependencies, access model-provider APIs, publish releases/packages, merge PRs, or perform project business actions. It does upload one redacted acceptance-report artifact for CI inspection, with a 14-day retention period.
- The workflow's SHA pin makes the reusable workflow definition immutable for that call. Third-party actions in the current workflow are pinned to full commit SHAs; when upgrading an action, verify the selected commit against the upstream release and update the pin deliberately.
- A green run establishes only that the consumer-provided command exited successfully. It does not prove the quality or completeness of the command itself.


## Ownership boundary for consumer pilots

The Harness repository owns the reusable workflow implementation and its debugging lifecycle. For any consumer pilot (including `wosafety0/wosafety0clamp`):

- Fix reusable workflow behavior, report schema/verifier, provenance and identity checks, runtime orchestration, artifact handling, gate logic, and Harness regression tests in `wosafety0/dev-workflow-kit`.
- Validate and archive the Harness fix in this repository first. Do not use a consumer repository as a development branch for Harness implementation.
- The consumer repository owns only its immutable Harness SHA pin, its own acceptance command and project tests, and minimal consumer-side configuration/documentation.
- When a consumer run reveals a suspected Harness defect, preserve the failing run as evidence, reproduce and fix it in the Harness repository, then update the consumer pin only after the exact Harness commit passes Harness CI. Re-run consumer CI to validate the integration.
- Do not copy the verifier or reusable workflow implementation into consumer repositories, and do not add temporary Harness-debugging/probe workflows to a consumer repository unless the user explicitly authorizes a narrowly scoped diagnostic exception.
- Keep consumer trial PRs Draft/unmerged until separately reviewed and explicitly authorized.

This boundary separates reusable product development from consumer integration and prevents debugging fixes from becoming duplicated, consumer-specific implementations.
