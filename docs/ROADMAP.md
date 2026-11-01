## 2026-11-01 — Reusable entrypoint trigger regression guard

- Added `test_reusable_workflow_is_not_directly_triggered` to the reusable workflow contract suite. It asserts the called workflow exposes `workflow_call` and does not acquire direct `push`, `pull_request`, `pull_request_target`, or `workflow_dispatch` triggers. This keeps the acceptance entry point reusable-only; consumer-specific PR trust policy remains the caller's responsibility.
- The exact test head `0f964dc07cee3dc8d952cf9bdb8788646ddfb52e` passed PR-context CI [41274381898](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274381898): offline contract suite, Python reusable selftest, Node/pnpm reusable selftest, report upload, and fail-closed gate all succeeded. Temporary artifact [13070786417](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41274381898) expires 2026-11-15. Push-triggered CI for this exact SHA was not independently retrieved.
- PR #40 remains Draft/open/unmerged. No consumer was rerun or repinned; private consumer execution and browser E2E remain pending. No merge, tag, release, deployment, or account/policy change occurred.

## 2026-11-01 — Consumer execution trust boundary and contract regression

- Completed a source-level review of both current consumer PR heads and clarified in the reusable-workflow guide that `test-command` is executable consumer-controlled shell, not a sandbox. A `pull_request` caller can run PR-controlled workflow/test code; read-only permissions and absence of explicitly passed secrets reduce risk but do not isolate execution or restrict network egress.
- Added a reusable-workflow contract regression test forbidding secrets declarations, direct secrets-context references, and `secrets: inherit` in the reusable workflow. The test is intentionally scoped to the called workflow; it cannot enforce caller-side policy or prevent a consumer from creating a separate privileged workflow.
- Exact test-contract head `b7bdf5deba5b3b919af3760408893829e5a01f80` passed PR-context CI [41271489648](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41271489648): offline tests, Python selftest, Node/pnpm selftest, report upload, and final gate all succeeded. The preceding documentation head `2415539ccd09abb5e2b6f9efb413909948ff9c89` passed PR-context CI [41271405922](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41271405922). Push-triggered CI for these exact SHAs was not independently retrieved.
- Public consumer remains accepted only for its recorded exact head and immutable Harness pin. Private consumer remains unaccepted: no runner was allocated due to the recorded account payment/spending eligibility gate; static validation does not substitute for browser E2E.
- Stage 4 consumer safeguards and private runtime acceptance remain incomplete. Initial 0.x scope approval, exact release candidate, and tag/release preflight remain open. No consumer changes, merge, tag, release, deployment, billing, permission, visibility, or Actions-policy change occurred.

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

## Pre-archive head CI and archive verification — 2026-11-01

- Verified pre-archive head: `f62dc4ae4ff578a921a8850b678790b0b162e080`. Exact-head Push CI [41256664945](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256664945) and PR-context CI [41256669345](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256669345) both completed successfully for this same SHA.
- Job-level inspection confirms all three jobs passed in both runs: `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`. Offline compilation, contract tests, redacted report generation/upload, and the fail-closed gate all succeeded; both reusable runtime selftests executed their consumer-owned acceptance commands.
- This entry labels `f62dc4ae...` as the verified pre-archive head and supersedes the preceding stale current-head labels. The archive commit created after that verified head is documentation-only; its own CI is verified separately and does not recursively update this snapshot.
- PR #40 remains Open/Draft/unmerged. The passing public consumer remains one independent pilot, not proof of universal compatibility. The private consumer remains blocked before runner allocation by the recorded account billing/spending eligibility gate. Stage 4 consumer-specific safeguards/archive-path acceptance remains unchecked.
- The proposed initial 0.x scope still requires repository-owner approval. No exact release-candidate SHA has been selected and no tag/release preflight is certified. No merge, tag, release, deployment, billing, or Actions-policy change occurred.

## Latest exact-head verification — 2026-11-01

- Current Node-consumer branch head before this documentation archive: `a9b6f17099afa07f9cbb2f8a0410560f9c1ed38b`. Exact-head Push CI [41228919858](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41228919858) and PR-context CI [41228924340](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41228924340) both succeeded; all three jobs were green and the offline suite reported **169 tests, OK**.
- Replaced the Node.js 20 `actions/upload-artifact` v4 pin with verified Node 24-compatible v7.0.2 commit `cf430e030ddbb5b0abf93d22962f4752f3646cd9`, and added a CI workflow pin-contract regression test. The final exact-head offline log contained no Node.js 20 deprecation warning.
- PR #40 remains Draft/open/unmerged. The private consumer acceptance gate remains blocked before runner allocation by its recorded account billing/spending eligibility condition. The 0.x scope proposal still requires owner approval; green CI is not release authorization.
- The following 2026-10-31 entries are historical snapshots and are superseded where they identify an older branch head as current. No merge, tag, release, billing/policy change, or deployment occurred.

## Historical archive verification — 2026-10-31 (superseded by 2026-11-01)

- Current branch head reviewed: `2d6399c09f6d979fdd839356238f15bfe1bdc13a` (documentation-only archive update).
- Exact-head Push CI [41181289361](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41181289361) and PR-context CI [41181291525](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41181291525) both completed successfully on this SHA. All three jobs succeeded in each run.
- Both runs passed `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`. The reusable workflow jobs executed their consumer-owned acceptance commands successfully; offline tests compiled Python, ran the contract suite, built/uploaded the redacted report, and passed the fail-closed gate.
- Harness PR #40 remains Draft/open/unmerged. Private-consumer acceptance remains blocked before runner allocation by the recorded account billing/spending eligibility annotation; the consumer-specific safeguards/archive-path gate remains unchecked.
- The initial 0.x scope remains a recommendation awaiting repository-owner approval. No tag, release, merge, billing/policy change, or deployment is authorized or performed by this archive.

## Current verification and release-candidate review — 2026-10-31

- **Latest verified implementation baseline before the documentation-only review archive:** `04a6ae3bb64db7fd348bfc2136dbc9430dc4d9ca`. Exact-head Push CI [41176249364](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41176249364) and PR-context CI [41176252292](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41176252292) both completed with conclusion `success`. Each run passed `offline-tests`, `reusable-python-selftest / acceptance`, and `reusable-node-pnpm-selftest / acceptance`.
- The current public independent consumer [AI-Worker-Proxy Draft PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2) pins Harness commit `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5` at consumer head `87c3633621e455f9ba75ec2caf3ae6ba206e60a8`. Exact-head reusable acceptance [41175900745](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900745), PR lint/type-check [41175900178](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900178), and Push lint/type-check [41175897003](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175897003) all passed. This is evidence for one independent Node.js 26/pnpm 11.4.0 consumer only. The PR remains Draft/unmerged.
- The private consumer [chatgpt-auto-send-assistant Draft PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1) remains **not accepted**. Consumer head `0d64bf825cc5a76f3d8603f2e0fb431613715b56` pins Harness SHA `37dc07c7d7055a740c754ab543eeecc9e01d9db0`. Run [41099042827](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) did not allocate a runner; check-run annotation `124212281392` identifies an account billing/spending eligibility gate. The message does not distinguish failed payment from spending-limit exhaustion. Do not count this as a test failure or a pass.
- **Release decision: not ready to tag yet.** The consumer-preservation criterion remains unchecked, the private consumer has no successful exact-head run, and no exact release-candidate SHA has been selected. A bounded initial 0.x scope recommendation is recorded in [RELEASE_CANDIDATE_REVIEW.md](RELEASE_CANDIDATE_REVIEW.md), but it has not been approved by the repository owner. Do not infer release authorization from green CI.
- Historical entries below that refer to older commits as current, or describe the private-consumer blocker as unknown, are snapshots of earlier evidence and are superseded by this section. No billing, Actions policy, secrets, merge, release, or deployment was changed.
- The documentation-only review archive at commit `3f6d912ea8e9479dc7108079739a4926dc9552c6` passed exact-head Push CI [41176608897](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41176608897) and PR-context CI [41176612118](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41176612118). All three jobs succeeded in both runs. This verifies the review/archive tree; it does not change the release decision.

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
- [x] Exercise hosted-workflow failure injection, including an actual artifact-upload step failure, and verify the run evidence: [run 40712433963](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40712433963). The test intentionally referenced a missing artifact path; the upload step failed and the final gate failed closed with `ARTIFACT_OUTCOME=failure`. This does **not** simulate a GitHub Artifact service outage; service-level outage behavior remains unverified.

## Stage 3 — versioned distribution

- [x] Add a minimal reusable acceptance workflow with read-only repository permissions and an explicit consumer-owned test command (`.github/workflows/reusable-acceptance.yml`).
- [x] Extend the reusable acceptance workflow with explicit Python/Node.js runtime selection and optional pinned pnpm setup; reject unsupported runtime/package-manager combinations before the consumer command runs.
- [x] Document immutable 40-character SHA pinning, security boundaries, and upgrade/rollback procedure (`docs/REUSABLE_ACCEPTANCE_WORKFLOW.md`).
- [x] Define a document precedence and stale-content maintenance policy (`docs/DOCUMENT_PRECEDENCE.md`).
- [ ] Tag an initial 0.x release only after acceptance criteria pass on the exact release candidate and the release scope is reviewed.

### Historical consumer pin verification snapshot — 2026-10-31 (superseded by current verification above)

- The first consumer now tests the latest reviewed Harness workflow SHA `37dc07c7d7055a740c754ab543eeecc9e01d9db0`, whose reusable workflow file blob is `a5fccae44358222a0d453c33afbe90f95d29f191`.
- Consumer branch head `4fc0c7f52070acef35afb5184bf82e3910577ccb` passed the reusable Node.js 26 + pnpm 11.4.0 acceptance workflow [41098792395](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41098792395) and both native lint/type-check runs [41098791776](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41098791776) and [41098781379](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41098781379).
- Only the consumer workflow's immutable Harness pin changed; no application behavior, secrets, settings, deployment, or provider API was touched. The separate private consumer's pre-step failure remains unresolved.

## Consumer preservation source cross-check — 2026-10-31

- Public consumer `AI-Worker-Proxy` keeps its existing native lint workflow alongside the separate Harness pilot; the pilot runs frozen-lockfile install, lint, type-check, and Prettier check on head `87c3633621e455f9ba75ec2caf3ae6ba206e60a8`. Exact-head Harness and native checks passed.
- Private consumer `chatgpt-auto-send-assistant` keeps its `npm test` command (`node scripts/validate.mjs`); `TESTING.md` continues to mark actual Tampermonkey/ChatGPT browser E2E as pending. Its current Harness run is blocked before runner allocation by the recorded account billing/spending eligibility gate, so no runtime result is available.
- This source-level cross-check found no visible replacement of consumer tests or removal of the documented browser-test limitation. It does **not** close Stage 4: the private consumer still lacks successful exact-head execution, and consumer-specific archive-path expectations have not been fully confirmed. See [release-candidate review](RELEASE_CANDIDATE_REVIEW.md).

## Stage 4 — consumer integration

- [x] Validate the first consumer pilot through a separate Draft PR at the latest reviewed reusable-workflow pin: [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), Harness commit `37dc07c7d7055a740c754ab543eeecc9e01d9db0`, consumer head `4fc0c7f52070acef35afb5184bf82e3910577ccb`; exact-head reusable acceptance [41098792395](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41098792395), native lint/type-check [41098791776](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41098791776) and [41098781379](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41098781379) all passed. The PR remains Draft/unmerged.
- [ ] Preserve each consumer's project-specific tests, safety constraints, and archive paths.

### Historical Harness head and archive verification snapshot — 2026-10-30

- Latest verified branch tree before this documentation refresh: `2658d5b042c85d287c5aa7ae3d1ecb96c4ee8443`. Exact-head Push CI [41055557393](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41055557393) and PR-context CI [41055567927](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41055567927) both succeeded on that SHA. This record is a snapshot before the current documentation-only refresh, not a claim that this refresh commit has already passed CI.
- Both exact-SHA `offline-tests` jobs passed Python compilation, all offline contract tests, redacted acceptance report generation/upload, and the final required-stage gate. Push artifact ID `12975854414`, digest `sha256:f9cef2edecfa3c033e3c3d5ae86ae657e218c5acf8c4f750d792d0ad2714a835`, expires `2026-11-13T12:28:16Z`.
- The reusable acceptance workflow supports Python and Node.js with optional pnpm, validates runtime/package-manager inputs before the consumer command, rejects blank commands, runs the consumer-owned command under Bash strict mode, pins actions to full commit SHAs, and disables checkout credential persistence.
- First consumer pilot: [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), pinned to Harness SHA `36533dd7726365fd817f48072e49ea055d339947`; its reusable acceptance run and native lint/type-check runs passed on consumer head `643659014370f85b61964bcbb978833ec6f74428`. The PR remains Draft/unmerged.
- Second consumer pilot: [chatgpt-auto-send-assistant PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1) remains blocked before job steps. Both attempts lack usable runner logs; the effective caller Actions policy and root cause remain unverified. Do not count this as a pass. No settings or visibility were changed.
- PR #40 remains Draft/open/unmerged. The second-consumer acceptance criterion and initial 0.x release decision remain pending. No merge, release, deployment, or repository access-policy change occurred.

## Non-negotiable acceptance rules

- Offline tests do not count as live model validation.
- Missing configuration, network errors, invalid output, or unverifiable evidence must never produce a passing review.
- CI results must link to the actual workflow run and identify the exact tested commit.
- No credentials in source, artifacts, or logs.
- No automatic PR merge or project business actions.
- Remote GitHub changes must not be described as synced to a local worktree unless independently verified.
- Documentation conflicts must be resolved under `docs/DOCUMENT_PRECEDENCE.md`; obsolete current-facing descriptions must be updated.


### Second-consumer source cross-check — 2026-10-30
- Revalidated the caller workflow and reusable workflow at the exact pinned Harness SHA. The reusable file exists, declares `workflow_call`, and exposes the input names/types used by the consumer; no obvious workflow path, immutable pin, or input mismatch was found.
- The second-consumer run still fails before steps with an empty step list and unavailable logs. Effective Actions policy settings could not be read through the available connector, so the cause remains unknown. Do not mark the second-consumer criterion complete or change visibility/settings without an evidence-based, authorized decision.
- PR #1 remains Draft/unmerged; no consumer implementation, settings, visibility, permissions, release, or deployment changes were made. Historical note: archive CI was pending at the time this entry was written; later exact-head verification is recorded below and supersedes that pending status.


### Superseding exact-head verification update — 2026-10-30

- The earlier note above that the archive head's exact-head CI was pending is historical and is superseded by verification of current PR #40 branch head `010bdc400597ca7840bdf4928cd9cdeaae7dbd3b`.
- Push CI [41032611297](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41032611297) and PR-context CI [41032618160](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41032618160) both succeeded for that exact head. Both completed `offline-tests`, including Python compilation, offline contract tests, redacted acceptance report generation/upload, and the final required-stage gate.
- This resolves the archive-verification wording only. The second consumer remains blocked before job steps with root cause unknown; its acceptance checkbox remains unchecked. PR #40 remains Draft/open/unmerged, and no settings, permissions, visibility, release, or deployment changed.

### Latest roadmap consistency and checkout credential isolation — 2026-10-30

- Current PR #40 head at the time of this archive: `05cc91a6c272ff54ea5116aacc23b8fc6882ffdb`. This entry supersedes the earlier current-head references above; those remain historical evidence for their respective commits.
- Push CI [41034922115](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41034922115) and PR-context CI [41034929136](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41034929136) both succeeded for this exact head. Both completed Python compilation, offline contract tests, redacted acceptance report generation/upload, and the final gate.
- Hardened `.github/workflows/reusable-acceptance.yml` with `persist-credentials: false` on the SHA-pinned checkout step, and added a contract test to prevent accidental removal. This reduces unnecessary credential persistence; it is not evidence that a credential leak occurred.
- The second consumer still fails before steps with no assigned runner and unavailable logs. Root cause and effective caller Actions policy remain unknown; its acceptance checkbox remains unchecked. No settings, permissions, repository visibility, merge, release, or deployment changed. PR #40 remains Draft/open/unmerged.


### Exact-head CI confirmation — 2026-10-30

- Current PR #40 head `d081fcf74863fbcccbea027a8e1f1b2137197cdf` passed Push CI [41035581115](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41035581115) and PR-context CI [41035591455](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41035591455).
- Both runs completed successfully for this exact SHA. The current head is therefore verified; earlier wording that this commit's CI had not appeared is historical and superseded.
- The second consumer remains blocked before runner steps with root cause unknown. Its acceptance criterion remains unchecked. PR #40 and consumer PRs remain Draft/unmerged; no settings, permissions, visibility, release, merge, or deployment changed.


### Exact-head CI verification — 2026-10-30

- Archive commit `5da6a9d2ad3c1787d3148fdce877a71740ac2fea` passed Push CI [41036222709](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41036222709) and PR-context CI [41036230850](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41036230850), both for the exact same SHA.
- Both runs completed `offline-tests` successfully: Python compilation, all offline contract tests, redacted acceptance report generation/upload, and the final required-stage gate.
- The roadmap and progress archive now record this verified state. The next resulting documentation commit requires its own exact-head CI check; second-consumer acceptance remains incomplete and the cause of its pre-step failure remains unknown.
- PR #40 remains Draft/open/unmerged. No Actions settings, permissions, visibility, merge, release, or deployment changed.


### Permission-contract hardening and second-consumer diagnostic update — 2026-10-30

- Current Harness PR #40 head before this archive: `1cd44edbc71dfaff4eb4d03b67d9d7d7eec87244`. The permission contract test now rejects any permission key set to `write`, not only a short allowlist. Exact-head Push CI [41041286644](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41041286644) and PR-context CI [41041302017](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41041302017) both succeeded.
- New read-only inspection of consumer run [41021315209](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41021315209) confirms GitHub recorded the reusable-workflow reference at the intended immutable SHA `36533dd7726365fd817f48072e49ea055d339947`. This reduces the likelihood of a missing path/ref as the explanation, but does not prove the caller's effective Actions policy is permissive.
- Attempt 2 job [123960822318](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41021315209/job/123960822318) still has `runner_id: 0`, no runner name, and an empty step list. The log endpoint returns `BlobNotFound`; the annotations endpoint is not accessible through the current GitHub connector. Effective caller/org policy and the failure annotation text remain unverified. Root cause is still unknown; no settings, permissions, or visibility were changed.
- This update is an evidence clarification, not a second-consumer pass. Its acceptance checkbox remains unchecked. All PRs remain Draft/unmerged; no release or deployment occurred.


### Current verified status — 2026-10-30

- Current PR #40 head: `4a2aa5cedb67b1d59c011544eaa50a4b8bca11ee`.
- Exact-head Push CI [41055907724](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41055907724) and PR-context CI [41055920956](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41055920956) both completed successfully. Each `offline-tests` job passed compilation, all offline contract tests, redacted acceptance report generation/upload, and the final required-stage gate.
- Push acceptance-report artifact [12976945877](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41055907724) was present and not expired when checked; digest `sha256:fe0bd9167a6a537ae844e175f4f129ba77ddb87daee52f1f6514fea9d07b51d8`, expiry `2026-11-13T12:31:02Z`. It is temporary, not a permanent archive.
- The second consumer `chatgpt-auto-send-assistant` remains blocked before job steps: run [41021315209](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41021315209) has a failed job and no step details. The root cause and effective caller Actions policy remain unconfirmed; do not count this pilot as passing.
- This current status supersedes earlier historical entries that describe older branch heads as current or say later CI was still pending. PR #40 and both consumer PRs remain Draft/open/unmerged. No settings, permissions, visibility, merge, release, or deployment changed.



### Current status superseding older head references — 2026-10-31

- Latest verified implementation head before this documentation-only status refresh: `bd2f2083332b8050c6dd6b5753575bfe0783bc24`. Exact-head Push CI [41056295005](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41056295005) and PR-context CI [41056302765](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41056302765) both succeeded, including compilation, all offline contract tests, redacted acceptance-report generation/upload, and the final required-stage gate.
- Push acceptance-report artifact [12976294611](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41056295005) had digest `sha256:3561ba3e4a5e30e2d4a6a00a8c0d6b20977a91fa7b3eb05292e58b2efca047c5` and expiry `2026-11-13T12:34:06Z`; it is temporary evidence, not a permanent archive.
- The reusable workflow currently supports Python and Node.js with optional pnpm, read-only repository permissions, full-SHA action pins, checkout credential persistence disabled, and fail-closed contract tests.
- First consumer pilot [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2) passed its reusable acceptance run and native lint/type-check on consumer head `643659014370f85b61964bcbb978833ec6f74428`; it remains Draft/unmerged.
- Second consumer pilot [chatgpt-auto-send-assistant PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1) remains blocked before job steps. Run [41021315209](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41021315209) has no assigned runner/steps and unavailable logs; root cause and effective Actions policy remain unverified. This is not a pass.
- This entry supersedes older entries above that label older SHAs as the current head or describe the newer CI as pending. PR #40 and both consumer PRs remain Draft/open/unmerged; no settings, permissions, visibility, merge, release, or deployment changed.


### Workflow-contract regression coverage and latest CI state — 2026-10-31

- Contract tests now explicitly guard the reusable `workflow_call` entry point and the default inputs (Python `3.12`, Node.js `24`, package manager `none`, pnpm `11.4.0`). Regex escaping was corrected in commit [78005435b11150f141da4739b30d2158c40e1377](https://github.com/wosafety0/dev-workflow-kit/commit/78005435b11150f141da4739b30d2158c40e1377).
- Exact-head Push CI [41103982861](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41103982861) and PR-context CI [41103993312](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41103993312) are both reported successful for that SHA. The connector exposed job-level conclusions but no step details; record only the run-level success.
- Remaining acceptance risk: [chatgpt-auto-send-assistant PR #1](https://github.com/wosafety0/chatgpt-auto-send-assistant/pull/1) still fails before any job steps in [run 41099042827](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827). Root cause/effective Actions policy are unknown; do not treat this consumer as passed or change settings to work around it without evidence.
- Next: verify Push and PR-context CI against the resulting documentation-archive head, then continue diagnosing the second consumer from read-only evidence. PR #40 remains Draft/open/unmerged; no release or deployment occurred.

## Latest branch and release-gate recheck — 2026-11-01

- Pre-archive head `e2f7560235c20292539adec1dd2f53cacc9ad1be` passed exact-head Push [41256913332](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256913332) and PR-context [41256916534](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41256916534); all three jobs passed in each run.
- PR #40 remains Open/Draft/unmerged. Public consumer pin comparison shows 42 commits ahead/zero behind; private consumer comparison shows 63 ahead/zero behind. Neither comparison includes a change to `.github/workflows/reusable-acceptance.yml`; neither consumer was repinned.
- Private consumer run [41099042827](https://github.com/wosafety0/chatgpt-auto-send-assistant/actions/runs/41099042827) remains blocked before runner allocation (`runner_id: 0`, no steps) by the recorded account payment/spending eligibility annotation. It is not accepted.
- GitHub Releases inventory is empty; tag enumeration was unavailable through the connector, so tag availability is not certified. The initial 0.x scope still requires explicit owner approval; consumer-specific safeguards, private exact-head execution, candidate selection, and release preflight remain open.
- This is a pre-archive status record. The archive commit's CI is tracked separately; no merge, tag, release, deployment, billing, permission, visibility, or Actions-policy change occurred.

## Tag namespace and archive-head CI — 2026-11-01

- GitHub matching tag refs query returned an empty array: the repository currently has zero tag refs. This supersedes the earlier note that the tags-list endpoint was unavailable. The empty namespace is current-state evidence only, not a completed future tag-name preflight.
- Archive head `0342ef1beab6a0048e566c865191c0f78e146910` passed Push [41257280862](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41257280862) and PR-context [41257284495](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41257284495); all three jobs succeeded in both runs.
- PR #40 remains Open/Draft/unmerged. Private consumer exact-head acceptance remains blocked before runner allocation by the recorded account payment/spending eligibility gate; do not count it as passing.
- Owner approval of the bounded initial 0.x scope, consumer-specific safeguards acceptance, private exact-head execution, exact candidate selection, and final tag/release preflight remain unchecked. No tag/release/merge/deployment or account/policy change occurred.

## 2026-11-01 — Current head and consumer pin reconciliation

- Harness PR #40 current head: `e02393a028dcef947bade0a0c5ee3f22a9dd6142`, Open/Draft/unmerged. PR-context CI [41270587376](https://github.com/wosafety0/dev-workflow-kit/actions/runs/41270587376) passed all three jobs. A Push-triggered run for this exact SHA was not independently retrieved in this check.
- Main CI checkout now explicitly uses `persist-credentials: false`; a contract test protects this requirement. The reusable workflow interface/definition did not change in the 10-commit range since `0342ef1...`.
- Correct current public consumer state: [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), head `87c3633621e455f9ba75ec2caf3ae6ba206e60a8`, pins `c4cf3e1c11deec098c6a7a6e3837bbe983dcece5`. Commit [87c3633](https://github.com/wosafety0/AI-Worker-Proxy/commit/87c3633621e455f9ba75ec2caf3ae6ba206e60a8) deliberately changed the preceding `37dc07c...` pin back to `c4cf3e1...` to verify the previously green revision. Exact-head Harness run [41175900745](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900745) and native PR lint/type-check [41175900178](https://github.com/wosafety0/AI-Worker-Proxy/actions/runs/41175900178) passed.
- The reusable workflow file at public pin `c4cf3e1...`, private pin `37dc07c...`, and current Harness head `e02393a...` has identical blob SHA `a5fccae44358222a0d453c33afbe90f95d29f191`. Public/private source comparisons are 53/74 commits ahead respectively, zero behind; no reusable workflow definition change appears in either range. This is compatibility evidence only.
- Private consumer remains blocked before runner allocation by the account payment/spending eligibility gate and is not accepted. Do not rerun or change billing/policy as part of this work.
- Release gates remain open: owner approval of bounded 0.x scope, complete consumer-specific safeguards/archive-path acceptance, private exact-head runtime acceptance, exact release-candidate selection, and tag/release preflight. No consumer repin, merge, tag, release, deployment, or account/policy change occurred.

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
