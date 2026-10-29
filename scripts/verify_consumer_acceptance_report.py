"""Fail-closed verification of the reusable workflow's redacted consumer report."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_SHA = re.compile(r"^[0-9a-f]{40}$")
_EXPECTED_TESTS = {"runtime-validation", "consumer-acceptance-command"}
_KEYS = {
    "schema_version",
    "consumer_commit_sha",
    "caller_workflow_ref",
    "caller_workflow_sha",
    "tests",
    "status",
}


def verify_report(
    report: object,
    expected_sha: str,
    expected_workflow_ref: str,
    expected_workflow_sha: str,
) -> bool:
    if not isinstance(report, dict) or set(report) != _KEYS:
        return False
    if not isinstance(expected_sha, str) or not _SHA.fullmatch(expected_sha):
        return False
    if not isinstance(expected_workflow_ref, str) or not expected_workflow_ref.strip():
        return False
    if not isinstance(expected_workflow_sha, str) or not _SHA.fullmatch(expected_workflow_sha):
        return False
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        return False
    if report["consumer_commit_sha"] != expected_sha:
        return False
    if report["caller_workflow_ref"] != expected_workflow_ref:
        return False
    if report["caller_workflow_sha"] != expected_workflow_sha:
        return False
    if report["status"] != "passed":
        return False
    tests = report["tests"]
    if not isinstance(tests, dict) or set(tests) != _EXPECTED_TESTS:
        return False
    return all(
        isinstance(name, str)
        and bool(name)
        and name == name.strip()
        and status == "passed"
        for name, status in tests.items()
    )


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--expected-workflow-ref", required=True)
    parser.add_argument("--expected-workflow-sha", required=True)
    args = parser.parse_args(argv)
    try:
        report = json.loads(
            Path(args.report).read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, UnicodeError, ValueError):
        print("Consumer acceptance report verification failed")
        return 1
    if not verify_report(
        report,
        args.expected_sha,
        args.expected_workflow_ref,
        args.expected_workflow_sha,
    ):
        print("Consumer acceptance report verification failed")
        return 1
    print("Consumer acceptance report verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
