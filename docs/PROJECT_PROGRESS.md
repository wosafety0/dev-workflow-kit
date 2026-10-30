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


## 2026-10-30 — downstream integration candidate based on PR #24

- Created isolated candidate `integration/pr24-plus-bounded-semantic-review-20261030` from PR #24 exact head `58702b8ba7e7fde2c384671677aec8784f216c97`, preserving PR #23 fail-fast ordering and PR #24's HTTPS redirect-handler regression.
- Selectively carried PR #33's bounded provider-response read (1 MiB plus sentinel byte), duplicate-JSON-key rejection at provider envelope/model content/CLI input boundaries, stable-contract wording, and Windows-resolved path expectations in runner tests.
- Re-composed `tests/test_ai_semantic_review.py` by retaining PR #33 candidate coverage and restoring PR #24's HTTPS redirect-handler test. This branch does not replace PR #32's expanded runner test suite in any future unified branch.
- Validation-only Draft PR; exact-head hosted CI required. No local tests, live provider request, credential use, merge, release, or deployment is claimed.

- Candidate PR opened: [PR #36](https://github.com/wosafety0/dev-workflow-kit/pull/36), Draft/open/unmerged, based on PR #24. Exact final archived head at this checkpoint: `68c58ef4dbcff2072c866b19aa46d3e538a40558`. Exact-head Harness CI run [40990216035](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40990216035) completed successfully: compile, offline contract tests, redacted acceptance report, artifact upload, and final required-stage gate all succeeded.


## 2026-10-30 — combined path/config integrity candidate on PR #36 chain

- Created isolated branch `integration/pr24-pr33-pr32-20261030` from PR #36 exact head `84d7fed0ae91f71d4572572c093b3af7999c3b2b`; no original PR or prior candidate was retargeted or merged.
- Selectively merged PR #32 runner protections into the current PR #24/#33 chain: duplicate-key config rejection, tracked-config requirement, stale-artifact invalidation before config validation, trusted-source/symlink checks, output/config collision guard, and post-task worktree/output revalidation.
- Preserved PR #36's fail-fast execution behavior and semantic-review-last requirement. The runner regression suite starts from PR #32's expanded tests, then restores PR #36's loopback semantic-review test and selectively applies the Windows-resolved path assertions.
- Documentation changes are limited to runner safety and acceptance-contract scope; unrelated historical workflow/docs changes from PR #32's branch are not copied wholesale.
- Candidate implementation head `7b30ae63b8f0e3d1fe5c79daeecde64e80f1fdd3` was followed by workflow-trigger/archive commits; exact pre-archive combined head `299eb3b9e77c1737d132a693c031f22bd50d51f8` passed Harness CI [run 40990589875](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40990589875): compile, all offline contract tests, redacted report generation, artifact upload, and final gate succeeded. This connector did not run local tests. Final archive head receives its own CI check. No real provider call, merge, release, or deployment is claimed.

- CI trigger correction: added `integration/**` to both `push` and `pull_request` target filters because this validation branch namespace was previously excluded. This allows exact-head CI for integration candidates without manual dispatch; original workflow branches and permissions are preserved.


## 2026-10-30 — final unified candidate source/diff audit

- Audited original PR #24/#32/#33 patches and unified Draft PR #37. PR #37 net file list is exactly 8 intended paths: CI workflow, runner guide, progress archive, stable acceptance contract, semantic-review implementation/tests, Harness runner implementation/tests. No unrelated source modules are introduced by the net diff.
- Verified PR #37 `scripts/ai_semantic_review.py` is byte-for-byte identical to the reconstructed PR #33 candidate blob `4a29f02f370704e6b61d2a8ddfe718eb31d99e26`, retaining 1 MiB + sentinel response bounding, duplicate-key rejection, HTTPS redirect refusal, and fail-closed parsing.
- Compared runner test names: all 31 tests from PR #32's candidate suite are present in PR #37; one additional PR #36 loopback preflight test is retained (32 total). Windows-resolved script/input/output assertions are retained.
- Confirmed runner code includes tracked-config enforcement, duplicate-key config parsing, stale report/review invalidation before config validation, source/path symlink rejection, config/output alias checks, fail-fast task ordering, and post-task Git/output integrity revalidation. Hosted CI verifies the current code path, but no local test run or live provider request is claimed.
- Workflow net change only adds `integration/**` to push and pull-request base-branch filters; existing full-SHA-pinned checkout/setup-python actions, read-only contents permission, and final gate remain present. The current PR targets a `test/**` base (already covered by PR filters); the push filter ensures the integration head also receives branch CI.
- Audit conclusion: no missing test method from PR #32's candidate suite was detected in the unified test file. This is a code/diff audit plus hosted CI evidence, not a human approval or merge authorization. PR #37 remains Draft/unmerged; originals #24/#32/#33 and candidates #34–#36 remain untouched and unmerged.


## 2026-10-30 — follow-up audit: restore inherited fail-fast regressions

- A deeper base-to-head test inventory found that the unified PR #37 candidate had unintentionally dropped two tests inherited from the PR #24 base: `test_stops_after_failure_and_marks_remaining_tasks_not_run` and `test_semantic_review_must_be_last_configured_task`. The previous audit statement that all base fail-fast tests were retained was therefore incomplete; this is corrected here.
- Restored both original regression tests without changing the runner implementation. The unified runner test module now contains 34 test methods, includes every one of the 14 test methods from PR #24's base file, all 31 methods from PR #32's candidate suite, and the additional loopback preflight regression. No duplicate test method names were found.
- Exact corrected head `731c39a5a8c9d1a21312b2c959a6e6dc3c732123` passed Harness CI [run 40991595301](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40991595301): Python compilation, all offline contract tests, redacted acceptance report build/upload, and final required-stage gate succeeded.
- This was a source-level inventory plus hosted CI verification; no local tests or live provider requests were run. PR #37 remains Draft/unmerged; original PRs and earlier candidates remain unchanged.


## 2026-10-30 — optional Git-bound semantic-review mode

- Created isolated branch `feat/optional-git-bound-review-20261030` from unified candidate head `d035dea4426e2dbbb39b22770fc206a5671bfc68`; PR #37 and all earlier candidate branches remain unchanged.
- Preserved compatibility mode: caller-supplied semantic-review JSON remains accepted when neither `--review-base` nor `--review-head` is supplied.
- Added opt-in strict mode requiring both full 40-character commit SHAs. The runner verifies both are commit objects, requires the requested head to equal the clean checked-out `HEAD`, derives the merge base and diff directly from Git, bounds Git diff/name-list reads to 4 MiB, replaces caller-provided `diff` and `changed_files`, and validates the generated input against the semantic-review parser before task execution.
- Strict-mode acceptance reports use schema version 2 and include base/head/merge-base SHAs, SHA-256 of the exact Git diff bytes, and changed-file paths. Ordinary compatibility-mode reports remain schema version 1.
- Added regression coverage for caller-diff replacement, generated diff/file-list consistency, malformed review context, checked-out-head mismatch, paired flag requirements, acceptance-report provenance validation, and a runner integration test using a real local Git commit range.
- Exact implementation head before this archive update: `7bfa3ecefa7d712e9c1fcd0bda840f424a3ad905`. Exact-head GitHub Harness CI [run 41003007865](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003007865) completed successfully: Python compilation, offline contract tests, redacted acceptance report generation/upload, and final required-stage gate all passed.
- This is hosted CI evidence; no local tests, live provider request, credential use, merge, release, deployment, or game action is claimed. The archive update will trigger a fresh exact-head CI run.
- Remaining boundaries: strict mode attests the Git diff bytes supplied to the review, not model-review completeness, dependency/runtime identity, or authorization to merge/deploy. Diff/path formats unsupported by the semantic-review parser fail closed.
- Follow-up audit found the first bounded Git-output reader could block while waiting for EOF before reaching its wait timeout. Replaced it with a streaming reader that enforces both the 4 MiB cap and a wall-clock timeout, and added regressions for oversized output and a hung subprocess. These tests passed on exact head `7bfa3ecefa7d712e9c1fcd0bda840f424a3ad905` in CI [run 41003007865](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003007865).
- Progress-archive head `52385cbae39d4ff9af91eaf5c354d2d24a67b342` also passed exact-head Push CI [run 41003043999](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003043999) and PR-context CI [run 41003048700](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003048700). Both completed successfully through report upload and the final required-stage gate.


## 2026-10-30 — acceptance-report path contract follow-up

- During downstream schema-v2 review, found that `scripts/acceptance_report.py` rejected absolute paths, backslashes, control characters, and traversal segments but did not reject Windows drive-prefixed paths such as `C:/outside.py` and `C:relative.py`. The stable acceptance contract already forbids drive prefixes, so the report validator was inconsistent with the contract.
- Updated the report validator to reject drive-prefixed provenance paths and added both forms as regression cases in `tests/test_acceptance_report.py`.
- Exact code head: `4e365c5d501e2b54c5c4e0b93bb20a3ad78771ab`. Exact-head GitHub Push CI [run 41003292886](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003292886) and PR-context CI [run 41003299444](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003299444) both completed successfully. Both run the compile step, full offline contract suite, redacted acceptance-report generation/upload, and final required-stage gate.
- The acceptance report is an allowlisted summary, not a complete provenance attestation: schema v2 structural validation does not independently re-derive Git ancestry or recompute the diff digest. The runner derives those fields from Git before producing the report.
- Hosted CI only; no local test run, live provider request, credentials, merge, release, deployment, or game action is claimed. PR #38 remains Draft and unmerged.


## 2026-10-30 — downstream acceptance contract audit

- Audited acceptance-report consumers and current-facing docs against the schema-v2 implementation.
- Fixed a concrete path-contract gap: schema-v2 provenance validation now rejects Windows drive-prefixed paths (`C:/outside.py`, `C:relative.py`) in addition to absolute paths, backslashes, traversal, controls, whitespace, and duplicates. Regression tests cover both drive-prefix forms.
- Updated `docs/ACCEPTANCE_REPORT_V1.md`: corrected the stale `rules_pin` example (it previously used a digest string rejected by the implementation), defined the exact lowercase SHA-256 shape, and documented the opt-in schema-v2 `review_provenance` extension while preserving schema-v1 compatibility mode.
- Corrected two unrelated but adjacent stale reuse docs: `docs/REUSABLE_ACCEPTANCE_WORKFLOW.md` now accurately says actions inside the reusable workflow are SHA-pinned, and `README.md` describes the current reusable workflow as Python-only rather than Python/Node.
- Exact code/documentation head: `33148f621b06a7fdc71a4cfd74c2004cdc5057a6`. Exact-head GitHub Push CI [run 41003415481](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003415481) and PR-context CI [run 41003420942](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003420942) both succeeded. Both completed Python compilation, the full offline contract suite, redacted acceptance-report generation/upload, and the final required-stage gate.
- Report schema validation is structural only: it validates recorded SHA formats and paths but does not independently recompute Git ancestry or the diff digest. The trusted runner derives the diff/provenance from Git before report construction.
- Hosted CI only; no local tests, live provider requests, credentials, merge, release, deployment, or game action are claimed. PR #38 remains Draft and unmerged.


## 2026-10-30 — acceptance schema documentation precision follow-up

- A second read-through of the report docs found two wording ambiguities: the v1 section described four input fields and six output fields without clearly scoping those statements to schema v1, and the stable contract described `head_sha` as if it were a top-level report field. Clarified that the four-field input/six-field output statements apply to schema v1 and that `review_provenance.head_sha` must equal top-level `commit_sha`.
- Exact latest code/documentation head: `057a99ade806aeab6faa0c923082571dc296852c`. Exact-head GitHub Push CI [run 41003525867](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003525867) and PR-context CI [run 41003530791](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003530791) both completed successfully. Both passed compile, the full offline contract suite, report generation/upload, and the final required-stage gate.
- Prior archive commit `0d1e592cd252fa1924f0ccdbcf474d1ab16a199a` independently passed Push CI [run 41003460146](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003460146) and PR-context CI [run 41003464980](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003464980).
- The report formatter remains a structural validator; the runner is the component that derives and supplies Git provenance. No local tests, live provider request, credentials, merge, release, deployment, or game action is claimed.


## 2026-10-30 — exact-head test and artifact evidence detail

- Inspected the final archive-head Push CI job log for run [41003571772](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003571772): `Ran 158 tests in 2.729s`, `OK`, report status `passed`, artifact upload succeeded, and the final orchestration gate passed. The PR-context run [41003576157](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41003576157) also passed all required stages on the same SHA `cdd5cecf76a8498f0158f2d48042a54b81f6a17b`.
- GitHub Actions artifact metadata identifies artifact ID `12954302746`, name `acceptance-report`, size 366 bytes, and ZIP digest `sha256:1147bf6b1dde880d9fb8e5dcec6f2d272f189e3e0418d3c055dbff20f7943974`. The digest in the job upload log matches the artifact API metadata. The ZIP was not downloaded and independently re-hashed in this audit; do not describe this as independent recomputation.


## 2026-10-30 — strict-review path contract alignment

- Follow-up review of the Git-bound diff → semantic-review validator → schema-v2 report chain found a path-contract mismatch: the report builder rejected every whitespace character, while the stable acceptance contract only requires trimmed repository-relative paths and the semantic-review input validator permits internal spaces. This made valid Git filenames such as `src/my file.py` fail closed during strict review. The semantic diff parser also assumed path headers contained no whitespace.
- Fixed the parser to resolve paths containing spaces against the declared changed-file set; rename paths with spaces are accepted only when explicit rename metadata exactly matches the Git header. Ambiguous/unsupported headers remain rejected.
- Updated schema-v2 provenance path validation to permit internal spaces while continuing to reject leading/trailing whitespace and unsafe path forms. Both path validators now reject Unicode Cc control characters, including C1 controls, rather than checking only ASCII C0/DEL. Added regression tests for internal-space paths, C1 controls, and existing unsafe-path cases.
- Latest implementation head: `518ba6b2ce4843c1b1285c859541d3d43784ec40`. Exact-head Push CI [run 41004069453](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41004069453) and PR-context CI [run 41004076034](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41004076034) both succeeded. The PR-context job log reports `Ran 161 tests in 2.837s`, report status `passed`, and successful final orchestration gate.
- Several intermediate commits intentionally failed CI while regression tests exposed fixture and assertion issues; those were corrected before this verified head. No local test run, live provider request, credentials, merge, release, deployment, or game action is claimed.


## 2026-10-30 — real-Git spaced-path end-to-end verification

- Extended the real-Git-range runner regression to commit both a normal source path and `tests/test file.py`, then exercise strict mode through Git diff generation, semantic-review validation, and schema-v2 report construction.
- Git's unified diff header can append a tab-delimited suffix to a file header. The parser now normalizes that delimiter before comparing paths, and only accepts the simple quoted-space form for paths containing spaces; unsupported/ambiguous quoted paths remain fail-closed. Blocked-run diagnostics remain redacted and do not include raw path values.
- Exact implementation head `0b5eb8cf11239f63d9667cba3066d4887e934d10`: Push CI [run 41004596293](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41004596293) and PR-context CI [run 41004600921](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41004600921) both succeeded. PR-context log reports `Ran 161 tests in 2.580s`, acceptance status `passed`, successful artifact upload, and final required-stage gate success.
- Intermediate CI failures exposed the actual Git header representation and caught a test-diagnostic regression; those were fixed before the verified head. No local test run, live provider request, credentials, merge, release, deployment, or game action is claimed.


## 2026-10-30 — reject incomplete rename metadata in semantic-review diffs

- Continued auditing the compatibility-mode semantic-review parser. It correctly accepted explicit Git rename metadata, but a content-changing diff whose `diff --git` header named different old/new paths could pass without the required `rename from` / `rename to` metadata. Strict Git-bound mode currently uses `--no-renames`, so this was primarily a malformed caller-supplied diff risk in compatibility mode.
- Added structural invariants: rename metadata must be paired; distinct old/new paths require matching rename metadata; identical old/new paths must not claim a rename. File-header consistency checks run before these invariants so existing path-spoofing diagnostics remain specific. Added regression tests for missing and incomplete rename metadata while retaining tests for valid pure/content-changing renames.
- Exact implementation head `f6c220bce593d736a634e814f8552e23682e9c26`: Push CI [run 41005525831](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41005525831) and PR-context CI [run 41005531567](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41005531567) both succeeded. PR-context job log reports `Ran 163 tests in 2.763s`, acceptance status `passed`, artifact upload success, and final required-stage gate success.
- Intermediate CI runs exposed expected-message and fixture-newline mistakes in the new regressions; those were corrected before this verified head. No local test run, live provider request, credentials, merge, release, deployment, or game action is claimed.


## 2026-10-30 — disable Git replacement objects in provenance commands

- Strict-mode review originally relied on Git commands that honored `refs/replace/*`. A repository can keep the worktree clean and `HEAD` unchanged while a replacement ref causes `git diff base head` to read a different commit tree than the object identified by the recorded head SHA. That weakens the intended Git-source binding.
- Added a dedicated Git subprocess environment with `GIT_NO_REPLACE_OBJECTS=1` and applied it to the Runner's Git metadata, worktree, tracked-config, ignored-source, merge-base, diff, and changed-path commands. This ensures provenance is derived from the actual objects named by the commit SHAs, not replacement refs.
- Added a real temporary-Git-repository regression: create a real base/head, install a replacement ref whose tree contains forged content, and verify strict review still derives the diff from the original head object.
- Exact implementation head `11929c11a231123da994ab1008630ef2b3450552`: Push CI [run 41005772744](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41005772744) and PR-context CI [run 41005779128](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41005779128) both succeeded. PR-context job log reports `Ran 164 tests in 2.521s`, acceptance status `passed`, artifact upload success, and final required-stage gate success.
- Intermediate implementation/test commits were verified or corrected before this exact passing head; no local test run, live provider request, credentials, merge, release, deployment, or game action is claimed.

### Git provenance environment isolation (2026-10-30)

- Implementation commit: `c175014e51e2e5deab63b713b30c3ae92bebd0b7`. Git provenance subprocesses discard inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and `GIT_COMMON_DIR` while retaining `GIT_NO_REPLACE_OBJECTS=1`.
- Regression-test commit: `893d7294cb36093f6f078913b513e25d89d88481`. Added a unit test asserting these four overrides are absent from the derived Git environment.
- Exact implementation/test head `893d7294cb36093f6f078913b513e25d89d88481` passed GitHub Actions push run [41006559844](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41006559844) and pull-request run [41006566427](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41006566427).
- Scope remains limited: this does not claim full Git environment isolation, independently attest the runtime, or prove protection against concurrent filesystem mutation. No local tests, live provider requests, credentials, merge, release, deployment, or game actions were performed.

### Git provenance: isolate all inherited Git environment overrides (2026-10-30)

- Implementation commit `4fd2114256c1d97dd50ec4cd503eecb777d801b9`: provenance Git subprocesses discard all inherited `GIT_*` variables and then explicitly set `GIT_NO_REPLACE_OBJECTS=1`; ordinary non-Git process environment remains available.
- Regression-test commit `af18eaf5e5179d7d868eebebeee41fc63eaa2004`: extended environment isolation assertions for Git object directories, alternate objects, and Git config injection variables, alongside repository/worktree/index overrides.
- Exact implementation/test head `af18eaf5e5179d7d868eebebeee41fc63eaa2004` passed GitHub Actions [push run 41007110682](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41007110682) and [PR run 41007112836](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41007112836), both conclusion `success`.
- This does not independently attest the executable, Git config files, runtime, concurrent filesystem mutation, or artifact contents. No local tests, live provider requests, credentials, merge, release, deployment, or game actions are claimed.

### Git-bound semantic review: isolate global Git configuration (2026-10-30)

- Audited the strict review runner after inherited `GIT_*` environment isolation. Found that system/global Git configuration could still influence provenance commands, including a configured `core.fsmonitor` helper.
- Hardened `_git_environment()` to set `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=os.devnull` in addition to clearing inherited `GIT_*` variables and setting `GIT_NO_REPLACE_OBJECTS=1`.
- Disabled `core.fsmonitor` for the Git status invocation used in commit/worktree validation.
- Added regression assertions that verify the isolated environment explicitly sets both Git configuration controls.
- Implementation commit: `e04d3f76d2fa11628612d497b88bffc1dee2df64`. Exact-head Push CI [41010495951](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41010495951) and PR-context CI [41010503402](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41010503402) both succeeded.
- Regression-test commit: `9f3a6b3351b80f9bc64b5cdfd9e22ed6de478855`. Exact-head Push CI [41010765899](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41010765899) and PR-context CI [41010772487](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41010772487) both completed successfully. The PR-context run completed compilation, offline contract tests, redacted acceptance report generation, artifact upload, and the final required-stage gate.
- Verification boundary: this is hosted CI evidence only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.

### Git-bound review: neutralize repository-local binary diff driver settings (2026-10-30)

- Continued the configuration audit after isolating inherited, system, and global Git configuration. A repository-local `diff.<driver>.binary=true` setting combined with a matching `.gitattributes` driver could suppress ordinary text hunks in the generated review diff.
- Added Git's `--text` option to the strict review diff command so tracked textual source changes remain visible even when a local diff driver marks the path as binary. External diff and textconv remain explicitly disabled.
- Added a real temporary-Git-repository regression test that sets `diff.review.binary=true`, assigns that driver to `source.py`, changes the source across two commits, and asserts the generated review diff still includes the added line.
- Implementation commit: `1be7f0044951ea49b110344afbb89a854fb9d43b`.
- Regression-test head: `56127a867fa8c5ee8c281c0021b4b1b729c24714`. Exact-head Push CI [41011071189](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41011071189) and PR-context CI [41011076799](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41011076799) both succeeded. Both runs completed compilation, the offline contract suite, redacted acceptance report generation, artifact upload, and the final required-stage gate.
- Verification boundary: hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.


### Git-bound review: fail closed on changed submodule pointers (2026-10-30)

- Continued the bounded audit of repository-local Git configuration. A local `diff.ignoreSubmodules=all` or `submodule.<name>.ignore=all` setting could otherwise make a submodule pointer change disappear from the strict review diff, while the parent repository's diff does not contain the submodule's internal source.
- Strict review now explicitly uses `--ignore-submodules=none` for raw change metadata, generated diff, and changed-file listing. It inspects bounded raw Git change metadata and rejects changes involving Git mode `160000` with a clear fail-closed error; submodule source is not recursively reviewed by this Harness.
- Added a real temporary-Git-repository regression with a changed submodule commit and both repository-local ignore settings enabled. The test verifies strict review rejects the submodule pointer change rather than treating the commit metadata as a complete source review.
- Exact implementation/test head `c717152db535b1b22b1bcea53e259d55a13f0181` passed GitHub Actions Push CI [run 41011490948](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41011490948) and PR-context CI [run 41011496030](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41011496030). Both ran all 167 offline contract tests successfully and passed the final required-stage gate.
- Verification boundary: hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.

### Git-bound review: reject ambiguous merge bases (2026-10-30)

- Continued the bounded audit of the strict review baseline. Git histories with criss-cross merges can have more than one best common ancestor; selecting one silently would make the review baseline ambiguous.
- Strict mode now runs `git merge-base --all` and proceeds only when exactly one valid SHA is returned. Zero, malformed, or multiple results fail closed with an explicit ambiguous-merge-base error. Compatibility mode is unchanged.
- Added a unit regression for multi-line merge-base output and a real temporary Git repository regression that constructs two criss-cross merge commits, verifies `git merge-base --all` returns both best ancestors, and asserts strict review rejects the range.
- Exact implementation/test head `660a3843430ff6bf109cc8ed33eeeb7b6639fbdd` passed Push CI [run 41012640138](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41012640138) and PR-context CI [run 41012648370](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41012648370). Both ran all 169 offline contract tests successfully and passed the final required-stage gate.
- Verification boundary: hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.

### Git-bound review: isolate ancestry from legacy grafts metadata (2026-10-30)

- Continued auditing repository-local Git metadata that can affect ancestry. The legacy `.git/info/grafts` file can rewrite the parentage Git uses for merge-base calculations even when replace refs are disabled.
- `_git_environment()` now sets `GIT_GRAFT_FILE` to the platform null device, alongside the existing inherited `GIT_*`, replace-ref, system-config, and global-config isolation.
- Added a real temporary-repository regression that writes a graft making the head commit appear root-like, then verifies strict review still derives the true parent commit as the merge base and includes the source change. The environment regression also asserts the graft override.
- Exact implementation/test head `9ab754bafcc791e37b49ea6afc3e7d26e45fde86` passed Push CI [run 41012770557](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41012770557) and PR-context CI [run 41012776765](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41012776765). Both passed the required-stage gate; Push CI ran all 170 offline contract tests successfully.
- Verification boundary: hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.

### Git-bound review: reject shallow repository history (2026-10-30)

- Continued the ancestry audit after isolating replace refs and legacy grafts. A shallow repository marks commits as history boundaries; merge-base can therefore return a baseline derived from incomplete ancestry even when the requested commit objects are present.
- Strict Git-bound review now checks git rev-parse --is-shallow-repository and fails closed unless Git explicitly reports false. Compatibility mode is unchanged.
- Added a real temporary-repository regression that retains both base/head commit objects, marks the head as a shallow boundary via .git/shallow, confirms Git reports a shallow repository, and verifies strict review rejects it before merge-base/diff derivation.
- Exact implementation/test head 32096f2bf2ccbc70007ac9a68414b3acaf3d18c8 passed Push CI [run 41013208958](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41013208958) and PR-context CI [run 41013217001](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41013217001). Both ran all 171 offline contract tests successfully, generated a passed acceptance report, uploaded the report artifact, and passed the final required-stage gate.
- Verification boundary: hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.

### Acceptance clean-worktree gate: detect dirty submodules (2026-10-30)

- Continued the clean-worktree audit after strict review began rejecting submodule pointer changes. Found that the separate acceptance commit-provenance check used git status without overriding repository-local submodule ignore settings. A local submodule ignore rule could therefore hide modifications inside an otherwise unchanged gitlink.
- The worktree status command now explicitly uses --ignore-submodules=none, so dirty submodule contents are visible to the clean-worktree gate. Generated artifacts remain excluded as before.
- Added a real temporary-repository regression: initialize and commit a submodule, modify a tracked file inside it without changing the parent gitlink, set both diff.ignoreSubmodules=all and submodule.deps/sub.ignore=all in the parent repository, and verify the acceptance provenance check rejects the dirty worktree.
- Exact implementation/test head 436e8527030657b47511529d73bf026c840edc80 passed Push CI [run 41013436852](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41013436852) and PR-context CI [run 41013442141](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41013442141). Both ran all 172 offline contract tests successfully, generated a passed acceptance report, uploaded the report artifact, and passed the final required-stage gate.
- Verification boundary: hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.

### Acceptance worktree gate: reject sparse checkouts (2026-10-30)

- Continued the execution-environment audit. A sparse checkout can leave tracked project files absent from the working tree while HEAD still identifies a valid full commit; test discovery may then run against only a subset of the repository.
- The acceptance provenance check now reads the repository's core.sparseCheckout setting and fails closed when sparse checkout is enabled. If Git cannot establish the sparse-checkout state, the gate also fails closed. Normal full worktrees and compatibility-mode review input are unchanged; the guard is in the common acceptance provenance check.
- Added a real Git regression that enables cone-mode sparse checkout, selects only docs/ and scripts/, verifies the tracked tests file is absent, and asserts that acceptance provenance rejects the workspace before tasks run.
- Exact implementation/test head 8c6c422c51ae464b5c1927e7b7a652d9f50b9e82 passed Push CI [run 41013802438](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41013802438) and PR-context CI [run 41013805393](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41013805393). Both ran the complete offline contract suite, built the redacted acceptance report, uploaded the artifact, and passed the required-stage gate.
- Verification boundary: hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.


### Acceptance task runtime: isolate Python import environment (2026-10-30)

- Continued the acceptance-environment audit beyond Git metadata. Python task subprocesses inherit ambient interpreter variables by default; caller-controlled `PYTHONPATH`, `PYTHONHOME`, user-site configuration, and related `PYTHON*` variables could influence imports and make acceptance results depend on modules outside the committed repository.
- The task runner now removes inherited environment entries whose names are `PYTHONPATH`, `PYTHONHOME`, or start with `PYTHON`, then explicitly sets `PYTHONNOUSERSITE=1`. Other environment entries, including `PATH`, remain available to configured tasks.
- Added a regression test that injects `PYTHONPATH`, `PYTHONHOME`, `PYTHONUSERBASE`, and `PYTHONINSPECT` and verifies none reach the task subprocess while `PYTHONNOUSERSITE=1` is set.
- Exact implementation/test head `ce490949dcc16dd14c11de16787a899e97ce44c0` passed GitHub Actions Push CI [run 41014360849](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41014360849) and PR-context CI [run 41014365771](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41014365771). Both workflow runs completed successfully.
- Verification boundary: GitHub-hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.


### Git-bound review: resolve Git executable outside caller-controlled PATH (2026-10-30)

- Continued the Git provenance audit after isolating Git environment variables and repository-local configuration. Git subprocesses were still invoked by the bare executable name `git`, so a caller-controlled `PATH` could select a different executable and undermine the provenance checks themselves.
- Added a single `_git_argv()` helper that resolves Git using the platform default executable search path (`os.defpath`) rather than the inherited `PATH`, canonicalizes the executable path, and fails closed if Git cannot be found. All Harness Git metadata/provenance subprocesses now use this helper.
- Added a regression test that sets an untrusted ambient `PATH` and verifies executable resolution uses `os.defpath` instead.
- Exact implementation/test head `b77c52fce7ef46595910b7abccee17c213d5117e` passed GitHub Actions Push CI [run 41014953208](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41014953208) and PR-context CI [run 41014960597](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41014960597). Both completed all required stages successfully; Push CI reports all 175 offline contract tests passed.
- Verification boundary: GitHub-hosted CI only; no local test run, live provider request, credential use, merge, release, deployment, or game action is claimed. PR #38 remains Draft/open/unmerged.
