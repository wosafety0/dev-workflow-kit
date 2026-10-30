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

### Reusable workflow Node.js support and first consumer pilot — 2026-10-30

- Added explicit `runtime` selection to `.github/workflows/reusable-acceptance.yml`: `python` remains the default; `node` is supported. Unsupported runtime and package-manager values fail before the consumer command runs.
- Added Node.js version selection and optional pnpm setup. Python cannot be combined with a package manager; pnpm is configured only for the Node.js runtime. Consumer-owned test commands remain passed through an environment variable and run under Bash strict mode.
- Pinned and checked action references: `actions/setup-node` v6.4.0 -> `48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e`; `pnpm/action-setup` v6.0.0 -> `08c4be7e2e672a47d11bd04269e27e5f3e8529cb`. Added static contract tests for runtime allowlisting, read-only permissions, action SHA pins, command handling, and job timeout.
- Exact implementation head `36533dd7726365fd817f48072e49ea055d339947` passed Push CI [41020958838](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41020958838) and PR-context CI [41020991858](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41020991858). Both completed compilation, offline contract tests, acceptance report generation/upload, and the final gate.
- Created the first independent consumer pilot in `wosafety0/AI-Worker-Proxy`: Draft PR [#2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), consumer head `643659014370f85b61964bcbb978833ec6f74428`, pinned to the immutable tested Harness SHA above. Harness Acceptance Pilot [run 41021060938](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41021060938) succeeded; existing consumer Lint and Type Check PR run [41021060320](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41021060320) and push run [41021049711](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41021049711) also succeeded.
- The consumer workflow runs frozen pnpm installation, ESLint, TypeScript type-check, and Prettier check. It requests only `contents: read`; the deployment workflow, secrets, provider APIs, Cloudflare actions, and application code were untouched. PR #2 remains Draft/unmerged.
- Updated Stage 4 in `docs/ROADMAP.md` to record that a first immutable-SHA consumer pilot has been validated. A second unrelated consumer, review/acceptance of the pilot PR, and release decision remain pending.
- This progress entry is an archive-only commit and triggers fresh Harness CI; its new head must be independently verified before claiming the archive commit itself is CI-verified. No Harness PR was merged, no release or deployment was performed, and no game action occurred.
