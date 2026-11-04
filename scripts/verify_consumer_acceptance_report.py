"""Fail-closed verification of the reusable workflow's redacted consumer report."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_SHA = re.compile(r"^[0-9a-f]{40}$")
_EXPECTED_TESTS = {"runtime-validation", "consumer-acceptance-command"}
_MAX_REPORT_BYTES = 1_048_576
_KEYS = {
    "schema_version",
    "consumer_commit_sha",
    "caller_workflow_ref",
    "caller_workflow_sha",
    "harness_workflow_ref",
    "harness_workflow_sha",
    "tests",
    "status",
}


def verify_report(
    report: object,
    expected_sha: str,
    expected_workflow_ref: str,
    expected_workflow_sha: str,
    expected_harness_workflow_ref: str,
    expected_harness_workflow_sha: str,
) -> bool:
    if type(report) is not dict or any(type(key) is not str for key in report) or set(report) != _KEYS:
        return False
    if type(expected_sha) is not str or not _SHA.fullmatch(expected_sha):
        return False
    if type(expected_workflow_ref) is not str or not expected_workflow_ref.strip():
        return False
    if type(expected_workflow_sha) is not str or not _SHA.fullmatch(expected_workflow_sha):
        return False
    if type(expected_harness_workflow_ref) is not str or not expected_harness_workflow_ref.strip():
        return False
    if type(expected_harness_workflow_sha) is not str or not _SHA.fullmatch(expected_harness_workflow_sha):
        return False
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        return False
    if type(report["consumer_commit_sha"]) is not str or report["consumer_commit_sha"] != expected_sha:
        return False
    if type(report["caller_workflow_ref"]) is not str or report["caller_workflow_ref"] != expected_workflow_ref:
        return False
    if type(report["caller_workflow_sha"]) is not str or report["caller_workflow_sha"] != expected_workflow_sha:
        return False
    if type(report["harness_workflow_ref"]) is not str or report["harness_workflow_ref"] != expected_harness_workflow_ref:
        return False
    if type(report["harness_workflow_sha"]) is not str or report["harness_workflow_sha"] != expected_harness_workflow_sha:
        return False
    if type(report["status"]) is not str or report["status"] != "passed":
        return False
    tests = report["tests"]
    if type(tests) is not dict or set(tests) != _EXPECTED_TESTS:
        return False
    return all(
        type(name) is str
        and bool(name)
        and name == name.strip()
        and type(status) is str
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


def _read_report(path: Path) -> object:
    with path.open("rb") as report_file:
        raw = report_file.read(_MAX_REPORT_BYTES + 1)
    if len(raw) > _MAX_REPORT_BYTES:
        raise ValueError("consumer acceptance report exceeds size limit")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--expected-workflow-ref", required=True)
    parser.add_argument("--expected-workflow-sha", required=True)
    parser.add_argument("--expected-harness-workflow-ref", required=True)
    parser.add_argument("--expected-harness-workflow-sha", required=True)
    args = parser.parse_args(argv)
    try:
        report = _read_report(Path(args.report))
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("Consumer acceptance report verification failed")
        return 1
    if not verify_report(
        report,
        args.expected_sha,
        args.expected_workflow_ref,
        args.expected_workflow_sha,
        args.expected_harness_workflow_ref,
        args.expected_harness_workflow_sha,
    ):
        print("Consumer acceptance report verification failed")
        return 1
    print("Consumer acceptance report verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
