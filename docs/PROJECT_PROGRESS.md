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
- PR #5 was merged into the integration branch after CI and diff verification. See the verified merge record below.

### Gate and test coverage

The final gate requires the test, report-build, and artifact-upload stages to report exact `success`. The existing offline CI run verifies the normal artifact-upload path, not a real GitHub artifact-service outage.

## Limits of current evidence

- PR #5 CI passed on the exact PR head before merge; both push and pull-request runs succeeded.
- No real hosted orchestration failure injection has been performed.
- No real model validation or cross-project consumer integration pilot has been completed.
- The local working tree/synchronization state has not been verified.
- No changes were made to `main`.

## Next steps

1. Design a controlled test for a real hosted artifact-service outage; the current test covers missing artifact input, not service outage.
2. Run a consumer-project integration pilot after defining minimal acceptance criteria; do not couple the Harness to KancolleBot by default.
3. Define objective 0.x release criteria after hardening and pilot evidence are available.
4. Conduct controlled real-model validation after offline and hosted reliability boundaries are documented.

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
- PR #7 remains draft and unmerged. No consumer repository has been integrated; no changes were made to `main`.

### Reusable acceptance workflow report and fail-closed gate

- Draft PR #8: https://github.com/wosafety0/dev-workflow-kit/pull/8
- Branch: `feat/reusable-acceptance-report-gate-20261028`; tested PR head: `58dc2c5a84099e588797beccc1ad3b9802614108`.
- Added a redacted consumer acceptance report containing only schema version, consumer commit SHA, caller workflow reference/SHA, test status, and overall status. The workflow attempts report generation and upload after test failure, then opens the gate only if test, report, and artifact stages all have exact `success`.
- Added `tests/test_reusable_workflow_contract.py` to check read-only permissions, immutable action pins, report allowlist, failure continuation, and final-gate rules.
- Updated reusable-workflow documentation, pilot checklist, and roadmap to reflect the implementation and its limits.
- Hosted CI run [40714595099](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40714595099), run number 108, completed successfully for PR #8's exact tested head `58dc2c5a84099e588797beccc1ad3b9802614108`. The run log confirms 93 offline tests passed, report generation passed, artifact ID `12827468404` was uploaded, and the final gate passed.
- This verifies the Harness repository's CI and static workflow contract tests. It does not yet verify invocation through a real `workflow_call` from a consumer workflow.
- PR #8 is draft and unmerged. No changes were made to `main`.

### Reusable workflow consumer smoke test

- Draft PR #9: https://github.com/wosafety0/dev-workflow-kit/pull/9
- Branch: `test/reusable-workflow-smoke-20261028`; head: `71ec801a1c84c2a52920386466d3c9b63075f0fa`.
- Added `.github/workflows/reusable-acceptance-smoke.yml`, which invokes the reusable workflow at immutable SHA `58dc2c5a84099e588797beccc1ad3b9802614108` and runs the offline unittest command.
- At the time of this log update, the connector had not yet returned a workflow run or status for PR #9. The real `workflow_call` smoke result remains pending/unverified.
- This is a same-repository smoke test only, not a completed second independent consumer pilot. PR #9 is draft and unmerged; no consumer production repository or `main` was modified.
