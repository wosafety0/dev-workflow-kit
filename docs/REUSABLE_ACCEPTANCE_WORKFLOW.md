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

- The reusable workflow has only `contents: read` permissions and does not receive secrets by default. The checkout step sets `persist-credentials: false`, so the consumer-supplied test command cannot read a persisted checkout token from `.git/config`.
- `test-command` is executable shell supplied by the consuming repository. Treat it as code, review it, and do not populate it from untrusted PR text, issue comments, model output, or other untrusted data.
- This workflow checks out and executes code from the consuming repository. Use it only for repositories and events where executing that code is appropriate.
- The reusable workflow does not install project dependencies, access model-provider APIs, publish releases/packages, merge PRs, or perform project business actions. It does upload one redacted acceptance-report artifact for CI inspection, with a 14-day retention period.
- The workflow's SHA pin makes the reusable workflow definition immutable for that call. Third-party actions in the current workflow are pinned to full commit SHAs; when upgrading an action, verify the selected commit against the upstream release and update the pin deliberately.
- A green run establishes only that the consumer-provided command exited successfully. It does not prove the quality or completeness of the command itself.


## Ownership boundary and parallel workstreams

The Harness repository is the sole owner of Harness implementation, debugging, and regression fixes across **all consumers**. Consumer projects must not take over, fork, duplicate, or conduct Harness debugging/development in their own repositories.

- Harness-owned work includes reusable workflow implementation, report schema and verifiers, provenance/identity checks, runtime orchestration, artifact handling, gate behavior, Harness regression tests, root-cause analysis, and CI evidence.
- Every Harness defect found by any consumer is treated as input evidence for the Harness backlog. Preserve the failing run, logs, exact pinned SHA, and minimal reproduction; then reproduce, prioritize, fix, and test in the Harness repository.
- Harness debugging proceeds **in parallel with Harness's own planned/core product development**. It is not a consumer-led workstream and does not require pausing ordinary Harness feature development. Prioritize fixes by severity, security/correctness impact, affected consumers, reproducibility, and release/blocking risk.
- Consumers own only their immutable Harness SHA pin, their own project acceptance command/tests, and the minimal configuration/documentation required to call a validated Harness revision. They may report failures and validate integration; they must not patch Harness internals or add Harness-specific diagnostic/probe implementations locally.
- After a Harness fix passes exact-head Harness CI, update a consumer pin only when needed and rerun that consumer's own acceptance CI. Keep the failure evidence linked to the Harness fix so the cause and resolution remain traceable.
- Do not copy Harness implementation into consumer repositories or add temporary Harness-debugging/probe workflows there unless the user explicitly authorizes a narrowly scoped diagnostic exception.
- Keep consumer trial PRs Draft/unmerged until separately reviewed and explicitly authorized.

This boundary applies to every current and future consumer, not only Clamp. It keeps one authoritative implementation and lets reusable Harness development and Harness debugging advance concurrently without consumer-specific forks.
