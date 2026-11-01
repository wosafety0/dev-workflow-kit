# Safe Harness Task Runner (v1)

Status: early implementation; reviewed task allowlist only. This is not an autonomous coding agent and does not edit source files, create commits, push branches, or merge pull requests.

## Example

From the project root, start with the checked-in example `examples/harness-config.json` or a reviewed project-specific config:

```json
{
  "schema_version": 1,
  "project": "example-project",
  "commands": ["python-unittest"]
}
```

Run:

```bash
python -I -S scripts/harness_runner.py --config examples/harness-config.json
```

The direct script entry point bootstraps the repository root on Python's module search path before importing local Harness modules. Launch it with \`-I -S\` as shown so the Harness process itself also ignores \`PYTHONPATH\` and disables site startup hooks; its Python task subprocesses use the same isolation flags.

The runner writes `artifacts/acceptance-report.json`. It requires the project root to be the Git repository root with a valid HEAD and a clean worktree outside generated `artifacts/`. The `--config` file must be tracked by the current HEAD and must not resolve under `artifacts/`; prior passing artifacts are invalidated before config validation. Duplicate JSON object keys at every nesting level are rejected. For an opt-in live model test, see [SEMANTIC_REVIEW_SMOKE_TEST.md](SEMANTIC_REVIEW_SMOKE_TEST.md) and the semantic-review example config/input.

## Task mapping

Configuration supplies only task IDs. The runner maps them to fixed argument vectors and never invokes a shell:

- `python-unittest`: `python -I -S -m unittest discover -s tests -v` using the current Python interpreter in isolated mode with site initialization disabled.
- `semantic-review`: the runner invokes `python -I -S scripts/ai_semantic_review.py --input - --output <path>` and supplies the preflighted review-input byte snapshot over standard input; callers still supply the source and artifact paths with `--review-input` and `--review-output`. The standalone CLI also accepts a file path for direct use.

If `semantic-review` is configured, a caller must pass `--review-input`, `--review-output`, and `--review-base-commit` (the full commit SHA of the target branch tip used to construct the review diff). The runner resolves the current `HEAD`, verifies that the base exists and shares a merge base with `HEAD`, then regenerates the canonical diff with fixed Git options and byte-compares it with the input `diff` before any task runs. The diff must therefore be generated from `git diff --binary --full-index --no-ext-diff --no-textconv --no-color --no-renames --no-relative --diff-algorithm=myers --src-prefix=a/ --dst-prefix=b/ <base>...HEAD --`. Review input must already exist and fit within the 4 MiB input limit. Its bytes and SHA-256 fingerprint are captured before task execution and the source path is rechecked immediately before semantic review. The exact preflight bytes are passed to the review subprocess over standard input, so a concurrent path replacement after the recheck cannot change the payload the model receives; if a preceding task changes the source file, the run is blocked. Review output and the acceptance report must be files under `artifacts/`. Output paths may not overwrite the config, review input, or one another. All configured tasks are preflighted before any task runs.

## Execution and exit behavior

- Each task has a timeout; default is 600 seconds, maximum is 3600 seconds.
- Tasks run in the order declared by the config. If `semantic-review` is configured, it must be the final task so local tests/validation run first. Execution stops at the first failed task; remaining tasks are recorded as `not_run`, and the overall report fails. This avoids unnecessary model requests when an earlier check already failed.
- Task stdout/stderr are suppressed by default to reduce accidental credential or private-payload disclosure in logs.
- Exit code `0`: all configured tasks passed and the report status is `passed`.
- Exit code `1`: at least one task failed; a redacted report is still written with overall status `failed`.
- Exit code `2`: invalid config/paths, missing required review arguments, project metadata failure, or report-writing failure blocks the run.

## Report contract

The runner reuses `scripts/acceptance_report.py` and emits only the current commit SHA, SHA-256 pin of the stable acceptance contract, runner version label, per-task status, and overall status. It never copies task output, environment variables, API keys, or raw logs into the report.

A passing runner result establishes only that the configured fixed tasks exited successfully on the recorded commit. The semantic-review input remains caller-supplied, but the runner now requires an explicit target base commit and verifies that the exact diff bytes match the canonical Git diff from that base to the current `HEAD`; it also retains the input fingerprint check between preflight and execution. This binds the reviewed patch to the current source commit and declared base, but does not prove that the chosen base is the correct policy target or that the model reasoning is complete. Binary diff metadata cannot receive semantic-review `PASS`; the binary payload is not available as reviewable source text. The report's `commit_sha` identifies the checked-out source commit. It is not proof that semantic review detects every defect and is not authorization to merge, deploy, or perform project actions.

## Security boundaries

- Unknown task IDs fail closed in `scripts/harness_config.py`.
- The runner never evaluates configuration text as shell code and does not accept executable paths or arbitrary arguments from config.
- Trusted source inputs (`tests/`, the semantic-review script, and the stable acceptance contract) must resolve inside the project root, outside `artifacts/`, and contain no symlinked source paths. Caller-supplied config/report/review paths reject symlink components before reads or writes.
- The semantic-review output must not alias the Harness config, even when both paths are inside `artifacts/`; generated report/review outputs are revalidated immediately before report emission.
- Every semantic-review result must include at least one non-empty `limitations` entry; the field cannot be an empty list, including on `PASS`. Each semantic-review finding's `rule_quote` must be an exact substring of either `global_rules` or `project_instructions` individually; a quote assembled across the boundary between those fields is rejected. The diff parser also validates both old and new repository-relative paths from every `diff --git` header, so an unsafe rename source cannot be hidden behind a safe destination path.
- Each finding's `line_start`/`line_end` must exactly match the minimum/maximum source lines mapped from its cited diff evidence; merely providing a broad range that happens to include the evidence is rejected. Added-line and context-line evidence use resulting-file line numbers; deleted-line evidence uses old-file coordinates. Context in a deleted file also uses old-file coordinates because no resulting file exists. Exact evidence substrings must also be unique within the cited file's diff section; repeated evidence is rejected as ambiguous rather than widened into a multi-location range. Evidence that spans deleted lines and context/added lines in an ordinary modified file is rejected because those lines use different coordinate systems; context within a deleted file continues to use old-file coordinates.
- The runner requires `--review-base-commit` for semantic-review and regenerates the canonical Git diff from that base to current `HEAD` using fixed, non-extensible Git diff options; input diff bytes must match exactly. The base must be an available full commit SHA with a merge base against `HEAD`. This binds the patch to the checked-out source and supplied base but does not attest that the supplied base is the correct target branch.
- Caller-supplied semantic-review input is capped at 4 MiB by both runner and standalone CLI. It is read into a byte snapshot and fingerprinted before task execution, then the source path is rechecked immediately before the semantic-review task. The snapshot bytes are passed to the child over standard input, avoiding a check/use race where a concurrent replacement could otherwise change the bytes actually reviewed. If a preceding task changes or replaces the source input, the run is blocked.
- The standalone semantic-review CLI rejects symlink components in both input and output paths and writes the final review artifact through a same-directory temporary file plus atomic replacement. This reduces partial-artifact exposure and prevents the final output entry from redirecting a write through a symlink; it is not a general filesystem sandbox against hostile concurrent parent-directory replacement. The artifact is valid JSON with a real trailing newline.
- After all tasks, the runner rechecks the full Git worktree (tracked changes and non-ignored untracked files outside `artifacts/`) as well as HEAD and ignored Python sources. Task-created or task-modified source files must block report emission. On any blocked run after output paths are safely established, stale report/review artifacts are best-effort removed; cleanup preserves any output path that resolves to a config or review-input path.
- Before task execution and again after all tasks, the runner rejects ignored importable Python code files (`.py`, `.pyc`, `.so`, and `.pyd`) anywhere in the repository. It excludes only repository-root generated `artifacts/` and recognized virtual-environment directories (`.venv`, `venv`, `env`, `.tox`), plus `__pycache__` directories at any depth. A nested project directory named `env` or `.venv-custom` is not exempt. The dependency/runtime environment itself is not attested by the source commit.
- Python task subprocesses use isolated mode (`-I`) and disable site initialization (`-S`), preventing `PYTHONPATH`, user-site packages, `sitecustomize`, and `.pth` startup hooks from changing task imports. The repository currently uses only Python standard-library imports; task subprocesses therefore do not load installed third-party site packages. This does not attest the selected Python executable, its standard library, the host OS, or the Git executable.
- The runner is not a sandbox: test suites are repository code and may have side effects. Run it only against a trusted worktree and review project tests before enabling the runner in CI.
- All input/output paths must remain within the project root; output files are restricted to `artifacts/`.
- The semantic-review task may make a provider request only when explicitly configured in the task list and when the required provider environment variables are present. Provider/configuration errors fail closed.
- The runner does not commit, push, create PRs, merge, deploy, or invoke game/business actions.
