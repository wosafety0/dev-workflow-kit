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
- [x] Exercise hosted-workflow failure injection, including an actual artifact-upload step failure, and verify the run evidence: [run 40712433963](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40712433963). The test intentionally referenced a missing artifact path; the upload step failed and the final gate failed closed with `ARTIFACT_OUTCOME=failure`. This does **not** simulate a GitHub Artifact service outage; service-level outage behavior remains unverified.

## Stage 3 — versioned distribution

- [x] Add a minimal reusable acceptance workflow with read-only repository permissions and an explicit consumer-owned test command (`.github/workflows/reusable-acceptance.yml`).
- [x] Extend the reusable acceptance workflow with explicit Python/Node.js runtime selection and optional pinned pnpm setup; reject unsupported runtime/package-manager combinations before the consumer command runs.
- [x] Document immutable 40-character SHA pinning, security boundaries, and upgrade/rollback procedure (`docs/REUSABLE_ACCEPTANCE_WORKFLOW.md`).
- [x] Define a document precedence and stale-content maintenance policy (`docs/DOCUMENT_PRECEDENCE.md`).
- [ ] Tag an initial 0.x release only after acceptance criteria pass on the exact release candidate and the release scope is reviewed.

## Stage 4 — consumer integration

- [x] Validate a first consumer pilot through a separate PR pinned to a tested toolkit SHA: [AI-Worker-Proxy PR #2](https://github.com/wosafety0/AI-Worker-Proxy/pull/2), pinned to Harness commit `36533dd7726365fd817f48072e49ea055d339947`; the reusable-workflow run passed on consumer head `643659014370f85b61964bcbb978833ec6f74428`. The PR remains Draft/unmerged.
- [ ] Preserve each consumer's project-specific tests, safety constraints, and archive paths.

### Latest Harness head and archive verification — 2026-10-30

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
