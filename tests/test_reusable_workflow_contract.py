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
        self.assertNotRegex(self.source, r"(?m)^\s+[a-zA-Z0-9_-]+:\s*write\b")

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
            r"(?s)test-command:\n\s+description:.*?required: true\n\s+type: string",
        )

    def test_input_validation_precedes_consumer_execution(self):
        validation = self.source.index("      - name: Validate runtime and package-manager inputs")
        command = self.source.index("      - name: Run consumer-owned acceptance command")
        self.assertLess(validation, command)
        self.assertIn('case "$ACCEPTANCE_RUNTIME" in', self.source[validation:command])
        self.assertIn('case "$ACCEPTANCE_PACKAGE_MANAGER" in', self.source[validation:command])

    def test_whitespace_only_command_is_rejected_before_shell_execution(self):
        command_step = self.source.split(
            "      - name: Run consumer-owned acceptance command", 1
        )[1]
        self.assertIn('if [ -z "${ACCEPTANCE_COMMAND//[[:space:]]/}" ]; then', command_step)
        self.assertLess(
            command_step.index('if [ -z "${ACCEPTANCE_COMMAND//[[:space:]]/}" ]; then'),
            command_step.index('bash -euo pipefail -c "$ACCEPTANCE_COMMAND"'),
        )

    def test_command_guard_rejects_whitespace_at_runtime(self):
        import os
        import subprocess

        step = self.source.split(
            "      - name: Run consumer-owned acceptance command", 1
        )[1]
        script = step.split("        run: |\n", 1)[1]
        script = "\n".join(
            line[10:] if line.startswith("          ") else line
            for line in script.splitlines()
        )
        for command in ("", "   ", "\t\n "):
            with self.subTest(command=repr(command)):
                env = dict(os.environ, ACCEPTANCE_COMMAND=command)
                result = subprocess.run(
                    ["bash", "-euo", "pipefail", "-c", script],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("test-command must not be empty.", result.stderr)

    def test_runtime_validation_rejects_unsupported_values_at_runtime(self):
        import os
        import subprocess

        step = self.source.split(
            "      - name: Validate runtime and package-manager inputs", 1
        )[1].split("      - name: Set up Python", 1)[0]
        script = step.split("        run: |\n", 1)[1]
        script = "\n".join(
            line[10:] if line.startswith("          ") else line
            for line in script.splitlines()
        )
        for runtime, manager in (
            ("ruby", "none"),
            ("node", "npm"),
            ("python", "pnpm"),
        ):
            with self.subTest(runtime=runtime, manager=manager):
                env = dict(
                    os.environ,
                    ACCEPTANCE_RUNTIME=runtime,
                    ACCEPTANCE_PACKAGE_MANAGER=manager,
                )
                result = subprocess.run(
                    ["bash", "-euo", "pipefail", "-c", script],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("::error::", result.stderr)

    def test_runtime_validation_accepts_supported_combinations(self):
        import os
        import subprocess

        step = self.source.split(
            "      - name: Validate runtime and package-manager inputs", 1
        )[1].split("      - name: Set up Python", 1)[0]
        script = step.split("        run: |\n", 1)[1]
        script = "\n".join(
            line[10:] if line.startswith("          ") else line
            for line in script.splitlines()
        )
        for runtime, manager in (
            ("python", "none"),
            ("node", "none"),
            ("node", "pnpm"),
        ):
            with self.subTest(runtime=runtime, manager=manager):
                env = dict(
                    os.environ,
                    ACCEPTANCE_RUNTIME=runtime,
                    ACCEPTANCE_PACKAGE_MANAGER=manager,
                )
                result = subprocess.run(
                    ["bash", "-euo", "pipefail", "-c", script],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_consumer_command_failure_is_propagated(self):
        import os
        import subprocess

        step = self.source.split(
            "      - name: Run consumer-owned acceptance command", 1
        )[1]
        script = step.split("        run: |\n", 1)[1]
        script = "\n".join(
            line[10:] if line.startswith("          ") else line
            for line in script.splitlines()
        )
        env = dict(os.environ, ACCEPTANCE_COMMAND="exit 7")
        result = subprocess.run(
            ["bash", "-euo", "pipefail", "-c", script],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 7)

    def test_job_has_a_bounded_timeout(self):
        self.assertIn("timeout-minutes: 15", self.source)


    def test_consumer_command_success_is_propagated_and_output_is_visible(self):
        import os
        import subprocess

        step = self.source.split(
            "      - name: Run consumer-owned acceptance command", 1
        )[1]
        script = step.split("        run: |\\n", 1)[1]
        script = "\\n".join(
            line[10:] if line.startswith("          ") else line
            for line in script.splitlines()
        )
        env = dict(
            os.environ,
            ACCEPTANCE_COMMAND="printf 'consumer-command-ok\\n'",
        )
        result = subprocess.run(
            ["bash", "-euo", "pipefail", "-c", script],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("consumer-command-ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
