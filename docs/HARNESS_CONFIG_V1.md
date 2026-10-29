# Versioned Harness Configuration (v1)

Status: v1 configuration contract consumed by `scripts/harness_runner.py`; early implementation, not a stable API guarantee.

## Example

```json
{
  "schema_version": 1,
  "project": "example-project",
  "commands": [
    "python-unittest",
    "semantic-review"
  ]
}
```

## Rules

- `schema_version` must be the integer `1`; booleans and unknown versions are rejected.
- The object must contain exactly `schema_version`, `project`, and `commands`.
- `project` must be a non-empty, trimmed string.
- `commands` must be a non-empty list of unique task IDs.
- Currently recognized task IDs are `python-unittest` and `semantic-review`.
- Configuration cannot provide executable names, arbitrary arguments, or unknown task IDs.
- Unknown keys and unknown task IDs fail closed.
- Validation in `scripts/harness_config.py` remains offline and side-effect free. It does not execute tasks, read credentials, access the network, or resolve paths.
- The runner maps each task ID to reviewed fixed behavior and does not treat configuration as permission to execute arbitrary commands. See `docs/HARNESS_RUNNER_V1.md`.

## Limits

This module validates shape and allowlist membership only. It does not prove that a project is safe, does not run tests, and does not authorize a remote write or merge. The allowlist is deliberately narrow and may only be expanded by a reviewed code change plus tests.
