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

The report contains no raw test output, environment dump, credentials, or logs. The workflow verifies the report against trusted GitHub context values for both the caller and the actual reusable workflow definition. The `job.workflow_ref` and `job.workflow_sha` values identify the called workflow, while `github.workflow_ref` and `github.workflow_sha` identify the caller. It rejects missing or malformed reports, unknown fields, duplicate JSON object keys, identity mismatches, and any non-passing test status. The final gate separately requires runtime validation, the consumer command, report generation, artifact upload, and report verification to succeed.

## Consumer responsibility

- Pin the reusable workflow to a reviewed immutable commit SHA rather than a moving branch or tag.
- Keep the test command owned and reviewed by the consuming repository; do not pass untrusted input as a shell command.
- Treat the workflow conclusion as authoritative only for the exact run/commit being reviewed. A report artifact by itself is not proof that the workflow passed.
- Keep consumer CI and branch-protection policy under the consuming project's control. A green result does not itself authorize merge, release, deployment, or live actions.
- If a workflow is pinned to an older commit, its behavior is the behavior of that immutable version; changes to the current reusable workflow do not retroactively alter existing pins.

## Validation boundaries

The verifier establishes report shape, status, and agreement with expected GitHub context values. It does not independently prove the trustworthiness of GitHub itself, the semantic correctness of the consumer tests, or provenance of a report copied outside its originating workflow run. Consumers must retain the workflow run and commit association.
