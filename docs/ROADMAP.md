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
- [x] Document immutable 40-character SHA pinning, security boundaries, and upgrade/rollback procedure (`docs/REUSABLE_ACCEPTANCE_WORKFLOW.md`).
- [x] Define a document precedence and stale-content maintenance policy (`docs/DOCUMENT_PRECEDENCE.md`).
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


## 2026-11-02 — Main CI checkout credential persistence

- [x] Harden the report-verifier feature stack's main CI checkout with `persist-credentials: false`.
- [x] Add a contract regression test covering every checkout step in `.github/workflows/ci.yml`.
- [x] Exact-head implementation/test commit `c873e1567f4688a0e8623ee9af5e38effc1dec76` passed Push [41459437408](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41459437408) and PR [41459446214](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41459446214), each with **153 tests**. Documentation archive head `064013ce3a09fc5778343e9ffd37fde0b56f349f` also passed Push [41459685402](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41459685402) and PR [41459694362](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41459694362), each with **153 tests**.
- The reusable consumer workflow already had credential persistence disabled; it was left unchanged.



## 2026-11-02 — Upload Artifact Node 24 compatibility

- [x] Replace the Node 20 `actions/upload-artifact@v4.6.2` pin in both workflows with immutable `v7.0.2` commit `cf430e030ddbb5b0abf93d22962f4752f3646cd9`.
- [x] Add CI and reusable-workflow regression assertions for the Node 24-compatible pin.
- [x] Exact-head implementation/test commit `a55d8bf2ca5cfa133bd6536f3714226181157b03` passed Push [41460735695](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41460735695) and PR [41460744746](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41460744746), each with **155 tests**. Both upload-artifact pin regressions and checkout credential-persistence regression passed.
- GitHub's official v4.6.2 action metadata declares Node 20; v7.0.2 declares Node 24. GitHub removed the Node 20 runner runtime on 2026-09-23.



## 2026-11-02 — isolate trusted consumer report steps

- [x] Prevent consumer-controlled `GITHUB_PATH` changes and workspace module shadowing from affecting the report producer or inline verifier.
- [x] Run both trusted inline Python steps from `$RUNNER_TEMP` using the absolute `/usr/bin/python3 -I` interpreter; resolve the report under `GITHUB_WORKSPACE`.
- [x] Add regression coverage that executes the exact inline source from an isolated temporary directory containing same-named `json.py` and `os.py` shadow modules, and assert both workflow steps use the isolated absolute interpreter.
- Initial exact-head PR CI for implementation/test head `fe00d1b6b6fc6bd19d6a68eb1936c95973e0bceb`: [41464429903](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41464429903) succeeded. The final docs/archive head still requires exact-head Push and PR CI.
- This is an offline workflow hardening change. It does not make consumer test commands safe to run with secrets or write permissions; no consumer pin, permission, merge, tag, release, or deployment was changed.


### Follow-up — neutralize GitHub Actions environment injection

- [x] Override consumer-supplied `BASH_ENV` in every trusted post-test shell step.
- [x] Clear `LD_PRELOAD` and `LD_AUDIT`; constrain `LD_LIBRARY_PATH` and `PATH` to runner/system-owned directories for trusted report, verification, artifact, and final-gate steps.
- [x] Clear `NODE_OPTIONS` and `NODE_PATH` for the Node-based artifact upload action.
- [x] Add per-step workflow contract tests and a Bash startup-file regression.
- Implementation workflow commit: `3dc6a42b553141f8bb43649f3ba30c5105226ca0`; final regression-test commit: `eb3136645b7203d22dc774327aecd0cf4c4a7046`.
- Exact-head PR CI [41465822425](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41465822425) passed **159 offline tests**, compilation, report generation/upload, report verification, and the final gate.
- Push-triggered CI remains unverified for this exact head; do not mark full two-trigger acceptance until its result is independently read back.
