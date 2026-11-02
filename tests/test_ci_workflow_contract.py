import re
import unittest
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "ci.yml"
)


class CIWorkflowContractTests(unittest.TestCase):
    def test_every_checkout_step_disables_credential_persistence(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        steps = re.split(r"(?m)^\s+- name:", source)
        checkout_steps = [
            step for step in steps
            if re.search(r"(?m)^\s+uses:\s+actions/checkout@", step)
        ]
        self.assertTrue(checkout_steps, "CI must contain a checkout step")
        for step in checkout_steps:
            with self.subTest(step=step.splitlines()[0]):
                self.assertRegex(
                    step,
                    r"(?m)^\s+persist-credentials:\s*false\s*$",
                )

    def test_upload_artifact_uses_node24_compatible_v7_pin(self):
        expected = "actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2"
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertEqual(source.count("uses: actions/upload-artifact@"), 1)
        self.assertEqual(source.count("uses: " + expected), 1)


if __name__ == "__main__":
    unittest.main()
