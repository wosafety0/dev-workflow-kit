"""Fail-closed verification of a runner acceptance report against expected CI identity."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_SHA = re.compile(r"^[0-9a-f]{40}$")
_PIN = re.compile(r"^sha256:[0-9a-f]{64}$")
_KEYS = {"schema_version", "commit_sha", "rules_pin", "tool_version", "tests", "status"}


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def verify_report(report: object, expected_sha: str, expected_rules_pin: str) -> bool:
    if not isinstance(report, dict) or set(report) != _KEYS:
        return False
    if not isinstance(expected_sha, str) or not _SHA.fullmatch(expected_sha):
        return False
    if not isinstance(expected_rules_pin, str) or not _PIN.fullmatch(expected_rules_pin):
        return False
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        return False
    if report["commit_sha"] != expected_sha or report["rules_pin"] != expected_rules_pin:
        return False
    if report["status"] != "passed":
        return False
    # Bind the tool identity to the same commit as the report.
    # A non-empty arbitrary version string is insufficient provenance.
    if report["tool_version"] != f"dev-workflow-kit@{expected_sha}":
        return False
    tests = report["tests"]
    if not isinstance(tests, dict) or not tests:
        return False
    return all(
        isinstance(name, str)
        and bool(name)
        and name == name.strip()
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
        report = json.loads(
            Path(args.report).read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, UnicodeError, ValueError):
        print("Acceptance report verification failed")
        return 1
    if not verify_report(report, args.expected_sha, args.expected_rules_pin):
        print("Acceptance report verification failed")
        return 1
    print("Acceptance report verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
