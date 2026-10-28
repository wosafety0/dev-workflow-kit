# Roadmap and Acceptance Gates

## Document status and precedence

When current-facing documents conflict, follow the latest applicable, verified project version and correct the obsolete descriptions. Use [DOCUMENT_PRECEDENCE.md](DOCUMENT_PRECEDENCE.md) for the required resolution and maintenance procedure. A newer timestamp alone does not establish correctness; implementation claims require code/tests, and verification claims require evidence tied to the relevant commit. This roadmap describes the current development branch and does not imply its changes have been merged into `main`.

## Stage 0 — repository bootstrap

- [x] Create an independent repository.
- [x] Add a clear non-stable status statement.
- [x] Run independent CI and review its actual result.

## Stage 1 — reusable semantic-review core

- [x] Port the provider-agnostic semantic-review client.
- [x] Port offline contract tests.
- [x] Document inputs, secrets, status semantics, and limitations.
- [x] Publish the initial 0.x stable acceptance contract in `docs/STABLE_ACCEPTANCE_CONTRACT.md`.
- [x] Expand tests for malformed input, missing configuration, provider errors, and malformed provider responses.
- [x] Confirm CI is green on this repository.

## Stage 2 — project contract and deterministic orchestration

- [x] Define a versioned project configuration schema (`docs/HARNESS_CONFIG_V1.md`; validation-only, no runner).
- [x] Validate model-provider configuration without requiring a model API.
- [x] Define a safe, explicit task-ID allowlist; unknown IDs fail closed and configuration does not execute commands.
- [x] Build a deterministic, strict-allowlist acceptance report with commit SHA, rules pin, tool version, and test status (`docs/ACCEPTANCE_REPORT_V1.md`).
- [x] Wire CI to generate and upload the report using the workflow commit SHA, rules-contract content hash, toolkit revision, and test-step outcome.
- [x] Verify that a historical GitHub Actions run (Run 40639692633; tested commit `cfbcf095850b8e13c52c2a1ab9050d6397886f50`) uploaded the report artifact and passed the fail-closed job gate. This is historical evidence only.
- [x] Verify PR-head CI run [40691689194](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40691689194) succeeded for tested commit `4fa5f05316876cefa39bd8cdbe4187f63ee0757a`. This establishes the result for that exact PR head only; it does not independently verify the later merge commit `9b236112d4d6f07e15480b5b0ae6e9a3ef5c8aea`.
- [x] Add failure-injection tests for model-provider fail-closed behavior.
- [x] Add an orchestration fault matrix and test that test, report-generation, and artifact-upload outcomes must all be exactly successful before the final gate opens (`docs/ORCHESTRATION_FAULT_MATRIX.md`, `tests/test_ci_gate.py`).
- [x] Verify a hosted missing-artifact-input failure closes the gate; this does not simulate an Artifact service outage.

## Stage 3 — versioned distribution

- [x] Add a minimal reusable acceptance workflow with read-only repository permissions and an explicit consumer-owned test command (`.github/workflows/reusable-acceptance.yml`).
- [x] Document immutable 40-character SHA pinning, security boundaries, and upgrade/rollback procedure (`docs/REUSABLE_ACCEPTANCE_WORKFLOW.md`).
- [x] Define a document precedence and stale-content maintenance policy (`docs/DOCUMENT_PRECEDENCE.md`).
- [ ] Validate the reusable workflow's redacted report and artifact fail-closed behavior on a hosted consumer-style workflow run.
- [ ] Tag an initial 0.x release only after acceptance criteria pass on the exact release candidate and the release scope is reviewed.

## Stage 4 — consumer integration

- [ ] Integrate a consumer through a separate PR pinned to a tested toolkit SHA.
- [ ] Preserve each consumer's project-specific tests, safety constraints, and archive paths.
- [ ] Pilot with a second, unrelated repository without copying the core.
- [ ] Publish a reusable-MVP decision based on actual evidence.

## Non-negotiable acceptance rules

- Offline tests do not count as live model validation.
- Missing configuration, network errors, invalid output, or unverifiable evidence must never produce a passing review.
- CI results must link to the actual workflow run and identify the exact tested commit.
- No credentials in source, artifacts, or logs.
- No automatic PR merge or project business actions.
- Remote GitHub changes must not be described as synced to a local worktree unless independently verified.
- Documentation conflicts must be resolved under `docs/DOCUMENT_PRECEDENCE.md`; obsolete current-facing descriptions must be updated.
