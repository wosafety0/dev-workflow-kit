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

- Created draft PR #7: https://github.com/wosafety0/dev-workflow-kit/pull/7
- Branch: `test/consumer-pilot-readiness-20261028`; tested head: `bff949fba82e5c514ed9f0f11a32120dae2faabf`.
- Added `docs/CONSUMER_PILOT_CHECKLIST.md` with entry criteria, controlled pilot steps, pass/fail criteria, evidence capture, and stop conditions. The file was read back from GitHub; blob SHA: `afdc2781809e8e1d1e332c739bdbee4d63989a22`.
- The checklist explicitly distinguishes a missing-artifact-input failure from a real GitHub Artifact service outage.
- PR #7 is draft and unmerged. No consumer repository has been integrated; no changes were made to `main`.
- Normal-path CI validation is requested by this PR, but the GitHub connector currently returned no workflow-run records or commit status checks for its head at the time of this log update. Therefore the normal-path result is **pending/unverified**, not a pass.
- Next: verify the normal-path CI result through GitHub's checks/runs, then select a low-risk independent consumer repository for the pilot. Do not wait indefinitely for a hard-to-reproduce service outage.


### Current reusable acceptance gate: isolated failure-closed verification (2026-10-29)

- Added \`tests/test_reusable_acceptance_fail_closed.py\` on isolated branch \`test/reusable-command-fail-closed-65544-20261029\`, based on the exact reusable workflow revision currently pinned by the clamp trial: \`65544e290fd875bb6c4e30f6525b238200037bba\`.
- Tests extract and execute the actual shell blocks from \`.github/workflows/reusable-acceptance.yml\`, including both the consumer-command step and final acceptance gate. Empty and whitespace-only commands return exit code 2 with the explicit \`test-command must not be empty.\` diagnostic; a nonexistent command returns nonzero and exposes the command-not-found error; the final gate then exits 1 and names \`tests\` as the unsuccessful stage. A valid command plus all-success outcomes opens the gate.
- Failure diagnostics are traceable across the job: the named \`Run consumer-owned acceptance command\` step contains the shell error; the redacted report records \`status: failed\`; the final gate names the failed \`tests\` stage. The report intentionally does not copy raw command output.
- Exact-head CI: [run 40801493718](https://github.com/wosafety0/dev-workflow-kit/actions/runs/40801493718), tested commit \`bfdba4d51dba0f776aad8f136c2e394510b6a939\`, conclusion \`success\`. CI logs confirm all 99 offline tests passed; Python compilation, report generation, artifact upload, and the final CI gate succeeded.
- Remote readback confirmed test-file blob \`e18a17432c8d204cad5cac6d8588c859f4c1f711\`.
- Status boundary: verified isolated contract tests only; this does not simulate a complete hosted run with empty/invalid input. The branch is unmerged, \`main\` is unchanged, and no release or consumer pin was changed.
