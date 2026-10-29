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
- PR #32 remains Draft/unmerged. This result validates the code commit above; the new progress-archive commit itself still requires its own exact-head CI check. PR-context CI for the current head is not yet confirmed. No consumer pin, PR target, branch topology, release, or deployment changed.
