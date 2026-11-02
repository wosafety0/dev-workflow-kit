## 2026-11-02 — Separate report-verifier and optional Git-bound-review stacks

- PRs #25–#31 form a clean report-verifier stack, but it is not part of PR #40. The current reusable workflow does not generate or verify a consumer acceptance report. Exact PR #31 head `10c5036e2889a9a28e05c3494b964dbb0023b088` passed Push [40862336044](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40862336044) and PR [40862345454](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40862345454).
- PR #38 is a clean optional Git-bound-review candidate, but its `--review-base`/`--review-head` API and schema v2/v3 differ from PR #40's mandatory `--review-base-commit` contract. Exact head `98edf6412d9866f4d6fe17d4c3029b4a14864945` passed Push [41020283705](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41020283705) and PR [41020289268](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41020289268). Do not merge as-is.
- PR #39 is documentation-only and its hosted artifact-failure evidence is already in the current roadmap. Original #32/#33 are dirty; reconstructed #34/#35 and unified #37 carry their intended changes; #36 is superseded by #37.
- Recommendation: keep report-verifier and optional provenance enhancements out of the current candidate until the repository owner approves the bounded 0.x scope. They can be evaluated as a separate follow-up release. No PR was closed or merged.

---

## 2026-11-02 — Stacked PR synchronization and current blockers

- PR #1 was reconciled with current main at `74445f42a161b98e25eeb690d3609c366f69379e`. PR #23/#24/#37/#40 now form a clean synchronized stack at `94db1daaea5d2111205e4d92c4ad9fbac0837ddf`, `c8836d419850a6c7fc94fd03c98b141d5da5dc25`, `a6839563ebff0e53642a03fa531551aa6abd8463`, and `6a2900ef34ac23ea1da2da60b8c129b32aadae05` respectively. All are Open and mergeable/clean; none has been merged.
- Exact-head Push and PR-context CI passed for each synchronized head; evidence is recorded in `docs/PROJECT_PROGRESS.md`. No force-push, branch deletion, main update, tag, release, or deployment occurred.
- Harness code/test head remains `22d113f618583eab731d637531110b2e2e9fd316`; immutable independent-consumer pin remains `3df51ca949872fdc75d18feb902220b95957ec37`.
- Private consumer remains unaccepted. Run [41099042827](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) stopped before runner allocation; annotation [124212281392](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) reports failed recent payments or a spending-limit increase requirement. Its `npm test` runs eight static checks plus JavaScript syntax, not browser E2E; `TESTING.md` leaves browser E2E unchecked. No billing/account/policy setting changed.
- Release remains not ready: owner approval of 0.x scope, private exact-head acceptance, browser E2E, consumer safeguards/archive-path acceptance, exact candidate selection, and release preflight remain outstanding.

---

## 2026-11-02 — Two independent consumers passed the current Harness candidate

- Both independent pilot consumers now pin immutable Harness candidate `3df51ca949872fdc75d18feb902220b95957ec37`.
- Node.js 26/pnpm consumer `wosafety0/AI-Worker-Proxy`, exact consumer head `493e561eab8484975c55360916ae15ea2c8320d9`, passed reusable acceptance [41443804502](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41443804502), native PR lint/type-check [41443804014](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41443804014), and push lint/type-check [41443797503](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41443797503).
- Python consumer `quirrellrevess-code/quirrellrevess-Research`, exact consumer head `a3db027b03f72e7504c4a0d31bae1d1027a0b0dd`, passed reusable acceptance [41444151275](https://github.com/quirrellrevess-code/quirrellrevess-Research/actions/runs/41444151275) with **144 tests, OK**, plus native CI [41444150768](https://github.com/quirrellrevess-code/quirrellrevess-Research/actions/runs/41444150768) including offline tests, AIRedirector patch validation, and .NET 10 passive sink smoke.
- This is current-candidate consumer acceptance for both supported runtime paths, not browser E2E, production deployment, or universal compatibility. The separate private `chatgpt-auto-send-assistant` consumer remains unaccepted with no runner allocation/browser E2E evidence.
- Both consumer PRs remain Draft/open/unmerged; Harness PR #40 remains Draft/open/unmerged. No merge, tag, release, deployment, application/game action, billing, permission, visibility, or Actions-policy change occurred.

---

## 2026-11-02 — Independent Node.js consumer passed the current candidate pin

- Updated only the existing public `AI-Worker-Proxy` Draft pilot workflow pin to Harness candidate `3df51ca949872fdc75d18feb902220b95957ec37`; application source, deployment workflow, secrets, permissions, and runtime configuration were unchanged.
- Exact consumer head `493e561eab8484975c55360916ae15ea2c8320d9` passed reusable acceptance [41443804502](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41443804502), native PR lint/type-check [41443804014](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41443804014), and push lint/type-check [41443797503](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41443797503).
- The reusable workflow executed Node.js 26/pnpm 11.4.0, frozen dependency installation, ESLint, TypeScript type-check, and Prettier. All exact-head checks succeeded. This verifies an independent Node.js consumer on the current candidate; it is not browser E2E, production validation, or release approval.
- Consumer PR #2 remains Draft/open/unmerged. Private consumer PR #1 remains unaccepted; no runner allocation or browser E2E evidence is available. The Python 144-test pilot remains tied to its historical Harness pin.
- Harness PR #40 remains Draft/open/unmerged. No merge, tag, release, deployment, consumer application change, secret, permission, billing, visibility, or Actions-policy change occurred.

---

## 2026-11-02 — Canonical Git diff timeout regression and consumer pin freshness

- Promoted the existing 20-second canonical Git diff generation timeout to a named constant and added a regression with a stalled child process. The test proves timeout termination, controlled fail-closed rejection, and no configured task execution.
- Code/test head `22d113f618583eab731d637531110b2e2e9fd316` passed Push [41443102520](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41443102520) and PR-context [41443112694](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41443112694); all four jobs succeeded in both runs. Offline tests: **205 OK**; Windows Runner tests: **65 OK**; reusable Python and Node/pnpm selftests passed. The timeout regression passed on Linux and Windows.
- Consumer recheck: public Node/pnpm PR #2 remains accepted only for its historical consumer head and Harness pin `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5` (240 commits behind this code/test head). The Python pilot's 144-test run used pin `c44f77d6f2b0aae07689e6127b203e1df4e3d77b` (75 commits behind). Neither is current-head consumer acceptance. Private consumer PR #1 remains unaccepted; its recorded run failed before runner allocation with no job steps, and browser E2E is absent. The specific pre-run cause was not independently revalidated.
- PR #40 base SHA `d035dea4426e2dbbb39b22770fc206a5671bfc68` matches PR #37 head. Both PRs remain Draft/open/unmerged. No consumer was modified or repinned. No merge, tag, release, deployment, billing, permissions, visibility, or Actions-policy change occurred.

---

## 2026-11-02 — Canonical Git diff output bounded during provenance verification

- A focused source review found that the caller-supplied semantic-review input was capped at 4 MiB, but the Runner's generated canonical Git diff was captured with an unbounded `subprocess.run` stdout buffer. A very large committed change could therefore consume excessive Runner memory before the input/diff mismatch was reported.
- The Runner now streams canonical diff output and retains at most 4 MiB plus one byte. It terminates Git and blocks before task execution when the diff exceeds 4 MiB or generation exceeds 20 seconds. The failure is closed; no truncated diff is accepted.
- Added a real-Git regression using a tracked file whose canonical diff exceeds 4 MiB; the Runner must return a blocked result and must not invoke configured tasks. Updated the Runner guide and stable acceptance contract.
- Exact implementation/test head `2f3292a2e8af69f819f23774cc0a8facf7034d7a` passed exact-head Push CI [41441441604](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41441441604) and PR-context CI [41441449725](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41441449725). All four jobs succeeded in both runs; offline suite **204 tests, OK**; Windows Runner suite **64 tests, OK**; reusable Python and Node/pnpm acceptance selftests passed.
- This bounds captured diff output, not Git's internal resource use, the Git executable, or the host environment. The Runner remains a trusted-worktree task lifecycle tool, not a sandbox. PR #40 remains Draft/open/unmerged; release decision remains unchanged and not ready to tag.

---

## 2026-11-02 — Cross-platform task descendant lifecycle verified

- POSIX task lifecycle control remains verified: each task runs in a dedicated session/process group; residual group members after normal exit or timeout are terminated, and a task with remaining descendants fails.
- Windows now uses a suspended task process assigned to a Job Object configured with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` before execution resumes. Because `subprocess.Popen` does not retain the primary thread handle, the runner locates the suspended primary thread through Toolhelp32 and resumes it only after assignment. After normal parent exit, the runner queries the Job Object process-ID list, honoring the returned assigned/available PID counts and resizing the query buffer as needed. Remaining descendants make the task fail; closing the Job Object terminates them. Timeout and error paths close the Job Object; setup/query/cleanup failures fail closed.
- Windows regressions cover successful task execution, direct Job Object setup/query, fail-closed setup failure before the suspended task can execute, delayed descendants after normal parent exit, and timeout with delayed descendants. The implementation head `2558861cabc2eaad3d5fb6c8de81252723797bc8` passed Push CI [41378652732](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41378652732) and PR-context CI [41378658408](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41378658408), all four jobs successful. The follow-up fail-closed regression head `64a535a71f73db044e97b7b353149047a6fcfad1` passed Push CI [41379222119](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41379222119) and PR-context CI [41379226619](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41379226619), all four jobs successful; offline suite **203 tests, OK (5 platform-specific skips)**; Windows Runner suite **63 tests, OK (2 POSIX-only tests skipped)**.
- The cross-platform process lifecycle control is **VERIFIED on POSIX and Windows GitHub-hosted runners**, but it is not a sandbox. Job Object assignment can fail under restrictive enclosing-job policies and must fail closed; tasks can still cause work through external brokers/services or other host facilities.
- Report-output path review confirmed that final path/symlink validation plus same-directory temporary write and atomic replacement do not prevent a hostile concurrent replacement of the `artifacts/` parent after the final check. This is documented as outside the trusted-worktree threat model; the Runner is not a filesystem sandbox.
- Release decision remains **not ready to tag or release**. Owner approval of the bounded 0.x scope, complete consumer-specific acceptance, private consumer runtime acceptance, browser E2E, and exact release-candidate selection remain outstanding. PR #40 remains Draft/open/unmerged; no merge, tag, release, or deployment occurred.

## 2026-11-01 — Reusable entrypoint trigger regression guard

- Added `test_reusable_workflow_is_not_directly_triggered` to the reusable workflow contract suite. It asserts the called workflow exposes `workflow_call` and does not acquire direct `push`, `pull_request`, `pull_request_target`, or `workflow_dispatch` triggers. This keeps the acceptance entry point reusable-only; consumer-specific PR trust policy remains the caller's responsibility.
- The exact test head `0f964dc07cee3dc8d952cf9bdb8788646ddfb52e` passed PR-context CI [41274381898](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274381898): offline contract suite, Python reusable selftest, Node/pnpm reusable selftest, report upload, and fail-closed gate all succeeded. Temporary artifact [13070786417](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274381898) expires 2026-11-15. Push-triggered CI for this exact SHA was not independently retrieved.
- PR #40 remains Draft/open/unmerged. No consumer was rerun or repinned; private consumer execution and browser E2E remain pending. No merge, tag, release, deployment, or account/policy change occurred.

## 2026-11-01 — Consumer trust-boundary review and secrets regression gate

- The reusable workflow's caller-supplied `test-command` is arbitrary shell execution of consumer code on a hosted runner, not a sandbox. A `pull_request` caller can be influenced by PR-controlled workflow/test changes. Read-only token permissions, disabled checkout credential persistence, no explicitly mapped secrets, pinned actions, and a bounded timeout reduce exposure but do not provide isolation or network-egress controls.
- The workflow documentation now explicitly warns against secrets/`secrets: inherit` and against using `pull_request_target` to execute PR-controlled code. Official reference: [GitHub — Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target).
- Added a regression test ensuring the reusable workflow itself does not declare secrets, reference the secrets context, or use `secrets: inherit`. Exact test-contract head `b7bdf5deba5b3b919af3760408893829e5a01f80` passed PR-context CI [41271489648](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41271489648), all three jobs successful. The prior docs head `2415539ccd09abb5e2b6f9efb413909948ff9c89` passed [41271405922](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41271405922). Exact-SHA Push CI for those commits was not independently retrieved.
- The public consumer remains one passing independent pilot at its recorded pin; the private consumer remains blocked before runner allocation and has not passed runtime acceptance. Its documented browser E2E remains pending.
- **Release decision unchanged: not ready to tag.** Consumer-specific acceptance, private runtime acceptance, owner approval of the bounded 0.x scope, exact candidate selection, and tag/release preflight remain outstanding. This review does not authorize merge, tag, release, or deployment.

## 2026-11-01 — Consumer PR execution boundary review

- Re-read the exact current consumer heads: public `AI-Worker-Proxy` `87c3633621e455f9ba75ec2caf3ae6ba206e60a8` and private `chatgpt-auto-send-assistant` `0d64bf825cc5a76f3d8603f2e0fb431613715b56`. Both pilot workflows trigger on `pull_request`, request only `contents: read`, and pin the reusable workflow by a full 40-character SHA. Neither caller explicitly maps secrets into the reusable workflow.
- Public consumer command: `pnpm install --frozen-lockfile`, `pnpm run lint`, `pnpm run type-check`, and Prettier check. Its `package.json` confirms the lint and type-check scripts; the current exact-head pilot and native checks are the previously recorded passing runs [41175900745](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900745), [41175900178](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900178), and [41175897003](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175897003). The existing native workflow and Cloudflare deployment boundary remain separate; no deployment workflow or application source was changed.
- Private consumer command: `npm test` resolves to `node scripts/validate.mjs`. The inspected validator checks userscript metadata/version, domains, defaults, status indicators, single-instance guard, and JavaScript syntax. Its own output explicitly says browser behavior is not tested. `TESTING.md` continues to leave real Tampermonkey/ChatGPT browser E2E unchecked. The private exact-head run remains blocked before runner allocation by the previously recorded account payment/spending eligibility annotation; no private runtime test result is available.
- **Security interpretation:** the reusable workflow checks out consumer code and executes the caller-supplied shell command. With a `pull_request` trigger, a PR that can modify the caller workflow or checked-out test code can influence what runs. This is arbitrary consumer-code execution on a hosted runner, not a sandbox. `contents: read`, disabled checkout credential persistence, no explicitly mapped secrets, pinned actions, and a 15-minute timeout reduce exposure but do not isolate the command or restrict network egress.
- Consumers must review the caller workflow and test command as executable code, keep effective token permissions read-only for untrusted PRs, avoid passing secrets or using `secrets: inherit`, and must not move this pattern to `pull_request_target` while checking out/executing PR-controlled code. Verify the effective repository/organization Actions policy for fork PRs rather than assuming defaults. Do not use this workflow as a security boundary for arbitrary third-party contributions.
- No code/workflow behavior changed in either consumer. No consumer rerun, repin, browser action, deployment, secret, permission, Actions-policy, visibility, merge, tag, or release change occurred. This source review does not close Stage 4 or approve release.

## 2026-11-01 — CI checkout credential hardening and exact-head verification (pre-archive f43024686b53b4e3668284539656d80bd19c6cfe)

- Security review found that the main `.github/workflows/ci.yml` offline-test job used `actions/checkout` with the default credential persistence behavior. Although the workflow grants only `contents: read`, leaving the token in local Git configuration was unnecessary while repository code/tests execute. Added `persist-credentials: false` to the checkout step.
- Added `test_checkout_does_not_persist_credentials` to `tests/test_ci_workflow_contract.py`, asserting the main CI checkout explicitly disables credential persistence. The reusable consumer workflow already had this protection; this change aligns the main CI job with it.
- Preserved the intermediate regression accurately: commit `545e1f743ab01085996a2219ab0e5ddf13b85cc8` failed Push and PR CI because the newly added regex assertion double-escaped whitespace. Corrected the assertion to use whitespace matching in `f43024686b53b4e3668284539656d80bd19c6cfe`; this was a test-expression defect, not a workflow runtime failure.
- Final exact-head Push CI [41270535774](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41270535774) and PR-context CI [41270538970](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41270538970) both completed successfully on `f43024686b53b4e3668284539656d80bd19c6cfe`. Job-level inspection confirms `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance` all passed in both runs. Offline compilation, contract tests, redacted acceptance-report generation/upload, and fail-closed gate passed.
- This is a narrow credential-hygiene improvement; it does not alter the reusable workflow API or consumer pins. PR #40 remains Open/Draft/unmerged. The public consumer remains one passing independent pilot. The private consumer remains blocked before runner allocation by the previously recorded account billing/spending eligibility gate and is not accepted.
- Owner approval of the bounded 0.x scope, complete consumer-specific safeguards/archive-path acceptance, exact release-candidate selection, and tag/release preflight remain outstanding. No consumer rerun/repin, merge, tag, release, deployment, billing, Actions-policy, permission, or visibility change occurred. This archive does not authorize release.

---

## 2026-11-01 — Latest Harness and consumer recheck (pre-archive head c46b9e4afcc3b4171ea97c768e0703d9d3033247)

- Re-read the current branch state and verified Harness PR #40 remains Open/Draft/unmerged at exact head `c46b9e4afcc3b4171ea97c768e0703d9d3033247`, based on `integration/pr24-pr33-pr32-20261030`; no reviewers are requested. Public consumer PR #2 and private consumer PR #1 also remain Open/Draft/unmerged at their previously recorded heads.
- Exact-head Harness Push CI [41259234649](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41259234649) and PR-context CI [41259239346](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41259239346) both completed successfully. Job-level inspection confirms all three jobs passed in both runs: `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`. Offline compilation, contract tests, redacted report generation/upload, and the fail-closed gate passed; both runtime selftests executed their consumer-owned commands.
- Public consumer [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), head `87c3633621e455f9ba75ec2caf3ae6ba206e60a8`, still has a passing Harness acceptance run [41175900745](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900745). Direct commit comparisons against current Harness head show its pin `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5` is 44 commits behind, zero behind the current branch, and the diff does not include `.github/workflows/reusable-acceptance.yml`.
- Private consumer [chatgpt-auto-send-assistant PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1), head `0d64bf825cc5a76f3d8603f2e0fb431613715b56`, remains **not accepted**. Its latest recorded run [41099042827](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) has a failed job with no steps/runner allocation. The previously retrieved check-run annotation identifies an account payment/spending-limit eligibility gate; the message does not distinguish which condition applies. Direct comparison shows its pin `37dc07c7d7055a740c754ab543eeecc9e01d9db0` is 65 commits behind, zero behind current Harness, and the diff does not include the reusable workflow definition. This compatibility comparison does not substitute for its missing runtime acceptance.
- The bounded 0.x scope still requires explicit repository-owner approval. Consumer-specific preservation/archive-path acceptance remains incomplete; no exact release-candidate SHA is selected. PR #40 and both consumer PRs remain Draft/unmerged.
- No rerun of the blocked private job, consumer repin, merge, tag, release, deployment, billing, Actions-policy, permission, or visibility change occurred. This is a pre-archive verification record; the resulting documentation commits require their own exact-head CI verification.

---

## Pre-archive head verification — 2026-11-01

- Verified pre-archive head: `f62dc4ae4ff578a921a8850b678790b0b162e080`. Exact-head Push CI [41256664945](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256664945) and PR-context CI [41256669345](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256669345) both completed successfully for the same SHA.
- PR-context and Push job-level inspection confirms all three jobs succeeded in both runs: `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`. Offline compilation, contract tests, redacted acceptance-report generation/upload, and the fail-closed gate passed; both reusable runtime jobs validated inputs and executed their consumer-owned acceptance commands.
- This entry records the verified pre-archive SHA rather than claiming the documentation commit created by this archive is its own parent. It supersedes the prior stale current-head labels. The archive commit is documentation-only and its CI is tracked independently.
- This CI result does not resolve private-consumer acceptance, prove browser end-to-end behavior, establish consumer archive-path requirements, approve the 0.x scope, or select a release-candidate SHA. PR #40 remains Open/Draft/unmerged.
- The private consumer remains blocked before runner allocation by the recorded account billing/spending eligibility gate; no rerun or billing/Actions-policy change was performed. Consumer-specific safeguard acceptance remains open.
- No consumer repin, merge, tag, release, deployment, billing, or repository policy change occurred. The release decision remains **not ready to tag or release**.

# 0.x Release Candidate Review

Review date: 2026-10-31  
Repository: `wosafety0/dev-workflow-kit`  
Review branch: `feat/reusable-node-runtime-20261030`  
Reviewed implementation baseline: `04a6ae3bb64db7fd348bfc2136dbc9430dc4d9ca` (subsequent commits in this review series changed documentation only)  
Decision: **Not ready to tag or release**

## Latest documentation-archive verification — 2026-10-31

- Current reviewed branch head after the consumer safeguard source cross-check: `96c73593ebebaad0a273ec69af8ad1adc7f0f8c6`.
- Exact-head Push CI [41180765645](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41180765645) and PR-context CI [41180769546](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41180769546) both completed with conclusion `success`; each passed `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`.
- This head contains documentation-only consumer safeguard review/archive changes after the implementation baseline stated above. These results verify the current archive tree and do not close the private-consumer runtime gate, confirm its archive-path expectations, or authorize a release.

## Latest exact-head CI and Node 24 maintenance review — 2026-11-01

- Current branch head reviewed: `78ecab1eea5efae51aaa5ccef970d15d78625f1d`. Exact-head Push CI [41229475265](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41229475265) and PR-context CI [41229480451](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41229480451) both completed successfully. Each run passed `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`.
- Intermediate Node 24 artifact-upload maintenance commit `cc9fae27f5ba39c210ecaed7fbca7e3f2549922f` failed both Push [41228890845](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41228890845) and PR [41228894623](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41228894623). Job logs identify a regression-test regex defect: `test_every_external_action_is_pinned_to_a_full_commit_sha` used double-escaped whitespace tokens and found zero `uses:` lines. The same single contract-test failure caused both offline and Python selftest failures; Node/pnpm selftest passed. This was not a workflow runtime failure.
- Follow-up commit `a9b6f17099afa07f9cbb2f8a0410560f9c1ed38b` corrected the test to match horizontal whitespace explicitly (`[ \\t]`), retained the full-SHA action-pin assertions, and used the verified Node 24-compatible `actions/upload-artifact@v7.0.2` immutable SHA `cf430e030ddbb5b0abf93d22962f4752f3646cd9`. Its exact-head Push [41228919858](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41228919858) and PR [41228924340](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41228924340) both passed all three jobs; the offline suite reported 169 tests, OK. Subsequent documentation heads `e6eac8a4...` and `78ecab1e...` also passed both CI contexts, with all six latest job results successful.
- The correction is test-only plus a CI artifact-action runtime pin; no consumer repositories were modified or repinned. The current head is a documentation archive after the tested maintenance implementation. No Node.js 20 deprecation warning remained in the final offline job log recorded for `a9b6f170...`.
- This verification does not close private-consumer exact-head acceptance, browser end-to-end validation, owner approval of the 0.x scope, or release-candidate SHA selection. PR #40 remains Draft/open/unmerged; no tag, release, merge, deployment, billing, or Actions policy change occurred.

## Scope

This is a bounded review of the reusable acceptance workflow, its caller-side CI integration, documented acceptance contract, workflow-contract regression tests, and current consumer pilot evidence. It is not a full security audit, dependency attestation, live model validation, or production-readiness certification.

## Verified evidence

- Harness exact-head Push CI [41176249364](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41176249364): conclusion `success`, head SHA `04a6ae3bb64db7fd348bfc2136dbc9430dc4d9ca`.
- Harness exact-head PR-context CI [41176252292](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41176252292): conclusion `success`, same head SHA. Both runs passed `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`.
- Independent public consumer [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), head `87c3633621e455f9ba75ec2caf3ae6ba206e60a8`, pins Harness SHA `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5`. Its reusable acceptance [41175900745](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900745), PR checks [41175900178](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900178), and Push checks [41175897003](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175897003) passed.
- Private consumer [chatgpt-auto-send-assistant PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1) remains unaccepted. Run [41099042827](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) failed before runner allocation; annotation `124212281392` cites account payment/spending-limit eligibility. It does not show that the workflow or test command executed.
- Both consumer PRs and Harness PR #40 remain Draft/open/unmerged.

## Bounded review findings

### Documentation drift corrected in follow-up review

A cross-document check found that `docs/ORCHESTRATION_FAULT_MATRIX.md` incorrectly said third-party Actions were still version-tag pinned, although the current workflows use full commit SHA pins. The claim is corrected. Two older roadmap headings that said “Latest” were also relabeled as historical snapshots because their referenced commits are superseded by the current-facing verification section. This is a documentation consistency correction, not a workflow behavior change.

### No reproducible defect found in the inspected workflow contract

The current source and regression tests cover:
- Explicit `workflow_call` interface and stable defaults.
- Allowlisted runtime/package-manager combinations and validation before the consumer command.
- Rejection of blank/whitespace-only commands.
- Consumer command execution through an environment variable under Bash strict mode, including propagation of command and pipeline failures.
- Workflow permission boundary `contents: read`.
- Third-party actions pinned to full commit SHAs.
- Checkout credential persistence disabled.
- A 15-minute reusable job timeout.
- Actual in-repository workflow-call integration for Python and Node/pnpm.

This finding is deliberately limited to the reviewed scope. A green CI run proves only the tested behavior for the exact SHA, not that every consumer command is safe or adequate.

### Consumer-specific safeguard cross-check — 2026-10-31

A source-level cross-check was completed against both current Draft consumer heads. This is narrower than successful runtime acceptance and does not close the Stage 4 gate.

- **Public Node.js/pnpm consumer** — [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), head `87c3633621e455f9ba75ec2caf3ae6ba206e60a8`: the Harness pilot is a separate `.github/workflows/harness-acceptance-pilot.yml` workflow. The consumer's existing `.github/workflows/lint.yml` remains present, and the Harness command independently runs frozen-lockfile installation, lint, type-check, and Prettier check. The exact-head Harness run [41175900745](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900745) and the existing native lint/type-check runs [41175900178](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900178) and [41175897003](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175897003) passed.
- **Private Node.js consumer** — [chatgpt-auto-send-assistant PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1), head `0d64bf825cc5a76f3d8603f2e0fb431613715b56`: the Harness pilot calls `npm test`, matching the existing `package.json` script `node scripts/validate.mjs`. `TESTING.md` still explicitly marks real Tampermonkey/ChatGPT browser end-to-end validation as pending and documents that static checks do not prove browser behavior. No browser automation, send/archive action, application-code change, or deployment was performed. The exact-head run remains blocked before runner allocation by the previously recorded account billing/spending eligibility annotation, so the command has not been executed by that run.
- No root `AGENTS.md` was present at either inspected consumer branch root (GitHub returned 404); the inspected consumer `README.md`, `package.json`, `TESTING.md`, and workflow files were used as available source evidence. This does not establish that no deeper or externally supplied project rules exist.
- **Result:** the visible pilot configuration does not replace the public consumer's native lint workflow or the private consumer's documented static test command, and the private consumer's manual browser-validation limitation remains explicit. However, the overall roadmap criterion “Preserve each consumer's project-specific tests, safety constraints, and archive paths” remains unchecked until the private consumer obtains a successful exact-head acceptance run and the remaining project-specific archive-path expectations are confirmed. Do not infer full acceptance from static inspection alone.

### Consumer archive-path and deployment-boundary inspection — 2026-10-31

Read-only recursive Git tree inspection at the pinned pilot heads was completed for both consumer repositories (GitHub returned `truncated: false` for each tree):

- Public `wosafety0/AI-Worker-Proxy` at `87c3633621e455f9ba75ec2caf3ae6ba206e60a8`: no tracked `AGENTS.md`, dedicated progress/archive document, or named archive directory was found by the path inspection. The tree contains distinct `.github/workflows/deploy.yml`, `lint.yml`, and `harness-acceptance-pilot.yml` files. Its README describes a Cloudflare deployment and secret/variable workflow; this consumer-owned deployment and credential boundary is **not** delegated to the Harness pilot. No deployment or credential operation was performed.
- Private `wosafety0/chatgpt-auto-send-assistant` at `0d64bf825cc5a76f3d8603f2e0fb431613715b56`: no tracked `AGENTS.md` or dedicated progress/archive path was found by the path inspection. Its `TESTING.md` remains the visible test-scope record, and its README warns that static validation is not a real browser end-to-end test. No browser or send/archive action was performed.
- The inspected trees establish **absence of a matching tracked path at those exact heads**, not absence of external/private project instructions, untracked files, or future consumer archive requirements. Consumer ownership of any later-defined archive destination remains intact. Do not mark Stage 4 complete on this negative evidence.
- Harness review branch was previously verified at `5a636ae507b23d51b06bcbbeffdb1f7d11251d17`: exact-SHA Push CI [41181327799](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41181327799) and PR-context CI [41181329725](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41181329725) each passed the offline, Python, and Node/pnpm jobs. This is historical evidence after this documentation update, not a claim about the new head.

### Draft PR #40 base-diff preflight — 2026-10-31

Read-only GitHub PR file-diff inspection found **8 changed files** relative to the PR base: `.github/workflows/ci.yml`, `.github/workflows/reusable-acceptance.yml`, `tests/test_reusable_workflow_contract.py`, `docs/ORCHESTRATION_FAULT_MATRIX.md`, `docs/PROJECT_PROGRESS.md`, `docs/RELEASE_CANDIDATE_REVIEW.md`, `docs/REUSABLE_ACCEPTANCE_WORKFLOW.md`, and `docs/ROADMAP.md`. GitHub reports 989 additions and 18 deletions. The changes are workflow wiring, workflow contract tests, and documentation; no consumer application code, deployment workflow, secrets file, or package lockfile is in this PR diff.

- The caller CI adds Python and Node/pnpm `workflow_call` selftests; the reusable workflow adds runtime selection and input validation, conditional setup, disabled checkout credential persistence, and a 15-minute timeout. The reviewed patch retains the consumer-owned shell command executed with `bash -euo pipefail`; it is **not** a sandbox for untrusted commands.
- The added contract test suite checks action SHA pin syntax, allowed input combinations, command validation, strict-shell failure propagation, and other workflow invariants. The exact-head documentation-archive commit `3887ae102f3eeabc536283462fe187dadbd3cc96` passed [Push CI 41211317391](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41211317391) and [PR-context CI 41211321794](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41211321794), all three jobs successful in each run.
- This is a **bounded changed-file preflight**, not a full dependency/security audit or a complete base-to-head source audit. No reproducible defect was identified in the inspected workflow patch; existing limits on consumer test coverage, private runner eligibility, and project-owned safety/archiving still apply.
- A read-only lookup for Git ref `refs/tags/v0.1.0` returned 404, but the complete tag namespace could not be enumerated through the available endpoint. Therefore **no tag-name availability or release preflight is certified**, and no specific release tag is selected.
- Do not equate this working-branch head with an approved release-candidate SHA. Owner scope approval, consumer-specific acceptance, candidate selection, and a complete tag/release preflight remain open.

### Consumer immutable-pin compatibility comparison — 2026-10-31

Read-only GitHub compare API checks against the last verified Harness documentation head `84f16686811c87618caab025e69c47fa628c7d3a`:

- Public `AI-Worker-Proxy` pins `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5`. Comparison to the reviewed head: `ahead`, 30 commits, zero behind. The compare file list contains **documentation changes only** (`docs/ORCHESTRATION_FAULT_MATRIX.md`, `docs/PROJECT_PROGRESS.md`, `docs/RELEASE_CANDIDATE_REVIEW.md`, `docs/ROADMAP.md`); it does not change the reusable workflow. This establishes identical workflow source between these two refs, not that the public consumer has run with the later SHA. Its successful pinned-head consumer CI remains the evidence for the older pin.
- Private `chatgpt-auto-send-assistant` pins `37dc07c7d7055a740c754ab543eeecc9e01d9db0`. Comparison to the reviewed head: `ahead`, 51 commits, zero behind. No change to `.github/workflows/reusable-acceptance.yml` appears in the compare file list; later changes include Harness `.github/workflows/ci.yml`, workflow contract tests, and documentation. Thus the reusable workflow definition is unchanged between the private pin and the reviewed head, but **private acceptance remains unexecuted** due to the account-level pre-run gate.
- The consumer pilot workflow files were re-read: public Node 26/pnpm 11.4.0 runs frozen install, lint, type-check, Prettier; private Node 24/no package manager setup runs `npm test`. Both reference full immutable 40-character Harness SHAs. Neither consumer was repinned or modified.
- Reviewed head `84f16686811c87618caab025e69c47fa628c7d3a` passed exact-head [Push CI 41211718609](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41211718609) and [PR-context CI 41211723904](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41211723904); all three jobs succeeded in each run. The evidence does not establish an approved release-candidate SHA or substitute for consumer-specific runtime acceptance.
- **Disposition:** no workflow-definition compatibility change detected in the compared range, but consumer adoption of the later SHA and the private consumer's successful run are unverified. Do not mark consumer safeguards or release gates complete.

### Remaining release gaps

1. **Consumer-specific safeguards:** Roadmap Stage 4 still requires preserving each consumer's own tests, safety constraints, and archive paths. The successful public pilot proves one integration configuration; the private consumer remains blocked before execution. Keep this criterion unchecked until evidence supports the criterion or the roadmap's acceptance scope is explicitly reviewed and changed.
2. **Private consumer evidence:** The account billing/spending eligibility gate needs to be resolved by the account owner. Do not repeatedly rerun, change Actions policy, or count the current run as acceptance.
3. **Exact release candidate:** Before tagging, choose and record the exact candidate SHA; inspect its diff and run Push and PR-context CI on that same SHA; ensure all required jobs succeed; and re-check the consumer pin/evidence against the candidate being released.
4. **Release scope approval:** The recommended scope and non-goals are now documented above. The repository owner still needs to approve or revise that scope; then verify the README and versioning/upgrade/rollback instructions match the approved scope.
5. **Distribution/release procedure:** Before any tag or release, verify the intended tag name does not already exist, document how consumers pin the immutable commit, and define rollback as reverting the consumer pin. No tag/release is created by this review.

## Proposed initial 0.x scope (recommendation; not release authorization)

The most maintainable first release would be a **source-distributed early-development toolkit**, consumed by immutable commit SHA rather than relying on a mutable branch or tag.

### Include
- Provider-agnostic semantic-review core and its input/output validation contract.
- Offline contract tests and fail-closed CI evidence generation.
- Versioned configuration validation and the fixed, allowlisted task runner.
- Deterministic, redacted acceptance reports and the reusable Python/Node.js acceptance workflow with optional pnpm setup.
- Documentation that defines consumer responsibilities, security boundaries, known limitations, and immutable-SHA upgrade/rollback.

### Explicitly do not promise
- A stable API/CLI compatibility guarantee beyond the documented early 0.x contract.
- Complete defect detection, model quality, or successful live-provider behavior from offline CI.
- Compatibility with every consumer project without consumer-specific tests and safeguards.
- Dependency provenance/attestation, sandboxing of arbitrary untrusted shell commands, or production readiness.
- Autonomous source edits, PR merges, deployments, or business actions.
- Permanent retention of CI artifacts; the workflow artifact is temporary evidence.

### Distribution and rollback recommendation
- Record one exact candidate commit SHA and its successful Push and PR-context CI runs.
- Create a version tag only after the remaining acceptance gates are met and the repository owner approves the release scope.
- Ask consumers to pin the reviewed 40-character SHA. Rollback is a consumer PR reverting to the previous known-good SHA and its recorded evidence.
- Keep the existing Draft PRs unmerged until their separate review/merge decisions are made.

This is a bounded scope recommendation for owner review, not evidence that the release is ready and not authorization to tag, publish, or merge.

## Gate checklist

- [x] Current Harness branch head identified.
- [x] Exact-head Push and PR-context CI conclusions verified.
- [x] Python and Node/pnpm reusable workflow integration jobs verified green.
- [x] One independent public consumer verified at a pinned Harness SHA.
- [x] Private-consumer pre-run blocker classified from its check-run annotation.
- [x] Bounded source/tests review recorded with limitations.
- [x] Cross-checked current-facing documentation against implementation; corrected the stale version-tag-pinning claim in `docs/ORCHESTRATION_FAULT_MATRIX.md` and labeled superseded roadmap evidence as historical snapshots.
- [ ] Consumer-specific safeguards acceptance criterion resolved with evidence.
- [ ] Release scope approved and written down.
- [ ] Exact release candidate SHA selected and its CI re-verified.
- [ ] Tag/release preflight completed.

## Safety and status

No merge, tag, release, deployment, billing change, repository policy change, secret change, or consumer application behavior change was performed. The current PR remains Draft/open/unmerged. Revisit this decision only after the unchecked gates are resolved; do not infer release readiness from green CI alone.

## Latest exact-head and release-gate recheck — 2026-11-01

- Pre-archive Harness head `e2f7560235c20292539adec1dd2f53cacc9ad1be` passed exact-head Push [41256913332](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256913332) and PR-context [41256916534](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256916534), with all three jobs successful in both runs. PR #40 remains Open/Draft/unmerged.
- Current-head comparisons to both consumer pins show no change to `.github/workflows/reusable-acceptance.yml`: public consumer pin `c4cf3e1c...` is 42 commits behind the current branch; private consumer pin `37dc07c7...` is 63 commits behind. Neither consumer was repinned. This is source compatibility evidence only, not consumer execution.
- Private consumer run [41099042827](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) still has no runner or steps; annotation [124212281392](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) cites an account payment/spending eligibility gate without distinguishing its underlying billing condition. Private exact-head acceptance remains incomplete.
- GitHub Releases inventory returned no releases. The tags-list endpoint was unavailable through the current connector, so tag namespace availability is not certified. No release candidate is selected; initial 0.x scope approval and consumer-specific acceptance remain outstanding.
- No merge, tag, release, deployment, billing, permissions, visibility, or Actions-policy change was made. This is a pre-archive record; verify the resulting archive commit's CI independently.

## Tag namespace and latest archive-head CI — 2026-11-01

- GitHub's matching tag refs endpoint returned an empty array; the repository currently has zero Git tag refs. This supersedes the earlier note that the tags-list endpoint was unavailable. A future candidate tag-name conflict check is still required after the exact candidate and tag name are selected.
- Archive head `0342ef1beab6a0048e566c865191c0f78e146910` passed exact-head Push [41257280862](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41257280862) and PR-context [41257284495](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41257284495), with all three jobs successful in both runs.
- PR #40 remains Open/Draft/unmerged. The public consumer pilot remains successful at its recorded immutable pin. The private consumer still has no successful exact-head execution because its job is blocked before runner allocation by the account payment/spending eligibility gate.
- Release gates remain open: consumer-specific safeguards acceptance, private exact-head execution, explicit owner approval of the bounded 0.x scope, exact release-candidate SHA selection, and candidate/tag-name release preflight. No merge, tag, release, deployment, billing, permissions, visibility, or Actions-policy change occurred.

## Latest verification update — 2026-11-01

- Current PR #40 head is `e02393a028dcef947bade0a0c5ee3f22a9dd6142`, Open/Draft/unmerged. PR-context CI [41270587376](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41270587376) passed all three jobs. A Push-triggered run for this exact SHA was not independently retrieved in this check; the PR-context result is not represented as Push CI.
- Main CI checkout now sets `persist-credentials: false`, and `tests/test_ci_workflow_contract.py` asserts this credential-isolation setting. The reusable acceptance workflow definition is unchanged from prior consumer pins.
- Current public consumer [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2) head `87c3633621e455f9ba75ec2caf3ae6ba206e60a8` actually pins Harness SHA `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5`. Consumer commit [87c3633](https://github.com/wosafety0/AI-Worker-Proxy/commit/87c3633621e455f9ba75ec2caf3ae6ba206e60a8) changed the preceding `37dc07c...` pin back to `c4cf3e1...`; earlier references to `37dc07c...` describe the preceding consumer head and must not be treated as the current pin. Exact-head Harness run [41175900745](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900745) and native PR check [41175900178](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900178) passed.
- The reusable workflow at public pin `c4cf3e1...`, private pin `37dc07c...`, and current Harness head `e02393a...` resolves to the same blob SHA `a5fccae44358222a0d453c33afbe90f95d29f191`. Current Harness comparisons are 53 commits ahead of the public pin and 74 ahead of the private pin, zero behind; neither range changes the reusable workflow definition. This is source compatibility evidence, not proof that either consumer executed at the current Harness head.
- Private consumer remains blocked before runner allocation by the recorded account payment/spending eligibility annotation. No rerun, billing change, Actions-policy change, or consumer repin was performed.
- Release scope approval, consumer-specific safeguards/archive-path acceptance, private exact-head execution, exact candidate SHA selection, and tag/release preflight remain outstanding. No merge, tag, release, or deployment occurred.

## 2026-11-01 — Exact latest-head CI and workflow-contract archive

- Current PR #40 head `f2ff0d8352cd8344ad22fd8a75010000b5454a39` is Open/Draft/unmerged against `integration/pr24-pr33-pr32-20261030`; GitHub reports `mergeable: true`. No review submissions or inline review threads are present.
- Both CI event types were independently queried for this exact SHA and completed successfully: Push [41274416669](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274416669) and PR-context [41274419365](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274419365). Each run passed all three jobs: `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`. Job inspection confirmed Python compilation, all offline contract tests, acceptance-report generation/upload, the fail-closed gate, and both runtime selftest commands.
- The current test head includes `test_reusable_workflow_is_not_directly_triggered`, which guards `workflow_call`-only exposure and rejects direct `push`, `pull_request`, `pull_request_target`, and `workflow_dispatch` triggers. The reusable workflow source blob remains `a5fccae44358222a0d453c33afbe90f95d29f191`; no consumer repin or reusable-workflow interface change occurred in this archive commit.
- Push artifact `acceptance-report` ID `13070885561` and PR-context artifact ID `13070546007` are retained until 2026-11-15. These are temporary CI evidence, not permanent release artifacts.
- Public consumer `AI-Worker-Proxy` remains verified only at its current immutable pin `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5`; it was not repinned. Private consumer `chatgpt-auto-send-assistant` remains blocked before runner allocation by the recorded account payment/spending eligibility annotation; do not rerun or alter billing/Actions policy as part of this work. Private exact-head acceptance and browser E2E remain incomplete.
- Release gates remain open: explicit owner approval of the bounded initial 0.x scope, complete consumer-specific safeguards/archive-path acceptance, private exact-head runtime acceptance, exact candidate SHA selection, and final tag/release preflight. No merge, tag, release, deployment, consumer repin, billing, permission, visibility, or Actions-policy change occurred.

## 2026-11-01 — Main CI permission regression contract

- Added `test_workflow_permissions_are_read_only` to `tests/test_ci_workflow_contract.py`. It asserts the main CI workflow retains top-level `contents: read` permissions and rejects write-scoped permission entries, complementing the existing reusable-workflow permission contract.
- Exact implementation/test head `7691473a46c98bf65e361ba3bfba442d91ed1140` passed both Push [41274828767](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274828767) and PR-context [41274833125](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274833125) CI. All three jobs succeeded in both runs; the offline compilation, full contract test suite, acceptance report upload, and fail-closed gate passed, as did reusable Python and Node/pnpm selftests.
- This is a regression guard for the existing read-only workflow configuration; it does not change workflow permissions or consumer behavior. PR #40 remains Draft/open/unmerged. Consumer-specific acceptance, private consumer execution, owner approval of the bounded 0.x scope, candidate selection, and tag/release preflight remain open. No merge, tag, release, deployment, consumer repin, billing, permission, visibility, or Actions-policy change occurred.

## 2026-11-01 — Main CI trigger and secret-boundary regression guards

- Added two tests to `tests/test_ci_workflow_contract.py`: `test_ci_workflow_does_not_use_pull_request_target` and `test_ci_workflow_does_not_forward_or_reference_secrets`. They protect the existing main CI `pull_request` trust model and prevent accidental secret declarations, direct secret-context references, or `secrets: inherit` in the CI workflow's reusable selftests. No workflow trigger, permission, secret, or consumer behavior was changed.
- The first test draft at `d589e5fb770bc5ad36a1da1c1d8080c4a9f70cce` failed both Push [41275111072](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275111072) and PR-context [41275113805](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275113805): the test delimiter was over-escaped and raised `IndexError` before evaluating the trigger. This was a test implementation error, not a workflow/runtime defect. The test was corrected in `dd516a11751f5f72902dd2f4e2553c72f14bbbcf`.
- Corrected exact-head Push [41275149674](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275149674) and PR-context [41275153223](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275153223) both completed successfully. All three jobs passed in each run. The offline log confirms **175 tests, OK**, including both new tests; report generation, artifact upload, and the fail-closed gate passed.
- Read-only review of the current consumer PR files confirms both pilot callers still use `pull_request`, `contents: read`, and full immutable Harness SHAs, without explicit secrets mapping. Public consumer checks remain green at its exact current consumer head and old Harness pin; private consumer remains blocked before runner allocation by the previously recorded account payment/spending eligibility gate. Its browser E2E is still incomplete.
- PR #40 remains Open/Draft/unmerged and mergeable; no review submissions or inline review threads were found. GitHub rulesets and tag refs returned empty lists; releases inventory is empty. These observations do not constitute a branch-protection guarantee or release authorization. Owner approval of the bounded 0.x scope, consumer-specific acceptance, private exact-head runtime acceptance, candidate selection, and release preflight remain outstanding. No merge, tag, release, deployment, consumer repin, billing, permissions, visibility, or Actions-policy change occurred.

## 2026-11-01 — Harness Runner direct-script entrypoint fix

- The documented `python scripts/harness_runner.py` command imported `scripts.acceptance_report` and `scripts.harness_config` before ensuring the repository root was on `sys.path`. Direct script execution places `scripts/` first on the module path, so the documented invocation could fail with `ModuleNotFoundError` in a clean environment. This was a real CLI usability gap; earlier unit tests called the imported `main()` function and did not exercise the process entry point.
- Updated `scripts/harness_runner.py` to add its repository root to `sys.path` only when invoked as a direct script, before importing local Harness modules. Added `test_documented_script_entrypoint_supports_direct_execution`, which launches the documented script in a subprocess with `--help` from the repository root. This verifies startup/import and CLI parsing; it does not claim a full end-to-end runner task execution.
- Implementation/test head `9d1d64347b0eb305a34daabe733249d4756b2f40` passed exact-head Push [41275439065](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275439065) and PR-context [41275440891](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275440891). All three jobs passed in both runs. Offline suite reported **176 tests, OK**, including the subprocess entrypoint test; acceptance report generation/upload and the fail-closed gate passed.
- Documentation was updated in `docs/HARNESS_RUNNER_V1.md` to explain why the direct invocation is supported. This is a local CLI usability fix; it does not change task allowlists, runner execution semantics, consumer workflow, permissions, or release scope. PR #40 remains Draft/open/unmerged. All consumer and 0.x release gates remain as previously recorded. No merge, tag, release, deployment, consumer repin, billing, permission, visibility, or Actions-policy change occurred.

## 2026-11-01 — Semantic-review evidence-line documentation reconciliation

- Found and corrected a stale statement in `docs/SEMANTIC_REVIEW.md` claiming that the validator does not establish whether finding line numbers match quoted diff evidence. Current `validate_review()` calls `_evidence_line_numbers()` and requires `line_start`/`line_end` to equal the exact mapped source-line range; it rejects ambiguous repeated evidence. Context lines use resulting-file coordinates and deleted-file evidence uses old-file coordinates.
- The revised documentation now states this bounded guarantee while preserving the limitations: evidence/line mapping does not establish reasoning correctness, prove that supplied diffs or instructions are authoritative/complete, or guarantee complete defect detection. `PASS` remains advisory, not total-compliance proof.
- No implementation or test behavior changed in this documentation-only correction. The immediately preceding exact-head `a77150f88d9c6b191064b6c0630e804987e88b8b` passed Push [41275503718](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275503718) and PR-context [41275507009](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275507009), all three jobs successful; offline suite reported 176 tests, OK. The resulting documentation head requires its own exact-head CI verification.
- PR #40 remains Draft/open/unmerged. Consumer acceptance and all previously recorded 0.x release gates remain open. No merge, tag, release, deployment, consumer repin, permission, secret, billing, visibility, or Actions-policy change occurred.

## 2026-11-01 — Full direct CLI execution test and fixture correction

- Strengthened `test_documented_script_entrypoint_supports_direct_execution`: it now launches the actual `scripts/harness_runner.py` process against an isolated temporary Git project, runs the fixed `python-unittest` task, and asserts the generated acceptance report is present and `passed`. This goes beyond the earlier `--help` import/argument-parser smoke check.
- The first full-execution test attempt at `a685a38df3b21f4944a5d48361d79a95166b04ae` failed Push [41275690169](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275690169) and PR-context [41275693339](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275693339): the temporary fixture omitted a `.gitignore` for Python `__pycache__`, so the runner correctly rejected the task-created untracked cache as a dirty worktree. This was a fixture setup defect and demonstrated the intended fail-closed source-integrity check; it was not a runner implementation failure.
- Added `__pycache__/` to the temporary project's `.gitignore`. Corrected exact-head `e09c59362c507e4f01f9b4834e176a1959f9ca62` passed Push [41275736090](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275736090) and PR-context [41275740240](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41275740240), all three jobs successful in both runs. Offline suite reported **176 tests, OK**, including the full subprocess CLI execution test.
- The direct CLI fix remains limited to bootstrapping the repository root for direct-script invocation. The runner still requires a trusted, clean project worktree and a tracked config; normal generated interpreter caches should be ignored by the consuming project's `.gitignore`. No consumer workflow, task allowlist, permission, secret, merge, tag, release, or deployment behavior changed.
