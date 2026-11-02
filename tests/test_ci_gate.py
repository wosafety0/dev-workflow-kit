import contextlib
import io
import unittest

from scripts.ci_gate import gate_passes, main


class CiGateTests(unittest.TestCase):
    def test_only_all_exact_success_outcomes_pass(self):
        self.assertTrue(gate_passes("success", "success", "success"))
        for stage_index, bad_outcome in enumerate(
            ("failure", "cancelled", "skipped", "neutral", "", "Success", "unknown")
        ):
            for index in range(3):
                outcomes = ["success", "success", "success"]
                outcomes[index] = bad_outcome
                with self.subTest(stage_index=index, bad_outcome=bad_outcome):
                    self.assertFalse(gate_passes(*outcomes))

    def test_missing_or_extra_stage_outcomes_fail_closed(self):
        self.assertFalse(gate_passes())
        self.assertFalse(gate_passes("success"))
        self.assertFalse(gate_passes("success", "success"))
        self.assertFalse(gate_passes("success", "success", "success", "success"))

    def test_cli_returns_zero_only_when_all_required_stages_succeed(self):
        self.assertEqual(main(["success", "success", "success"]), 0)
        for outcomes in (
            ["failure", "success", "success"],
            ["success", "failure", "success"],
            ["success", "success", "failure"],
            ["cancelled", "success", "success"],
            ["success", "skipped", "success"],
            ["success", "success", "neutral"],
        ):
            with self.subTest(outcomes=outcomes):
                self.assertEqual(main(outcomes), 1)

    def test_cli_rejects_wrong_argument_count(self):
        for args in ([], ["success"], ["success", "success"], ["success"] * 4):
            with self.subTest(args=args):
                self.assertEqual(main(args), 2)

    def test_failure_message_names_failed_stages_without_echoing_values(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = main(["success", "failure", "cancelled"])
        self.assertEqual(result, 1)
        message = stderr.getvalue()
        self.assertIn("report", message)
        self.assertIn("artifact", message)
        self.assertNotIn("cancelled", message)
        self.assertNotIn("failure", message)


if __name__ == "__main__":
    unittest.main()
