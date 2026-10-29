import json
import subprocess
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
    def test_review_output_cannot_overwrite_config_inside_artifacts(self):
        self.config_path = self.root / "artifacts" / "harness.json"
        self.write_config(["semantic-review"])
        original_config = self.config_path.read_bytes()
        (self.root / "review-input.json").write_text("{}", encoding="utf-8")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner(
                "--config", "artifacts/harness.json",
                "--review-input", "review-input.json",
                "--review-output", "artifacts/harness.json",
            )
        self.assertEqual(code, 2)
        self.assertIn("review-output must not overwrite config", stderr)
        run_task.assert_not_called()
        self.assertEqual(self.config_path.read_bytes(), original_config)

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


    def initialize_git_worktree(self):
        """Commit fixture sources so provenance checks use a real Git worktree."""
        commands = [
            ["git", "init", "-q"],
            ["git", "add", "."],
            ["git", "-c", "user.name=Harness Test",
             "-c", "user.email=harness-test@example.invalid",
             "commit", "-qm", "fixture"],
        ]
        for command in commands:
            subprocess.run(command, cwd=self.root, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    def test_runner_rejects_modified_tracked_code_before_execution(self):
        self.initialize_git_worktree()
        test_file = self.root / "tests" / "test_example.py"
        test_file.write_text(test_file.read_text(encoding="utf-8") + "# modified\n",
                             encoding="utf-8")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("clean", stderr)
        run_task.assert_not_called()
        self.assertFalse((self.root / "artifacts" / "report.json").exists())

    def test_runner_rejects_untracked_source_but_allows_artifact_files(self):
        self.initialize_git_worktree()
        (self.root / "artifacts" / "old-output.json").write_text("{}",
                                                                  encoding="utf-8")
        with patch("scripts.harness_runner._run_task", return_value=("passed", 0)):
            code, _, stderr = self.run_runner()
        self.assertEqual((code, stderr), (0, ""))
        (self.root / "scripts" / "new_untracked.py").write_text("# untracked\n",
                                                                 encoding="utf-8")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("clean", stderr)
        run_task.assert_not_called()
        self.assertFalse((self.root / "artifacts" / "report.json").exists())

    def test_runner_rejects_task_that_mutates_tracked_code(self):
        self.initialize_git_worktree()
        test_file = self.root / "tests" / "test_example.py"

        def mutate_source(*_args):
            test_file.write_text(test_file.read_text(encoding="utf-8") + "# mutated\n",
                                 encoding="utf-8")
            return "passed", 0

        with patch("scripts.harness_runner._run_task", side_effect=mutate_source):
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("clean", stderr)
        self.assertFalse((self.root / "artifacts" / "report.json").exists())

    def test_commit_provenance_rejects_nested_project_root(self):
        self.initialize_git_worktree()
        with self.assertRaisesRegex(harness_runner.HarnessRunnerError, "repository root"):
            harness_runner._git_commit_sha(self.root / "scripts")



    def test_rejects_duplicate_json_config_keys_before_task_execution(self):
        duplicate_configs = (
            '{"schema_version":1,"schema_version":1,"project":"test-project","commands":["python-unittest"]}',
            '{"schema_version":1,"project":"test-project","commands":["semantic-review"],"commands":["python-unittest"]}',
            '{"schema_version":1,"project":"test-project","commands":["python-unittest"],"metadata":{"mode":"safe","mode":"unsafe"}}',
        )
        for raw in duplicate_configs:
            with self.subTest(raw=raw):
                self.config_path.write_text(raw, encoding="utf-8")
                with patch("scripts.harness_runner._run_task") as run_task:
                    code, _, stderr = self.run_runner()
                self.assertEqual(code, 2)
                self.assertIn("Could not read a valid JSON Harness config", stderr)
                run_task.assert_not_called()


    def test_runner_rejects_tests_directory_symlink_outside_root(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        (Path(outside.name) / "test_external.py").write_text(
            "def test_external(): pass\\n", encoding="utf-8"
        )
        tests_dir = self.root / "tests"
        saved_tests = self.root / "tests-saved"
        tests_dir.rename(saved_tests)
        try:
            tests_dir.symlink_to(Path(outside.name), target_is_directory=True)
        except (OSError, NotImplementedError):
            saved_tests.rename(tests_dir)
            self.skipTest("directory symlink creation is unavailable")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("tests directory resolves outside", stderr)
        run_task.assert_not_called()

    def test_runner_rejects_semantic_review_script_symlink_outside_root(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        external_script = Path(outside.name) / "ai_semantic_review.py"
        external_script.write_text("# external script\\n", encoding="utf-8")
        script = self.root / "scripts" / "ai_semantic_review.py"
        script.unlink()
        try:
            script.symlink_to(external_script)
        except (OSError, NotImplementedError):
            script.write_text("# test fixture\\n", encoding="utf-8")
            self.skipTest("file symlink creation is unavailable")
        self.write_config(["semantic-review"])
        (self.root / "review-input.json").write_text("{}", encoding="utf-8")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner(
                "--review-input", "review-input.json",
                "--review-output", "artifacts/review.json",
            )
        self.assertEqual(code, 2)
        self.assertIn("semantic-review script resolves outside", stderr)
        run_task.assert_not_called()

    def test_rules_pin_rejects_contract_symlink_outside_root(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        external_contract = Path(outside.name) / "STABLE_ACCEPTANCE_CONTRACT.md"
        external_contract.write_text("external mutable rules", encoding="utf-8")
        contract = self.root / "docs" / "STABLE_ACCEPTANCE_CONTRACT.md"
        contract.unlink()
        try:
            contract.symlink_to(external_contract)
        except (OSError, NotImplementedError):
            contract.write_text("contract", encoding="utf-8")
            self.skipTest("file symlink creation is unavailable")
        with self.assertRaisesRegex(
            harness_runner.HarnessRunnerError,
            "stable acceptance contract resolves outside",
        ):
            harness_runner._rules_pin(self.root)


    def test_trusted_source_resolver_rejects_generated_artifact_paths(self):
        with self.assertRaisesRegex(
            harness_runner.HarnessRunnerError,
            "source path must not resolve inside artifacts/",
        ):
            harness_runner._resolve_trusted_source(
                self.root, "artifacts/generated-source.py", "source path"
            )


    def test_trusted_source_resolver_rejects_in_root_symlink_to_ignored_directory(self):
        ignored = self.root / ".venv"
        ignored.mkdir()
        target = ignored / "mutable-source.py"
        target.write_text("# mutable ignored source\\n", encoding="utf-8")
        source = self.root / "scripts" / "ai_semantic_review.py"
        source.unlink()
        try:
            source.symlink_to(target)
        except (OSError, NotImplementedError):
            source.write_text("# test fixture\\n", encoding="utf-8")
            self.skipTest("file symlink creation is unavailable")
        with self.assertRaisesRegex(
            harness_runner.HarnessRunnerError,
            "semantic-review script must not use symlinked source paths",
        ):
            harness_runner._resolve_trusted_source(
                self.root, "scripts/ai_semantic_review.py", "semantic-review script"
            )

    def test_trusted_source_resolver_rejects_nested_symlink_in_tests_directory(self):
        ignored = self.root / ".venv"
        ignored.mkdir()
        target = ignored / "mutable_test.py"
        target.write_text("import unittest\\n", encoding="utf-8")
        source = self.root / "tests" / "test_mutable.py"
        try:
            source.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("file symlink creation is unavailable")
        with self.assertRaisesRegex(
            harness_runner.HarnessRunnerError,
            "tests directory must not contain symlinked source paths",
        ):
            harness_runner._resolve_trusted_source(self.root, "tests", "tests directory")


    def test_runner_rejects_config_symlink_into_ignored_directory(self):
        ignored = self.root / ".venv"
        ignored.mkdir()
        target = ignored / "mutable-config.json"
        target.write_text(self.config_path.read_text(encoding="utf-8"), encoding="utf-8")
        self.config_path.unlink()
        try:
            self.config_path.symlink_to(target)
        except (OSError, NotImplementedError):
            self.config_path.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
            self.skipTest("file symlink creation is unavailable")
        with patch("scripts.harness_runner._run_task") as run_task:
            code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("config must not use symlinked paths", stderr)
        run_task.assert_not_called()

    def test_runner_rejects_report_output_symlink_before_deleting_target(self):
        target = self.root / "artifacts" / "preserve.json"
        target.write_text('{"keep": true}', encoding="utf-8")
        report = self.root / "artifacts" / "report.json"
        try:
            report.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("file symlink creation is unavailable")
        code, _, stderr = self.run_runner()
        self.assertEqual(code, 2)
        self.assertIn("report-output must not use symlinked paths", stderr)
        self.assertEqual(target.read_text(encoding="utf-8"), '{"keep": true}')
        self.assertTrue(report.is_symlink())


if __name__ == "__main__":
    unittest.main()
