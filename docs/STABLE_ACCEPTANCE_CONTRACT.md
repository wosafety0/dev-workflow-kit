# Stable Acceptance Contract (0.x)

Status: initial contract for the current semantic-review core. This is not a stable API guarantee and does not claim that AI review detects every defect.

## 1. Purpose and scope

This contract defines the minimum acceptance behavior for the provider-agnostic semantic-review module in this repository. It is intended to be reusable by unrelated projects without replacing their project-specific instructions, tests, safety constraints, or archive requirements.

The current contract covers input validation, diff integrity, evidence-grounded review output, fail-closed behavior, and CI evidence. It does not define the future orchestration/configuration schema. JSON parsing for review inputs, provider response envelopes, and model-produced review content must reject duplicate object keys; accepting last-key-wins JSON can make the validated meaning differ from the submitted representation.

## 2. Required inputs

The review input must contain non-empty string fields:

- \`task\`
- \`diff\`
- \`global_rules\`
- \`project_instructions\`

It must also contain \`changed_files\`, a list of non-empty, trimmed path strings. Duplicate paths are rejected. Paths must be repository-relative and must not contain absolute-path prefixes, Windows separators, drive prefixes, empty path segments, \`.\` or \`..\` segments, or control characters. A path longer than 4096 characters is rejected.

## 3. Diff integrity and numeric bounds

The supplied diff must be structurally parseable and consistent with the declared changed-file set. The validator rejects malformed hunk headers and bodies, hunk counts that disagree with the body, unsupported path/header mismatches, duplicate file sections, and evidence that cannot be mapped to the diff.

Hunk numeric fields are bounded before integer conversion. Supported hunk values and computed line ranges must not exceed 2,147,483,647. Over-limit or malformed values must be rejected as a review-validation error; they must not escape as an uncaught conversion exception or be treated as valid evidence.

## 4. Review output contract

The output must be a JSON object with exactly these top-level keys:

- \`status\`: one of \`PASS\`, \`NEEDS_CHANGES\`, \`INCONCLUSIVE\`
- \`summary\`: non-empty string
- \`checked_scope\`: non-empty list of non-empty strings
- \`limitations\`: list of non-empty strings
- \`findings\`: list of findings matching the validator's required schema

Each finding must use a supported severity and identify a changed file, a valid line range, a rule reference and quote, diff evidence, rationale, and recommendation. Findings must be supported by the supplied diff and rules; unverified claims must not be accepted as grounded findings.

## 5. Fail-closed conditions

The following conditions must never yield an accepted passing review:

- Missing or malformed required input.
- Unsafe or inconsistent changed-file paths.
- Malformed or internally inconsistent diff structure.
- Hunk numbers outside supported bounds.
- Invalid output schema or unsupported status/severity.
- Findings whose file, line range, rule quote, or evidence cannot be verified.
- Missing required provider configuration, network/provider errors, or malformed provider responses.
- Model-provider response bodies larger than 1 MiB; the client reads at most 1 MiB plus one sentinel byte before failing closed.

The caller must treat validation/provider failures as failure or inconclusive outcomes, not as approval to merge or perform project actions.

## 6. Credentials, side effects, and reporting

- Credentials must be supplied through environment/configuration mechanisms and must not be committed or printed.
- Remote model-provider endpoints must use HTTPS. Cleartext HTTP is allowed only for a literal loopback IP address (for example, `127.0.0.1` or `[::1]`) to support local inference servers; `localhost` hostnames and non-loopback HTTP endpoints are rejected. Requests to these literal loopback HTTP endpoints bypass configured proxies for that request only; no global proxy setting is changed. Credentials embedded in URLs, query strings, and fragments are rejected. Redirect responses must fail closed; clients must not automatically follow redirects, because redirects can disclose authorization headers to a different endpoint.
- Authorization headers, API keys, and other secrets must not appear in logs or reports.
- The review module is advisory validation; it does not merge pull requests or execute project/business actions.
- A green offline test suite establishes only that the tested offline contract cases pass. It does not establish live provider behavior, completeness of defect detection, or production readiness.

## 7. CI evidence and acceptance procedure

A change to this contract or its implementation is accepted only when:

1. Tests are added or updated for the changed behavior.
2. The relevant GitHub Actions run completes with conclusion \`success\`.
3. The run's tested commit SHA matches the intended commit.
4. The test summary and job result are inspected, not inferred from a commit alone.
5. Any PR remains unmerged unless merge is separately authorized.

Remote GitHub changes are not considered synchronized to a local worktree without independent verification.

## 8. Reuse and versioning

Consumers should pin the toolkit to a reviewed immutable commit SHA until a versioned distribution mechanism exists. Each consumer must retain its own project instructions, allowlists, safety checks, acceptance tests, and required progress/archive paths. Do not copy this contract as a substitute for project-specific rules.

This document is a living 0.x contract. A change that weakens a fail-closed rule requires explicit rationale, corresponding tests, and review of the resulting risk; it must not happen implicitly as a side effect of refactoring.


## Runner configuration integrity

- Harness configuration must reject duplicate JSON object keys at every nesting level.
- The config must be tracked by the current Git HEAD and must not resolve under generated `artifacts/`; a blocked run must invalidate stale passing report/review artifacts before configuration validation.
- Config, report, review-input, and review-output paths reject symlink components. Trusted test, semantic-review, and contract sources must resolve inside the project root, outside `artifacts/`, and contain no symlinked source paths.
- The runner must preserve fail-fast task ordering and revalidate the Git worktree and generated output paths before writing the final acceptance report.
