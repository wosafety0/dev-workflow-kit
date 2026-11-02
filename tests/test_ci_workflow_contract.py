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


if __name__ == "__main__":
    unittest.main()
