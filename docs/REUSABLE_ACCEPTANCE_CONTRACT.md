# Reusable Acceptance Workflow Contract

## Scope

The reusable acceptance workflow runs a consumer-owned, explicitly supplied test command in a clean GitHub-hosted job. It is an auxiliary gate and does not grant permission to merge, deploy, call live model providers, or perform application/game actions.

## Report identity

The workflow writes `artifacts/consumer-acceptance-report.json` with exactly these fields:

- `schema_version`: integer `1`
- `consumer_commit_sha`: the consumer commit SHA from the caller's workflow context
- `caller_workflow_ref`: the caller workflow reference from GitHub context
- `caller_workflow_sha`: the caller workflow file SHA from GitHub context
- `harness_workflow_ref`: the actual reusable workflow reference from the GitHub `job` context
- `harness_workflow_sha`: the commit SHA of the reusable workflow definition from the GitHub `job` context
- `tests`: exactly `runtime-validation` and `consumer-acceptance-command`, each set to `passed`, `failed`, or `not_run`
- `status`: `passed` only when runtime validation and the consumer command both passed; otherwise `failed`

The report contains no raw test output, environment dump, credentials, or logs. The producer rejects a symlinked `artifacts/` directory and writes to a temporary file followed by atomic replacement, so a consumer-created symlink or hard link at the report filename cannot redirect the report write. The workflow verifies the report against trusted GitHub context values for both the caller and the actual reusable workflow definition. The `job.workflow_ref` and `job.workflow_sha` values identify the called workflow, while `github.workflow_ref` and `github.workflow_sha` identify the caller. It rejects missing or malformed reports, unknown fields, duplicate JSON object keys, identity mismatches, and any non-passing test status. The final gate separately requires runtime validation, the consumer command, report generation, artifact upload, and report verification to succeed.

## Trusted post-test execution

The consumer-owned command runs before report generation and may write GitHub Actions command files such as `GITHUB_PATH` and `GITHUB_ENV`, or leave executable/module files in the checked-out workspace. The trusted report producer and inline verifier therefore do not resolve Python through the consumer-modifiable `PATH` or import from the consumer workspace: both change directory to the runner's `RUNNER_TEMP`, invoke `/usr/bin/python3 -I` by absolute path, and resolve the report only through the runner-provided `GITHUB_WORKSPACE`.

The trusted post-test steps explicitly override the consumer's `BASH_ENV`, loader injection variables (`LD_PRELOAD`, `LD_AUDIT`), `LD_LIBRARY_PATH`, and `PATH`. The library search path is restricted to system-owned directories. The report upload action also overrides `NODE_OPTIONS`, `NODE_PATH`, and the loader/search-path variables so consumer-written `GITHUB_ENV` entries cannot inject Node startup code into the Artifact action. Regression tests execute the exact inline source from an isolated temporary working directory containing shadow modules, and assert the per-step environment overrides and trusted search paths.

This narrows the post-test trust boundary; it does not make an arbitrary consumer test command safe to run with secrets or write-capable permissions. The reusable job remains read-only and checkout credential persistence remains disabled.

## Consumer responsibility

- Pin the reusable workflow to a reviewed immutable commit SHA rather than a moving branch or tag.
- Keep the test command owned and reviewed by the consuming repository; do not pass untrusted input as a shell command.
- Treat the workflow conclusion as authoritative only for the exact run/commit being reviewed. A report artifact by itself is not proof that the workflow passed.
- Keep consumer CI and branch-protection policy under the consuming project's control. A green result does not itself authorize merge, release, deployment, or live actions.
- If a workflow is pinned to an older commit, its behavior is the behavior of that immutable version; changes to the current reusable workflow do not retroactively alter existing pins.

## Validation boundaries

The inline workflow verifier and standalone Harness verifier must enforce the same report schema. The standalone verifier requires `--expected-harness-workflow-ref` and `--expected-harness-workflow-sha` in addition to caller identity arguments, and checks both against the report. The verifier establishes report shape, status, and agreement with expected GitHub context values. It does not independently prove the trustworthiness of GitHub itself, the semantic correctness of the consumer tests, or provenance of a report copied outside its originating workflow run. Consumers must retain the workflow run and commit association.
