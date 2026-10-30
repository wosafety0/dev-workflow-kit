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


def build_acceptance_report(metadata: Any) -> dict[str, Any]:
    """Build schema v1 normally, or schema v2 when Git-bound review provenance is present."""
    if not isinstance(metadata, dict):
        raise AcceptanceReportError("metadata must be a JSON object")
    keys = set(metadata)
    if keys not in (_REQUIRED_ROOT_KEYS, _REQUIRED_ROOT_KEYS | {"review_provenance"}):
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
    report = {
        "schema_version": 2 if "review_provenance" in metadata else 1,
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
    return report
