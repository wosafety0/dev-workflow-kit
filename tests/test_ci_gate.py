import contextlib
import io
import unittest

from scripts.ci_gate import gate_passes, main


class CiGateTests(unittest.TestCase):
    def test_only_all_exact_success_outcomes_pass(self):
        self.assertTrue(gate_passes("success", "success", "success", "success"))
        for stage_index, bad_outcome in enumerate(
            ("failure", "cancelled", "skipped", "neutral", "", "Success", "unknown")
        ):
            outcomes = ["success"] * 4
            outcomes[stage_index] = bad_outcome
            with self.subTest(stage_index=stage_index, bad_outcome=bad_outcome):
                self.assertFalse(gate_passes(*outcomes))

    def test_missing_or_extra_stage_outcomes_fail_closed(self):
        self.assertFalse(gate_passes())
        self.assertFalse(gate_passes("success"))
        self.assertFalse(gate_passes("success", "success", "success"))
        self.assertFalse(gate_passes(*(["success"] * 5)))

    def test_cli_returns_zero_only_when_all_required_stages_succeed(self):
        self.assertEqual(main(["success"] * 4), 0)
        cases = (
            ["failure", "success", "success", "success"],
            ["success", "failure", "success", "success"],
            ["success", "success", "failure", "success"],
            ["success", "success", "success", "failure"],
            ["cancelled", "success", "success", "success"],
            ["success", "skipped", "success", "success"],
            ["success", "success", "neutral", "success"],
            ["success", "success", "success", "skipped"],
        )
        for outcomes in cases:
            with self.subTest(outcomes=outcomes):
                self.assertEqual(main(outcomes), 1)

    def test_cli_rejects_wrong_argument_count(self):
        for args in ([], ["success"], ["success"] * 2, ["success"] * 3, ["success"] * 5):
            with self.subTest(args=args):
                self.assertEqual(main(args), 2)

    def test_failure_message_names_failed_stages_without_echoing_values(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = main(["success", "failure", "cancelled", "skipped"])
        self.assertEqual(result, 1)
        message = stderr.getvalue()
        self.assertIn("report", message)
        self.assertIn("artifact", message)
        self.assertIn("verification", message)
        self.assertNotIn("cancelled", message)
        self.assertNotIn("failure", message)


if __name__ == "__main__":
    unittest.main()
