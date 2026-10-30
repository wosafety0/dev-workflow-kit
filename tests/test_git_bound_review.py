import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import harness_runner


BASE = "a" * 40
HEAD = "b" * 40
DIFF = (
    "diff --git a/tests/test_example.py b/tests/test_example.py\n"
    "index 1234567..89abcde 100644\n"
    "--- a/tests/test_example.py\n"
    "+++ b/tests/test_example.py\n"
    "@@ -1 +1,2 @@\n"
    " original\n"
    "+added\n"
)


class GitBoundReviewTests(unittest.TestCase):
    def setUp(self):
        self.source = json.dumps({
            "task": "Review only the source changes",
            "diff": "caller supplied forged diff",
            "changed_files": ["forged.py"],
            "global_rules": "Follow the supplied rules.",
            "project_instructions": "Review the requested task.",
        }).encode("utf-8")

    def mocked_git(self, names=b"tests/test_example.py\0"):
        return (
            patch.object(
                harness_runner, "_resolve_git_commit", side_effect=[BASE, HEAD]
            ),
            patch.object(harness_runner, "_git_text", return_value=BASE),
            patch.object(
                harness_runner, "_git_bytes_bounded",
                side_effect=[b"", DIFF.encode("utf-8"), names],
            ),
        )

    def test_replaces_caller_diff_with_validated_git_diff(self):
        patches = self.mocked_git()
        with patches[0], patches[1], patches[2]:
            task_bytes, provenance = harness_runner._build_git_bound_review_input(
                Path("."), self.source, BASE, HEAD, HEAD
            )

        payload = json.loads(task_bytes.decode("utf-8"))
        self.assertEqual(payload["diff"], DIFF)
        self.assertEqual(payload["changed_files"], ["tests/test_example.py"])
        self.assertNotEqual(payload["diff"], "caller supplied forged diff")
        self.assertEqual(provenance["base_sha"], BASE)
        self.assertEqual(provenance["head_sha"], HEAD)
        self.assertEqual(provenance["merge_base_sha"], BASE)
        self.assertEqual(provenance["changed_files"], ["tests/test_example.py"])
        self.assertEqual(len(provenance["diff_sha256"]), 64)

    def test_rejects_head_that_does_not_match_checked_out_head(self):
        with patch.object(
            harness_runner, "_resolve_git_commit", side_effect=[BASE, HEAD]
        ), patch.object(harness_runner, "_git_text") as git_text:
            with self.assertRaisesRegex(
                harness_runner.HarnessRunnerError, "review-head must equal"
            ):
                harness_runner._build_git_bound_review_input(
                    Path("."), self.source, BASE, HEAD, "c" * 40
                )
        git_text.assert_not_called()

    def test_rejects_git_diff_when_changed_file_list_does_not_match(self):
        patches = self.mocked_git(names=b"other.py\0")
        with patches[0], patches[1], patches[2]:
            with self.assertRaisesRegex(
                harness_runner.HarnessRunnerError,
                "failed semantic-review input validation",
            ):
                harness_runner._build_git_bound_review_input(
                    Path("."), self.source, BASE, HEAD, HEAD
                )

    def test_git_diff_output_is_capped_without_buffering_unbounded_output(self):
        real_popen = subprocess.Popen

        def oversized_process(_argv, **kwargs):
            return real_popen(
                [sys.executable, "-c", "import sys; sys.stdout.write('x' * 1000)"],
                **kwargs,
            )

        with patch.object(harness_runner, "_MAX_REVIEW_INPUT_BYTES", 16), patch.object(
            harness_runner.subprocess, "Popen", side_effect=oversized_process
        ):
            with self.assertRaisesRegex(
                harness_runner.HarnessRunnerError, "exceeds the 4 MiB input limit"
            ):
                harness_runner._git_bytes_bounded(Path("."), [], "test diff")

    def test_git_diff_read_has_a_wall_clock_timeout(self):
        real_popen = subprocess.Popen

        def hanging_process(_argv, **kwargs):
            return real_popen(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                **kwargs,
            )

        with patch.object(harness_runner, "_GIT_COMMAND_TIMEOUT_SECONDS", 0.05), patch.object(
            harness_runner.subprocess, "Popen", side_effect=hanging_process
        ):
            with self.assertRaisesRegex(
                harness_runner.HarnessRunnerError, "Could not verify test diff"
            ):
                harness_runner._git_bytes_bounded(Path("."), [], "test diff")

    def test_git_provenance_ignores_inherited_repository_overrides(self):
        overrides = {
            "GIT_DIR": "/tmp/other-repository",
            "GIT_WORK_TREE": "/tmp/other-worktree",
            "GIT_INDEX_FILE": "/tmp/other-index",
            "GIT_COMMON_DIR": "/tmp/other-common",
            "GIT_OBJECT_DIRECTORY": "/tmp/other-objects",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/tmp/other-alternates",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.worktree",
            "GIT_CONFIG_VALUE_0": "/tmp/other-worktree",
            "GIT_CONFIG_SYSTEM": "/tmp/other-config",
        }
        with patch.dict(harness_runner.os.environ, overrides):
            environment = harness_runner._git_environment()
        for key in overrides:
            self.assertNotIn(key, environment)
        self.assertEqual(environment["GIT_NO_REPLACE_OBJECTS"], "1")
        self.assertEqual(environment["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertEqual(environment["GIT_CONFIG_GLOBAL"], harness_runner.os.devnull)

    def test_git_replace_refs_cannot_change_reviewed_commit_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=root, check=True, capture_output=True, text=True
                )

            git("init", "-q")
            git("config", "user.name", "Harness Test")
            git("config", "user.email", "harness-test@example.invalid")
            source = root / "source.py"
            source.write_text("VALUE = 'old'" + chr(10), encoding="utf-8")
            git("add", "source.py")
            git("commit", "-qm", "base")
            base_sha = git("rev-parse", "HEAD").stdout.strip()

            source.write_text("VALUE = 'new'" + chr(10), encoding="utf-8")
            git("add", "source.py")
            git("commit", "-qm", "actual head")
            head_sha = git("rev-parse", "HEAD").stdout.strip()

            git("checkout", "--detach", base_sha)
            source.write_text("VALUE = 'forged replacement'" + chr(10), encoding="utf-8")
            git("add", "source.py")
            git("commit", "-qm", "replacement tree")
            replacement_sha = git("rev-parse", "HEAD").stdout.strip()

            git("checkout", "--detach", head_sha)
            git("replace", head_sha, replacement_sha)

            task_bytes, provenance = harness_runner._build_git_bound_review_input(
                root, self.source, base_sha, head_sha, head_sha
            )
            payload = json.loads(task_bytes.decode("utf-8"))
            self.assertIn("+VALUE = 'new'", payload["diff"])
            self.assertNotIn("forged replacement", payload["diff"])
            self.assertEqual(provenance["head_sha"], head_sha)
            self.assertEqual(provenance["changed_files"], ["source.py"])

    def test_local_binary_diff_driver_cannot_hide_text_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=root, check=True, capture_output=True, text=True
                )

            git("init", "-q")
            git("config", "user.name", "Harness Test")
            git("config", "user.email", "harness-test@example.invalid")
            git("config", "diff.review.binary", "true")
            (root / ".gitattributes").write_text("source.py diff=review\\n", encoding="utf-8")
            source = root / "source.py"
            source.write_text("VALUE = 'old'\\n", encoding="utf-8")
            git("add", ".gitattributes", "source.py")
            git("commit", "-qm", "base")
            base_sha = git("rev-parse", "HEAD").stdout.strip()

            source.write_text("VALUE = 'new'\\n", encoding="utf-8")
            git("add", "source.py")
            git("commit", "-qm", "head")
            head_sha = git("rev-parse", "HEAD").stdout.strip()

            task_bytes, provenance = harness_runner._build_git_bound_review_input(
                root, self.source, base_sha, head_sha, head_sha
            )
            payload = json.loads(task_bytes.decode("utf-8"))
            self.assertIn("+VALUE = 'new'", payload["diff"])
            self.assertEqual(provenance["changed_files"], ["source.py"])


    def test_local_config_cannot_hide_changed_submodule_from_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            child = root / "child"
            child.mkdir()

            def git(cwd, *args):
                return subprocess.run(
                    ["git", *args], cwd=cwd, check=True,
                    capture_output=True, text=True,
                )

            git(child, "init", "-q")
            git(child, "config", "user.name", "Harness Test")
            git(child, "config", "user.email", "harness-test@example.invalid")
            (child / "module.py").write_text("VALUE = 1\\n", encoding="utf-8")
            git(child, "add", "module.py")
            git(child, "commit", "-qm", "submodule base")

            git(root, "init", "-q")
            git(root, "config", "user.name", "Harness Test")
            git(root, "config", "user.email", "harness-test@example.invalid")
            git(root, "-c", "protocol.file.allow=always", "submodule", "add", "-q",
                str(child), "deps/sub")
            git(root, "commit", "-qam", "superproject base")
            base_sha = git(root, "rev-parse", "HEAD").stdout.strip()

            git(root / "deps/sub", "config", "user.name", "Harness Test")
            git(root / "deps/sub", "config", "user.email", "harness-test@example.invalid")
            (root / "deps/sub/module.py").write_text("VALUE = 2\\n", encoding="utf-8")
            git(root / "deps/sub", "add", "module.py")
            git(root / "deps/sub", "commit", "-qm", "submodule head")
            git(root, "add", "deps/sub")
            git(root, "commit", "-qm", "superproject head")
            head_sha = git(root, "rev-parse", "HEAD").stdout.strip()

            # Both repository-local settings would otherwise hide the gitlink change.
            git(root, "config", "diff.ignoreSubmodules", "all")
            git(root, "config", "submodule.deps/sub.ignore", "all")
            with self.assertRaisesRegex(
                harness_runner.HarnessRunnerError,
                "does not support submodule pointer changes",
            ):
                harness_runner._build_git_bound_review_input(
                    root, self.source, base_sha, head_sha, head_sha
                )


    def test_rejects_malformed_review_context_json(self):
        with patch.object(
            harness_runner, "_resolve_git_commit", side_effect=[BASE, HEAD]
        ), patch.object(harness_runner, "_git_text", return_value=BASE), patch.object(
            harness_runner, "_git_bytes_bounded",
            side_effect=[b"", DIFF.encode("utf-8"), b"tests/test_example.py\0"],
        ):
            with self.assertRaisesRegex(
                harness_runner.HarnessRunnerError, "valid UTF-8 JSON"
            ):
                harness_runner._build_git_bound_review_input(
                    Path("."), b'{"task":', BASE, HEAD, HEAD
                )


if __name__ == "__main__":
    unittest.main()
