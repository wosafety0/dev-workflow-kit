# Roadmap and Acceptance Gates

## Stage 0 — repository bootstrap

- [x] Create a separate private repository.
- [x] Add a clear non-stable status statement.
- [ ] Run independent CI and review its actual result.

## Stage 1 — reusable semantic-review core

- [x] Port the provider-agnostic semantic-review client.
- [x] Port offline contract tests.
- [x] Document inputs, secrets, status semantics, and limitations.
- [ ] Expand tests for malformed input, missing configuration, provider errors, and malformed provider responses.
- [ ] Confirm CI is green on this repository.

## Stage 2 — project contract and deterministic orchestration

- [ ] Define a versioned project configuration schema.
- [ ] Validate configuration without requiring a model API.
- [ ] Define safe, explicit command allowlists; never execute arbitrary project config commands by default.
- [ ] Emit a redacted, traceable report with commit SHA, rules pin, tool version, and test status.
- [ ] Add failure-injection tests for all fail-closed paths.

## Stage 3 — versioned distribution

- [ ] Add a reusable workflow or package entry point.
- [ ] Document immutable SHA pinning and upgrade procedure.
- [ ] Tag an initial 0.x release only after acceptance criteria pass.

## Stage 4 — consumer integration

- [ ] Integrate KancolleBot through a separate PR pinned to a tested Harness SHA.
- [ ] Preserve project-specific tests, safety constraints, and progress archive paths.
- [ ] Pilot with a second, unrelated repository without copying the core.
- [ ] Publish a reusable-MVP decision based on actual evidence.

## Non-negotiable acceptance rules

- Offline tests do not count as live model validation.
- Missing configuration, network errors, invalid output, or unverifiable evidence must never produce a passing review.
- CI results must link to the actual workflow run.
- No credentials in source, artifacts, or logs.
- No automatic PR merge or project business actions.
- Remote GitHub changes must not be described as synced to a local worktree unless independently verified.
