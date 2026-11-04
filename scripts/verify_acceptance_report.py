"""Fail-closed verification of a runner acceptance report against expected CI identity."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_SHA = re.compile(r"^[0-9a-f]{40}$")
_PIN = re.compile(r"^sha256:[0-9a-f]{64}$")
_KEYS = {"schema_version", "commit_sha", "rules_pin", "tool_version", "tests", "status"}
_MAX_REPORT_BYTES = 1_048_576


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _read_report(path: Path) -> object:
    with path.open("rb") as report_file:
        raw = report_file.read(_MAX_REPORT_BYTES + 1)
    if len(raw) > _MAX_REPORT_BYTES:
        raise ValueError("acceptance report exceeds size limit")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)


def verify_report(report: object, expected_sha: str, expected_rules_pin: str) -> bool:
    if type(report) is not dict or any(type(key) is not str for key in report) or set(report) != _KEYS:
        return False
    if type(expected_sha) is not str or not _SHA.fullmatch(expected_sha):
        return False
    if type(expected_rules_pin) is not str or not _PIN.fullmatch(expected_rules_pin):
        return False
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        return False
    if type(report["commit_sha"]) is not str or report["commit_sha"] != expected_sha:
        return False
    if type(report["rules_pin"]) is not str or report["rules_pin"] != expected_rules_pin:
        return False
    if type(report["status"]) is not str or report["status"] != "passed":
        return False
    # Bind the tool identity to the same commit as the report.
    # A non-empty arbitrary version string is insufficient provenance.
    if (
        type(report["tool_version"]) is not str
        or report["tool_version"] != f"dev-workflow-kit/harness-runner@{expected_sha}"
    ):
        return False
    tests = report["tests"]
    if type(tests) is not dict or not tests:
        return False
    return all(
        type(name) is str
        and bool(name)
        and name == name.strip()
        and type(status) is str
        and status == "passed"
        for name, status in tests.items()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--expected-rules-pin", required=True)
    args = parser.parse_args(argv)
    try:
        report = _read_report(Path(args.report))
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("Acceptance report verification failed")
        return 1
    if not verify_report(report, args.expected_sha, args.expected_rules_pin):
        print("Acceptance report verification failed")
        return 1
    print("Acceptance report verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
