import re
import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"


class CIWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_every_external_action_is_pinned_to_a_full_commit_sha(self):
        uses = re.findall(r"(?m)^[ \t]+uses:[ \t]+([^ \t]+)", self.source)
        actions = [ref for ref in uses if not ref.startswith("./")]
        self.assertGreaterEqual(len(actions), 3)
        for action in actions:
            self.assertRegex(
                action,
                r"^[^@]+@[0-9a-f]{40}$",
                msg=f"Action is not pinned to a full SHA: {action}",
            )

    def test_checkout_does_not_persist_credentials(self):
        self.assertRegex(
            self.source,
            r"(?s)- name: Check out repository\\n\\s+uses: actions/checkout@[0-9a-f]{40} # v5\\n\\s+with:\\n\\s+persist-credentials: false",
        )

    def test_artifact_upload_uses_node24_compatible_v7_pin(self):
        self.assertIn(
            "uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2",
            self.source,
        )
        self.assertNotIn(
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
            self.source,
        )


if __name__ == "__main__":
    unittest.main()
