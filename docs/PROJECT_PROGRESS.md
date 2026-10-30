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


### 2026-10-29 clean-worktree commit-provenance gate (stacked draft PR #18)

- Draft PR: https://github.com/wosafety0/dev-workflow-kit/pull/18; branch `fix/runner-commit-provenance-20261029`, based on PR #14 (`fix/runner-stale-artifacts-20261029`), which itself depends on draft PR #13.
- Finding: the runner could execute dirty or test-mutated source while labeling a passing acceptance report with the original Git HEAD SHA. This is a provenance mismatch, not proof that the code in that commit passed.
- Change: require the exact Git repository root and a clean staged/unstaged/untracked source tree outside generated `artifacts/` before tasks; recheck cleanliness and HEAD after tasks, before writing the report. Common generated Python files are ignored via a reviewed `.gitignore`. Four Git-backed regression tests cover modified tracked code, untracked code, post-task mutation, and nested Git roots.
- Test-first commit `39cb4749e7cffd415c762201596d0fd06333fb73`: expected failure run https://github.com/wosafety0/dev-workflow-kit/actions/runs/40733601898 (four new tests did not pass before implementation).
- Implementation/ignore-rule commit `b175599a3824cda3b1174431d6d97913e518d1ac`: successful hosted push CI https://github.com/wosafety0/dev-workflow-kit/actions/runs/40733749977, 107 offline tests passed; acceptance artifact ID `12837210211` uploaded and final gate passed.
- Documentation commit `91460c2e3f79754f6ee5e4a6f2bfaf5459c421f2`: hosted push CI https://github.com/wosafety0/dev-workflow-kit/actions/runs/40733848128 succeeded for that exact head. This progress-log change itself requires a new exact-head CI check.
- Limits: cleanliness is not a sandbox, concurrent-worktree lock, or cryptographic attestation; `artifacts/` is intentionally excluded, so executable source must not be placed there. The PR remains draft and unmerged; no change to `main`, no release/deploy, no live model request, and no consumer integration. The local Windows worktree was not inspected or synchronized.
- Approval required: review PR #13 -> #14 -> #18 in dependency order, and separately PR #12 -> #15 -> #17; integrate only after explicit authorization and combined-branch CI. The independent Node consumer pilot remains draft/unmerged.


## 2026-10-29 — prevent review-output/config alias before stale-artifact cleanup

- Re-review of the runner dependency chain (#13 → #14 → #18) found a destructive path alias not covered by those heads: when both `--config` and `--review-output` pointed to the same file under `artifacts/`, stale-artifact invalidation unlinked that file before attempting to parse the config.
- The protection existed as a separate change in PR #19, but that branch is based directly on #13 and is not an ancestor of #14/#18. The #14 → #18 chain therefore did not contain the guard.
- Created a narrow follow-up branch based on the exact #18 head; added an early alias rejection, a regression that verifies the config bytes remain unchanged and no task executes, and a security-boundary note. This is not a merge or a rebase; it keeps the fix reviewable against the provenance/stale-artifact line.
- Validation status at archive time: code and test changes committed to the follow-up branch; exact-head hosted CI is pending. No live model requests, game actions, deployment, release, or merge.


## 2026-10-29 — review-output/config alias fix CI result

- PR #32 exact head `8c02d63aea03a3705cb75783b57182f713eb2185` passed hosted Push CI: [run 40821391073](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40821391073). The job ran 108 offline tests (`OK`), built and uploaded the redacted acceptance report, and passed the final gate.
- This is evidence for the exact #32 head only. PR #32 remains Draft/unmerged and stacked on PR #18; the independent PR #19 remains a separate branch. No branch was merged or retargeted.


## 2026-10-29 runner config ambiguity hardening (PR #32)

- Reviewed runner report generation and the fail-closed report verifier. The report builder derives overall status from every declared task status; the runner's process exit code remains a separate required signal, and consumers must independently validate report identity/provenance.
- Found a remaining ambiguity at the Harness config boundary: Python's default JSON decoder silently accepts duplicate object keys (including nested keys), so two syntactically valid-looking configs could be interpreted by last-value-wins behavior.
- Updated `scripts/harness_runner.py` to reject duplicate keys at every JSON object nesting level using `object_pairs_hook`; parser failures fail closed before any task executes.
- Added regression coverage for duplicate top-level `schema_version` and duplicate `commands` keys. Both cases return blocked exit code 2 and assert no task execution.
- Documented strict duplicate-key rejection in `docs/HARNESS_RUNNER_V1.md`.
- Exact branch head: `10a091c086bfa8de9557f329d6f121cbbaddb796`.
- Exact-head Push CI: https://github.com/wosafety0/dev-workflow-kit/actions/runs/40822592220 — success; offline suite ran 109 tests, including the new duplicate-config regression.
- PR #32 remains open and unmerged, stacked on `fix/runner-commit-provenance-20261029`. No rebase, retarget, merge, release, live model call, or game action was performed.


- Follow-up coverage refinement: added a nested duplicate-key config case (`metadata.mode`) to verify the same strict parser hook rejects duplicate keys below the top level, not only duplicate root fields.
- Exact-head Push CI for this added regression: https://github.com/wosafety0/dev-workflow-kit/actions/runs/40822740014 — success at `7570b6b0a7ace791922fc9c4776e3f3017c0f314`.


## 2026-10-29 — constrain runner provenance inputs to committed source paths (PR #32)

- Runner provenance review found that a clean Git HEAD alone does not bind execution to committed content if a task entrypoint or acceptance-contract file resolves through a symlink. The existing cleanliness gate intentionally excludes generated `artifacts/`, so a source symlink targeting that directory would also bypass source-change detection.
- Hardened `scripts/harness_runner.py`: the `tests/` directory, semantic-review entrypoint, and stable acceptance contract now resolve through a trusted-source path check. Targets outside the repository root and targets under generated `artifacts/` are rejected before task execution or rules hashing.
- Added regressions for external symlinks targeting the test directory, semantic-review entrypoint, and acceptance contract, plus direct rejection of paths under `artifacts/`. Tests skip symlink-specific cases only when the platform cannot create symlinks; the generated-artifact path guard is tested independently.
- Updated `docs/HARNESS_RUNNER_V1.md` to document the provenance boundary.
- Implementation commit: `b9cba674b3697664cea9a65c7fa8a57c6f364714`; follow-up artifact-exclusion commit: `0286e2e930400b9d1c618c876971647a23459fcd`. Regression-test commits: `722398956021c4b875fc046485d14160d67d415d` and `748c7cf27121b9f346bcf6c2dae79174795708ff`. Documentation commits: `587d3ec6f3da1a95304c64c3f014ed322330b465` and `8e10cc9988cacbba503d52753b8ea2ea3371d503`.
- Verification boundary: the code and tests are committed to the existing PR #32 branch. Exact-head hosted CI for the final code-and-archive head must be checked before this change is considered validated. PR #32 remains Draft/unmerged; no branch rebase, retarget, merge, release, live model request, or consumer action occurred.


## 2026-10-29 — enable PR-context CI for stacked fix branches

- The Runner provenance hardening is stacked on PR #18, whose base branch is `fix/runner-commit-provenance-20261029`. Review of `.github/workflows/ci.yml` found that `push` included `fix/**`, but `pull_request.branches` omitted it. As a result, this PR target did not match the configured PR-context CI branch filter; a successful Push CI alone would not prove the PR-context gate ran.
- Updated the pull-request branch filter to include `fix/**`, so stacked fix PRs receive the same offline test/report/final-gate workflow in PR context.
- Workflow-filter change commit: `41c997a49ef9b4d75d1be60e9db0877a8ddd8238`.
- Verification boundary: this commit should trigger both branch Push CI and PR-context CI, but neither run is claimed passed until an exact-head result is observed. PR #32 remains Draft/unmerged; no rebase, retarget, merge, consumer pin update, live model call, or game action occurred.


## 2026-10-29 — close in-repository ignored-path symlink provenance gap (PR #32)

- Follow-up threat review found that checking only “inside repository root” and “outside artifacts/” was insufficient: a trusted-source path could be a symlink into an ignored in-repository location such as `.venv/`. Git cleanliness does not attest to mutable ignored targets, so such a link could still make a clean commit execute content that was not pinned by the commit.
- Updated `_resolve_trusted_source` to reject symlinked path components and, for directory sources such as `tests/`, any nested symlink entry. This supplements the existing outside-root and generated-artifact rejection.
- Added regression tests for a semantic-review entrypoint symlink into an ignored in-repository directory and a nested symlink inside `tests/`. Existing external-symlink and generated-artifact cases remain in place.
- Code commit: `38e8dfd9b0386345ea34c892744263e2edd99642`; test commit: `f2bca798744de56a052597a3a62add6541e52160`; documentation commit: `7dccb4fc5b82655c6d53424c3fc6aea943af0392`.
- Verification boundary: hosted CI for the final code-and-archive head remains unconfirmed through the currently available run/status retrieval interface. The workflow filter now includes `fix/**` for PR-context checks; do not mark this branch validated until exact-head Push and PR-context results are independently observed. PR #32 remains Draft/unmerged and no consumer pin was changed.


## 2026-10-29 — PR-context CI result for symlink provenance hardening

- PR #32 PR-context Harness CI completed successfully for branch head `b59f83a1d4c394eade420ce4eadced7897f2a92a`: [run 40858714785](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40858714785).
- The hosted job ran all **115 offline tests**, including both new regressions for symlinks into ignored in-repository paths and nested symlinks under `tests/`; Python compilation, redacted acceptance-report generation/upload (artifact `12889309542`), and the final orchestration gate all passed.
- This is PR-context CI evidence; the report's `github.sha` is the PR merge commit, as expected for that event. A separate exact branch Push CI result is not exposed by the currently available commit-run retrieval wrapper, so it is not claimed here.
- The workflow filter was added to the PR #32 head and its base branch so stacked fix PRs can trigger PR-context CI. PR #32 remains Draft/unmerged; no consumer pin change or topology operation occurred.


## 2026-10-29 — reject symlinked caller IO paths before reads or cleanup (PR #32)

- Continued review of `scripts/harness_runner.py` found that the trusted-source guard did not cover caller-supplied config and review-input paths, and output paths were resolved before cleanup. A tracked symlink could therefore point at mutable ignored content, while an output symlink could cause cleanup to unlink the resolved target rather than the requested link.
- Added `_reject_symlink_path` and applied it to the configured Harness JSON, report output, semantic-review input, and semantic-review output. Path containment validation still runs first; symlink components are then rejected before config reads, report invalidation, or review output creation.
- Added regression tests for a config symlink into an ignored `.venv/` location and for an acceptance-report output symlink, asserting the latter's target content is preserved and no task executes on the blocked config case.
- Code commit: `4fdff5b416ba62e848eee2bdfa7a3da04b6d07d6`; regression tests: `bcdf017020c1766a036426c7a203c43b808c043d`; runner documentation: `436a656a42591de9287dc29cf12bcb423ab66a64`.
- Validation boundary: no local test runtime is available through this GitHub-only workflow, so hosted CI is required. Prior PR-context CI passed on earlier code head `b59f83a1d4c394eade420ce4eadced7897f2a92a` (115 tests), but does not validate these new changes. Exact-head CI must be observed before calling this revision validated. PR #32 remains Draft/unmerged; no consumer pin change or branch topology change occurred.


## 2026-10-29 — require committed Harness runner configuration (PR #32)

- Follow-up provenance review found the runner's config path was containment-checked and symlink-checked, but was not required to exist in the current Git HEAD. Since generated `artifacts/` and ignored paths are outside the cleanliness gate, a mutable ignored/untracked config could affect task selection without being bound to the reported commit.
- Added a fail-closed config provenance check before stale-artifact invalidation and config reads: reject config paths under `artifacts/`, then require the exact repository-relative path to be present in `git ls-tree HEAD`. Existing clean-worktree checks bind the tracked file contents to the reported commit before task execution.
- Added regression coverage for config under `artifacts/`, an ignored untracked config under `.venv/`, and acceptance of a normal HEAD-tracked config. Existing symlink and report-contract protections remain unchanged.
- Code commit: `6c3dea5372a8c233a59990c428c08288c71df602`; regression tests commit: `b9097574e2f84ee2880176f3fd7ab3996c11645e`; documentation commit: `cabcd885e6b53a176532cffb8e3910ce41a7430d`.
- Validation boundary: changes are committed to the existing PR #32 branch; hosted exact-head Push CI and PR-context CI must be observed for the final code-and-archive head before treating this follow-up as validated. PR #32 remains Draft/unmerged; no consumer pin, PR target, branch topology, release, or deployment changed.


## 2026-10-29 — committed-config provenance regression suite passes (PR #32)

- Finalized the config provenance gate while preserving the existing review-output/config alias rejection precedence. Config paths under `artifacts/` are rejected, and other config paths must be present in the current Git HEAD tree before config parsing or stale-output cleanup.
- Regression coverage includes an `artifacts/` config, an ignored untracked config under `.venv/`, and acceptance of a normal tracked config. The existing alias-protection regression remains intact.
- Code commit: `ff00e73d29a363e5f3d20b578f68c22331c2fc30`.
- Exact-head Push CI: [run 40860841336](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40860841336) — success. All **120 offline tests** passed; Python compilation, redacted acceptance-report generation/upload, and the final orchestration gate passed.
- The workflow now prints only the three required stage outcomes (tests/report/artifact) before evaluating the gate, improving diagnosis without exposing user data or secrets.
- Exact-head Push CI also passed for the progress-archive commit `b5a0dc4d94c76006a0929c3166c80844b4595ee5`: [run 40860979797](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40860979797), including the 120-test suite, report upload, and final gate. PR #32 remains Draft/unmerged. PR-context CI for the current head is not yet confirmed; do not infer it from the older PR-context run. No consumer pin, PR target, branch topology, release, or deployment changed.


## 2026-10-29 — stale-report invalidation on rejected config provenance (PR #32)

- Follow-up review found an ordering regression introduced by config provenance enforcement: an untracked or `artifacts/` config was rejected before prior acceptance artifacts were cleared, potentially leaving an old PASS report available after a blocked run.
- Moved the config provenance gate to after path-alias checks and stale report/review-output invalidation, while keeping it before config parsing and task execution. This preserves config bytes when paths alias outputs and ensures blocked runs cannot leave stale passing artifacts.
- Added regression coverage that pre-seeds a passing report, then verifies both `artifacts/harness.json` and ignored `.venv/harness.json` are rejected and the stale report is removed; the task executor is never called.
- Implementation commit: `7a57238b56a3443624d86fa84bcb3dcf1e774096`; regression-test commit: `a7384851b96dcfcc850f6e66b11915b9ecb128af`; documentation commit: `74c369c9175681af93f0527e9eedad66b90f9c19`.
- Exact-head Push CI passed for the code commit `7a57238b56a3443624d86fa84bcb3dcf1e774096` ([run 40861667123](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40861667123)), the regression-test commit `a7384851b96dcfcc850f6e66b11915b9ecb128af` ([run 40861684438](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40861684438)), the documentation commit `74c369c9175681af93f0527e9eedad66b90f9c19` ([run 40861706360](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40861706360)), and the archive commit `ee9a853b66c15afb3300cba01d5f04f97eafa826` ([run 40861716196](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40861716196)). All runs passed the 120-test offline suite, Python compilation, redacted report generation/upload, and final gate. PR-context CI for this newer head remains unconfirmed; the latest PR-context run predates these changes. PR #32 remains Draft/unmerged; no consumer pin, target branch, branch topology, release, or deployment changed.

## 2026-10-29 — revalidate generated output paths after task execution (PR #32)

- Continued adversarial review found that caller output paths were checked before task execution, but the runner intentionally excludes `artifacts/` from Git cleanliness checks. A task could replace the `artifacts/` directory with a symlink after the preflight checks, potentially redirecting the final report write outside the worktree.
- Updated `scripts/harness_runner.py` to recheck report-output and review-output symlink components after all tasks complete and immediately before report emission; it also revalidates that outputs remain inside the generated-artifacts boundary.
- Added a regression that moves the original artifacts directory outside the worktree, replaces it with a directory symlink during the task, and asserts the run is blocked and no report is written to the symlink target.
- Updated `docs/HARNESS_RUNNER_V1.md` with the post-task output-path boundary.
- Runner implementation commit: `43449b15cb00adbcfe39ad7097b2de8c729c566d`.
- Regression-test commit: `e9613efeacba83971153064651bcb7d25be13906`.
- Documentation commit: `68b6589ff0336115ea51dc91c32bba426483f526`.
- Validation boundary: these commits have been pushed to the existing PR #32 branch; exact-head Push CI and PR-context CI must be checked for the final code-and-archive head before the change is treated as validated. PR #32 remains Draft/unmerged; no rebase, retarget, merge, or consumer pin change occurred.

## 2026-10-29 — PR #32 PR-context trigger metadata discrepancy

- Current branch ref API reports target branch `fix/runner-commit-provenance-20261029` at `e4be499e36ed9d8e22ff45065d95f92e0876df34`, and its `.github/workflows/ci.yml` includes `fix/**` in the `pull_request.branches` filter.
- The PR #32 API payload and workflow-run metadata still report the base SHA as `b402101ef41d3f9d4f9533545ea83128ba5843a6`, and no PR-context run has been recorded for the latest head `92b7ed9d45429a1d4cedee0cc1907e1880690d86`. Latest known exact-head Push CI passed at [run 40861810273](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40861810273).
- This is an observed GitHub PR/base metadata and trigger-evidence discrepancy, not proof that the new PR-context gate passed. Do not change PR topology or use older PR-context results as a substitute. Continue by checking exact-head Push CI for the new output-path fix and investigating whether GitHub updates the PR base metadata/trigger behavior; keep the PR Draft/unmerged.

### Validation update — post-task output path revalidation

- Exact-head Push CI passed for runner commit `43449b15cb00adbcfe39ad7097b2de8c729c566d`: [run 40866390716](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40866390716).
- Exact-head Push CI passed for regression-test commit `e9613efeacba83971153064651bcb7d25be13906`: [run 40866416039](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40866416039). The run compiled Python, passed all **121 offline tests** including `test_runner_rejects_artifacts_directory_replaced_by_symlink_during_task`, generated and uploaded the redacted report, and passed the final gate.
- Exact-head Push CI passed for documentation commit `68b6589ff0336115ea51dc91c32bba426483f526`: [run 40866441316](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40866441316).
- Progress archive commit `2d13728f4080272ef3eb63011e6280d77fa7040a` also passed exact-head Push CI: [run 40866473003](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40866473003).
- The new output-path regression is validated by exact-head Push CI. PR-context CI for this newer head remains unconfirmed due the previously recorded PR/base metadata discrepancy; no topology change or consumer pin update was made.

### PR-context CI root-cause narrowed by exact workflow revision comparison

- Fetched `.github/workflows/ci.yml` by immutable commit ref at both PR #32's reported base SHA and the live target branch head.
- At reported base SHA `b402101ef41d3f9d4f9533545ea83128ba5843a6` (blob `e06ac71bcbd823bc774a6ac118c6e2bcd82d591c`), the `pull_request.branches` filter is `[main, "feat/**", "test/**"]` and omits `fix/**`.
- At live target branch head `e4be499e36ed9d8e22ff45065d95f92e0876df34` (blob `73c528ed3280f0c0c50d50740dac453fc2f801c5`), the filter includes `fix/**`.
- This makes the stale base-SHA/workflow revision mismatch a concrete explanation for why no new PR-context run appears, although the exact GitHub event/metadata update behavior remains unconfirmed. The latest exact-head Push CI remains green; no PR topology operation was performed.
- Do not mark PR #32's PR-context gate passed based on earlier runs. Continue investigating a topology-preserving way to refresh or validate the PR event without merging, retargeting, rebasing, or closing/reopening the PR.

## 2026-10-29 — continued review and PR-context event refresh attempt

- Re-read the current Runner implementation and reusable acceptance workflow at their exact branch refs. Confirmed the Runner now checks report/review output symlink components and artifact containment after tasks, before report emission; the dedicated directory-symlink replacement regression is included in the 121-test passing suite.
- Re-read the reusable acceptance producer and contract: consumer test output is suppressed from logs; report schema binds caller and reusable workflow identities; duplicate keys and unknown fields are rejected; report writing uses a temporary file and atomic replacement; final gate requires runtime, test, report, artifact upload, and verification success.
- PR #32 remains open and Draft. Its API still reports base SHA `b402101ef41d3f9d4f9533545ea83128ba5843a6`, while the live base branch ref was observed at `e4be499e36ed9d8e22ff45065d95f92e0876df34`. The older base commit's CI workflow omits `fix/**`; the live base branch workflow includes it. This is consistent with the missing PR-context event but does not yet prove GitHub's event refresh semantics.
- This archive update intentionally creates a new head commit on the existing PR branch to test whether a fresh `synchronize` event evaluates the updated base workflow. This does not change the PR target, close/reopen the PR, rebase, merge, or alter consumer pins.
- Validation requirement: inspect the new commit's Push CI and any newly generated PR-context run separately. If GitHub still emits no PR-context run, retain that as an unresolved platform/event evidence blocker rather than declaring the gate passed.

### CI trigger probe result

- Probe/archive head `6ab6c6b438aa6ae4b638a12863e48acbe9090af5` passed exact-head Push CI: [run 40867026733](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40867026733).
- After this fresh head update, the PR API still reported base SHA `b402101ef41d3f9d4f9533545ea83128ba5843a6`, and no new PR-context run appeared for the new head. The probe therefore did not close the PR-context gap.
- A PR comment records this result. Continue to keep PR #32 Draft/unmerged and do not treat Push CI as a substitute for PR-context validation. No PR topology changes or consumer pin changes were made.

## 2026-10-29 continued review — runner output hardening and PR-context CI gap

- Harness repository: `wosafety0/dev-workflow-kit`; PR #32 remains Draft/open/unmerged, head branch `fix/review-output-config-collision-20261029`, current head before this archive: `49baad3adc1d508a74204b22c545cbf8fbf53b16`.
- Runner output-path review: `scripts/harness_runner.py` revalidates report/review output symlink components after task completion, rechecks the artifacts boundary, and writes the acceptance report using a same-directory temporary file plus `os.replace`. Regression coverage for an artifacts-directory symlink swap was included in the 121-test suite.
- Exact-head Push CI for `49baad3adc1d508a74204b22c545cbf8fbf53b16` passed: run [40867111522](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40867111522). This is Push CI evidence only.
- PR-context CI remains unresolved for PR #32. The PR API reports base SHA `b402101ef41d3f9d4f9533545ea83128ba5843a6`, while the live base branch ref is `e4be499e36ed9d8e22ff45065d95f92e0876df34`. The workflow at the live base includes `fix/**`, while the older base SHA's workflow omitted it. A progress-only head update did not create a newer PR-context run. Do not count older PR-context success as current-head validation.
- Safe-boundary decision: no PR retarget, merge, rebase, close/reopen, consumer pin update, or further no-op trigger-probe commits. The trigger gap is recorded as a blocker pending a solution that preserves PR topology.
- PR #31 remains Draft/open/unmerged. Its latest known exact-head Push and PR-context validation were previously recorded at archive commit `10c5036e2889a9a28e05c3494b964dbb0023b088`; no consumer pins were changed.
- Next: continue source-level Harness security review and validate the latest archive commit's Push CI. Reassess PR-context CI only if a non-topology-changing route becomes available.


## 2026-10-29 — ignored Python unittest source gate

- Fixed the ignored-test regression in `scripts/harness_runner.py`: before allowing `python -m unittest discover -s tests -v`, the Runner enumerates ignored, untracked paths under `tests/` with `git ls-files --others --ignored --exclude-standard -z` and rejects any basename matching Python unittest discovery's `test*.py` pattern. NUL-delimited parsing is used so filenames are handled without line-splitting ambiguity.
- Added `test_runner_rejects_ignored_python_test_module_before_execution`; it verifies the Runner exits with the policy error, removes any pre-existing report, and never invokes the task runner.
- Exact-head Push CI for `5dacf82089a383094d9855e77852af0abd0f7868` passed: [run 40889112448](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40889112448). The run completed all **122 offline tests**, including the new regression test.
- PR #32 remains open and Draft. Its reported base SHA is still `b402101ef41d3f9d4f9533545ea83128ba5843a6`; the latest PR-context run is still for an older head (`b59f83a1d4c394eade420ce4eadced7897f2a92a`, run [40858714785](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40858714785)). Therefore current-head PR-context CI is **not** validated. Do not substitute the successful Push run for that gate.
- No PR retarget/rebase/merge/close-reopen, consumer pin change, or game action was performed. Next: keep the PR-context gap explicit and continue review only where a meaningful, topology-preserving action is available.

## 2026-10-29 — reusable workflow supply-chain hardening

- Pinned the reusable acceptance workflow's `actions/checkout` and `actions/setup-python` dependencies to full commit SHAs: `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09` and `ece7cb06caefa5fff74198d8649806c4678c61a1`.
- Verified the upstream `actions/checkout` `v5` ref and `actions/setup-python` `v6` ref each resolve directly to the selected commit SHA.
- Updated `docs/REUSABLE_ACCEPTANCE_WORKFLOW.md` and `docs/ORCHESTRATION_FAULT_MATRIX.md` so they no longer claim those workflow dependencies remain tag-pinned.
- Exact-head Push CI for `3653ac1ff7304c4715f34c11d80857c57e76e845` passed: [run 40891643084](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40891643084). The run completed compilation, all offline contract tests, acceptance report generation, artifact upload, and final gate.
- PR #32 remains Draft/open/unmerged. Its PR-context CI gap is still unresolved; this Push run does not satisfy that gate. No PR target/topology changes or consumer pin updates were made.
- Remaining acceptance gaps include real hosted-workflow failure injection (especially an actual artifact-upload failure) and a second unrelated consumer-repository pilot.


## 2026-10-29 — immutable-blob correction for PR #32 trigger diagnosis

- Revalidated the workflow using Git tree entries and immutable blob reads rather than the file-fetch wrapper's ref parameter, which did not return the requested historical revision in the earlier check.
- At PR #32's reported base commit `b402101ef41d3f9d4f9533545ea83128ba5843a6`, tree `975445bf91ef08ae40c1cc28b357961d3f41748a` points to `.github/workflows/ci.yml` blob `e06ac71bcbd823bc774a6ac118c6e2bcd82d591c`; its `pull_request.branches` filter is `[main, "feat/**", "test/**"]` and does **not** include `fix/**`.
- The live target branch head `e4be499e36ed9d8e22ff45065d95f92e0876df34` points to tree `e8c2a57d61396dfbca4d690922f0a11976aceb4c`, whose workflow blob `73c528ed3280f0c0c50d50740dac453fc2f801c5` does include `fix/**`.
- This immutable-blob comparison restores the earlier diagnosis: the workflow revision associated with the PR's reported base SHA excludes the target branch pattern, while the live target branch contains the fix. The prior statement that the base-SHA workflow already included `fix/**` was based on a non-authoritative historical-file read and is superseded by this entry.
- Current head `fac475685b446e0e1a54984f6b1517f7aecf7a5f` has successful exact-head Push CI run [40891713223](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40891713223), but the PR-context run remains absent. A fresh head update did not refresh the reported base SHA, so no further no-op probes will be made.
- Safe boundary remains unchanged: PR #32 stays Draft/open/unmerged; no retarget, rebase, merge, close/reopen, or consumer pin changes. A topology-preserving solution is still needed to make the PR-context gate observable.


## 2026-10-29 — PR-context run timeline and hosted-fault-test boundary

- Current PR #32 head `e86dc0c0b0a68f9ac570369f1c6389b72d0600a8` has exact-head Push CI success (run [40892206446](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40892206446)); the Actions API query for `event=pull_request` shows no run for this head.
- The latest listed PR-context run associated with PR #32 is [40858714785](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40858714785), for head `b59f83a1d4c394eade420ce4eadced7897f2a92a`, created at 2026-10-29T10:35:06Z. The target branch's live commit `e4be499e36ed9d8e22ff45065d95f92e0876df34` was created at 10:37:11Z. This is a temporal correlation, not proof that the target branch update caused the missing runs.
- The PR API continues to report base ref `fix/runner-commit-provenance-20261029` with SHA `b402101ef41d3f9d4f9533545ea83128ba5843a6`, while the branch's observed live head is `e4be499e36ed9d8e22ff45065d95f92e0876df34`. Treat this ref/SHA mismatch as unresolved evidence; do not claim a proven single root cause.
- `.github/workflows/ci.yml` at the current head already contains `fix/**` in the PR base-branch filter. The historical workflow blob at reported base SHA `b402101...` does not. No retarget/rebase/merge/close-reopen or consumer pin changes were made.
- The fault matrix still explicitly distinguishes offline gate tests from hosted artifact-service behavior. Current CI run proves a successful real artifact upload, not a failed upload. The connected GitHub actions available in this session provide run/job reads and file writes but no workflow-dispatch action; therefore a manually dispatched hosted-fault workflow cannot be honestly reported as executed from this session. Do not add a knowingly failing workflow or call offline simulation hosted evidence. A safe next option is a dedicated `workflow_dispatch` fault-injection workflow that expects a controlled missing-file upload to fail and asserts the final gate rejects it, followed by an authorized manual dispatch in GitHub UI; this verifies hosted action failure handling, not an actual GitHub Artifact service outage.


## 2026-10-29 — latest PR #32 exact-head CI recheck

- Current PR #32 head is `f48bc6a89ab7f64679eae80ee7a1c2ecf1a6dd03`. Exact-head Push CI run [40892691379](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40892691379) completed successfully. The job summary confirms checkout, Python setup, rule hash pinning, compilation, offline tests, redacted report generation, artifact upload, and the final gate all succeeded.
- The current-head Actions API query still shows no PR-context run for this head. The latest PR #32 PR-context run returned by the query remains run [40858714785](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40858714785) for older head `b59f83a1d4c394eade420ce4eadced7897f2a92a`. Do not count the current Push CI result as PR-context validation.
- Current PR metadata still reports base SHA `b402101ef41d3f9d4f9533545ea83128ba5843a6`, while the target branch's observed live head is `e4be499e36ed9d8e22ff45065d95f92e0876df34`. The immutable workflow revision at the reported base SHA excludes `fix/**`; the live target branch workflow includes it. This remains the leading explanation for the missing event, but GitHub's exact event/metadata behavior is not proven as a single root cause.
- No further progress-only trigger probes were made. PR #32 remains Draft/open/unmerged; no retarget, rebase, merge, close/reopen, or consumer pin update occurred.
- Hosted fault-injection boundary remains unchanged: prior hosted tests prove fail-closed behavior for a deliberately missing artifact input, not an actual GitHub Artifact service outage. No workflow-dispatch tool is available in this session, so no new manual hosted fault run is claimed.

## 2026-10-29 — PR #32 branch-reference discrepancy and preservation

- The previously recorded PR #32 head `54f7d244be17dc32f945009264e8fee6322e9226` was confirmed retrievable as a commit, and a preservation branch `rescue/pr-32-last-known-head-20261029` was created at that exact SHA.
- The live source branch name `fix/runner-commit-provenance-20261029` currently resolves to the same `scripts/harness_runner.py` blob as base head `e4be499e36ed9d8e22ff45065d95f92e0876df34`; compare also reports those refs identical. This conflicts with the PR body/history that records a later implementation head.
- The earlier PR progress-log update attempt returned HTTP 409 because the target file blob did not match the expected SHA. No change was forced through that conflict.
- Recovery branch exact-SHA comparison verified identical to `54f7d244be17dc32f945009264e8fee6322e9226`. The original PR branch was not force-updated, retargeted, closed, or merged. Restore requires an explicit branch-ref change and is therefore paused pending user decision.
- CI evidence boundary unchanged: historical exact-head Push CI exists for earlier commits, but current PR-context validation is not established.


## 2026-10-30 — Correction: PR #32 head/base refs were previously conflated

- Re-fetched PR #32 metadata directly. The actual PR head ref is `fix/review-output-config-collision-20261029` at `9d3fb4bce16ff75dbfd6003103c3e4d67b02f126`; the PR base ref is `fix/runner-commit-provenance-20261029`, whose recorded base SHA is `b402101ef41d3f9d4f9533545ea83128ba5843a6`.
- Exact-ref comparisons confirm the PR head branch equals its recorded head SHA. The earlier “source branch identical to base” check had compared the PR's *base branch* name to the newer live base head, not the PR head branch. Therefore the prior branch-reference-discrepancy conclusion was incorrect; this is a correction to the investigation record, not evidence of lost code.
- The PR diff is supported by exact commit comparison: recorded base SHA `b402101...` to PR head `9d3fb4b...` is ahead by 62 commits and reports the expected seven changed files. PR #32's current base branch has advanced to `e4be499e36ed9d8e22ff45065d95f92e0876df34`; comparing that live base branch to the PR head reports divergence with the PR head 3 commits behind. This stacked-branch/base drift and `mergeable=false` remain genuine issues to resolve.
- Rescue branch `rescue/pr-32-last-known-head-20261029` is still preserved as an additional snapshot at the previously recorded `54f7d244...` plus its archive commit. No original PR ref, base, review state, or consumer pin was changed.
- Validation boundary: historical Push CI evidence remains historical; current-head PR-context CI is not established by this check. No tests or CI were run in this step.


## 2026-10-30 — Direct source/base file verification (PR #32)

- Read `scripts/harness_runner.py` at the exact merge-base SHA `b402101ef41d3f9d4f9533545ea83128ba5843a6`, the live base SHA `e4be499e36ed9d8e22ff45065d95f92e0876df34`, and the actual source branch `fix/review-output-config-collision-20261029`.
- The merge-base and live-base file blob SHA is `b1be5c0480875aee62f152f5025396c4936d78dd` (12,815 characters). The source branch file blob SHA is `55b39b22113df5a07da7d6e0dcd9108baf1276df` (18,185 characters).
- The source version contains `_reject_duplicate_json_keys` and review-output/config collision protection; the checked base version does not. The source test file blob (`98d5ac1f0b661106533c90003e0476edc26065a7`, 26,571 characters) is also larger than the live-base test file (`0914a5fe3968d5d406f4436f3068606fb97e6c0f`, 13,452 characters) and contains duplicate-key regression coverage.
- This is read-only content verification. No branch or PR refs were changed; no tests or CI were run. Exact-head CI remains unverified for the current source branch.

## 2026-10-30 — Reconcile stacked-branch drift findings (PR #32)

- Fresh PR metadata and commit comparisons confirm the recorded PR head SHA `9d3fb4bce16ff75dbfd6003103c3e4d67b02f126` is exactly the current `fix/review-output-config-collision-20261029` branch tip; the previously suspected source-head mismatch is not reproducible and is resolved as a stale/inconsistent earlier observation.
- The PR's recorded base `b402101ef41d3f9d4f9533545ea83128ba5843a6` advanced to `e4be499e36ed9d8e22ff45065d95f92e0876df34` by three commits. Comparing those base SHAs shows only `.github/workflows/ci.yml` and `docs/PROJECT_PROGRESS.md` changed in that interval; the core runner and test files were not modified by those three commits.
- The current PR head compared with the live base remains diverged (62 commits ahead, 3 behind) and GitHub reports `mergeable=false`. The 62 includes stacked history; it is not a count of changes to replay.
- Read-only patch review confirms PR #32's net implementation includes duplicate JSON key rejection, review-output/config alias rejection, source/config/symlink hardening, and regression tests. The current base's CI workflow and progress log must be preserved during any candidate reconstruction rather than overwritten with stale branch copies.
- The connector's current-head workflow-run lookup returned no PR-triggered run for `9d3fb4b...`; because this lookup filters to PR-triggered runs, this is not proof that Push CI is absent. Exact-head CI remains unverified. No tests were run; no PR/base/source ref was changed.

- Cross-PR overlap check: PR #32 and PR #33 both modify `tests/test_harness_runner.py`. The shared semantic-review argv assertion currently differs: #32 expects raw `Path` string forms, while #33 changes expectations to `.resolve()` for the script, input, and output paths to handle Windows path normalization. Any combined candidate should retain #32's expanded Git/provenance and regression tests while carrying forward #33's resolved-path expectations; do not take either entire test file wholesale.


## 2026-10-30 — candidate reconstruction refs recorded

- Built isolated current-base reconstruction `reconcile/pr-32-on-current-base-20261030` from `e4be499e36ed9d8e22ff45065d95f92e0876df34`, and a CI-intended branch `fix/reconcile-pr-32-current-base-20261030` at commit `ec37ca93e225aef668472e52bd4db485c107fe23`.
- The candidate compare shows 7 changed files, 8 commits ahead, 0 behind; ahead count includes candidate commits and is not a patch-size metric. Files match the expected PR #32 scope. Exact-head CI is not yet visible: combined status is empty and the available workflow-run query returned no runs (it filters to PR-triggered runs).
- Original PR #32 and all rescue snapshots remain untouched. Candidate is not approved for merge; tests/CI remain unverified.


### 2026-10-30 reconciliation candidate final validation
- Candidate branch `fix/reconcile-pr-32-current-base-20261030` now has final archived head `8ac03e05414c36366d96bee87aa482cc45cefbf4`, based on current PR #18 head `e4be499e36ed9d8e22ff45065d95f92e0876df34`.
- Validation-only Draft PR #35: https://github.com/wosafety0/dev-workflow-kit/pull/35 (open, draft, unmerged; GitHub reports mergeable=true).
- Exact-head Harness CI run [40989078845](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40989078845) completed successfully. Verified Python compilation, offline contract tests, redacted acceptance report generation, artifact upload, and final required-stage gate all succeeded.
- Original PR #32 remains unchanged/open/draft at head `9d3fb4bce16ff75dbfd6003103c3e4d67b02f126`; its old base SHA differs from PR #18's current head, and GitHub still reports mergeable=false. No merge, close, retarget, or force-push was performed.


### 2026-10-30 final diff-audit and latest-head CI follow-up
- Final candidate head is now `6055555ce94dc15441048b753744db18feaee59a` on `fix/reconcile-pr-32-current-base-20261030`; validation-only Draft PR #35 remains open and GitHub reports `mergeable=true`.
- Latest exact-head Harness CI [run 40989353911](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40989353911) completed successfully. Verified compilation, offline contract tests, redacted report generation, artifact upload, and final required-stage gate all succeeded.
- Audit confirmed the candidate's `scripts/harness_runner.py` and `tests/test_harness_runner.py` blobs are identical to original PR #32. The candidate's CI workflow additionally fixes the printf newline escape. Original PR #32 remains open/draft at its original head/base and mergeable=false; no original PR state was changed.
- Cross-PR overlap in `tests/test_harness_runner.py` is documented: if a combined branch is needed later, merge PR #33's resolved-path assertions selectively and retain PR #32's expanded suite.


## 2026-10-30 — dependency-chain audit follow-up (PR #32/#18)

- Rechecked live PR metadata and ancestry: PR #18 is still based on PR #14 (which is based on PR #13); PR #32 candidate is based exactly on the current PR #18 head `e4be499e36ed9d8e22ff45065d95f92e0876df34`.
- PR #18's current head is 8 commits beyond PR #14's head; the compare lists `.github/workflows/ci.yml`, `.gitignore`, `docs/HARNESS_RUNNER_V1.md`, `docs/PROJECT_PROGRESS.md`, `scripts/harness_runner.py`, and `tests/test_harness_runner.py`. These are inherited upstream changes, not unexpected PR #32 candidate changes.
- The PR #32 candidate compare against its exact base is 12 commits ahead, 0 behind, and limited to the expected seven files. The commit count includes candidate history; use the seven-file net diff and exact blob checks, not ahead count, as the scope check.
- PR #19's output-alias guard is a sibling branch based directly on PR #13 and is not in the PR #14 → #18 ancestry. PR #32 correctly carries that guard into the #18 line. Do not drop it as a duplicate unless the dependency topology is intentionally redesigned.
- PR #23/#24 are on the separate runner/loopback line (#20 → #22 → #23 → #24) and are not dependencies of PR #32. No evidence in this audit requires importing them into the PR #32 runner/provenance line.
- Candidate CI exact-head run [40989353911](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40989353911) succeeded on candidate head `6055555ce94dc15441048b753744db18feaee59a`. Original PR #32 remains open/draft/unmerged and unchanged; no merge or branch mutation was performed.


## 2026-10-30 — downstream dependency verification follow-up

- Refreshed live metadata for PRs #20, #22, #23, #24, #32–#35. PR #23 remains open/draft/unmerged and mergeable on base #22's recorded head `f71025d2303737dafe18ae823f93cad9cdd1249d`; PR #24 remains open/draft/unmerged and mergeable on PR #23 head `7962697d273e04716e71fcf95536154b03704032`.
- Exact-head hosted Harness CI is green for PR #23 head `7962697...` ([run 40804425695](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40804425695)) and PR #24 head `58702b8...` ([run 40805458873](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40805458873)); inspected job steps confirm Python compilation, offline contract tests, redacted report generation, artifact upload, and final gate all succeeded.
- PR #24 is downstream of the loopback/redirect chain and is not a prerequisite for PR #32's provenance-based candidate. Keep these chains separate unless intentionally building a combined integration branch; do not infer that PR #32 candidate includes PR #23/#24.
- Original PR #32 remains open/draft/unmerged at its recorded head/base; candidate PR #35 remains open/draft/unmerged and mergeable. No PR or branch topology was changed in this review.


## 2026-10-30 — unified validation candidate PR #37
- Created Draft PR #37: https://github.com/wosafety0/dev-workflow-kit/pull/37, based on PR #24's tested head `58702b8ba7e7fde2c384671677aec8784f216c97`.
- Exact archived candidate head `ea05b0813ed25abe5354b7f2bf8d2655a86bf181` passed Harness CI [run 40990643340](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40990643340). Python compilation, offline contract tests, redacted report generation, artifact upload, and final gate all succeeded.
- Candidate combines PR #32 config/path/source protections with PR #33 bounded response/duplicate-key protections while preserving PR #24 redirect handling and fail-fast execution. The shared runner test suite combines expanded path/provenance tests with loopback and Windows path assertions.
- Compare against PR #24 base: 15 commits ahead, 0 behind; intended net diff is 8 files including CI trigger coverage for `integration/**` branches.
- Validation-only Draft; do not merge based solely on CI. Original PR #32 remains open/draft/unmerged and its branch was not altered.


## 2026-10-30 — final unified candidate audit and exact-head CI
- Final audited PR #37 head: `169fa027fecfa0f361da751f86e7df4d2251b4ff`; exact-head Harness CI [run 40990807374](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40990807374) succeeded. Python compilation, offline contract tests, redacted report build, artifact upload, and final required-stage gate all succeeded.
- Diff audit confirms the semantic-review implementation matches PR #33 candidate blob `4a29f02f370704e6b61d2a8ddfe718eb31d99e26`; all 31 PR #32 candidate runner tests are retained, plus the loopback preflight regression (32 runner tests total). Net changed-file list is 8 intended files; no unrelated source modules in the net diff.
- Candidate remains Draft/unmerged; originals #24/#32/#33 and candidates #34–#36 remain open/draft/unmerged. No live provider call, release, or deployment.


## 2026-10-30 — PR #37 follow-up audit correction
- The unified candidate initially omitted two fail-fast regression tests inherited from PR #24's base. Both were restored on candidate head `731c39a5a8c9d1a21312b2c959a6e6dc3c732123`: `test_stops_after_failure_and_marks_remaining_tasks_not_run` and `test_semantic_review_must_be_last_configured_task`.
- Read-back inventory confirms all 14 PR #24 base runner test methods and all 31 PR #32 candidate runner test methods are present, plus the loopback preflight test (34 unique runner test methods total).
- Corrected exact-head CI [run 40991595301](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40991595301) passed compilation, offline contract tests, report build/upload, and final gate. No local test execution or live provider request is claimed.
- PR #37 remains Draft/unmerged; original PR #32 and its branch are unchanged.


## 2026-10-30 — final PR #37 corrected archive head
- Final PR #37 head after the candidate progress archive: `04f455b23e5b17956705a76b5ef74d263956a96c`.
- Exact-head Push Harness CI [run 40991648743](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40991648743) and PR-context CI [run 40991653272](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40991653272) both succeeded, including compilation, offline contract tests, redacted report build/upload, and final gate.
- Final read-back confirms PR #37 has 34 unique runner test methods, all 14 PR #24 base methods, all 31 PR #32 candidate methods, plus the loopback preflight test. PR #37 remains Draft/unmerged; original PR #32 remains unchanged.

 
## 2026-10-30 — unified candidate ignored-source provenance fix
- Static audit of unified PR #37 found the ignored-source check blocked ignored `test*.py` files but did not block ignored helper modules such as `tests/helper.py`, which tracked tests could import while the Git worktree still appeared clean.
- Corrected on PR #37 candidate branch `integration/pr24-pr33-pr32-20261030`: head `bf0b96b2c8dfbcaf623f6b57d09614dc6422ee0b`. The runner now blocks all ignored `.py` files under `tests/`; regression coverage includes an ignored helper module and the existing ignored-test case.
- Exact-head Push CI [run 40992682760](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992682760) and PR-context CI [run 40992686555](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992686555) both succeeded, including compilation, offline contract tests, report generation/upload, and final gate.
- This is a follow-up finding/fix on the unified validation candidate; it does not alter the original PR #32/#33 source refs, and does not authorize merging PR #37.


## 2026-10-30 — broaden ignored-source provenance guard beyond tests/
- Follow-up review found the initial PR #37 correction still checked only `tests/`; ignored Python helper modules under `scripts/` or repository-root paths could also be importable by tracked tests.
- Final correction on PR #37 candidate head `2ee839b9c8cada2fe3c5646d6eae57bc83a138e4`: reject ignored `.py` files across the project tree, excluding generated `artifacts/`, common virtual-environment directories (`.venv`, `venv`, `env`, `.tox`), and `__pycache__`. Added regression coverage for ignored helpers under both `tests/` and `scripts/`; updated runner and acceptance-contract docs.
- Exact-head Push CI [run 40992914390](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992914390) and PR-context CI [run 40992921060](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40992921060) both succeeded for the final head, including compilation, offline tests, report generation/upload, and final gate.
- Dependency/runtime environment contents are not attested by the source commit. The unified candidate remains Draft/unmerged; this archive does not change original PR #32/#33 refs or authorize merge.


## 2026-10-30 — post-task ignored-source revalidation
- Further review identified that a task could create an ignored Python source after preflight; Git status excludes ignored files, so post-task commit checks alone would not catch it.
- PR #37 candidate head `d0c513b19876f057017c4c7fbb5ca52c7d377253` now rejects ignored project Python sources before task planning/execution and rechecks after all tasks. Regression coverage verifies rejection when a task creates an ignored helper; runner and stable contract docs state the boundary.
- Exact-head Push CI [run 40993134186](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993134186) and PR-context CI [run 40993140527](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993140527) both succeeded.
- PR #37 remains Draft/unmerged. Original PR #32 is unchanged; no merge or release is authorized by this archive.


## 2026-10-30 — post-task source cleanliness gate
- Static review found that the runner checked only HEAD after tasks; a task could modify tracked source or create non-ignored untracked source while leaving HEAD unchanged.
- PR #37 candidate head `b9748c3230782e3065923f386bacbd7a2ba83bdd` now reruns the full Git provenance/clean-worktree check after task execution, in addition to checking ignored Python source inventory. Added regression tests for task-created untracked source and task-modified tracked source; updated runner and contract documentation.
- Exact-head Push CI [run 40993507598](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993507598) and PR-context CI [run 40993515179](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993515179) both succeeded.
- Candidate PR #37 remains Draft/unmerged. Original PR #32 source refs remain untouched. Runtime/dependency environment is not attested by source commit.


## 2026-10-30 — semantic-review CLI output hardening
- Static review found the standalone semantic-review CLI accepted symlinked input/output paths and wrote its final JSON directly, exposing output to final-path redirection and partial-write risks.
- Candidate PR #37 head `93adba0e56d3b6b3981c863ec8da24b6df7f482c` rejects symlink components in both CLI paths and writes the result through a same-directory temporary file plus atomic replacement. Output path is rechecked after provider processing. This is not a filesystem sandbox against hostile concurrent parent-directory replacement.
- Regression tests cover symlinked input/output paths and verify a symlink target is preserved. Exact-head Push CI [40993820393](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993820393) and PR-context CI [40993826168](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40993826168) both succeeded.
- Candidate PR #37 remains Draft/unmerged; original PR #32 remains untouched. No local tests or live provider calls are claimed.

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
