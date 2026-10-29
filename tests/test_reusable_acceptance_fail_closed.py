"""Execute the actual shell gates from the pinned reusable acceptance workflow.

This isolates empty/invalid/valid consumer commands without changing a live workflow run.
It checks the command step, redacted report, and final workflow gate.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "reusable-acceptance.yml"
COMMAND_STEP = "Run consumer-owned acceptance command"
REPORT_STEP = "Build redacted consumer acceptance report"
FINAL_GATE_STEP = "Fail job unless all required stages succeeded"


def extract_run_block(source: str, step_name: str) -> str:
    step_pattern = re.compile(
        r"(?ms)^      - name: " + re.escape(step_name)
        + r"\n(?P<step>(?:(?: {8,}.*| *)\n)+)"
    )
    match = step_pattern.search(source)
    if match is None:
        raise AssertionError(f"workflow step not found: {step_name}")
    run_match = re.search(
        r"(?m)^        run: \|\n(?P<script>(?:(?: {10}.*| *)\n)+)",
        match.group("step"),
    )
    if run_match is None:
        raise AssertionError(f"shell run block not found in step: {step_name}")
    return textwrap.dedent(run_match.group("script"))


@unittest.skipUnless(shutil.which("bash"), "Bash is required; CI runs on Ubuntu")
class ReusableAcceptanceFailClosedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = WORKFLOW.read_text(encoding="utf-8")
        cls.command_script = extract_run_block(cls.source, COMMAND_STEP)
        cls.report_script = extract_run_block(cls.source, REPORT_STEP)
        cls.gate_script = extract_run_block(cls.source, FINAL_GATE_STEP)

    def run_script(
        self, script: str, *, cwd: Path = ROOT, **values: str
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update(values)
        return subprocess.run(
            ["bash", "-euo", "pipefail", "-c", script],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )

    def assert_gate_closes_for_test_failure(self) -> None:
        gate = self.run_script(
            self.gate_script,
            TEST_OUTCOME="failure",
            REPORT_OUTCOME="success",
            ARTIFACT_OUTCOME="success",
        )
        self.assertEqual(gate.returncode, 1, gate.stdout + gate.stderr)
        self.assertIn("Acceptance gate closed", gate.stderr)
        self.assertIn("tests", gate.stderr)

    def test_empty_command_fails_and_final_gate_closes(self) -> None:
        result = self.run_script(self.command_script, ACCEPTANCE_COMMAND="")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("test-command must not be empty.", result.stderr)
        self.assert_gate_closes_for_test_failure()

    def test_whitespace_only_command_fails_and_final_gate_closes(self) -> None:
        result = self.run_script(self.command_script, ACCEPTANCE_COMMAND=" \t \n ")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("test-command must not be empty.", result.stderr)
        self.assert_gate_closes_for_test_failure()

    def test_invalid_command_reports_error_and_final_gate_closes(self) -> None:
        invalid = "__harness_acceptance_command_that_does_not_exist__"
        result = self.run_script(self.command_script, ACCEPTANCE_COMMAND=invalid)
        combined = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, combined)
        self.assertIn(invalid, combined)
        self.assertRegex(combined, r"command not found|not found")
        self.assert_gate_closes_for_test_failure()

    def test_failed_report_identifies_acceptance_stage_without_raw_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory)
            result = self.run_script(
                self.report_script,
                cwd=output_dir,
                CONSUMER_COMMIT_SHA="a" * 40,
                CALLER_WORKFLOW_REF="wosafety0/dev-workflow-kit/.github/workflows/ci.yml@refs/heads/test",
                CALLER_WORKFLOW_SHA="b" * 40,
                TEST_OUTCOME="failure",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report_path = output_dir / "artifacts" / "consumer-acceptance-report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["tests"]["consumer-acceptance-command"], "failed")
            self.assertIn("Acceptance status: failed", result.stdout)
            self.assertNotIn("__harness_acceptance_command_that_does_not_exist__", json.dumps(report))

    def test_valid_command_and_all_successful_stages_open_gate(self) -> None:
        command = self.run_script(
            self.command_script,
            ACCEPTANCE_COMMAND="printf 'acceptance-command-ok\\n'",
        )
        self.assertEqual(command.returncode, 0, command.stdout + command.stderr)
        self.assertIn("acceptance-command-ok", command.stdout)

        gate = self.run_script(
            self.gate_script,
            TEST_OUTCOME="success",
            REPORT_OUTCOME="success",
            ARTIFACT_OUTCOME="success",
        )
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        self.assertIn("Acceptance orchestration gate passed.", gate.stdout)

    def test_logs_have_stable_step_and_failed_stage_identifiers(self) -> None:
        self.assertIn(f"- name: {COMMAND_STEP}", self.source)
        self.assertIn("id: tests", self.source)
        self.assertIn("continue-on-error: true", self.source)
        self.assertIn(f"- name: {REPORT_STEP}", self.source)
        self.assertIn(f"- name: {FINAL_GATE_STEP}", self.source)
        self.assertIn('failed+=("tests")', self.source)
        self.assertIn('print("Acceptance status: " + report["status"])', self.source)


if __name__ == "__main__":
    unittest.main()
