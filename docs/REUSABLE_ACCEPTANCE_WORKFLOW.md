# Reusable Acceptance Workflow

## Status and scope

This early 0.x reusable workflow provides a small, fail-closed execution gate for a consuming repository's explicitly declared acceptance command. It supports Python and Node.js, with optional pnpm setup for Node.js consumers. It does not replace project instructions, review rules, tests, safety constraints, or archive requirements.

## Inputs

- `runtime`: `python` (default) or `node`; any other value fails before the consumer command runs.
- `python-version`: Python version used only when `runtime: python` (default `3.12`).
- `node-version`: Node.js version used only when `runtime: node` (default `24`).
- `package-manager`: `none` (default) or `pnpm`. pnpm setup is permitted only for the Node.js runtime.
- `pnpm-version`: pinned pnpm version requested from the setup action when `package-manager: pnpm` (default `11.4.0`).
- `test-command`: required consumer-owned shell command. It is passed through an environment variable and executed with Bash strict mode. It may install dependencies and run the consumer's own checks, but must not be populated from untrusted PR text, issue comments, model output, or other untrusted data.

The workflow has `contents: read` permissions, a 15-minute job timeout, and action dependencies pinned to full commit SHAs. It does not install consumer dependencies automatically, access model-provider APIs, publish artifacts, merge PRs, deploy services, or perform project business actions.

## Example: Python consumer

Call this workflow using the full 40-character toolkit commit SHA reviewed for that version:

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
      runtime: python
      python-version: "3.12"
      test-command: "python -m unittest discover -s tests -v"
```

## Example: Node.js and pnpm consumer

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
      runtime: node
      node-version: "26"
      package-manager: pnpm
      pnpm-version: "11.4.0"
      test-command: "pnpm install --frozen-lockfile && pnpm run check"
```

Replace the placeholder with a real, reviewed commit SHA from this repository. Do not commit the placeholder. Do not use a moving branch or tag as the production pin. The consumer's tests and command remain consumer-owned.

## Upgrade procedure

1. Select a candidate toolkit commit and inspect its diff, workflow, tests, and acceptance contract.
2. Verify that commit's own CI run completed with conclusion `success`; record the exact 40-character SHA and run URL.
3. Update the consumer's `uses:` reference to that SHA in a separate PR.
4. Review the consumer-specific command, permissions, tests, safety boundaries, and archive paths.
5. Confirm the consumer PR's checks pass on the exact resulting commit before any separately authorized merge.
6. Keep the prior SHA and evidence in the consumer's change history so rollback is a pin revert.

## Security boundaries

- The reusable workflow grants only `contents: read` and does not receive secrets by default.
- `test-command` is executable shell supplied by the consuming repository. Review it as code and do not populate it from untrusted data.
- The workflow checks out and executes code from the consuming repository. Use it only for repositories and events where executing that code is appropriate.
- The workflow does not install dependencies automatically; dependency installation is part of the consumer-owned command.
- The workflow definition and all third-party actions invoked inside it are pinned to full commit SHAs. Re-verify those pins during upgrades.
- A green run establishes only that the consumer-provided command exited successfully. It does not prove the quality or completeness of the command, attest every dependency, or establish production readiness.
