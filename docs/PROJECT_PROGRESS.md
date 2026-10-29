# Project Progress Log

Last updated: 2026-10-28

## Current repository state

- Repository: `wosafety0/dev-workflow-kit`
- Integration target branch: `feat/semantic-review-core-20261028`
- This is the generic AI Development Harness project; it is not yet integrated into KancolleBot.
- No 0.x release has been created. The default branch `main` was not changed by this work round.

## Verified progress

### PR #4 merged

- PR: https://github.com/wosafety0/dev-workflow-kit/pull/4
- Title: `test: orchestration fault matrix`
- Source head: `817d4e6342ac975efa61a73ac6c10f36fcd0f68d`
- CI run: https://github.com/wosafety0/dev-workflow-kit/actions/runs/40696961658
- CI conclusion: success for the exact PR head SHA. The offline job completed compilation, offline contract tests, redacted acceptance report generation, artifact upload, and final gate.
- Merge commit on `feat/semantic-review-core-20261028`: `75b0892c4976e7e060a7f43f68c150777458e7b5`

### Supply-chain pinning proposal

- Branch: `fix/pin-github-actions-sha-20261028`
- Pinned `actions/checkout` v5 to `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09`.
- Pinned `actions/setup-python` v6 to `ece7cb06caefa5fff74198d8649806c4678c61a1`.
- Pinned `actions/upload-artifact` v4 to `ea165f8d65b6e75b540449e92b4886f43607fa02`.
- The SHA values were read from the corresponding official `actions/*` GitHub tag refs during this work round. These are pinned to the resolved commits, with readable tag comments retained.
- Workflow permissions remain explicitly limited to `contents: read`.
- PR #5 was merged into the integration branch after CI and diff verification.

### Gate and test coverage

The final gate requires the test, report-build, and artifact-upload stages to report exact `success`. Hosted evidence covers the normal artifact-upload path and fail-closed behavior when artifact input is missing or the consumer test command fails. No real GitHub Artifact service outage has been simulated.

## Limits of current evidence

- PR #5 CI passed on the exact PR head before merge; both push and pull-request runs succeeded.
- Hosted failure-path tests have been performed for missing artifact input and consumer test-command failure. They do not establish behavior during an actual Artifact service outage.
- No real model validation or second independent consumer integration pilot has been completed.
- The local working tree/synchronization state has not been verified.
- No changes were made to `main`.

## Next steps

1. Review the successful Node.js consumer pilot evidence and decide whether to revise the consumer PR; keep it draft until separately reviewed.
2. Review the completed independent consumer pilot evidence; keep the consumer PR draft/unmerged until separately authorized.
3. Begin controlled real-model validation with strict quotas and no production actions, then define 0.x release criteria from the accumulated evidence.
3. Define objective 0.x release criteria after the independent pilot evidence is available.
4. Conduct controlled real-model validation after offline and hosted reliability boundaries are documented.
5. Keep the Artifact-service-outage boundary explicitly unverified; do not let this hard-to-reproduce scenario block a low-risk independent consumer pilot.

## Decision record

- PR #4 was merged only into `feat/semantic-review-core-20261028` after explicit user authorization.
- PR #5 supply-chain pinning was merged into the integration branch after explicit user direction and successful CI.
- Do not merge to `main`, create a release, or integrate into a consumer project without separate review and authorization.

### PR #5 merged: supply-chain pinning

- PR: https://github.com/wosafety0/dev-workflow-kit/pull/5
- Merge commit on `feat/semantic-review-core-20261028`: `50c8027dd6e410f7d40d21778e74a8c5b22fe364`
- PR head: `5af3377d0533229d98eb7ccaa86830fbb4d48af3`
- Both automatic CI runs passed; no manual workflow dispatch was used.
- Actions are pinned to full commit SHAs; workflow permissions remain `contents: read`.

### Hosted fault-path validation: missing artifact input

- Temporary PR: https://github.com/wosafety0/dev-workflow-kit/pull/6 (closed, not merged).
- Test commit: `1add4e2369f6e1daa343e36b442bd10b51dae63c`.
- Run: https://github.com/wosafety0/dev-workflow-kit/actions/runs/40712433963
- Result: 89 offline tests passed; report generation passed; upload step failed as deliberately configured because the requested artifact path did not exist; final gate failed with `ARTIFACT_OUTCOME=failure` and named `artifact` as the unsuccessful required stage.
- This proves the hosted workflow closes the gate on an upload-step failure. It does **not** simulate a GitHub artifact-service outage or validate service-level behavior.
- The test-only PR was closed after evidence collection and was never merged. Its workflow was restored to the normal artifact path in cleanup commit `9254c3058196a192227bb56a1d6c634ecefbc72d`. The temporary branch remains for auditability; no changes were made to `main`.

### Consumer pilot preparation and normal-path verification

- Draft PR #7: https://github.com/wosafety0/dev-workflow-kit/pull/7
- Branch: `test/consumer-pilot-readiness-20261028`; tested head: `bff949fba82e5c514ed9f0f11a32120dae2faabf`.
- Added `docs/CONSUMER_PILOT_CHECKLIST.md` with entry criteria, controlled pilot steps, pass/fail criteria, evidence capture, and stop conditions. The file was read back from GitHub; blob SHA: `afdc2781809e8e1d1e332c739bdbee4d63989a22`.
- The checklist explicitly distinguishes a missing-artifact-input failure from a real GitHub Artifact service outage.
- Hosted CI run [40713631149](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40713631149), run number 100, completed successfully for the exact PR head `bff949fba82e5c514ed9f0f11a32120dae2faabf`. Offline tests, report generation, artifact upload, and final gate all succeeded; artifact ID `12826902344`.
- PR #7 was closed unmerged after its checklist content was carried into PR #8; no consumer repository has been merged or released, and no changes were made to `main`.

### Reusable acceptance workflow report and fail-closed gate

- Draft PR #8: https://github.com/wosafety0/dev-workflow-kit/pull/8
- Branch: `feat/reusable-acceptance-report-gate-20261028`; tested PR head: `58dc2c5a84099e588797beccc1ad3b9802614108`.
- Added a redacted consumer acceptance report containing only schema version, consumer commit SHA, caller workflow reference/SHA, test status, and overall status. The workflow attempts report generation and upload after test failure, then opens the gate only if test, report, and artifact stages all have exact `success`.
- Added `tests/test_reusable_workflow_contract.py` to check read-only permissions, immutable action pins, report allowlist, failure continuation, and final-gate rules.
- Updated reusable-workflow documentation, pilot checklist, and roadmap to reflect the implementation and its limits.
- Hosted CI run [40714595099](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40714595099), run number 108, completed successfully for PR #8's exact tested head `58dc2c5a84099e588797beccc1ad3b9802614108`. The run log confirms 93 offline tests passed, report generation passed, artifact ID `12827468404` was uploaded, and the final gate passed.
- This validates the Harness repository CI and workflow-contract tests, not by itself the called workflow's behavior in a consumer context.
- PR #8 is draft and unmerged. No changes were made to `main`.

### Reusable workflow consumer normal-path smoke test

- Draft PR #9: https://github.com/wosafety0/dev-workflow-kit/pull/9
- Branch: `test/reusable-workflow-smoke-20261028`; tested head: `71ec801a1c84c2a52920386466d3c9b63075f0fa`.
- Added `.github/workflows/reusable-acceptance-smoke.yml`, invoking the reusable workflow at immutable SHA `58dc2c5a84099e588797beccc1ad3b9802614108`.
- Consumer workflow run [40714715392](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40714715392) completed successfully. The called job's checkout, Python setup, consumer test command, redacted report generation, artifact upload, and final gate all succeeded.
- Artifact `consumer-acceptance-report` ID: `12827428586`; digest: `sha256:b9b896241e5840897a9c65595cf0008bab79a5e2ea9d6287fe624ba1dd8b40cf`.
- The same PR's Harness CI run [40714714617](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40714714617) also succeeded.
- This is a same-repository smoke test only, not proof of a second independent consumer. PR #9 was closed unmerged after its successful run and artifact evidence were recorded.

### Reusable workflow consumer failure-path smoke test

- Temporary draft PR #10: https://github.com/wosafety0/dev-workflow-kit/pull/10 (closed, not merged).
- Branch: `test/reusable-workflow-failure-smoke-20261028`; tested head: `dc46f7593f95fd1e84e0438d2b5c2bdf661910a2`.
- Run [40714856655](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40714856655) completed with the expected failure. The consumer test command exited 23; the report step still succeeded and recorded `status: failed`; the artifact uploaded successfully (artifact ID `12827258524`); the final gate exited 1 and reported only the unsuccessful required stage `tests`.
- The run log verified `TEST_OUTCOME=failure`, `REPORT_OUTCOME=success`, and `ARTIFACT_OUTCOME=success`. This demonstrates that a consumer test failure cannot be hidden by a successful report upload.
- The temporary PR was closed after evidence collection and was never merged. No changes were made to `main`.


### Multi-runtime reusable workflow implementation

- Extended the reusable acceptance workflow to support explicit `python` and `node` runtimes; unsupported runtime values fail closed.
- Node setup action pin verified against the official `actions/setup-node` repository: commit `48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e`, release v6.4.0.
- Added contract tests for the runtime allowlist, conditional setup steps, immutable Node action pin, and disabled package-manager cache.
- Workflow-code candidate SHA: `65544e290fd875bb6c4e30f6525b238200037bba`.
- Hosted Harness CI run [40715196026](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40715196026), run number 126, completed successfully for that exact code SHA; the 93-test suite, report, artifact upload, and final gate succeeded. Artifact ID: `12827137999`.
- Latest PR #8 head after documentation evidence updates: `7e58aaf1d73d82319808a22bf26004e062b67b19`; hosted CI run [40715766990](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40715766990), run number 136, also completed successfully.
- The Node runtime was subsequently verified by the independent consumer pilot below.

### Independent Node.js consumer pilot

- Draft consumer PR: https://github.com/wosafety0/AI-Worker-Proxy/pull/1
- Branch: `test/dev-workflow-kit-pilot-20261028`; tested head: `642c627bdb8f2e3c791835ec78f837a258c3eb97`.
- Added `.github/workflows/dev-workflow-kit-pilot.yml`, pinned to Harness SHA `65544e290fd875bb6c4e30f6525b238200037bba`, using Node.js 26 and the consumer's existing `pnpm check` after a frozen-lockfile install.
- Consumer workflow run [40715309593](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/40715309593) completed successfully for exact head `642c627bdb8f2e3c791835ec78f837a258c3eb97`. Node.js 26 setup succeeded; `pnpm install --frozen-lockfile` installed 236 packages; `pnpm check` passed (`tsc --noEmit && eslint src`); redacted report generation, artifact upload, and final gate succeeded.
- Consumer artifact `consumer-acceptance-report` ID: `12828925328`; digest: `sha256:ab0642ac0f7590352cabc08d504b21c75a3b8612e14b6be72ac6fd33f23c938d`.
- The consumer's existing `Lint and Type Check` run [40715308397](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/40715308397) also completed successfully.
- This verifies cross-repository Node runtime consumption on the exact tested Harness SHA. The PR is draft and unmerged; it adds only a read-only acceptance workflow and does not deploy the Cloudflare Worker or modify `main`.


### Updated multi-runtime Node failure-path validation

- Temporary draft PR #11: https://github.com/wosafety0/dev-workflow-kit/pull/11 (closed, not merged).
- Tested head: `e353f34d314aff450801a1108e00dd2a409166f2`; reusable workflow pinned to candidate SHA `65544e290fd875bb6c4e30f6525b238200037bba`.
- Run [40715636382](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40715636382) completed with the expected failure after Node.js 26 setup succeeded.
- The consumer command exited 23; the report recorded `status: failed`; artifact upload succeeded (artifact ID `12828236019`); the final gate exited 1 and named `tests` as the failed required stage.
- Run logs verified `TEST_OUTCOME=failure`, `REPORT_OUTCOME=success`, and `ARTIFACT_OUTCOME=success`. The temporary PR was closed after evidence capture and was never merged.


### Local inference endpoint transport hardening

- Draft PR #12: https://github.com/wosafety0/dev-workflow-kit/pull/12
- Branch: `fix/local-loopback-model-endpoint-20261028`; latest tested head: `c0df7982e1b1767450199ee42ff17395f3573ae4`.
- Changed `validate_model_config` to allow HTTPS for remote providers and HTTP only for literal loopback IPs (IPv4/IPv6). Hostname-based `localhost`, non-loopback HTTP, embedded URL credentials, query strings, fragments, malformed ports, and control characters remain rejected.
- Loopback HTTP requests use a request-scoped opener with proxy handling disabled, without changing global/system proxy settings.
- Added offline config tests and a local mock-server request test with proxy environment variables deliberately set. The test proves a real loopback HTTP request succeeds without routing through the configured proxy. Updated `docs/STABLE_ACCEPTANCE_CONTRACT.md`.
- Hosted CI run [40717962173](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40717962173), run number 187, succeeded on the exact tested head. 91 offline tests passed, including the loopback request test; the acceptance report uploaded (artifact ID `12829482177`), and the final gate passed.
- This does not constitute a live model request or prove that the user's local LM Studio endpoint is reachable from this environment. PR #12 remains draft and unmerged.


### Safe allowlisted task runner

- Draft PR #13: https://github.com/wosafety0/dev-workflow-kit/pull/13
- Branch: `feat/safe-task-runner-20261028`; latest tested head: `8dd0e4b58cdf7384ebe703b8fd076ec97e98fd72`.
- Added `scripts/harness_runner.py`, mapping only the existing `python-unittest` and `semantic-review` task IDs to fixed argv arrays. It does not invoke a shell or accept executable names/arbitrary arguments from config.
- Added preflight validation before any task executes, per-task timeout, project-root path containment, `artifacts/`-only outputs, suppressed raw task stdout/stderr, and a redacted report built through the existing strict acceptance-report module.
- Added `tests/test_harness_runner.py`, including an end-to-end test that executes the fixed unittest task in a temporary project, failure/report behavior, path traversal/output protections, semantic-review argument requirements, and timeout handling.
- Added `examples/harness-config.json`, `examples/harness-config-semantic-review.json`, and an evidence-grounded negative review fixture; added `docs/HARNESS_RUNNER_V1.md` and `docs/SEMANTIC_REVIEW_SMOKE_TEST.md`, updated configuration/README docs, and recorded the runner gate in the roadmap.
- Hosted CI run [40718581286](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40718581286), run number 203, succeeded on exact head `8dd0e4b58cdf7384ebe703b8fd076ec97e98fd72`: 101 offline tests passed, including end-to-end runner execution, both task mappings, both example configs, and validation of the negative-review fixture. Acceptance report uploaded (artifact ID `12829517160`); final gate passed.
- The model smoke test remains opt-in and was not run by CI; no live model request has been made.
- PR #13 remains draft/unmerged. The runner is not a sandbox; running project tests can have side effects, so consumers must use trusted worktrees and review their test commands. No live model request was made.


### Integration preflight: PR #12 and #13 branch divergence (2026-10-29)

- Read-only GitHub compare confirmed both branches diverge from integration branch `feat/semantic-review-core-20261028` (base SHA `a3fbe350739b2108cd72bf063015281417fdd628`).
- `fix/local-loopback-model-endpoint-20261028`: 6 ahead / 7 behind; changed files: `docs/STABLE_ACCEPTANCE_CONTRACT.md`, `scripts/ai_semantic_review.py`, `tests/test_ai_semantic_review.py`.
- `feat/safe-task-runner-20261028`: 27 ahead / 6 behind; changed files include runner, examples, docs, and `tests/test_ai_semantic_review.py`.
- The shared test file is an integration overlap, not proof of an actual merge conflict. Individual green CI results do not establish combined compatibility. Next: construct a non-main integration candidate, resolve any conflicts explicitly, and run full offline tests and acceptance gate before recommending merges.
- No PR merged, no main branch change, no model calls or game operations in this preflight.


### Runner configuration output alias hardening (2026-10-29)

- Draft PR #19: https://github.com/wosafety0/dev-workflow-kit/pull/19 ; head `956b43939dc010f7a62561d8e1f7ceb766b61b68`; base `feat/safe-task-runner-20261028` (not `main`).
- Fixed a preflight alias bug: if a valid Harness config lived inside `artifacts/`, `--review-output` could target the same path and overwrite it. The runner now rejects that alias before any task runs.
- Added a regression test asserting exit 2, no task execution, and intact config content.
- Hosted CI run [40793868543](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40793868543), job `offline-tests` ID `123185427562`, completed successfully. Decoded job logs confirm 102 offline tests passed; report creation, artifact upload, and final acceptance gate succeeded.
- PR remains draft/unmerged. No `main` modification, deployment, or model request.


### Runner and loopback integration candidate (2026-10-29)

- Draft PR #20: https://github.com/wosafety0/dev-workflow-kit/pull/20; branch `test/runner-loopback-integration-20261029`; head `b44b7f139fdabe62cc215b173d022c5c13cc5c90`; base `fix/runner-output-alias-20261029`.
- Combined PR #12's loopback HTTP transport/proxy-bypass implementation and acceptance contract with PR #13/#19's runner and output alias protection. Added both loopback endpoint and actual mock-server proxy bypass tests to the combined test module.
- Initial workflow-run lookup for the integration head returned no runs; combined CI result is **pending/unverified**, not a pass. Next: inspect workflow trigger and obtain hosted CI evidence before merge recommendation.
- PR #20 is draft/unmerged; no changes to `main`, no live provider model calls, no game operations.


### Integration CI trigger investigation (2026-10-29)

- Reviewed `.github/workflows/ci.yml`: pull-request trigger targets `main`, `feat/**`, `test/**`; the original PR #20 base `fix/runner-output-alias-20261029` was **not** in the PR trigger filter. Push trigger separately includes `test/**`.
- Retargeted draft PR #20 to `feat/safe-task-runner-20261028` to make the pull-request trigger eligible while preserving PR #19's fix in the integration head. The integration head remains `b44b7f139fdabe62cc215b173d022c5c13cc5c90`.
- Connector's commit workflow lookup returned no PR-triggered runs after retargeting at inspection time. This lookup only includes pull-request-triggered runs, so it cannot establish whether a push-triggered run occurred. **No CI pass is claimed.**
- Follow-up: obtain explicit PR-triggered workflow run/job evidence, or inspect run history through an appropriate run-list interface. PR remains draft; no merge or deployment.


### Integrated runner and loopback fail-closed regression (2026-10-29)

- Draft PR #20 received commit `827bb99d2eb97ac61909979094f68471f081150b` on `test/runner-loopback-integration-20261029`.
- New `test_loopback_semantic_review_task_is_preflighted_without_network` verifies literal loopback endpoint normalization, reviewed runner task dispatch, and failed semantic-review propagation into the overall acceptance report. The test mocks task execution and makes no real provider request.
- The integration candidate includes loopback proxy-bypass mock-server tests, safe runner, and output alias regression. Workflow lookup for the new head returned no PR-triggered runs at inspection time; CI pass remains **unverified**. A commit workflow lookup alone is insufficient to assess push-triggered runs.
- PR stays draft; no merge or release.


### Independent consumer pilot: clamp (2026-10-29)

- Consumer repository: `wosafety0/wosafety0clamp`; trial PR #14: https://github.com/wosafety0/wosafety0clamp/pull/14.
- Consumer branch: `feat/harness-trial-gate-20261029`; reusable workflow pinned to this repository's exact tested commit `827bb99d2eb97ac61909979094f68471f081150b`.
- Verified consumer run [40798692801](https://github.com/wosafety0/wosafety0clamp/actions/runs/40798692801) and repeat run [40798667539](https://github.com/wosafety0/wosafety0clamp/actions/runs/40798667539) both completed successfully. Checkout, Python 3.12 setup, and the consumer-owned Node static tests + Python compile + offline unittest command all passed.
- Result: the reusable workflow is proven to run in one independent consumer repository for the configured offline acceptance suite. This is a successful integration pilot, not a general release or real-model validation.
- Boundaries: consumer PR remains draft/unmerged; the consumer's existing CI remains unchanged; no game operations or provider API calls were made.
