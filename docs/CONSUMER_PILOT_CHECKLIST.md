# Consumer Pilot Readiness Checklist

## Purpose

Use this checklist to decide whether a low-risk consumer repository can adopt the reusable acceptance workflow. This is a readiness checklist, not evidence that a pilot has already passed.

## Entry criteria

- [ ] The consumer repository is independent of production game automation and other safety-critical side effects.
- [ ] The target branch and rollback path are identified.
- [ ] The consumer's existing test command is known and can run without secrets or live external services.
- [ ] The reusable workflow reference is pinned to a reviewed full commit SHA.
- [ ] The caller grants only the permissions required by its own workflow; the reusable workflow currently requests `contents: read`.
- [ ] The consumer can inspect the uploaded redacted acceptance report without exposing credentials or private payloads.

## Pilot procedure

1. Create an isolated feature branch in the consumer repository.
2. Add a minimal caller workflow using `.github/workflows/reusable-acceptance.yml`.
3. Pass the consumer's explicit Python version and test command.
4. Open a draft pull request; do not merge it during the pilot.
5. Verify the normal path: checkout, Python setup, tests, report generation, artifact upload, and final gate all succeed.
6. Verify a controlled required-stage failure closes the gate. Prefer a deterministic test-command failure over external-service disruption.
7. Inspect the `consumer-acceptance-report` artifact and workflow logs for accidental secret or payload disclosure.
8. Record setup effort, required consumer-specific changes, observed failures, and cleanup/rollback results.

## Pass criteria

- The consumer can call the reusable workflow without copying its implementation.
- The normal path succeeds on the exact tested commit.
- A deterministic required-stage failure produces a failed final gate.
- The report contains only the allowlisted status metadata, is useful and redacted, and no credentials or sensitive test payloads appear in logs or artifacts.
- The workflow permissions and immutable action/workflow references are reviewed.
- The pilot remains isolated: no automatic merge, release, deployment, or production/game action.

## Stop / fail criteria

Stop the pilot and do not merge if the workflow skips required stages, reports success after a required-stage failure, leaks sensitive data, requires unexpectedly broad permissions, or causes unrelated consumer changes.

## Evidence record

For the pilot, record:

- Consumer repository and branch:
- Reusable workflow commit SHA:
- Consumer test command and Python version:
- Successful run URL and tested commit SHA:
- Required-stage failure run URL and tested commit SHA:
- Artifact/report review:
- Setup time and consumer-specific changes:
- Known untested boundaries:
- Decision: pass / revise / stop

A missing-artifact-input test demonstrates fail-closed behavior when artifact upload fails; it does not establish behavior during a GitHub Artifact service outage. Do not claim service-outage coverage unless it has been independently demonstrated.
