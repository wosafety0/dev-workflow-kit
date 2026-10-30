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

- [x] Define a versioned project configuration schema (`docs/HARNESS_CONFIG_V1.md`) with an explicit task-ID allowlist.
- [x] Validate the fixed-behavior task runner (`scripts/harness_runner.py`) on exact PR head `e96c35484bd199e36cc84e4f673a17169c328f5b`: argv arrays only (no shell), repository-root path boundaries, `artifacts/`-only outputs, redacted report, fail-closed task status, end-to-end execution/mapping tests for both allowlisted task IDs, and a validated checked-in example config. Evidence: [CI run 40717650992](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40717650992); 100 offline tests passed.
- [x] Validate model-provider configuration without requiring a model API.
- [x] Define a safe, explicit task-ID allowlist; unknown IDs fail closed and configuration does not execute commands.
- [x] Build a deterministic, strict-allowlist acceptance report with commit SHA, rules pin, tool version, and test status (`docs/ACCEPTANCE_REPORT_V1.md`).
- [x] Wire CI to generate and upload the report using the workflow commit SHA, rules-contract content hash, toolkit revision, and test-step outcome.
- [x] Verify that a historical GitHub Actions run (Run 40639692633; tested commit `cfbcf095850b8e13c52c2a1ab9050d6397886f50`) uploaded the report artifact and passed the fail-closed job gate. This is historical evidence only.
- [x] Verify PR-head CI run [40691689194](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40691689194) succeeded for tested commit `4fa5f05316876cefa39bd8cdbe4187f63ee0757a`. This establishes the result for that exact PR head only; it does not independently verify the later merge commit `9b236112d4d6f07e15480b5b0ae6e9a3ef5c8aea`.
- [x] Add failure-injection tests for model-provider fail-closed behavior.
- [x] Add an orchestration fault matrix and test that test, report-generation, and artifact-upload outcomes must all be exactly successful before the final gate opens (`docs/ORCHESTRATION_FAULT_MATRIX.md`, `tests/test_ci_gate.py`).
- [ ] Exercise real hosted-workflow failure injection (including an actual artifact-upload failure) and verify the resulting run evidence.

## Stage 3 — versioned distribution

- [x] Add a minimal reusable acceptance workflow with read-only repository permissions and an explicit consumer-owned test command (`.github/workflows/reusable-acceptance.yml`).
- [x] Extend the reusable acceptance workflow with explicit Python/Node.js runtime selection and optional pinned pnpm setup; reject unsupported runtime/package-manager combinations before the consumer command runs.
- [x] Document immutable 40-character SHA pinning, security boundaries, and upgrade/rollback procedure (`docs/REUSABLE_ACCEPTANCE_WORKFLOW.md`).
- [x] Define a document precedence and stale-content maintenance policy (`docs/DOCUMENT_PRECEDENCE.md`).
- [ ] Tag an initial 0.x release only after acceptance criteria pass on the exact release candidate and the release scope is reviewed.

## Stage 4 — consumer integration

- [x] Validate a first consumer pilot through a separate PR pinned to a tested toolkit SHA: [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), pinned to Harness commit `36533dd7726365fd817f48072e49ea055d339947`; the reusable-workflow run passed on consumer head `643659014370f85b61964bcbb978833ec6f74428`. The PR remains Draft/unmerged.
- [ ] Preserve each consumer's project-specific tests, safety constraints, and archive paths.
- [ ] Pilot with a second, unrelated repository without copying the core. An isolated attempt was made in private `wosafety0/chatgpt-auto-send-assistant` [Draft PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1), pinned to the same tested SHA; [run 41021315209](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41021315209) failed before any job steps and exposed no runner logs. Repository metadata confirms the consumer is private while the reusable workflow repository is public. This is consistent with a GitHub Actions cross-repository access restriction, but the exact cause is not yet confirmed. No repository settings were changed; the second-consumer acceptance item remains incomplete.
- [ ] Publish a reusable-MVP decision based on actual evidence.

## Non-negotiable acceptance rules

- Offline tests do not count as live model validation.
- Missing configuration, network errors, invalid output, or unverifiable evidence must never produce a passing review.
- CI results must link to the actual workflow run and identify the exact tested commit.
- No credentials in source, artifacts, or logs.
- No automatic PR merge or project business actions.
- Remote GitHub changes must not be described as synced to a local worktree unless independently verified.
- Documentation conflicts must be resolved under `docs/DOCUMENT_PRECEDENCE.md`; obsolete current-facing descriptions must be updated.
