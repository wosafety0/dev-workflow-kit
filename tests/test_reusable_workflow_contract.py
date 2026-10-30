import re
import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "reusable-acceptance.yml"


class ReusableAcceptanceWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_permissions_are_read_only(self):
        self.assertRegex(self.source, r"(?m)^permissions:\n  contents: read\s*$")
        self.assertNotRegex(self.source, r"(?m)^\s+(?:issues|pull-requests|actions|contents):\s*write\b")

    def test_checkout_does_not_persist_credentials(self):
        self.assertRegex(
            self.source,
            r"(?s)- name: Check out consuming repository\n\s+uses: actions/checkout@[0-9a-f]{40} # v5\n\s+with:\n\s+persist-credentials: false",
        )

    def test_runtime_is_explicit_and_defaults_to_python(self):
        self.assertRegex(self.source, r"(?s)runtime:\n\s+description:.*?required: false\n\s+type: string\n\s+default: python")
        self.assertIn("python|node)", self.source)
        self.assertIn("runtime must be python or node.", self.source)

    def test_python_and_node_setup_are_conditionally_selected(self):
        self.assertIn("if: inputs.runtime == 'python'", self.source)
        self.assertIn("if: inputs.runtime == 'node'", self.source)
        self.assertIn("python-version: ${{ inputs.python-version }}", self.source)
        self.assertIn("node-version: ${{ inputs.node-version }}", self.source)

    def test_optional_pnpm_setup_is_allowlisted_and_node_only(self):
        self.assertIn("none|pnpm)", self.source)
        self.assertIn("package-manager must be none or pnpm.", self.source)
        self.assertIn('if: inputs.runtime == \'node\' && inputs.package-manager == \'pnpm\'', self.source)
        self.assertIn("package-manager is supported only when runtime is node.", self.source)
        self.assertIn("version: ${{ inputs.pnpm-version }}", self.source)

    def test_every_action_uses_a_full_commit_sha(self):
        actions = re.findall(r"(?m)^\s+uses:\s+([^\s]+)", self.source)
        self.assertGreaterEqual(len(actions), 4)
        for action in actions:
            self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$", msg=f"Action is not pinned to a full SHA: {action}")

    def test_consumer_command_is_nonempty_and_not_interpolated_into_run_script(self):
        self.assertIn("ACCEPTANCE_COMMAND: ${{ inputs.test-command }}", self.source)
        self.assertIn('bash -euo pipefail -c "$ACCEPTANCE_COMMAND"', self.source)
        self.assertIn("test-command must not be empty.", self.source)
        run_script = self.source.split("      - name: Run consumer-owned acceptance command", 1)[1]
        self.assertNotIn("${{ inputs.test-command }}", run_script.split("run: |", 1)[1])

    def test_consumer_command_is_required(self):
        self.assertRegex(
            self.source,
            r"(?s)test-command:\\n\\s+description:.*?required: true\\n\\s+type: string",
        )

    def test_input_validation_precedes_consumer_execution(self):
        validation = self.source.index("      - name: Validate runtime and package-manager inputs")
        command = self.source.index("      - name: Run consumer-owned acceptance command")
        self.assertLess(validation, command)
        self.assertIn('case "$ACCEPTANCE_RUNTIME" in', self.source[validation:command])
        self.assertIn('case "$ACCEPTANCE_PACKAGE_MANAGER" in', self.source[validation:command])

    def test_job_has_a_bounded_timeout(self):
        self.assertIn("timeout-minutes: 15", self.source)


if __name__ == "__main__":
    unittest.main()
