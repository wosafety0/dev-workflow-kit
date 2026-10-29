import unittest

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

    def test_rejects_malformed_identity(self):
        self.assertFalse(verify_report(valid(), "not-a-sha", PIN))
        self.assertFalse(verify_report(valid(), SHA, "not-a-pin"))
        self.assertFalse(verify_report([], SHA, PIN))


if __name__ == "__main__":
    unittest.main()
