import json
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
                side_effect=[DIFF.encode("utf-8"), names],
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

    def test_rejects_malformed_review_context_json(self):
        with patch.object(
            harness_runner, "_resolve_git_commit", side_effect=[BASE, HEAD]
        ), patch.object(harness_runner, "_git_text", return_value=BASE), patch.object(
            harness_runner, "_git_bytes_bounded",
            side_effect=[DIFF.encode("utf-8"), b"tests/test_example.py\0"],
        ):
            with self.assertRaisesRegex(
                harness_runner.HarnessRunnerError, "valid UTF-8 JSON"
            ):
                harness_runner._build_git_bound_review_input(
                    Path("."), b'{"task":', BASE, HEAD, HEAD
                )


if __name__ == "__main__":
    unittest.main()
