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

### 2026-10-29 - Bounded semantic-review response on the runner integration line

- Added `MAX_MODEL_RESPONSE_BYTES = 1 MiB` to `scripts/ai_semantic_review.py`. The client now reads at most the limit plus one sentinel byte and rejects oversized provider responses before JSON parsing; the error is a fixed message and does not include the response body.
- Added an offline regression that asserts the bounded read size and fail-closed `ReviewError` for an oversized response. Updated `docs/STABLE_ACCEPTANCE_CONTRACT.md` to document the limit.
- Preserved the redirect-denying opener and request-scoped loopback proxy bypass from the PR #22 runner-integration line. This change is a separate follow-up branch based on PR #22's exact head; it does not merge or close PR #15 or PR #17.
- Fixed two Windows-only test expectation mismatches by resolving expected paths, and adjusted the loopback test to preserve OS-required environment variables while explicitly setting upper/lowercase proxy variables and clearing `NO_PROXY`. This is test portability only; no machine-wide proxy or environment setting was changed.
- Verification: `python -m compileall -q scripts tests` passed; `python -m unittest discover -s tests -v` passed **107 tests**; `git diff --check` passed. The loopback HTTP test used only an ephemeral local server and disposable test token. No real model provider call, credential, game action, merge, release, or deployment occurred.
- Exact-head Push CI for the code-bearing commit `92f975ddbef582f692592b7a861271bf7fe60af9` passed [run 40822632816](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40822632816), including compile, offline tests, report generation, artifact upload, and final gate. Draft follow-up PR #33 is open against PR #22 branch: https://github.com/wosafety0/dev-workflow-kit/pull/33. The PR remains Draft and unmerged; this progress update is documentation-only.


## 2026-10-29 — reject duplicate JSON keys throughout semantic review pipeline (PR #33)

- Cross-branch audit found that the bounded-response/redirect-protected Runner integration branch still used default last-key-wins parsing for the provider response envelope, model-produced review JSON, and CLI input JSON. The active Harness development branch already rejects duplicate object keys, but this protection had not been carried into PR #33's branch.
- Added `_reject_duplicate_json_keys` and applied it to all three JSON parsing boundaries. Provider-envelope parsing now converts duplicate-key `ValueError` into a fail-closed `ReviewError`; malformed model-produced review JSON is likewise rejected.
- Added regression cases for duplicate keys in the provider envelope, duplicate keys inside model content, and duplicate keys in the input file; updated `docs/STABLE_ACCEPTANCE_CONTRACT.md` to make this behavior explicit.
- Implementation commit: `2ce63cb3029b024ebcbdc64ad1fe570e94475922`; tests: `bcf960e451520dab8aa9b3db70f6d7375615724a`; contract update: `44188cf9b1d8d78887b66e660e7a86128fce14ef`.
- Verification boundary: hosted CI for this code-and-archive head remains pending. PR #33 remains Draft/unmerged; no PR was merged, rebased, retargeted, or closed; no consumer pin was changed.


## 2026-10-29 — downstream PR base workflow filter corrected

- The base branch reported by PR #33, `fix/semantic-review-no-redirect-20261029`, was checked at its PR base SHA and still had the old `pull_request.branches` filter without `fix/**`. The fix was therefore applied to PR #22's actual branch and archived there.
- PR #22 base-branch workflow update: `f6bb3db6cf1c93a18a98bd844cd253a043fae38a`; archive commit on that branch: `46587adaf9160c4e0b8503dfe49dc779cd976a33`.
- A successful downstream PR-context run for PR #33 has not yet appeared in the currently retrieved run list. The duplicate-key fix remains unvalidated until its exact code/archive head receives hosted CI evidence. PR #33 remains Draft/unmerged.

## 2026-10-29 — correct duplicate-key regression fixture on PR #33

- Source review found that the regression intended to exercise duplicate keys inside model-produced JSON had over-escaped quotes. The provider-envelope fixture was malformed before the inner JSON parser could be tested, so the test did not independently prove duplicate-key rejection in model content.
- Corrected the fixture so the outer provider response is valid JSON and its `message.content` is the valid JSON text `{"status":"PASS","status":"NEEDS_CHANGES"}`. The inner parser must now reject the duplicate `status` key.
- Test fixture commit: `070d7c9a2387acbb724275cdecbd5f51612dcdd6`; read-back confirmed the intended literal at `tests/test_ai_semantic_review.py`.
- Validation boundary: no test execution was performed by this connector; exact-head hosted CI for this commit has not yet been observed. PR #33 remains Draft/open/unmerged.
- Dependency note: PR #33 still reports base SHA `f71025d2303737dafe18ae823f93cad9cdd1249d`, while PR #22's current PR metadata reports head SHA `071c168bc9532ba8d8c6a9f4708046e164879568` on the same base branch name. This indicates a branch-ref/base-SHA mismatch in the PR metadata snapshot; do not assume the downstream PR has inherited every current base-branch change. No retarget, rebase, merge, close/reopen, or consumer pin change was performed.

## 2026-10-29 — test import correction for duplicate-input regression

- Read-only review of the current PR #33 branch found that `test_duplicate_input_json_keys_fail_closed_before_model_call` patches `sys.stderr` with `StringIO`, but the test module did not import `StringIO`. This would raise `NameError` when the test executes.
- Added `from io import StringIO` to the test module imports in commit `d8792d225a972eb8885187676be0ae8d3e073091`.
- This is a narrow test-harness correction; no production behavior was changed.
- Validation boundary: this connector has not executed the test suite. Exact-head hosted CI for this commit remains unverified until a run tied to this SHA is inspected. PR #33 remains Draft/open/unmerged; no merge, rebase, retarget, release, deployment, or consumer integration occurred.

## 2026-10-29 — PR #33 dependency and current-head CI boundary

- Fresh PR metadata confirms PR #33 base ref is `fix/semantic-review-no-redirect-20261029`, but its recorded base SHA remains `f71025d2303737dafe18ae823f93cad9cdd1249d`; PR #22's current head is `071c168bc9532ba8d8c6a9f4708046e164879568`. Comparing current PR #22 head to PR #33 head `d6d0b797ea789f3c46c3f0940edfdec2f69115e2` reports `diverged`, with the downstream branch 3 commits behind the updated base. GitHub currently reports PR #33 `mergeable=false`.
- PR #22's current head `071c168bc9532ba8d8c6a9f4708046e164879568` has a successful Harness CI run `40860087284`; this validates PR #22's head only, not PR #33's current code.
- The current PR #33 head has no run returned by the connector's PR-triggered-run lookup and no commit status checks returned. The lookup filters to pull-request-triggered runs, so this is not proof that no push-triggered run exists; exact-head CI for PR #33 remains unverified.
- No automatic rebase, retarget, force-push, merge, or PR closure was performed because reconciling the stacked branch could change its review diff. Keep PR #33 Draft/open/unmerged until its dependency is reconciled and its own current head has exact-SHA validation.

## 2026-10-29 — PR #33 branch-reference discrepancy and preservation

- The previously recorded PR #33 head `c37ad36019a9bf6504e6e3be7450ddb27db1e73d` was confirmed retrievable as a commit, and a preservation branch `rescue/pr-33-last-known-head-20261029` was created at that exact SHA.
- The live source branch name `fix/semantic-review-no-redirect-20261029` currently resolves to the same `scripts/ai_semantic_review.py` blob as base head `071c168bc9532ba8d8c6a9f4708046e164879568`; compare also reports those refs identical. This conflicts with the PR body/history that records a later implementation head.
- No source-branch restoration, force update, retarget, closure, or merge was performed. Recovery branch exact-SHA comparison verified identical to `c37ad36019a9bf6504e6e3be7450ddb27db1e73d`. Restoring the original PR branch requires an explicit branch-ref change and is paused pending user decision.
- CI evidence boundary unchanged: PR #22's successful run is not evidence for PR #33's preserved implementation head; exact-head CI for the preserved PR #33 revision remains unverified.


## 2026-10-30 — Correction: PR #33 head/base refs were previously conflated

- Re-fetched PR #33 metadata directly. The actual PR head ref is `fix/runner-loopback-bounded-response-20261029` at `c37ad36019a9bf6504e6e3be7450ddb27db1e73d`; the PR base ref is `fix/semantic-review-no-redirect-20261029`, whose recorded base SHA is `f71025d2303737dafe18ae823f93cad9cdd1249d`.
- Exact-ref comparisons confirm the PR head branch equals its recorded head SHA. The earlier “source branch identical to base” check had compared the PR's *base branch* name to the newer live base head, not the PR head branch. Therefore the prior branch-reference-discrepancy conclusion was incorrect; this is a correction to the investigation record, not evidence of lost code.
- The PR diff is supported by exact commit comparison: recorded base SHA `f71025d...` to PR head `c37ad36...` is ahead by 12 commits and reports the expected five changed files. The base branch has advanced to `071c168bc9532ba8d8c6a9f4708046e164879568`; comparing that live base to the PR head reports divergence with the PR head 3 commits behind. This stacked-branch/base drift and `mergeable=false` remain genuine issues to resolve.
- Rescue branch `rescue/pr-33-last-known-head-20261029` remains preserved as an additional snapshot at the recorded `c37ad360...` plus its archive commit. No original PR ref, base, review state, or consumer integration was changed.
- Validation boundary: PR #22's successful Harness CI run validates PR #22's head only. Current-head PR-context CI for PR #33 is not established by this check. No tests or CI were run in this step.


## 2026-10-30 — Direct source/base file verification (PR #33)

- Read `scripts/ai_semantic_review.py` at the exact merge-base SHA `f71025d2303737dafe18ae823f93cad9cdd1249d`, the live base SHA `071c168bc9532ba8d8c6a9f4708046e164879568`, and the actual source branch `fix/runner-loopback-bounded-response-20261029`.
- The merge-base and live-base file blob SHA is `490479537c35b19336de11020454154f0178f0fb` (21,462 characters). The source branch file blob SHA is `bf72f77855a79428c44296d401d9c4a7f2ee6542` (22,281 characters).
- The source version contains `MAX_MODEL_RESPONSE_BYTES` and duplicate-JSON-key rejection; the checked base version does not. The source test file blob (`193b9c046ae7e1fd70a734b7d15c65cbed7c802f`, 42,246 characters) differs from the live-base test file (`8c2ab28620683a843235043147828df38be0e215`, 39,727 characters) and includes duplicate-key regression coverage.
- This is read-only content verification. No branch or PR refs were changed; no tests or CI were run. Exact-head CI remains unverified for the current source branch.

## 2026-10-30 — Reconcile stacked-branch drift findings (PR #33)

- Fresh PR metadata and commit comparisons confirm the recorded PR head SHA `c37ad36019a9bf6504e6e3be7450ddb27db1e73d` is exactly the current `fix/runner-loopback-bounded-response-20261029` branch tip; the previously suspected source-head mismatch is not reproducible and is resolved as a stale/inconsistent earlier observation.
- The PR's recorded base `f71025d2303737dafe18ae823f93cad9cdd1249d` advanced to `071c168bc9532ba8d8c6a9f4708046e164879568` by three commits. Comparing those base SHAs shows only `.github/workflows/ci.yml` and `docs/PROJECT_PROGRESS.md` changed in that interval; the semantic-review implementation and its tests were not modified by those three commits.
- The current PR head compared with the live base remains diverged (12 commits ahead, 3 behind) and GitHub reports `mergeable=false`. The 12 includes stacked history; it is not a count of changes to replay.
- Read-only patch review confirms PR #33's net implementation adds a 1 MiB bounded provider response read and duplicate JSON key rejection at the provider-envelope, model-content, and input JSON boundaries, with offline regression coverage. The current base's CI workflow and progress log must be preserved during any candidate reconstruction rather than overwritten with stale branch copies.
- The connector's current-head workflow-run lookup returned no PR-triggered run for `c37ad360...`; because this lookup filters to PR-triggered runs, this is not proof that Push CI is absent. Exact-head CI remains unverified. No tests were run; no PR/base/source ref was changed.

- Cross-PR overlap check: PR #32 and PR #33 both modify `tests/test_harness_runner.py`. The shared semantic-review argv assertion currently differs: #32 expects raw `Path` string forms, while #33 changes expectations to `.resolve()` for the script, input, and output paths to handle Windows path normalization. Any combined candidate should retain #32's expanded Git/provenance and regression tests while carrying forward #33's resolved-path expectations; do not take either entire test file wholesale.


## 2026-10-30 — candidate reconstruction refs recorded

- Built isolated current-base reconstruction `reconcile/pr-33-on-current-base-20261030` from `071c168bc9532ba8d8c6a9f4708046e164879568`, and a CI-intended branch `fix/reconcile-pr-33-current-base-20261030` at commit `06858e97bd0a3657c2a379f97807003876b15202`.
- The candidate compare shows 5 changed files, 6 commits ahead, 0 behind; ahead count includes candidate commits and is not a patch-size metric. Files match the expected PR #33 scope. Exact-head CI is not yet visible: combined status is empty and the available workflow-run query returned no runs (it filters to PR-triggered runs).
- Original PR #33 and all rescue snapshots remain untouched. Candidate is not approved for merge; tests/CI remain unverified.


### 2026-10-30 reconciliation candidate final validation
- Candidate branch `fix/reconcile-pr-33-current-base-20261030` now has final archived head `75133380b20f2ee89243e1d5e4f875b4a7894f05`, based on current PR #22 head `071c168bc9532ba8d8c6a9f4708046e164879568`.
- Validation-only Draft PR #34: https://github.com/wosafety0/dev-workflow-kit/pull/34 (open, draft, unmerged; GitHub reports mergeable=true).
- Exact-head Harness CI run [40989084503](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40989084503) completed successfully. Verified Python compilation, offline contract tests, redacted acceptance report generation, artifact upload, and final required-stage gate all succeeded.
- Original PR #33 remains unchanged/open/draft at head `c37ad36019a9bf6504e6e3be7450ddb27db1e73d`; its old base SHA differs from PR #22's current head, and GitHub still reports mergeable=false. No merge, close, retarget, or force-push was performed.


### 2026-10-30 final diff-audit and latest-head CI follow-up
- Final candidate head is now `bd61fd4f58cbb60c99dbf09b7689c545f5da576a` on `fix/reconcile-pr-33-current-base-20261030`; validation-only Draft PR #34 remains open and GitHub reports `mergeable=true`.
- Latest exact-head Harness CI [run 40989359956](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40989359956) completed successfully. Verified compilation, offline contract tests, redacted report generation, artifact upload, and final required-stage gate all succeeded.
- Audit confirmed `tests/test_ai_semantic_review.py` and shared `tests/test_harness_runner.py` are identical to original PR #33. The semantic-review source differs only in using `ReviewError` for duplicate-key rejection rather than a bare `ValueError`, preserving fail-closed handling. No live provider call or local test run was performed.
- Original PR #33 remains open/draft at its original head/base and mergeable=false; no original PR state was changed. Shared runner-test overlap with PR #32 remains documented for any future combined branch.


## 2026-10-30 — dependency-chain audit follow-up (PR #33/#22)

- Rechecked live ancestry: PR #22 is based exactly on PR #20 head `827bb99d2eb97ac61909979094f68471f081150b`; PR #20 combines the PR #12 loopback transport work, PR #13 runner, and PR #19 output-alias fix on the safe-runner base. PR #22's redirect hardening then adds nine commits across the CI workflow, progress log, acceptance contract, semantic-review implementation, and tests.
- PR #33 candidate is based exactly on current PR #22 head `071c168bc9532ba8d8c6a9f4708046e164879568`; compare reports 14 commits ahead, 0 behind, with only the five intended files in the net diff. The commit count includes candidate history and is not the feature patch size.
- Important downstream follow-ups exist outside PR #22's head: PR #23 adds fail-fast task orchestration and requires semantic review to run last; PR #24 adds explicit HTTPS redirect-handler regression coverage on top of PR #23. These are not ancestors of PR #33 candidate because its declared base is PR #22. Before any future integration of the broader runner/loopback stack, review and validate #23 and #24 in order; do not silently assume the #33 candidate includes them.
- PR #33's bounded-response and duplicate-key changes are independent additions to the semantic-review client. No unintentional extra source files were found in the candidate net diff. Shared runner test overlap with PR #32 remains a selective-combination issue, not a reason to replace either full test file.
- Candidate exact-head CI [40989359956](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40989359956) succeeded on `bd61fd4f58cbb60c99dbf09b7689c545f5da576a`. Original PR #33 remains open/draft/unmerged and unchanged; no merge or branch mutation was performed.


## 2026-10-30 — downstream dependency verification follow-up (PR #23/#24)

- Refreshed live PR metadata and exact-head CI for the full runner/loopback dependency tail. PR #23 head `7962697d273e04716e71fcf95536154b03704032` passed Harness CI [run 40804425695](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40804425695); PR #24 head `58702b8ba7e7fde2c384671677aec8784f216c97` passed Harness CI [run 40805458873](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40805458873). Inspected jobs show successful Python compilation, offline contract tests, redacted report generation, artifact upload, and final required-stage gate.
- PR #24's latest head is later than the earlier documented tested code head `afe632...`; the current exact-head run #40805458873 closes that verification gap for the current PR head.
- Current dependency tail remains PR #20 → PR #22 → PR #23 → PR #24. PR #33/#34 currently target PR #22, so they intentionally do not inherit fail-fast/order enforcement from #23 or HTTPS-specific regression coverage from #24.
- For the broader integration candidate, the safer order is to start from PR #24's current head, then selectively port PR #33's bounded-response/duplicate-key changes and carefully combine shared tests; separately port PR #32's runner/provenance guard only if the target integration is intended to combine both branches. Do not merge the two branch families by blindly replacing shared files.
- Original PR #33 and validation candidate PR #34 remain open/draft/unmerged. No PR or branch topology was changed in this review.


## 2026-10-30 — unified validation candidate PR #37
- Created Draft PR #37: https://github.com/wosafety0/dev-workflow-kit/pull/37, based on PR #24's tested head `58702b8ba7e7fde2c384671677aec8784f216c97`.
- Exact archived candidate head `ea05b0813ed25abe5354b7f2bf8d2655a86bf181` passed Harness CI [run 40990643340](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40990643340). Python compilation, offline contract tests, redacted report generation, artifact upload, and final gate all succeeded.
- Candidate carries the bounded response and duplicate-key checks from PR #33 alongside PR #32 runner/config protections; the PR #24 HTTPS redirect regression and fail-fast ordering were retained. Shared runner tests were combined selectively, not overwritten wholesale.
- Compare against PR #24 base: 15 commits ahead, 0 behind; intended net diff is 8 files including CI trigger coverage for `integration/**` branches.
- Validation-only Draft; no live provider request or credential use. Original PR #33 remains open/draft/unmerged and its branch was not altered.


## 2026-10-30 — final unified candidate audit and exact-head CI
- Final audited PR #37 head: `169fa027fecfa0f361da751f86e7df4d2251b4ff`; exact-head Harness CI [run 40990807374](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40990807374) succeeded. Python compilation, offline contract tests, redacted report build, artifact upload, and final required-stage gate all succeeded.
- Diff audit confirms the semantic-review implementation matches PR #33 candidate blob `4a29f02f370704e6b61d2a8ddfe718eb31d99e26`; all 31 PR #32 candidate runner tests are retained, plus the loopback preflight regression (32 runner tests total). Net changed-file list is 8 intended files; no unrelated source modules in the net diff.
- Candidate remains Draft/unmerged; originals #24/#32/#33 and candidates #34–#36 remain open/draft/unmerged. No live provider call, release, or deployment.


## 2026-10-30 — PR #37 follow-up audit correction
- A deeper base-to-head inventory found two PR #24 inherited fail-fast tests missing from the first unified candidate; both were restored on candidate head `731c39a5a8c9d1a21312b2c959a6e6dc3c732123`: `test_stops_after_failure_and_marks_remaining_tasks_not_run` and `test_semantic_review_must_be_last_configured_task`.
- The corrected candidate contains all 14 runner test methods from the PR #24 base and all 31 from PR #32's candidate suite, plus the loopback preflight test (34 unique methods total).
- Exact-head Harness CI [run 40991595301](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40991595301) passed compilation, offline contract tests, redacted report build/upload, and final gate. No local tests or live provider request are claimed.
- PR #37 remains Draft/unmerged; original PR #33 and its branch are unchanged.


## 2026-10-30 — final PR #37 corrected archive head
- Final PR #37 head after the candidate progress archive: `04f455b23e5b17956705a76b5ef74d263956a96c`.
- Exact-head Push Harness CI [run 40991648743](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40991648743) and PR-context CI [run 40991653272](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40991653272) both succeeded, including compilation, offline contract tests, redacted report build/upload, and final gate.
- Final read-back confirms PR #37 has 34 unique runner test methods, all 14 PR #24 base methods, all 31 PR #32 candidate methods, plus the loopback preflight test. PR #37 remains Draft/unmerged; original PR #33 remains unchanged.

 
## 2026-10-30 — unified candidate ignored-source provenance fix
- Static audit of unified PR #37 found the ignored-source check blocked ignored `test*.py` files but did not block ignored helper modules such as `tests/helper.py`, which tracked tests could import while the Git worktree still appeared clean.
- Corrected on PR #37 candidate branch `integration/pr24-pr33-pr32-20261030`: head `bf0b96b2c8dfbcaf623f6b57d09614dc6422ee0b`. The runner now blocks all ignored `.py` files under `tests/`; regression coverage includes an ignored helper module and the existing ignored-test case.
- Exact-head Push CI [run 40992682760](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992682760) and PR-context CI [run 40992686555](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992686555) both succeeded, including compilation, offline contract tests, report generation/upload, and final gate.
- This is a follow-up finding/fix on the unified validation candidate; it does not alter the original PR #32/#33 source refs, and does not authorize merging PR #37.


## 2026-10-30 — project-wide ignored Python source guard
- Follow-up review found ignored Python helper modules outside `tests/` could also be imported by tracked tests.
- PR #37 candidate head `2ee839b9c8cada2fe3c5646d6eae57bc83a138e4` now checks ignored Python sources across the project tree, excluding generated artifacts, common virtual environments, and Python caches. Regression tests cover ignored helpers under `tests/` and `scripts/`; runner and contract docs were updated.
- Exact-head Push CI [run 40992914390](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992914390) and PR-context CI [run 40992921060](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992921060) both succeeded.
- Candidate remains Draft/unmerged; original PR #33 was not changed. Runtime/dependency environment contents are not attested by the source commit.


## 2026-10-30 — post-task ignored-source revalidation
- Additional audit found a task could create ignored Python source after the initial preflight. The runner now repeats the ignored-source check after all tasks, before the report can be emitted.
- Final PR #37 candidate head: `d0c513b19876f057017c4c7fbb5ca52c7d377253`; regression coverage verifies that a task-created ignored helper blocks acceptance.
- Exact-head Push CI [run 40993134186](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993134186) and PR-context CI [run 40993140527](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993140527) both succeeded.
- PR #37 remains Draft/unmerged. Original PR #33 remains unchanged; no merge or release is authorized by this archive.


## 2026-10-30 — post-task source cleanliness gate
- Static review found the runner only compared HEAD after tasks; tracked changes and non-ignored untracked source could slip through while HEAD stayed the same.
- Candidate PR #37 head `b9748c3230782e3065923f386bacbd7a2ba83bdd` now rechecks full Git provenance/clean-worktree status after task execution. Regression tests cover tracked source modification and non-ignored untracked source creation during a task.
- Exact-head Push CI [run 40993507598](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993507598) and PR-context CI [run 40993515179](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993515179) both succeeded.
- Candidate PR #37 remains Draft/unmerged; original PR #33 remains unchanged.


## 2026-10-30 — semantic-review CLI output hardening
- Static review found standalone semantic-review input/output paths did not reject symlink components and final JSON was written directly to the destination.
- Candidate PR #37 head `93adba0e56d3b6b3981c863ec8da24b6df7f482c` now rejects symlink components and uses a same-directory temporary file with atomic replacement, rechecking the output path before replacement. This mitigates final-entry symlink redirection and partial writes, but is not a full filesystem sandbox against hostile concurrent parent-directory replacement.
- Regression tests cover symlinked input/output paths and target preservation. Exact-head Push CI [40993820393](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993820393) and PR-context CI [40993826168](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993826168) both succeeded.
- Candidate PR #37 remains Draft/unmerged; original PR #33 remains unchanged.

## 2026-10-30 — semantic-review input integrity guard
- Static audit found that a preceding task could modify the caller-supplied review input before the final semantic-review task. Because generated `artifacts/` files are excluded from Git cleanliness checks, this could silently change what the model reviewed.
- Candidate PR #37 head `e68e66ef61513611910892223957648a68695212` fingerprints the review input before task execution and rechecks its SHA-256 and symlink path immediately before semantic review. A changed/unverifiable input blocks the run; the model is not called on the altered payload.
- Added regression coverage where the preceding task mutates the review input; expected result is blocked execution, only the first task runs, and no review/acceptance artifact remains. Updated `docs/HARNESS_RUNNER_V1.md`.
- Exact-head Push CI [40994253760](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994253760) and PR-context CI [40994260335](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994260335) both succeeded for this exact SHA; compilation, offline tests, report generation/upload, and final gate completed successfully.
- No local tests or live provider requests are claimed. PR #37 remains Draft/open/unmerged; no original candidate PR was merged, closed, or retargeted.

## 2026-10-30 — rule-quote boundary validation and exact-head checkpoint
- A second static review found that semantic-review rule quotes were checked against `global_rules + "\\n" + project_instructions`, allowing a fabricated quote to span the boundary between two separate instruction fields. Validation now requires the entire quote to occur inside one source field.
- Added a regression test using a quote composed from the end of the global rules and the start of the project instructions; updated runner documentation.
- Current PR #37 head: `6f2263b1c821c5eb3882f43902debcab336f42a8`. This head also includes the earlier review-input SHA-256 guard and mutation regression test.
- Exact-head Push CI [40994473127](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994473127) and PR-context CI [40994478252](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994478252) both succeeded for the same exact SHA. Each completed compile, offline contract tests, redacted report generation, artifact upload, and final required-stage gate.
- These are hosted GitHub CI results only; no local test execution or live provider request is claimed. PR #37 remains Draft/open/unmerged. No original PR was merged, closed, or retargeted.

## 2026-10-30 — precise evidence-line validation and diff-provenance caveat
- Static audit found that a finding could cite a real diff substring while claiming an unnecessarily broad line range. Validation now requires the supplied line range to match the minimum/maximum source lines mapped from the evidence; a regression test covers a broad range.
- Documented an important remaining boundary: review input is caller-supplied. Its fingerprint prevents mutation between preflight and review, but does not prove the supplied diff corresponds to the runner's current Git `HEAD`; the acceptance report's `commit_sha` identifies the runner worktree, not the review target unless the caller establishes that relationship.
- Current PR #37 head: `49d12ba3e53fa227b184a92b4f30f33072f6874e`.
- Exact-head Push CI [40994746009](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994746009) and PR-context CI [40994750887](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994750887) both succeeded for the same exact SHA. Both completed compilation, offline contract tests, redacted report generation, artifact upload, and final required-stage gate.
- The current head also includes the earlier fixes for review-input mutation and rule quotes spanning the boundary between `global_rules` and `project_instructions`. No local tests or live provider calls are claimed; PR #37 remains Draft/open/unmerged.

## 2026-10-30 — strict acceptance-rules digest validation
- Static audit found that `scripts/acceptance_report.py` accepted any non-empty `rules_pin`. In CI, a failed digest command could theoretically emit a malformed but non-empty value while the final gate did not directly require the pin step's outcome.
- Acceptance reports now require `rules_pin` to match `sha256:` plus exactly 64 lowercase hexadecimal characters. The CI hash step now uses `set -euo pipefail`, verifies the contract file exists, and validates the digest before writing its output.
- Updated report tests and runner fixtures to use valid SHA-256-shaped pins, with negative tests for malformed pins.
- Current PR #37 head: `4ba0108f5c4804fdedd55b7e3fe8850f8ea56143`. Exact-head Push CI [40994944355](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994944355) and PR-context CI [40994950381](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40994950381) both succeeded for the same SHA, including compile, offline tests, report generation, artifact upload, and final gate.
- The current head also includes review-input mutation protection, single-source rule quote validation, precise evidence line ranges, and the documented caller-supplied diff-provenance limitation. No local tests or live provider requests are claimed.

## 2026-10-30 — atomic review artifact and input snapshot hardening
- Fixed semantic-review JSON output to write an actual newline rather than the literal backslash-plus-n sequence. The successful CLI regression test now checks the output ends in a real newline and round-trips through `json.loads`.
- Closed a check/use race in the runner's review input handling: it captures the input bytes and SHA-256 before task execution, checks the source path and hash again immediately before review, then passes the captured bytes to the child over standard input. A path replacement after the check cannot change the bytes reviewed. The CLI supports `--input -` for stdin while retaining path-based standalone use.
- Updated runner tests and `docs/HARNESS_RUNNER_V1.md` to describe the snapshot flow accurately.
- Current PR #37 head: `49191bd53c998a9af31862cb1ff75d46a16a769b`.
- Exact-head Push CI [40996142543](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40996142543) and PR-context CI [40996147886](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40996147886) both succeeded for the same SHA. Both completed compilation, offline contract tests, redacted report generation/upload, and the final required-stage gate.
- No local tests or live provider calls are claimed. PR #37 remains Draft/open/unmerged; no candidate PRs were merged, closed, or retargeted.

## 2026-10-30 — bounded semantic-review input
- Added a 4 MiB maximum for caller-supplied semantic-review input in both the Harness runner and standalone CLI. The runner reads at most limit+1 bytes into its verified snapshot; the CLI rejects oversized file or stdin input before JSON parsing/model invocation.
- Added regression tests that oversized input is rejected and the model/task runner is not called; updated `docs/HARNESS_RUNNER_V1.md` to document the cap and stdin snapshot contract.
- Current PR #37 head: `90564d4550142af0fb776c0e7aaa78b92698357d`.
- Exact-head Push CI [40996448203](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40996448203) and PR-context CI [40996455446](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40996455446) both succeeded for the same SHA. Compilation, offline contract tests, redacted acceptance report generation/upload, and final required-stage gate all succeeded.
- This head includes the prior atomic JSON newline fix and verified stdin byte-snapshot flow. No local tests or live provider calls are claimed; PR #37 remains Draft/open/unmerged.

## 2026-10-30 — bounded review input and unambiguous evidence
- Added a 4 MiB cap for semantic-review input in both runner and standalone CLI. The runner snapshots at most limit+1 bytes; the CLI rejects oversized file/stdin input before parsing or calling the model.
- Static audit found that repeated evidence substrings across multiple lines/hunks could be merged into a broad range and accepted without uniquely identifying the cited location. Validation now rejects evidence substrings that occur more than once in the cited file diff; tests were updated to make ambiguity fail closed.
- The first CI attempt for the evidence change correctly failed because the new test's hunk counts were malformed and an older test still expected multi-location aggregation. Both tests were corrected to assert the new fail-closed contract.
- Current PR #37 head: `2bd757ec21247af583386498a7a90ffdce0de847`.
- Exact-head Push CI [40997023835](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40997023835) and PR-context CI [40997028514](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40997028514) both succeeded for the same SHA. Compilation, all offline contract tests, redacted acceptance report generation/upload, and the final required-stage gate succeeded.
- This head also includes the verified stdin byte-snapshot flow, real trailing newline in review JSON, strict acceptance-rules digest validation, rule-quote source separation, and the documented caller-supplied diff provenance limitation. No local tests or live provider requests are claimed. PR #37 remains Draft/open/unmerged.

## 2026-10-30 — precise context-line coordinates
- A follow-up audit found context lines were mapped to both old and resulting-file line numbers. That made a context finding's accepted range broader than the actual source location. Context evidence now maps to resulting-file coordinates; deleted files use old-file coordinates because no resulting file exists.
- Updated the regression test to accept the exact resulting-side line and reject the old/new combined range. A first CI attempt exposed only a stale expected error message in the test; the assertion was corrected to the validator's specific “line range is broader” failure.
- Current PR #37 head: `ab05ccd42f5650f893a1a68523c4d8399e13069e`.
- Exact-head Push CI [40997442576](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40997442576) and PR-context CI [40997448652](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40997448652) both succeeded for the same SHA. Compilation, offline contract tests, redacted report generation/upload, and the final required-stage gate passed.
- The current head also includes rejection of repeated/ambiguous evidence, a 4 MiB review-input cap, verified stdin byte snapshots, and the earlier acceptance-report and CLI hardening. No local tests or live provider requests are claimed. PR #37 remains Draft/open/unmerged.
