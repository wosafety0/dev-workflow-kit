import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "reusable-acceptance.yml"


class ReusableAcceptanceWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_permissions_are_read_only_and_actions_are_sha_pinned(self):
        self.assertIn("permissions:\n  contents: read", self.source)
        self.assertIn("actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09", self.source)
        self.assertIn("actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1", self.source)
        self.assertIn("actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02", self.source)
        self.assertNotIn("secrets.", self.source)

    def test_test_failure_is_recorded_and_does_not_skip_reporting(self):
        self.assertIn("id: tests", self.source)
        self.assertIn("continue-on-error: true", self.source)
        self.assertIn("id: report\n        if: always()", self.source)
        self.assertIn("id: artifact\n        if: always()", self.source)
        self.assertIn("id: artifact", self.source)

    def test_report_uses_an_allowlisted_metadata_shape(self):
        for field in (
            '"schema_version": 1',
            '"consumer_commit_sha": os.environ["CONSUMER_COMMIT_SHA"]',
            '"caller_workflow_ref": os.environ["CALLER_WORKFLOW_REF"]',
            '"caller_workflow_sha": os.environ["CALLER_WORKFLOW_SHA"]',
            '"tests": {"consumer-acceptance-command": test_status}',
            '"status": "passed" if test_status == "passed" else "failed"',
        ):
            self.assertIn(field, self.source)
        self.assertIn("artifacts/consumer-acceptance-report.json", self.source)
        self.assertIn("retention-days: 14", self.source)

    def test_final_gate_requires_exact_success_for_every_required_stage(self):
        self.assertIn('[[ "$TEST_OUTCOME" == "success" ]] || failed+=("tests")', self.source)
        self.assertIn('[[ "$REPORT_OUTCOME" == "success" ]] || failed+=("report")', self.source)
        self.assertIn('[[ "$ARTIFACT_OUTCOME" == "success" ]] || failed+=("artifact")', self.source)
        self.assertIn("if (( ${#failed[@]} > 0 )); then", self.source)
        self.assertIn('echo "Acceptance orchestration gate passed."', self.source)


if __name__ == "__main__":
    unittest.main()
