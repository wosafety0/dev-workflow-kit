"""Build a deterministic, allowlisted acceptance report without copying logs or secrets."""
from __future__ import annotations

import re
import unicodedata
from typing import Any


class AcceptanceReportError(ValueError):
    """Raised when acceptance metadata is incomplete or unsafe."""


_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_ROOT_KEYS = {"commit_sha", "rules_pin", "tool_version", "tests"}
_ALLOWED_TEST_STATUSES = {"passed", "failed", "skipped", "not_run"}
_PROVENANCE_KEYS = {
    "base_sha", "head_sha", "merge_base_sha", "diff_sha256", "changed_files",
}
_CI_CONTEXT_KEYS = {
    "tested_commit_sha", "run_id", "run_attempt", "event_name", "pull_request_head_sha",
}
_ALLOWED_CI_EVENTS = {"push", "pull_request", "workflow_dispatch"}


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise AcceptanceReportError(f"{field} must be a non-empty trimmed string")
    return value


def _validate_review_provenance(value: Any, commit_sha: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _PROVENANCE_KEYS:
        raise AcceptanceReportError("review_provenance must contain exactly the required fields")
    normalized: dict[str, Any] = {}
    for field in ("base_sha", "head_sha", "merge_base_sha"):
        sha = _required_text(value[field], f"review_provenance.{field}")
        if not _SHA_RE.fullmatch(sha):
            raise AcceptanceReportError(f"review_provenance.{field} must be a full Git SHA")
        normalized[field] = sha.lower()
    if normalized["head_sha"] != commit_sha.lower():
        raise AcceptanceReportError("review_provenance.head_sha must equal commit_sha")
    digest = _required_text(value["diff_sha256"], "review_provenance.diff_sha256")
    if not _DIGEST_RE.fullmatch(digest):
        raise AcceptanceReportError("review_provenance.diff_sha256 must be a lowercase SHA-256 digest")
    normalized["diff_sha256"] = digest
    paths = value["changed_files"]
    if not isinstance(paths, list) or not paths:
        raise AcceptanceReportError("review_provenance.changed_files must be a non-empty list")
    checked_paths: list[str] = []
    for path in paths:
        if not isinstance(path, str) or not path or path != path.strip() or len(path) > 4096:
            raise AcceptanceReportError("review_provenance.changed_files contains an invalid path")
        parts = path.split("/")
        if (
            path.startswith("/")
            or re.match(r"^[A-Za-z]:", path) is not None
            or "\\" in path
            or any(part in {"", ".", ".."} for part in parts)
            or any(unicodedata.category(char) == "Cc" for char in path)
        ):
            raise AcceptanceReportError("review_provenance.changed_files contains an unsafe path")
        checked_paths.append(path)
    if len(set(checked_paths)) != len(checked_paths):
        raise AcceptanceReportError("review_provenance.changed_files must not contain duplicates")
    normalized["changed_files"] = sorted(checked_paths)
    return normalized


def _validate_ci_context(value: Any, commit_sha: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _CI_CONTEXT_KEYS:
        raise AcceptanceReportError("ci_context must contain exactly the required fields")
    tested_sha = _required_text(value["tested_commit_sha"], "ci_context.tested_commit_sha")
    if not _SHA_RE.fullmatch(tested_sha) or tested_sha.lower() != commit_sha.lower():
        raise AcceptanceReportError("ci_context.tested_commit_sha must equal commit_sha")
    for field in ("run_id", "run_attempt"):
        number = value[field]
        if type(number) is not int or number < 1:
            raise AcceptanceReportError(f"ci_context.{field} must be a positive integer")
    event_name = _required_text(value["event_name"], "ci_context.event_name")
    if event_name not in _ALLOWED_CI_EVENTS:
        raise AcceptanceReportError("ci_context.event_name is not an allowed GitHub event")
    pr_head = value["pull_request_head_sha"]
    if event_name == "pull_request":
        if not isinstance(pr_head, str) or not _SHA_RE.fullmatch(pr_head):
            raise AcceptanceReportError("ci_context.pull_request_head_sha must be a full Git SHA for pull_request")
        normalized_pr_head = pr_head.lower()
    else:
        if pr_head is not None:
            raise AcceptanceReportError("ci_context.pull_request_head_sha must be null outside pull_request events")
        normalized_pr_head = None
    return {
        "tested_commit_sha": tested_sha.lower(),
        "run_id": value["run_id"],
        "run_attempt": value["run_attempt"],
        "event_name": event_name,
        "pull_request_head_sha": normalized_pr_head,
    }


def build_acceptance_report(metadata: Any) -> dict[str, Any]:
    """Build schema v1, v2 for Git-bound provenance, or v3 with CI run context."""
    if not isinstance(metadata, dict):
        raise AcceptanceReportError("metadata must be a JSON object")
    keys = set(metadata)
    allowed_keys = {
        frozenset(_REQUIRED_ROOT_KEYS),
        frozenset(_REQUIRED_ROOT_KEYS | {"review_provenance"}),
        frozenset(_REQUIRED_ROOT_KEYS | {"ci_context"}),
        frozenset(_REQUIRED_ROOT_KEYS | {"review_provenance", "ci_context"}),
    }
    if frozenset(keys) not in allowed_keys:
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

    normalized_tests = dict(sorted(normalized_tests.items()))
    overall = "passed" if all(s == "passed" for s in normalized_tests.values()) else "failed"
    schema_version = 3 if "ci_context" in metadata else (2 if "review_provenance" in metadata else 1)
    report = {
        "schema_version": schema_version,
        "commit_sha": commit_sha.lower(),
        "rules_pin": rules_pin,
        "tool_version": tool_version,
        "tests": normalized_tests,
        "status": overall,
    }
    if "review_provenance" in metadata:
        report["review_provenance"] = _validate_review_provenance(
            metadata["review_provenance"], commit_sha
        )
    if "ci_context" in metadata:
        report["ci_context"] = _validate_ci_context(metadata["ci_context"], commit_sha)
    return report
