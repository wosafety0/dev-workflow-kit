# Document Precedence and Stale-Content Policy

## Purpose

Keep documentation, implementation, tests, and progress records consistent as the toolkit evolves. When descriptions conflict, use the latest current, verified version as the reference and update obsolete files instead of silently preserving contradictions.

## Precedence rules

1. The user's latest explicit instruction governs the requested task, unless it conflicts with higher-priority safety or access constraints.
2. The latest applicable project-specific rules and accepted decisions govern project behavior. A generic toolkit document must not override a consumer project's instructions, safety controls, tests, or archive requirements.
3. For claims about what is implemented, inspect the current target branch's code and tests. For claims about what has been verified, require actual test or CI evidence tied to the relevant commit.
4. The latest verified project status or decision record supersedes older progress notes. A newer timestamp alone is not proof that a claim is correct.
5. Older documents remain historical only when explicitly identified as historical or branch-specific. Otherwise, conflicting current-facing descriptions must be corrected.

## Required maintenance when a contradiction is found

- Identify the conflicting statements and determine the latest verified state.
- Update every affected current-facing file, including README, roadmap, acceptance contracts, workflow guides, and progress records where applicable.
- Keep status labels precise: implemented, locally tested, CI-verified, pending verification, planned, or historical.
- Do not turn a planned feature into a completed claim without evidence.
- Preserve traceability: record relevant commit SHAs and CI run URLs when available.
- Do not modify a protected/default branch directly when the repository's workflow requires a pull request. Make the correction on an appropriate branch and submit it for review.
- Do not claim local synchronization, CI success, release, or merge unless independently verified.

## Scope boundary

This policy resolves documentation drift; it does not authorize weakening project rules, changing safety boundaries, merging pull requests, triggering CI, or performing project/business actions. Each consumer repository remains responsible for its own instructions, acceptance tests, safety constraints, and archive paths.
