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


## Troubleshooting cross-repository calls

If a consumer workflow fails before the reusable job starts, do not assume the consumer test command or runtime setup caused the failure: those steps may never have run.

1. Confirm the caller's `uses:` path is exactly `wosafety0/dev-workflow-kit/.github/workflows/reusable-acceptance.yml@<40-character-SHA>`, and verify that the referenced SHA exists and is the reviewed version.
2. Inspect the run attempt, job status, **check-run annotations**, and available logs in GitHub Actions. An empty step list or unavailable log blob is evidence that diagnostics are incomplete, not a root-cause explanation. When the job never receives a runner, check-run annotations can still provide the decisive pre-run error even if job logs do not exist.
3. **Classify the reported failure before changing workflow code or access policies.** If GitHub reports that the job was not started because recent account payments failed or the spending limit needs to be increased, treat this as an account billing/spending eligibility blocker. The message alone does not distinguish a failed payment from an exhausted spending limit. Ask the account owner to inspect **Billing & plans**; do not modify payment settings, repeatedly rerun blocked jobs, or claim the acceptance command failed. Keep consumer acceptance pending until an exact-head run succeeds.
4. If no account-level blocker is reported, check the caller repository's **Settings → Actions → General** access/policy controls and any applicable organization or enterprise policy. Confirm whether the caller is allowed to use the referenced reusable workflow and its source repository. Read the effective policy before changing anything.
5. Prefer the narrowest access change that matches the intended trust boundary. Do not enable broad third-party action access, expose secrets, or change repository visibility merely as a troubleshooting shortcut.
6. After any separately authorized configuration change, rerun the same pinned workflow and preserve the exact caller SHA, reusable-workflow SHA, run URL, attempt number, and conclusion. A successful retry verifies that run, but does not by itself prove which setting caused an earlier failure.

GitHub documents reusable-workflow access controls in its [reusing workflow configurations guide](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations). Effective access depends on the caller's repository policy and any higher-level policy; a private caller/public reusable-workflow combination alone is not sufficient to identify a failure cause.
