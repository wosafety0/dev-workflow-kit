import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.verify_consumer_acceptance_report import main, verify_report


SHA = "a" * 40
WORKFLOW_SHA = "b" * 40
WORKFLOW_REF = "wosafety0/example/.github/workflows/ci.yml@refs/heads/main"


def valid_report():
    return {
        "schema_version": 1,
        "consumer_commit_sha": SHA,
        "caller_workflow_ref": WORKFLOW_REF,
        "caller_workflow_sha": WORKFLOW_SHA,
        "tests": {"runtime-validation": "passed", "consumer-acceptance-command": "passed"},
        "status": "passed",
    }


class VerifyConsumerAcceptanceReportTests(unittest.TestCase):
    def test_valid_report_passes(self):
        self.assertTrue(verify_report(valid_report(), SHA, WORKFLOW_REF, WORKFLOW_SHA))

    def test_wrong_commit_or_workflow_identity_fails(self):
        for field, expected in (
            ("consumer_commit_sha", "c" * 40),
            ("caller_workflow_ref", "another/repo/.github/workflows/ci.yml@refs/heads/main"),
            ("caller_workflow_sha", "d" * 40),
        ):
            report = valid_report()
            report[field] = expected
            with self.subTest(field=field):
                self.assertFalse(verify_report(report, SHA, WORKFLOW_REF, WORKFLOW_SHA))

    def test_failed_or_empty_tests_fail(self):
        for tests, status in (({"check": "failed"}, "failed"), ({"check": "skipped"}, "failed"),
                              ({}, "passed"), ({" ": "passed"}, "passed")):
            report = valid_report()
            report["tests"] = tests
            report["status"] = status
            with self.subTest(tests=tests, status=status):
                self.assertFalse(verify_report(report, SHA, WORKFLOW_REF, WORKFLOW_SHA))

    def test_required_stage_set_is_exact(self):
        for tests in (
            {"consumer-acceptance-command": "passed"},
            {"runtime-validation": "passed", "unexpected": "passed"},
            {"runtime-validation": "passed", "consumer-acceptance-command": "passed", "extra": "passed"},
        ):
            report = valid_report()
            report["tests"] = tests
            with self.subTest(tests=tests):
                self.assertFalse(verify_report(report, SHA, WORKFLOW_REF, WORKFLOW_SHA))

    def test_schema_and_expected_identity_are_strict(self):
        for mutate in (
            lambda r: r.update(schema_version=True),
            lambda r: r.update(extra="not allowed"),
            lambda r: r.update(status="PASS"),
        ):
            report = valid_report()
            mutate(report)
            self.assertFalse(verify_report(report, SHA, WORKFLOW_REF, WORKFLOW_SHA))
        self.assertFalse(verify_report(valid_report(), "bad-sha", WORKFLOW_REF, WORKFLOW_SHA))
        self.assertFalse(verify_report(valid_report(), SHA, "", WORKFLOW_SHA))
        self.assertFalse(verify_report(valid_report(), SHA, WORKFLOW_REF, "bad-sha"))

    def test_cli_accepts_matching_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text(json.dumps(valid_report()), encoding="utf-8")
            self.assertEqual(main([
                "--report", str(path), "--expected-sha", SHA,
                "--expected-workflow-ref", WORKFLOW_REF,
                "--expected-workflow-sha", WORKFLOW_SHA,
            ]), 0)

    def test_cli_rejects_missing_and_corrupt_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            args = [
                "--report", str(path), "--expected-sha", SHA,
                "--expected-workflow-ref", WORKFLOW_REF,
                "--expected-workflow-sha", WORKFLOW_SHA,
            ]
            self.assertEqual(main(args), 1)
            path.write_text("{broken", encoding="utf-8")
            self.assertEqual(main(args), 1)

    def test_cli_rejects_duplicate_json_object_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            command = [
                sys.executable, "scripts/verify_consumer_acceptance_report.py",
                "--report", str(path), "--expected-sha", SHA,
                "--expected-workflow-ref", WORKFLOW_REF,
                "--expected-workflow-sha", WORKFLOW_SHA,
            ]
            duplicate_top_level = (
                '{"schema_version":1,"schema_version":1}'
            )
            duplicate_nested = (
                '{"schema_version":1,"consumer_commit_sha":"' + SHA
                + '","caller_workflow_ref":"' + WORKFLOW_REF
                + '","caller_workflow_sha":"' + WORKFLOW_SHA
                + '","tests":{"runtime-validation":"failed",'
                + '"runtime-validation":"passed",'
                + '"consumer-acceptance-command":"passed"},"status":"passed"}'
            )
            for raw in (duplicate_top_level, duplicate_nested):
                with self.subTest(raw=raw):
                    path.write_text(raw, encoding="utf-8")
                    result = subprocess.run(command, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("verification failed", result.stdout.lower())
                    self.assertNotIn("Traceback", result.stderr)

    def test_subprocess_cli_rejects_stale_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text(json.dumps(valid_report()), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable, "scripts/verify_consumer_acceptance_report.py",
                    "--report", str(path), "--expected-sha", "c" * 40,
                    "--expected-workflow-ref", WORKFLOW_REF,
                    "--expected-workflow-sha", WORKFLOW_SHA,
                ],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("verification failed", result.stdout.lower())
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
