"""Offline validation for the versioned AI development harness config.

This module validates task identifiers only. It never executes commands, invokes a
shell, reads secrets, or performs network or filesystem operations.
"""
from __future__ import annotations

from typing import Any


SUPPORTED_SCHEMA_VERSION = 1

# Stable task IDs map to documented intent. The configuration cannot override
# executable names or arguments; an eventual runner must implement these IDs
# explicitly and independently enforce its own safety checks.
ALLOWED_COMMAND_IDS = frozenset({
    "python-unittest",
    "semantic-review",
})


class HarnessConfigError(ValueError):
    """Raised when a harness configuration is invalid or unsafe."""


def validate_harness_config(config: Any) -> dict[str, Any]:
    """Validate the v1 project config without executing or resolving any task."""
    if not isinstance(config, dict):
        raise HarnessConfigError("Configuration must be a JSON object")

    expected_keys = {"schema_version", "project", "commands"}
    if set(config) != expected_keys:
        raise HarnessConfigError("Configuration keys must be exactly: commands, project, schema_version")

    version = config["schema_version"]
    if type(version) is not int or version != SUPPORTED_SCHEMA_VERSION:
        raise HarnessConfigError("Unsupported schema_version; expected integer 1")

    project = config["project"]
    if not isinstance(project, str) or not project.strip() or project != project.strip():
        raise HarnessConfigError("project must be a non-empty trimmed string")

    commands = config["commands"]
    if not isinstance(commands, list) or not commands:
        raise HarnessConfigError("commands must be a non-empty list of allowlisted task IDs")

    if any(not isinstance(item, str) or not item for item in commands):
        raise HarnessConfigError("each command must be a non-empty task ID string")
    if len(commands) != len(set(commands)):
        raise HarnessConfigError("commands must not contain duplicate task IDs")

    unknown = sorted(set(commands) - ALLOWED_COMMAND_IDS)
    if unknown:
        raise HarnessConfigError("unknown command ID(s): " + ", ".join(unknown))

    # Return a copy so callers cannot mutate the original through this result.
    return {
        "schema_version": SUPPORTED_SCHEMA_VERSION,
        "project": project,
        "commands": list(commands),
    }
