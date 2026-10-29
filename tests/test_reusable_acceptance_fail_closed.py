"""Isolated fail-closed tests for the reusable acceptance workflow command step.

These tests extract and execute the actual shell block from the reusable workflow,
so they verify the checked-in guard rather than a separately copied implementation.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "reusable-acceptance.yml"
STEP_NAME = "Run consumer-owned acceptance command"


def acceptance_step() -> tuple[str, str]:
    source = WORKFLOW.read_text(encoding="utf-8")
    step_pattern = re.compile(
        r"(?ms)^      - name: " + re.escape(STEP_NAME)
        + r"\n(?P<step>(?: {8,}.*\n)+)"
    )
    match = step_pattern.search(source)
    if match is None:
        raise AssertionError(f"workflow step not found: {STEP_NAME}")

    run_match = re.search(
        r"(?m)^        run: \|\n(?P<script>(?:          .*\n)+)",
        match.group("step"),
    )
    if run_match is None:
        raise AssertionError(f"shell run block not found in step: {STEP_NAME}")
    return STEP_NAME, textwrap.dedent(run_match.group("script"))


@unittest.skipUnless(shutil.which("bash"), "Bash is required; CI runs on Ubuntu")
class ReusableAcceptanceCommandFailClosedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.step_name, cls.script = acceptance_step()

    def run_step(self, command: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["ACCEPTANCE_COMMAND"] = command
        return subprocess.run(
            ["bash", "-euo", "pipefail", "-c", self.script],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )

    def test_workflow_names_the_failing_acceptance_step(self) -> None:
        self.assertEqual(self.step_name, STEP_NAME)

    def test_empty_command_fails_with_explicit_diagnostic(self) -> None:
        result = self.run_step("")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("test-command must not be empty.", result.stderr)

    def test_whitespace_only_command_fails_closed(self) -> None:
        result = self.run_step(" \t \n ")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("test-command must not be empty.", result.stderr)

    def test_invalid_command_fails_and_reports_the_command(self) -> None:
        invalid_command = "__harness_acceptance_command_that_does_not_exist__"
        result = self.run_step(invalid_command)
        combined = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, combined)
        self.assertIn(invalid_command, combined)
        self.assertRegex(combined, r"command not found|not found")

    def test_valid_command_can_pass(self) -> None:
        result = self.run_step("printf 'acceptance-command-ok\\n'")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("acceptance-command-ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
