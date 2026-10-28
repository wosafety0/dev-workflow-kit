import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts import harness_runner


class HarnessRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "docs").mkdir()
        (self.root / "scripts").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "artifacts").mkdir()
        (self.root / "docs" / "STABLE_ACCEPTANCE_CONTRACT.md").write_text(
            "contract", encoding="utf-8"
        )
        (self.root / "scripts" / "ai_semantic_review.py").write_text(
            "# test fixture\n", encoding="utf-8"
        )
        (self.root / "tests" / "test_example.py").write_text(
            "import unittest\nclass Example(unittest.TestCase):\n"
            "    def test_ok(self): self.assertTrue(True)\n",
            encoding="utf-8",
        )
        self.config_path = self.root / "harness.json"
        self.write_config(["python-unittest"])

    def write_config(self, commands):
        self.config_path.write_text(
            json.dumps({
                "schema_version": 1,
                "project": "test-project",
                "commands": commands,
            }),
            encoding="utf-8",
        )

    def run_runner(self, *extra):
        args = [
            "--project-root", str(self.root),
            "--config", "harness.json",
            "--report-output", "artifacts/report.json",
            "--timeout-seconds", "10",
            *extra,
        ]
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = harness_runner.main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_python_unittest_maps_to_fixed_argv_and_writes_allowlisted_report(self):
        with patch("scripts.harness_runner._git_commit_sha", return_value="a" * 40), patch(
            "scripts.harness_runner._rules_pin", return_value="sha256:contract"
        ), patch(
            "scripts.harness_runner._run_task", return_value=("passed", 0)
        ) as run_task:
            code, stdout, stderr = self.run_runner()

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Task python-unittest: passed", stdout)
        argv = run_task.call_args.args[0]
        self.assertEqual(
            argv,
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        )
        report = json.loads((self.root / "artifacts" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["tests"], {"python-unittest": "passed"})
        self.assertEqual(
            set(report),
            {"schema_version", "commit_sha", "rules_pin", "tool_version", "tests", "status"},
        )

    def test_runner_executes_fixed_task_end_to_end(self):
        with patch("scripts.harness_runner._git_commit_sha", return_value="c" * 40), patch(
            "scripts.harness_runner._rules_pin", return_value="sha256:contract"
        ):
            code, stdout, stderr = self.run_runner()

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Task python-unittest: passed", stdout)
        report = json.loads((self.root / "artifacts" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["tests"], {"python-unittest": "passed"})

    def test_task_failure_writes_failed_report_and_returns_one(self):
        with patch("scripts.harness_runner._git_commit_sha", return_value="b" * 40), patch(
            "scripts.harness_runner._rules_pin", return_value="sha256:contract"
        ), patch(
            "scripts.harness_runner._run_task", return_value=("failed", 23)
        ):
            code, stdout, stderr = self.run_runner()

        self.assertEqual(code, 1)
        self.assertEqual(stderr, "")
        self.assertIn("Task python-unittest: failed (exit 23)", stdout)
        report = json.loads((self.root / "artifacts" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["tests"], {"python-unittest": "failed"})

    def test_runs_configured_tasks_in_order_with_explicit_review_paths(self):
        self.write_config(["python-unittest", "semantic-review"])
        (self.root / "review-input.json").write_text("{}", encoding="utf-8")
        with patch("scripts.harness_runner._git_commit_sha", return_value="d" * 40), patch(
            "scripts.harness_runner._rules_pin", return_value="sha256:contract"
        ), patch(
            "scripts.harness_runner._run_task",
            side_effect=[("passed", 0), ("passed", 0)],
        ) as run_task:
            code, stdout, stderr = self.run_runner(
                "--review-input", "review-input.json",
                "--review-output", "artifacts/review.json",
            )

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Task python-unittest: passed", stdout)
        self.assertIn("Task semantic-review: passed", stdout)
        calls = [call.args[0] for call in run_task.call_args_list]
        self.assertEqual(calls[0], [
            sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"
        ])
        self.assertEqual(calls[1], [
            sys.executable,
            str(self.root / "scripts" / "ai_semantic_review.py"),
            "--input", str(self.root / "review-input.json"),
            "--output", str(self.root / "artifacts" / "review.json"),
        ])
        report = json.loads((self.root / "artifacts" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "passed")
        self.assertEqual(
            report["tests"],
            {"python-unittest": "passed", "semantic-review": "passed"},
        )

    def test_rejects_output_outside_artifacts_before_running_tasks(self):
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner("--report-output", "scripts/ai_semantic_review.py")
        self.assertEqual(code, 2)
        self.assertIn("inside the artifacts/", stderr)
        run_task.assert_not_called()

    def test_semantic_review_requires_explicit_input_and_output_before_any_task_runs(self):
        self.write_config(["python-unittest", "semantic-review"])
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("semantic-review requires both", stderr)
        run_task.assert_not_called()

    def test_semantic_review_output_must_not_overwrite_source_files(self):
        self.write_config(["semantic-review"])
        (self.root / "review-input.json").write_text("{}", encoding="utf-8")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner(
                "--review-input", "review-input.json",
                "--review-output", "scripts/ai_semantic_review.py",
            )
        self.assertEqual(code, 2)
        self.assertIn("review-output must be inside the artifacts/", stderr)
        run_task.assert_not_called()

    def test_rejects_path_traversal_before_running_tasks(self):
        with patch("scripts.harness_runner._run_task") as run_task:
            stdout = StringIO()
            stderr = StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = harness_runner.main([
                    "--project-root", str(self.root),
                    "--config", "../outside.json",
                    "--report-output", "artifacts/report.json",
                ])
        self.assertEqual(code, 2)
        self.assertIn("safe repository-relative path", stderr.getvalue())
        run_task.assert_not_called()

    def test_invalid_config_fails_closed_without_running_tasks(self):
        self.write_config(["python -c 'print(1)'"])
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("unknown command ID", stderr)
        run_task.assert_not_called()

    def test_invalid_config_removes_stale_passing_report(self):
        report_path = self.root / "artifacts" / "report.json"
        report_path.write_text('{"status": "passed"}', encoding="utf-8")
        self.write_config(["unreviewed-command"])
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("unknown command ID", stderr)
        self.assertFalse(report_path.exists())
        run_task.assert_not_called()

    def test_missing_review_input_removes_stale_review_and_report(self):
        self.write_config(["semantic-review"])
        report_path = self.root / "artifacts" / "report.json"
        review_path = self.root / "artifacts" / "review.json"
        report_path.write_text('{"status": "passed"}', encoding="utf-8")
        review_path.write_text('{"status": "PASS"}', encoding="utf-8")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner(
                "--review-input", "missing-review-input.json",
                "--review-output", "artifacts/review.json",
            )
        self.assertEqual(code, 2)
        self.assertIn("review-input must identify an existing file", stderr)
        self.assertFalse(report_path.exists())
        self.assertFalse(review_path.exists())
        run_task.assert_not_called()

    def test_timeout_is_a_failed_task_without_echoing_process_output(self):
        with patch(
            "scripts.harness_runner.subprocess.run",
            side_effect=harness_runner.subprocess.TimeoutExpired(["test"], 1),
        ):
            status, exit_code = harness_runner._run_task(
                [sys.executable, "-c", "pass"], self.root, 1
            )
        self.assertEqual((status, exit_code), ("failed", None))


if __name__ == "__main__":
    unittest.main()
