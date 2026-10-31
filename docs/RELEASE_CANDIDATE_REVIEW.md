# 0.x Release Candidate Review

Review date: 2026-10-31  
Repository: `wosafety0/dev-workflow-kit`  
Review branch: `feat/reusable-node-runtime-20261030`  
Reviewed branch head: `04a6ae3bb64db7fd348bfc2136dbc9430dc4d9ca`  
Decision: **Not ready to tag or release**

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

### Remaining release gaps

1. **Consumer-specific safeguards:** Roadmap Stage 4 still requires preserving each consumer's own tests, safety constraints, and archive paths. The successful public pilot proves one integration configuration; the private consumer remains blocked before execution. Keep this criterion unchecked until evidence supports the criterion or the roadmap's acceptance scope is explicitly reviewed and changed.
2. **Private consumer evidence:** The account billing/spending eligibility gate needs to be resolved by the account owner. Do not repeatedly rerun, change Actions policy, or count the current run as acceptance.
3. **Exact release candidate:** Before tagging, choose and record the exact candidate SHA; inspect its diff and run Push and PR-context CI on that same SHA; ensure all required jobs succeed; and re-check the consumer pin/evidence against the candidate being released.
4. **Release scope:** Review which surfaces are in the initial 0.x release (semantic-review core versus reusable workflow and orchestration features), state known limitations, and verify the README and versioning/upgrade/rollback instructions match that scope.
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
