import unittest

from scripts.ci_gate import gate_passes, main


class CiGateTests(unittest.TestCase):
    def test_only_exact_success_passes(self):
        self.assertTrue(gate_passes("success"))
        for outcome in ("failure", "cancelled", "skipped", "neutral", "", "Success"):
            with self.subTest(outcome=outcome):
                self.assertFalse(gate_passes(outcome))

    def test_cli_returns_zero_only_for_success(self):
        self.assertEqual(main(["success"]), 0)
        for outcome in ("failure", "cancelled", "skipped", "unknown"):
            with self.subTest(outcome=outcome):
                self.assertEqual(main([outcome]), 1)

    def test_cli_rejects_missing_argument(self):
        self.assertEqual(main([]), 2)


if __name__ == "__main__":
    unittest.main()
