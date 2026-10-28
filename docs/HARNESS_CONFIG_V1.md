# Versioned Harness Configuration (v1)

Status: validation contract only; this is not a command runner.

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
- Validation is offline and side-effect free. It does not execute tasks, read credentials, access the network, or resolve paths.
- An eventual runner must map each task ID to reviewed fixed behavior; it must not treat this configuration as permission to execute arbitrary commands.

## Limits

This module validates shape and allowlist membership only. It does not prove that a project is safe, does not run tests, and does not authorize a remote write or merge. The allowlist is deliberately narrow and may only be expanded by a reviewed code change plus tests.
