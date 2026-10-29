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
- Branch: `fix/local-loopback-model-endpoint-20261028`; tested head: `0b86ce1066e84c6056ec3eb5daa5329ce746c99a`.
- Changed `validate_model_config` to allow HTTPS for remote providers and HTTP only for literal loopback IPs (IPv4/IPv6). Hostname-based `localhost`, non-loopback HTTP, embedded URL credentials, query strings, fragments, malformed ports, and control characters remain rejected.
- Added offline tests for `http://127.0.0.1:1235/v1` and `http://[::1]:1235/v1`, and retained negative tests for unsafe HTTP endpoints. Updated `docs/STABLE_ACCEPTANCE_CONTRACT.md`.
- Hosted CI run [40716125120](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40716125120), run number 144, succeeded on the exact tested head. 90 offline tests passed, the acceptance report uploaded (artifact ID `12829135525`), and the final gate passed.
- This validates configuration parsing and security boundaries only. It does not constitute a live model request or prove that the user's local LM Studio endpoint is reachable from this environment. PR #12 remains draft and unmerged.

### Semantic-review redirect credential-leak fix (2026-10-29)

- During a local, isolated two-server reproduction, Python's default `urllib` behavior followed a model-endpoint HTTP 302 and forwarded the original `Authorization: Bearer ...` header to the redirect destination. The reproduction used only a disposable test token and local loopback listeners; no provider or user credential was involved.
- Added `_NoRedirectHandler` to reject redirects for both HTTPS provider requests and literal-loopback HTTP requests. Loopback requests still use a request-scoped empty `ProxyHandler`; no global proxy settings are changed.
- Updated `docs/STABLE_ACCEPTANCE_CONTRACT.md` to make redirect rejection an explicit fail-closed requirement; contract update commit: `50f814fce8cef6e9b3d9e10294255c06d5de44c3`.
- Added an offline loopback regression test that returns a redirect to a second local listener and asserts the destination receives no request. Updated transport mocks to use the explicit opener.
- PR #22: https://github.com/wosafety0/dev-workflow-kit/pull/22, Draft and unmerged. Tested source head before this archive update: `1443f15c578e4ea0862458d94aebdf77427701cd`.
- Exact-head push CI [run 40803605132](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40803605132) and PR-context CI [run 40803630242](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40803630242) both completed successfully. The PR-context job passed Python compilation, the offline contract suite, report generation, artifact upload, and the final gate.
- Verification boundary: this proves the redirect rejection behavior with local offline tests and the repo's CI. No real model provider request was made; no PR was merged and no release or deployment occurred.
- Follow-up exact-head verification: commit `9586439a74cc8c7a25dbdac89308111ff7f32865` passed push CI [40803733451](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40803733451) and PR-context CI [40803740841](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40803740841); both succeeded with **106 offline tests passed**, report generation, artifact upload, and final gate. These runs include the updated contract and the progress archive as committed on that head.

### Runner fail-fast and semantic-review ordering (2026-10-29)

- Follow-up static review found that the runner continued to later tasks after a failure. With `python-unittest` followed by `semantic-review`, this could make a model request even after the earlier local checks had failed.
- The runner now requires `semantic-review` to be the final configured task and stops after the first failed task. Remaining tasks are recorded as `not_run`; the report remains failed. All task arguments are still preflighted before any task executes.
- Added regression tests for both fail-fast behavior and rejection of a configuration that places semantic review before local tests. Updated `docs/HARNESS_RUNNER_V1.md` to match the behavior.
- Work is isolated on branch `fix/runner-stop-after-failure-20261029`, based on redirect-security candidate head `f71025d2303737dafe18ae823f93cad9cdd1249d`, and is tracked in Draft PR #23: https://github.com/wosafety0/dev-workflow-kit/pull/23. Exact tested code head before the CI-trigger adjustment `570738181f9224274bed3269c41ec4575524d690` passed push CI [run 40804237438](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40804237438): Python compilation, **108 offline tests**, report generation, artifact upload, and final gate all succeeded.
- Safety boundary: this change reduces unnecessary model calls after a failing prerequisite; it does not itself call a provider, execute game actions, merge, release, or deploy.
- Exact-head verification for `875d78882c499419a5bf32104393bf28408e5306`: push CI [40804336760](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40804336760) and PR-context CI [40804344244](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40804344244) both succeeded; each passed Python compilation, **108 offline tests**, report generation, artifact upload, and the final gate.
- CI trigger review found that `pull_request` events did not include base branches matching `fix/**`, so PRs targeting fix branches could miss PR-context checks. Added `fix/**` to `.github/workflows/ci.yml`; the workflow change is under exact-head push CI validation. The current PR's base branch predates this trigger change, so no PR-context run is claimed from that change alone.

### HTTPS redirect-handler regression coverage (2026-10-29)

- The redirect security fix already uses the same `_NoRedirectHandler` for HTTPS and literal-loopback HTTP. The two-server credential-forwarding regression specifically exercised loopback HTTP, so added a separate HTTPS-path test to prevent future removal of the redirect handler from that code path.
- The new offline test asserts `call_model` installs `_NoRedirectHandler` for an HTTPS endpoint and that the handler refuses a redirect. It uses a mocked response and a non-routable `.invalid` hostname; no network request or credential is used.
- Isolated follow-up branch: `test/https-redirect-handler-20261029`, based on the fail-fast candidate head `7962697d273e04716e71fcf95536154b03704032`, tracked in Draft PR #24: https://github.com/wosafety0/dev-workflow-kit/pull/24.
- Exact tested head `afe632edc0f5fdcef3d57289d8ef6da472f49365` passed push CI [40805356218](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40805356218) and PR-context CI [40805372630](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40805372630); both passed Python compilation, **109 offline tests**, redacted report generation, artifact upload, and final gate. The progress archive update itself will receive a new exact-head run.
- No merge, live model call, game operation, release, or deployment.

### Runner stale-report invalidation (2026-10-29)

- Combined review of the stacked runner/transport fixes identified a report-consumer hazard: when a prior invocation wrote a `passed` artifact and a later invocation failed during configuration preflight, the old report remained on disk. A downstream consumer that read only the artifact could mistake the stale result for the current run.
- The runner now validates the report output location and unlinks an existing report before reading or validating the config. Added offline regressions for invalid JSON and missing semantic-review arguments; both require exit code 2, no task execution, and absence of the stale report. Updated the runner contract document.
- Isolated Draft follow-up branch `fix/runner-stale-report-20261029` based on HTTPS regression candidate `58702b8ba7e7fde2c384671677aec8784f216c97`. No provider request, live game operation, merge, release, or deployment. CI evidence must be verified separately.


### Stale semantic-review output invalidation (2026-10-29)

- Combined runner review found a second artifact-only consumer hazard: a prior `PASS` semantic-review output could survive when an earlier local task fails and semantic review is marked `not_run`.
- The runner now unlinks a pre-existing semantic-review output after validating paths and before launching tasks. Added an offline regression with a pre-existing `PASS` review artifact, a failed first task, `semantic-review: not_run`, and an assertion that the stale artifact is absent. Updated `docs/HARNESS_RUNNER_V1.md`.
- Follow-up branch `fix/runner-stale-review-artifact-20261029` is stacked on stale acceptance report candidate `80c1be685de2ca521418aa5622da02eb62911ad1`. No live model requests, game actions, merges, releases, or deployments. CI evidence tracked separately.

## 2026-10-29 — early preflight stale-report invalidation (PR #27)

- Reviewed runner preflight order after PR #26 and identified that timeout validation and config-path resolution occurred before previous acceptance-report invalidation; a prior PASS could survive these blocked runs.
- Draft PR #27 (`fix/runner-early-stale-report-20261029`) moves report invalidation immediately after validating the project root and report output path, before timeout and other input-path preflight. Added two offline regressions and updated `docs/HARNESS_RUNNER_V1.md`.
- Exact code/docs head before this archive: `386b032745e6649d017e20871fd35e8ab6eca5fd`; push CI run `40810871038` completed successfully. PR-context run `40810887822` was still in progress at observation; not yet claimed passed.
- Limits: argparse failure, invalid project root, and invalid report path cannot guarantee artifact invalidation. Consumers must check exit code, report status, and commit identity. No live model request, game action, deployment, or merge.

## 2026-10-29 — report/config collision preservation (PR #28)

- Reviewed PR #27's earlier invalidation order and identified a destructive edge case: a caller could specify the same existing `artifacts/` file for `--config` and `--report-output`; unlink happened before the equality check.
- Draft PR #28 resolves config path and checks report/config equality before deleting the old report. Invalid config path still invalidates a safely resolved report, and timeout validation still occurs after invalidation.
- Added an offline regression that verifies the config file remains byte-for-byte unchanged and no task runs. Updated the runner contract documentation.
- Pre-archive code/docs head: `7cbc16cd63f8125dbd2b25c40f31f8292f32d198`. CI result not yet asserted. No live model calls, game actions, merge, or deployment.

## 2026-10-29 — acceptance report consumer identity verifier (PR #29)

- Verified PR #28 archived head `026b0d4d31bc22f2b46fe1f05a7e09e1909ab126` had successful push run `40811076003` and PR run `40811082217`.
- Added `scripts/verify_acceptance_report.py` and offline tests for expected commit SHA, reviewed contract pin, all-passed tasks, strict schema, and malformed identity. Consumer must independently check runner exit code and use trusted expected SHA/pin; report-content verification does not prove artifact provenance.
- Documentation updated. Code/docs head before this archive: `11d48221b27daa128b931410442bb86e3b1c3163`; CI not yet asserted for that head. No live provider requests, game actions, merge, or deployment.

- Follow-up validation: added subprocess-level CLI tests covering successful matching report verification, stale expected SHA, missing report, and malformed JSON. This verifies the actual command-line exit behavior, not only the pure validation function. CI pending for the new test commit.


### 2026-10-29: enforce acceptance report verification in Harness CI

- Follow-up branch: `feat/ci-enforce-report-verifier-20261029`, based on report-verifier PR #29 head `514f4f979a470c77b5a55ee699cbedd435e4857a`.
- Integrated `scripts/verify_acceptance_report.py` into `.github/workflows/ci.yml`. The verifier runs even after earlier failures, checks the generated report against trusted `github.sha` and the contract SHA-256 produced by the workflow, and its outcome is now a fourth required stage in `scripts/ci_gate.py`.
- Expanded `tests/test_ci_gate.py` for four required outcomes, missing/extra arguments, and verifier failure. Updated the runner consumer contract to distinguish toolkit CI enforcement from consumer responsibilities.
- Safety property: a missing, malformed, failed, stale-commit, or wrong-rules-pin report cannot open the final CI gate. The downstream caller must still check the runner process exit code and artifact provenance independently.
- After fixing the test-loop error, Push CI [40812321192](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40812321192) and PR CI [40812325841](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40812325841) both completed successfully for exact head `0f7ef64273b9ad53cc193509ca78d535d0e04ead`. The hosted job shows the report-verification step and final gate both succeeded. A documentation-only archive update follows; its new head must also be checked before calling the branch fully current.
- PRs remain draft/unmerged. No model-provider calls, game actions, releases, or deployments were performed.

- First hosted run on intermediate commit `26685fc91aed5809bd43dc642899a37300ca32a1` correctly exposed a test-loop indexing error (the new four-stage gate test iterated seven invalid values as stage indices). The implementation gate stayed closed. Fixed the test to exercise every invalid outcome at each of the four stages in commit `b329a5c3fbf3a6f4e1c163a9cafaecffe1debb4f`; final-head CI is pending.


### 2026-10-29: reusable consumer report identity verification

- Follow-up branch: `feat/reusable-consumer-report-verifier-20261029`, stacked on PR #30.
- Added `scripts/verify_consumer_acceptance_report.py` and offline tests for strict schema, consumer commit SHA, caller workflow ref/SHA, failed/skipped stages, missing/corrupt JSON, and subprocess CLI failure behavior.
- Updated `.github/workflows/reusable-acceptance.yml` to support the `python` and `node` runtimes, include runtime validation in the redacted report, verify the report against trusted caller GitHub context, and require runtime, command, report, artifact upload, and verification outcomes all to succeed.
- Added `docs/REUSABLE_ACCEPTANCE_CONTRACT.md` describing the consumer report schema, immutable pin requirement, and the limits of report-only evidence.
- This does not change Clamp PR #14's existing immutable workflow pin. The updated reusable workflow applies only to consumers that explicitly pin a commit containing this implementation.
- Exact implementation/documentation head `07b8000ab8c2a1dad0f91bd29e2d84028bec2c93` passed Push CI [40813229844](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40813229844) and PR CI [40813238148](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40813238148). This validates the verifier tests and Python source compilation in hosted CI. The immutable reusable-workflow commit selected for consumer trial is this verified head; a documentation-only archive follow-up will have its own CI run.


- Consumer integration exposed a real workspace-boundary bug: the reusable job checks out the consumer repository, so it cannot execute the verifier script stored only in the Harness repository. The first Clamp run on the new pin failed closed at verification for that reason; consumer tests themselves passed.
- Corrected `.github/workflows/reusable-acceptance.yml` to run the fail-closed report check inline in the reusable workflow job, avoiding a nonexistent consumer-workspace script path. Added `tests/test_reusable_acceptance_workflow.py`, which extracts and executes the actual inline verifier and checks matching-report success plus stale-SHA/failed-report rejection.
- The correction is in commit `a7045103c4213e90d8a622dbe5918c6b15aa8f0a`; hosted Push and PR CI for the corrected final head is pending. The previously selected immutable pin `07b8000ab8c2a1dad0f91bd29e2d84028bec2c93` is known to contain the defect and must not be reused by consumers.

- The first test of the inline verifier extractor failed because its test helper rejected blank lines in the YAML block; the production verifier itself passed the matching-report case and rejected stale/failed reports. Fixed the extractor to preserve blank lines in commit `ef7aebb7875bcd2dedf4e49fed68404150e1722c`. CI for the corrected test and final archive head is pending.

- A second hosted test run showed the extractor still included the shell heredoc launcher instead of only its embedded Python source. Corrected the test helper to begin after `python3 - <<'PY'` in commit `01c60a4bcf2dff0ee143a93bdd5062aa475a4e74`; the workflow's inline verifier itself had succeeded on the valid and invalid report cases. Re-run final-head CI before selecting a new consumer pin.

- Final corrected/archive head `0173c597e82364a91e50f9817a9c8d40876dc04c` passed Push CI [40813501693](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40813501693) and PR CI [40813508518](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40813508518). The tests execute the exact inline verifier code extracted from the reusable workflow; the matching report passes and stale identity/failed status are rejected. This is the first verified candidate pin after correcting the consumer workspace boundary.


## 2026-10-29 — reusable consumer report verifier edge-case coverage

- Extended `tests/test_reusable_acceptance_workflow.py` to execute the exact inline verifier from `.github/workflows/reusable-acceptance.yml` against mismatched caller workflow ref/SHA, empty test maps, unknown fields, boolean schema version, blank test names, skipped status, missing report, and malformed JSON.
- This is static/offline validation only; it does not execute consumer project actions. Test commit `fa7740e05af7b411ddce186d860434981bddda8a` passed hosted Push CI [40814889244](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40814889244) and PR CI [40814894902](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40814894902). These checks cover the exact code/test commit; progress-only archive commits followed at `8be6cb62c59ec355ca42ad32b1d193bba0dc68d0` and final archive head `ce91ef51f18f4a8c4aeb162f5e956e244e051874`.
- Keep all stacked PRs Draft/unmerged. No model calls, game actions, release, or deployment.


## 2026-10-29 — consumer contract review and Clamp trial metadata reconciliation

- Reviewed the reusable consumer-report contract end-to-end: report generation derives consumer commit and caller workflow identity from GitHub context; the inline verifier compares all three identity values, enforces exact schema, requires a non-empty all-passed test map, and rejects missing/corrupt JSON. The final orchestration gate independently requires runtime validation, consumer command, report generation, artifact upload, and verification to succeed.
- Kept the reusable workflow's verifier self-contained. It must not invoke a verifier script from the consumer checkout; that integration pattern previously failed because the helper is not present in the consumer repository. The helper script remains separately unit-tested, while workflow tests execute the actual inline verifier source.
- Clamp PR #14 description was reconciled to the current immutable pin `0173c597e82364a91e50f9817a9c8d40876dc04c` and exact-head CI evidence. Clamp exact-head Push CI [40813942417](https://github.com/wosafety0/wosafety0clamp/actions/runs/40813942417) and PR CI [40813945988](https://github.com/wosafety0/wosafety0clamp/actions/runs/40813945988) passed for head `887eb1ff23fd04207f52707fa7323f7bf93a2b0e`.
- Current Harness PR #29, #30, and #31, plus Clamp PR #14, remain Draft/unmerged. No live model calls, game actions, release, or deployment.

## 2026-10-29 — reusable workflow documentation consistency review

- Reviewed the consumer-facing reusable workflow guide against the actual `.github/workflows/reusable-acceptance.yml` implementation.
- Corrected two documentation mismatches: the workflow uploads a redacted acceptance-report artifact with 14-day retention (it does not publish releases/packages), and the current third-party actions are pinned to full commit SHAs rather than version tags.
- This is documentation-only; runtime behavior is unchanged. Exact-head CI must be checked after this archive commit. PR #31 remains Draft/unmerged; no live model calls, game actions, release, or deployment.


## 2026-10-29 — stacked runner and verifier CI reconciliation

- Re-checked current PR metadata and exact-head check runs for the runner/report-verifier stack. PR #27 head `072f8cd042f3069a2e2b31b9e9eff5368a77d4f8`, PR #28 head `026b0d4d31bc22f2b46fe1f05a7e09e1909ab126`, PR #29 head `514f4f979a470c77b5a55ee699cbedd435e4857a`, PR #30 head `8b2d33d2c2dddaf4134ec335b9dfb43d0f443d24`, and PR #31 head `0a21cb642d8bbb94223d7ae21b6e5ddc17f27f71` all remain open, Draft, and unmerged; each current head has successful hosted offline-tests check runs.
- PR #27 exact-head push/PR-context runs include [40811019802](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40811019802) and [40810916386](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40810916386). PR #28 exact-head push/PR-context runs [40811457560](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40811457560) and [40811082217](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40811082217) both passed. PR #28 description was updated to reflect the verified results.
- PR #29 exact-head push/PR-context runs [40812225939](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40812225939) and [40811638223](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40811638223) passed. PR #30 exact-head push/PR-context runs [40812364189](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40812364189) and [40812371458](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40812371458) passed. PR #31 current exact-head push/PR-context runs [40815828525](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40815828525) and [40815832720](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40815832720) passed.
- Static review of the runner's current preflight confirms it checks config/report and review input/output collisions before stale-report unlinking; the collision regression checks byte-for-byte config preservation and asserts no task runs. The runner returns distinct codes for passed tasks/report (0), task failure (1), and blocked/preflight/report-write failure (2). Downstream callers must still check that process exit code independently of report JSON.
- Stack relationship remains intentional: #27 → #28 → #29 → #30 → #31. PR #31's self-contained inline verifier remains necessary because the reusable job checks out the consumer workspace, not the Harness repository. Clamp PR #14 stays on its previously validated immutable pin; no pin change is needed from this review.
- Validation boundary: hosted CI establishes offline tests and workflow checks only. No real model request, game operation, deployment, release, or merge was performed. Local working-tree synchronization remains unverified.


## 2026-10-29 — open-PR dependency graph audit

- Re-read current open PR metadata for Harness PRs #13–#31 and checked current branch head/base SHAs. The repository is a dependency graph, not one simple linear stack: #13 is the safe-runner foundation; #14 and #18 form one runner-artifact/provenance line; #19 and #20 are separate branches based on #13; #15 → #17 is a model-response/redirect line; #20 → #22 → #23 → #24 → #25 → #26 → #27 → #28 → #29 → #30 → #31 is the loopback/transport, fail-fast, stale-artifact and report-verification line. All inspected PRs remain Draft and unmerged, and GitHub reports them mergeable at the time of review.
- Exact-head offline-tests checks were confirmed successful for PR #13 head `8dd0e4b58cdf7384ebe703b8fd076ec97e98fd72`, #14 `b0da9892f393f5219ef7f445327af7da893cd827`, #15 `3fff9561088d720cbea2223f69355de3b70f474e`, #17 `703a344f271dda5f304272c615c320943aabba2d`, #18 `b402101ef41d3f9d4f9533545ea83128ba5843a6`, #19 `956b43939dc010f7a62561d8e1f7ceb766b61b68`, #20 `827bb99d2eb97ac61909979094f68471f081150b`, and #22 `f71025d2303737dafe18ae823f93cad9cdd1249d`. Latest #23–#31 dependency SHAs were also rechecked; #31 archive head `0dcde172bd4573ad9e8e81279b0e91611fa52f50` has successful Push CI [40818091542](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40818091542) and PR CI [40818096294](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40818096294).
- Integration risk found: PR #17 and PR #22 independently implement the same semantic-review redirect rejection contract in different branches. #17 is stacked on #15 (response-size limit), while #22 is stacked on #20 (loopback runner integration). Before merging either line into the same target, reconcile the overlapping redirect-handler implementation/tests to avoid duplicate or conflicting edits; do not treat all open PRs as a single serial merge queue.
- Other parallel branches (#19 output alias, #18 commit provenance, #14 stale artifacts) depend on different bases. Merge order must follow the actual DAG and each PR's current base SHA; do not bulk-merge solely by PR number.
- This was a metadata/diff/CI review and documentation-only archive. No merge, provider request, game operation, release, or deployment occurred. Local working-tree synchronization remains unverified.


## 2026-10-29 — follow-up exact-head audit and PR status correction

- Re-read GitHub PR metadata and commit check-runs for the current Harness runner/verifier branches. Exact current heads with successful `offline-tests` checks: #18 `b402101ef41d3f9d4f9533545ea83128ba5843a6`, #19 `956b43939dc010f7a62561d8e1f7ceb766b61b68`, #20 `827bb99d2eb97ac61909979094f68471f081150b`, #22 `f71025d2303737dafe18ae823f93cad9cdd1249d`, #23 `7962697d273e04716e71fcf95536154b03704032`, #24 `58702b8ba7e7fde2c384671677aec8784f216c97`, #25 `80c1be685de2ca521418aa5622da02eb62911ad1`, #26 `06436a9ca9636565cd0d0dbb3abb233dd95227c7`, #27 `072f8cd042f3069a2e2b31b9e9eff5368a77d4f8`, #28 `026b0d4d31bc22f2b46fe1f05a7e09e1909ab126`, #29 `514f4f979a470c77b5a55ee699cbedd435e4857a`, #30 `8b2d33d2c2dddaf4134ec335b9dfb43d0f443d24`, and #31 `b1a3eb67d014a362115db3f9dfc4db31096bd486`. PR #31's exact-head checks are Push CI [40818564511](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40818564511) and PR CI [40818570117](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40818570117). These are offline/hosted workflow checks, not live-provider validation.
- PR #21 (`test: verify reusable workflow rejects empty consumer command`) is **closed and unmerged**, unlike the open Draft PRs in the dependency graph. The earlier broad wording that all PRs #13–#31 were open is too broad; evaluate state per PR. PR #13–#20 and #22–#31 remain open/Draft/unmerged at this audit, subject to later changes.
- Dependency graph remains non-linear: #13 is the safe-runner foundation; #14 and #18 form a runner artifact/provenance line; #19 and #20 branch from #13; #15 → #17 is a response-size/redirect line; #20 → #22 → #23 → #24 → #25 → #26 → #27 → #28 → #29 → #30 → #31 is the loopback transport, fail-fast, stale-artifact, and report-verification line. PR #17 and #22 overlap on redirect rejection and must be reconciled if their lines converge; no topology changes were made.
- Regression chain review: #25 invalidates stale acceptance reports before config preflight; #26 invalidates stale semantic-review PASS artifacts when review is skipped; #27 moves report invalidation earlier to cover additional preflight failures; #28 prevents the report output from deleting a colliding config; #29 verifies report identity/status/schema; #30 makes verification a required CI gate; #31 keeps the reusable workflow verifier inline because the consumer checkout does not contain the Harness helper script.
- No PR was merged or closed by this audit. No model-provider request, game action, release, or deployment occurred. Local working-tree synchronization remains unverified.


## 2026-10-29 — redirect-fix convergence review and foundation CI refresh

- Rechecked current exact-head offline-tests runs for PRs #13–#20. Successful checks are recorded for #13 `8dd0e4b58cdf7384ebe703b8fd076ec97e98fd72`, #14 `b0da9892f393f5219ef7f445327af7da893cd827`, #15 `3fff9561088d720cbea2223f69355de3b70f474e`, #16 `4b6349469c7c5a3fe55da43b27092348435a86c3`, #17 `703a344f271dda5f304272c615c320943aabba2d`, #18 `b402101ef41d3f9d4f9533545ea83128ba5843a6`, #19 `956b43939dc010f7a62561d8e1f7ceb766b61b68`, and #20 `827bb99d2eb97ac61909979094f68471f081150b`.
- Reviewed the actual redirect patches in #17 and #22. Both fail closed by returning `None` from a `urllib.request.HTTPRedirectHandler`, but they implement the opener path differently: #17 centralizes endpoint-specific opener setup in `_open_model_request(request, endpoint)` and keeps the response-size limit from its #15 ancestry; #22 adds the redirect handler directly in `call_model` on the #20 loopback branch. Both have a local two-server regression test proving the redirect destination is not contacted. Their security intent is equivalent, but their helper/mocking edits overlap.
- Non-destructive convergence recommendation for a future shared branch: retain one endpoint-aware request-opening helper (the #17 structure is easier to test and keeps proxy handling localized), carry forward #22's explicit two-listener credential-forwarding regression and contract text, and rerun the complete offline suite against the combined final head. This is a review recommendation only; no branch was rebased, retargeted, merged, or closed.
- Current status remains Draft/unmerged. CI proves offline tests only; no live provider request, game operation, release, or deployment occurred. Local working-tree synchronization remains unverified.


## 2026-10-29 — require the complete consumer report stage set

- Static contract review found that the inline report verifier accepted any non-empty all-passed test map, even if a required stage was omitted or an unknown stage substituted. The final workflow gate separately checked both actual stage outcomes, so this did not bypass the execution gate, but the report verifier was weaker than its documented contract.
- Tightened the inline verifier to require exactly `runtime-validation` and `consumer-acceptance-command`; added regressions for a missing required stage and an unexpected stage, and clarified the report contract.
- This is an offline contract-hardening change only. No provider requests, game actions, deployment, release, or merge.


## 2026-10-29 — parallel reusable-workflow branch compatibility review

- Reviewed open Draft PR #8 at exact head `ed9fccc0f510a1d4c0656589ae57e0a3ff6a4586`; its exact-head `offline-tests` check passed: [run 40801233092](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40801233092).
- Static contract comparison found that PR #8 emits a report with only `consumer-acceptance-command` and has no `runtime-validation` report stage, while current PR #31 verifier requires exactly `runtime-validation` and `consumer-acceptance-command`. Therefore these report/workflow revisions are not contract-compatible as-is; passing PR #8 CI proves its offline tests, not compatibility with the newer PR #31 verifier.
- PR #8 and PR #31 are separate open Draft branches with different ancestry. Do not combine their workflow files without reconciling the schema and stage semantics. No retarget, rebase, close, merge, or consumer pin change was performed.
- The current PR #31 chain remains the newer report-verification path for the consumer pilot. Keep PR #8 as an explicitly unresolved parallel candidate until its intended role is decided through the normal review/integration plan.


## 2026-10-29 — cross-branch runner safety finding (#32)

- Separate review of the runner branch chain found that PR #14 → #18 did not inherit PR #19's review-output/config alias guard. This was material because stale-artifact cleanup can delete the output path before config parsing; if both paths alias inside `artifacts/`, it could delete the config and block the run.
- Follow-up PR #32 adds the guard before cleanup, a byte-preservation regression, and a security-boundary note. It is stacked on PR #18 (`fix/runner-commit-provenance-20261029`), not on the reusable-workflow PR #31 chain; do not treat it as merged into the current consumer-report verifier line.
- PR #32 code head `8c02d63aea03a3705cb75783b57182f713eb2185` passed Push CI [run 40821391073](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40821391073), 108 offline tests. Its subsequent progress-archive head `8223a68ece83fbaf1d92e01aa2146016aee54284` also passed exact-head Push CI [run 40821497469](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40821497469), 108 offline tests.
- PR #32 remains Draft/unmerged; PR #19 remains a separate Draft line. No PR merge, rebase, retarget, consumer pin change, live model call, game operation, deployment, or release was performed.


## 2026-10-29 — reject duplicate JSON keys in acceptance reports

- Review of the standalone report verifier and reusable consumer workflow found that Python's default JSON decoder silently accepts duplicate object keys, keeping the last value. The report producers currently emit ordinary JSON, but strict verification should reject ambiguous input rather than rely on producer behavior.
- Added duplicate-key rejection to both the standalone verifier and the inline consumer workflow verifier; added CLI and extracted-inline-workflow regressions for duplicate top-level and nested `tests` keys; updated the reusable acceptance contract.
- Code commit `c989f2e75a0960aae16468c7afc6f9365cda6495` passed exact-head Push CI [run 40821977266](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40821977266) and PR CI [run 40821983450](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40821983450); both ran 138 offline tests successfully, including the standalone verifier and extracted inline-workflow regressions. The subsequent progress-only archive commit has its own CI run in progress at archive time. No live model calls, game actions, deployment, release, or merge.


## 2026-10-29 — bind acceptance report tool identity and normalize report names

- Follow-up review found that the standalone runner report verifier accepted any non-empty `tool_version` and accepted test names with surrounding whitespace. Tightened it to require `tool_version` to equal `dev-workflow-kit@<expected commit SHA>` and to reject empty or untrimmed test names.
- The first strict-verifier run correctly failed because the CI report producer used `dev-workflow-kit@<SHA>` while the runner emitted `dev-workflow-kit/harness-runner@<SHA>`. This exposed a producer-contract inconsistency; the fix was not to weaken verification, but to standardize the runner on the CI report's commit-bound identity and add an explicit runner regression assertion.
- Final code head `d9eb1df62a7e0c8b9a5d956dfa72fb17302078f7` passed exact-head Push CI [run 40822974635](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40822974635) and PR CI [run 40822982587](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40822982587). Push logs confirm 140 offline tests passed, the acceptance report verified, and the orchestration gate passed.
- The progress-only archive update that follows must also pass exact-head CI before this archive is considered fully validated. PR #31 remains Draft/unmerged. No live model calls, game actions, deployment, release, or merge occurred; local working-tree synchronization remains unverified.


## 2026-10-29 — revalidated strict report tool identity after branch-head drift

- A later branch-head audit found the CI producer and verifier identity strings had drifted again: the verifier's active contract requires `dev-workflow-kit/harness-runner@<expected SHA>`. The CI producer and contract documentation were realigned to that exact form, and the workflow regression asserts the producer string.
- Exact latest code head: `4743a0f762c34d59cb46763bc651e14993a8520f`.
- Exact-head Push CI passed: https://github.com/wosafety0/dev-workflow-kit/actions/runs/40823472625.
- Exact-head PR CI passed: https://github.com/wosafety0/dev-workflow-kit/actions/runs/40823479931.
- Both checks passed the 141-test offline suite and final report-verification gate. Earlier failing runs are retained as evidence of the contract mismatch; they are not counted as passing validation.
- PR #31 remains Draft/open/unmerged. No branch topology changes, live model calls, game actions, deployment, release, or merge.


## 2026-10-29 — align standalone consumer verifier with inline workflow

- A consistency audit found that `scripts/verify_consumer_acceptance_report.py` was weaker than the actual reusable workflow: its CLI accepted duplicate JSON keys, and its verifier accepted any non-empty test map instead of requiring exactly `runtime-validation` and `consumer-acceptance-command`.
- Hardened the standalone helper to reject duplicate object keys during JSON parsing, require the exact two-stage set, and reject blank/untrimmed test names. Added regressions for missing/extra stages and duplicate top-level/nested keys. The reusable workflow remains self-contained; it does not call this helper from the consumer checkout.
- Exact code head `ce76a71d5378ffdcf2be38ac109e3143738f11ae` passed Push CI [run 40823748577](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40823748577) and PR CI [run 40823754559](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40823754559). Both passed 143 offline tests; logs confirm the report verification and final orchestration gate succeeded.
- Follow-up test-quality review changed the duplicate top-level-key fixture into an otherwise-valid report with two `status` keys, so the test proves duplicate-key rejection rather than merely failing schema validation. Final code head `3bdb1bd0f1cd9546bd26b5b8472fc349e7c26a7b` passed Push CI [run 40823913329](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40823913329) and PR CI [run 40823918724](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40823918724).
- The report identity contract is currently aligned on `dev-workflow-kit/harness-runner@<commit SHA>` across the CI report producer, runner, verifier, and regression tests.
- Fresh local targeted verification passed 28 tests across the standalone report verifier, consumer verifier helper, and extracted inline reusable-workflow verifier; git diff --check passed. PR #31 remains Draft/open/unmerged. No live model calls, game actions, deployment, release, or merge; local working-tree synchronization remains unverified.


## 2026-10-29 — reject duplicate keys in Harness runner configuration

- The runner parsed `harness.json` with Python's default JSON decoder, which silently keeps the last occurrence of duplicate object keys. A crafted config could therefore contain ambiguous command declarations and still be accepted.
- Added duplicate-key rejection at config parsing time and a regression with duplicate `commands` keys where the last value would otherwise be valid. The test confirms the runner fails closed, invalidates any stale PASS report, and executes no task.
- Code head `329103d26c5a57ab3f2c6b9df8b5d9e0f1b6c133` passed exact-head Push CI [run 40824152546](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40824152546) and PR CI [run 40824160320](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40824160320). Both passed 144 offline tests; logs confirm report verification and the final orchestration gate succeeded.
- PR #31 remains Draft/open/unmerged. No live model calls, game actions, deployment, release, or merge; local working-tree synchronization remains unverified.


## 2026-10-29 — reject duplicate JSON keys in semantic review inputs and responses

- Extended fail-closed duplicate-key handling to the semantic-review client. Review input files, the provider's outer chat-completions JSON, and the model's JSON review content now reject duplicate object keys instead of silently keeping the last value.
- Added regressions for duplicate input fields (verifying the model is not called and stale PASS output is removed), duplicate provider response keys, and duplicate model-review fields.
- Final code head `89a7254e45494476665ea50fc5187d0b0ae1c111` passed exact-head Push CI [run 40824547635](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40824547635) and PR CI [run 40824552875](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40824552875). Both passed 145 offline tests; report verification and the final orchestration gate succeeded.
- PR #31 remains Draft/open/unmerged. No live model-provider requests were made by these tests, no game actions, deployment, release, or merge occurred; local working-tree synchronization remains unverified.


## 2026-10-29 — restore bounded model-provider response reads on the report-verifier branch

- Cross-branch comparison confirmed PR #15 had introduced a 1 MiB model-response cap, but the independent #20 → #22 → #31 line did not inherit it. Added the same bound to the current branch: read at most 1 MiB plus one sentinel byte, then fail closed if oversized. Kept duplicate-key rejection for both provider-envelope JSON and model review JSON, and documented the limit in the stable acceptance contract.
- Added a regression proving oversized responses are read only up to the configured bound and cannot produce a passing review.
- Code head `2546705be0c14d38f831934f3491306baf6abf1d` passed exact-head Push CI [run 40824844700](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40824844700) and PR CI [run 40824850667](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40824850667). Both passed 146 offline tests; report verification and the final orchestration gate succeeded.
- This restores the response-size guard without merging or rewriting the separate PR #15/#17 branches. PR #31 remains Draft/open/unmerged. No live model-provider requests, game actions, deployment, release, or merge; local working-tree synchronization remains unverified.

## 2026-10-29 - Windows-safe semantic-review test execution

- Normalized expected temporary-file paths with `Path.resolve()` in runner tests so assertions match Windows long-path/short-path normalization. Updated the local loopback HTTP test to preserve required OS environment (including `SystemRoot`) while explicitly clearing upper/lowercase proxy and `NO_PROXY` variables inside the test only. No machine-wide proxy or environment setting was changed.
- Exact code head `bb1e41be7937ea253a38aa16f3369d8f7d1ec67e` passed the full local Windows suite: **146 tests**, Python compilation, and `git diff --check`.
- Exact-head Push CI [40825108944](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40825108944) and PR CI [40825113981](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40825113981) both passed **146 offline tests**, report generation, artifact upload, strict report verification, and the final gate.
- PR #31 remains Draft/open/unmerged. No live model-provider call, game action, merge, release, or deployment occurred.


## 2026-10-29 — make duplicate-key verifier regressions decisive

- Review found that the standalone Harness report verifier's duplicate-key tests also contained unrelated invalid fields, so they could pass even if duplicate-key rejection regressed.
- Replaced those fixtures with otherwise-valid reports containing duplicate top-level `status` keys and duplicate nested test-status keys. Either fixture would pass verification if Python's default last-key-wins parser were used, so the tests now specifically prove duplicate-key rejection.
- Exact code head `78c6cb326c08dc482c60337a2a771e34ab2939c9` passed Push CI [run 40825814199](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40825814199) and PR CI [run 40825821246](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40825821246). Both passed 146 offline tests; report verification and the final orchestration gate succeeded.
- PR #31 remains Draft/open/unmerged. No live model-provider request, game action, merge, release, or deployment occurred.

## 2026-10-29 - Exact-head Windows verification after semantic-review hardening

- Re-ran the complete offline suite on exact head `e3c457717d1524383c037dc3ec901fedb4e9f5d4`, covering duplicate JSON-key rejection in reports, runner config, and semantic-review inputs/responses; bounded 1 MiB provider response reads; redirect rejection; and reusable consumer-report identity checks. Python compilation passed, **146 tests passed**, and `git diff --check` passed.
- Exact-head Push CI [40825902357](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40825902357) and PR-context CI [40825907701](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40825907701) both succeeded, including report generation, artifact upload, strict report verification, and the final gate.
- This is offline/local-loopback validation only; no external model-provider request was made. PR #31 remains Draft/open/unmerged; no merge, release, deployment, or game action occurred.


## 2026-10-29 — require a clean worktree for commit-bound runner reports

- Audit found that `git rev-parse HEAD` alone does not prove the tested source matches the reported commit: tracked edits and untracked inputs could affect task outcomes while the report still claimed the unchanged HEAD SHA.
- Updated `scripts/harness_runner.py` to require a successful, empty `git status --porcelain --untracked-files=all` result before accepting the HEAD SHA. Dirty or untracked worktrees now fail closed before any configured task executes; the previous acceptance report has already been invalidated by runner preflight.
- Added offline regressions for modified tracked files, untracked files, and clean-worktree SHA resolution; documented the rule in the stable acceptance contract.
- Exact code head `12a85f4cfee8a3e004827233ca63dc5d268e1f7c` passed Push CI [run 40826215546](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40826215546) and PR CI [run 40826223599](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40826223599). Both passed **148 offline tests**, compiled the Python sources, uploaded the redacted acceptance report, verified report identity, and passed the final orchestration gate.
- The guard intentionally rejects untracked review inputs too: a commit SHA cannot truthfully identify an acceptance run whose input file is outside the committed tree. Developers can still run ordinary test commands during active edits; only commit-bound Harness acceptance reporting requires a clean tree. This is an offline validation change only; no live model-provider request, game action, deployment, release, or merge occurred.


## 2026-10-29 — bind consumer reports to the actual reusable Harness workflow

- Audit of GitHub Actions context semantics found that `github.workflow_ref` and `github.workflow_sha` identify the caller context inside a reusable workflow, not the reusable workflow implementation itself. The previous report therefore bound consumer/caller identity but did not explicitly record which Harness workflow definition actually ran.
- Added `harness_workflow_ref` and `harness_workflow_sha` to the consumer report using GitHub's `job.workflow_ref` and `job.workflow_sha` contexts. The inline verifier now compares both fields with those trusted context values and rejects missing, malformed, or mismatched Harness workflow identity.
- Extended exact-inline-verifier tests to cover wrong Harness workflow ref/SHA, and updated the consumer report contract. This uses GitHub.com-specific `job.workflow_*` context fields; GitHub documents these fields as unavailable on GitHub Enterprise Server.
- Exact code head `af86451fc1b56b1f58af765c4a902b268910d243` passed Push CI [run 40826479485](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40826479485) and PR CI [run 40826485217](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40826485217). Both passed **148 offline tests**, including execution of the exact inline verifier with mismatched Harness workflow ref/SHA; report generation, artifact upload, strict verification, and final gate succeeded.
- The change updates only the reusable workflow source and its contract on the Harness feature branch. It does not change Clamp PR #14's existing immutable pin or activate the new contract in consumer repositories. PR #31 remains Draft/unmerged; no merge, deployment, release, live model request, or game action occurred.


## 2026-10-29 — Harness debugging ownership transferred from Clamp to Harness

- User directive: take over Harness debugging associated with the Clamp consumer pilot; do not let the Clamp project perform Harness-related development.
- Recorded the ownership boundary in `docs/REUSABLE_ACCEPTANCE_WORKFLOW.md`: reusable workflow implementation, report schema/verifier, provenance and identity checks, runtime orchestration, artifact handling, gate logic, Harness regression tests, root-cause fixes, and their CI evidence belong in `wosafety0/dev-workflow-kit`.
- Consumer responsibility is limited to its immutable Harness SHA pin, Clamp-owned acceptance command/tests, and minimal consumer integration configuration/documentation. A failing Clamp run is evidence to reproduce and fix in Harness first; only after exact-head Harness Push/PR CI passes should the consumer pin be updated and Clamp CI rerun.
- Posted this explicit boundary to Clamp Draft PR #14: https://github.com/wosafety0/wosafety0clamp/pull/14#issuecomment-6489307339. No Harness implementation changes were made in Clamp, and no Clamp branch or PR was modified by this policy change.
- This policy documentation commit's exact-head Push/PR CI and test counts will be recorded after verification. PR #31 remains Draft/unmerged; no merge, deployment, release, live model request, or game action.
