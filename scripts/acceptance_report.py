"""Build a deterministic, allowlisted acceptance report without copying logs or secrets."""
from __future__ import annotations

import re
from typing import Any


class AcceptanceReportError(ValueError):
    """Raised when acceptance metadata is incomplete or unsafe."""


_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_ALLOWED_ROOT_KEYS = {"commit_sha", "rules_pin", "tool_version", "tests"}
_ALLOWED_TEST_STATUSES = {"passed", "failed", "skipped", "not_run"}


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise AcceptanceReportError(f"{field} must be a non-empty trimmed string")
    return value


def build_acceptance_report(metadata: Any) -> dict[str, Any]:
    """Validate a strict metadata allowlist and return a deterministic report.

    The function deliberately does not accept logs, arbitrary metadata, credentials,
    environment variables, or filesystem/network inputs.
    """
    if not isinstance(metadata, dict):
        raise AcceptanceReportError("metadata must be a JSON object")
    if set(metadata) != _ALLOWED_ROOT_KEYS:
        raise AcceptanceReportError("metadata must contain exactly the required fields")

    commit_sha = _required_text(metadata["commit_sha"], "commit_sha")
    if not _SHA_RE.fullmatch(commit_sha):
        raise AcceptanceReportError("commit_sha must be a 40-character Git SHA")

    rules_pin = _required_text(metadata["rules_pin"], "rules_pin")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", rules_pin):
        raise AcceptanceReportError("rules_pin must be a lowercase SHA-256 digest")
    tool_version = _required_text(metadata["tool_version"], "tool_version")

    tests = metadata["tests"]
    if not isinstance(tests, dict) or not tests:
        raise AcceptanceReportError("tests must be a non-empty object")

    normalized_tests: dict[str, str] = {}
    for name, status in tests.items():
        if not isinstance(name, str) or not name or name != name.strip():
            raise AcceptanceReportError("test names must be non-empty trimmed strings")
        if name in normalized_tests:
            raise AcceptanceReportError("duplicate test name")
        if not isinstance(status, str) or status not in _ALLOWED_TEST_STATUSES:
            raise AcceptanceReportError(f"invalid status for test {name!r}")
        normalized_tests[name] = status

    # Sort test names to make the report stable across input insertion order.
    normalized_tests = dict(sorted(normalized_tests.items()))
    overall = "passed" if all(s == "passed" for s in normalized_tests.values()) else "failed"

    return {
        "schema_version": 1,
        "commit_sha": commit_sha.lower(),
        "rules_pin": rules_pin,
        "tool_version": tool_version,
        "tests": normalized_tests,
        "status": overall,
    }
