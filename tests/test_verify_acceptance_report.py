import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.verify_acceptance_report import verify_report

SHA = "a" * 40
PIN = "sha256:" + "b" * 64


def valid():
    return {
        "schema_version": 1,
        "commit_sha": SHA,
        "rules_pin": PIN,
        "tool_version": "dev-workflow-kit/harness-runner@" + SHA,
        "tests": {"python-unittest": "passed"},
        "status": "passed",
    }


class AcceptanceReportVerifierTests(unittest.TestCase):
    def test_accepts_matching_pass_report(self):
        self.assertTrue(verify_report(valid(), SHA, PIN))

    def test_rejects_stale_commit(self):
        self.assertFalse(verify_report(valid(), "c" * 40, PIN))

    def test_rejects_wrong_contract_pin(self):
        self.assertFalse(verify_report(valid(), SHA, "sha256:" + "c" * 64))

    def test_rejects_failed_or_skipped_task(self):
        for status in ("failed", "not_run", "skipped"):
            with self.subTest(status=status):
                report = valid()
                report["tests"]["python-unittest"] = status
                self.assertFalse(verify_report(report, SHA, PIN))

    def test_rejects_bad_schema_and_unknown_fields(self):
        for key, value in (("schema_version", True), ("schema_version", 2),
                           ("status", "failed"), ("tests", {})):
            with self.subTest(key=key, value=value):
                report = valid()
                report[key] = value
                self.assertFalse(verify_report(report, SHA, PIN))
        report = valid()
        report["unexpected"] = "extra"
        self.assertFalse(verify_report(report, SHA, PIN))

    def test_cli_accepts_matching_report_and_rejects_wrong_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(valid()), encoding="utf-8")
            command = [sys.executable, "scripts/verify_acceptance_report.py",
                       "--report", str(path), "--expected-sha", SHA,
                       "--expected-rules-pin", PIN]
            passed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertIn("verified", passed.stdout)
            command[command.index("--expected-sha") + 1] = "c" * 40
            failed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(failed.returncode, 1)
            self.assertNotIn("Traceback", failed.stderr)

    def test_cli_rejects_duplicate_json_object_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.json"
            command = [sys.executable, "scripts/verify_acceptance_report.py",
                       "--report", str(path), "--expected-sha", SHA,
                       "--expected-rules-pin", PIN]
            for raw in (
                '{"schema_version":1,"schema_version":1}',
                '{"schema_version":1,"commit_sha":"' + SHA
                + '","rules_pin":"' + PIN
                + '","tool_version":"v1","tests":{"unit":"failed","unit":"passed"},'
                + '"status":"passed"}',
            ):
                with self.subTest(raw=raw):
                    path.write_text(raw, encoding="utf-8")
                    result = subprocess.run(command, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("verification failed", result.stdout)
                    self.assertNotIn("Traceback", result.stderr)

    def test_cli_fails_closed_for_missing_or_corrupt_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = str(Path(tmp) / "missing.json")
            command = [sys.executable, "scripts/verify_acceptance_report.py",
                       "--report", missing, "--expected-sha", SHA,
                       "--expected-rules-pin", PIN]
            absent = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(absent.returncode, 1)
            corrupt_path = Path(tmp) / "corrupt.json"
            corrupt_path.write_text("{not-json", encoding="utf-8")
            command[command.index("--report") + 1] = str(corrupt_path)
            corrupt = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(corrupt.returncode, 1)
            self.assertNotIn("Traceback", corrupt.stderr)

    def test_rejects_malformed_identity(self):
        self.assertFalse(verify_report(valid(), "not-a-sha", PIN))
        self.assertFalse(verify_report(valid(), SHA, "not-a-pin"))
        self.assertFalse(verify_report([], SHA, PIN))


if __name__ == "__main__":
    unittest.main()
