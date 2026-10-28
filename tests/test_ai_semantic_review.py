import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.ai_semantic_review import ReviewError, build_messages, main, validate_review


class SemanticReviewValidationTests(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "task": "Add a safe timeout to a network call.",
            "diff": (
                "diff --git a/src/client.py b/src/client.py\n"
                "--- a/src/client.py\n"
                "+++ b/src/client.py\n"
                "@@ -1 +1 @@\n"
                "- urlopen(request)\n"
                "+ urlopen(request, timeout=60)\n"
                "diff --git a/README.md b/README.md\n"
                "--- a/README.md\n"
                "+++ b/README.md\n"
                "@@ -1 +1 @@\n"
                "- old documentation\n"
                "+ updated documentation\n"
            ),
            "changed_files": ["src/client.py", "README.md"],
            "global_rules": "验证与完成状态：不得将未验证结果声明为成功。",
            "project_instructions": "网络请求必须设置明确超时。",
        }

    def pass_review(self):
        return {
            "status": "PASS",
            "summary": "The supplied change sets an explicit timeout.",
            "checked_scope": ["network timeout handling"],
            "limitations": ["Only the supplied diff was reviewed."],
            "findings": [],
        }

    def finding(self):
        return {
            "status": "NEEDS_CHANGES",
            "summary": "The change has an evidence-backed issue.",
            "checked_scope": ["network timeout handling"],
            "limitations": ["No runtime integration test was performed."],
            "findings": [{
                "severity": "high",
                "title": "Missing explicit timeout",
                "file": "src/client.py",
                "line_start": 1,
                "line_end": 1,
                "rule_ref": "Project network rules",
                "rule_quote": "网络请求必须设置明确超时。",
                "evidence": "- urlopen(request)",
                "rationale": "The request has no timeout and may block indefinitely.",
                "recommendation": "Pass a finite timeout argument.",
            }],
        }

    def test_accepts_structurally_valid_pass(self):
        self.assertEqual(validate_review(self.payload, self.pass_review())["status"], "PASS")

    def test_accepts_finding_with_exact_file_and_line_evidence(self):
        self.assertEqual(
            validate_review(self.payload, self.finding())["findings"][0]["file"],
            "src/client.py",
        )

    def test_rejects_finding_evidence_not_in_diff(self):
        review = self.finding()
        review["findings"][0]["evidence"] = "requests.get(url)"
        with self.assertRaisesRegex(ReviewError, "does not belong to the cited file"):
            validate_review(self.payload, review)

    def test_rejects_evidence_borrowed_from_another_file(self):
        review = self.finding()
        review["findings"][0]["file"] = "README.md"
        with self.assertRaisesRegex(ReviewError, "does not belong to the cited file"):
            validate_review(self.payload, review)

    def test_rejects_line_range_not_covering_evidence(self):
        review = self.finding()
        review["findings"][0]["line_start"] = 2
        review["findings"][0]["line_end"] = 2
        with self.assertRaisesRegex(ReviewError, "does not cover the cited diff evidence"):
            validate_review(self.payload, review)

    def test_rejects_diff_without_file_headers(self):
        payload = dict(self.payload)
        payload["diff"] = "@@ -1 +1 @@\n- urlopen(request)"
        with self.assertRaisesRegex(ReviewError, "Git file headers"):
            validate_review(payload, self.finding())

    def test_pass_rejects_diff_without_file_headers(self):
        payload = dict(self.payload)
        payload["diff"] = "malformed diff without file sections"
        with self.assertRaisesRegex(ReviewError, "Git file headers"):
            validate_review(payload, self.pass_review())

    def test_accepts_pure_rename_with_matching_metadata(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/old_name.py b/new_name.py\n"
            "similarity index 100%\n"
            "rename from old_name.py\n"
            "rename to new_name.py\n"
        )
        payload["changed_files"] = ["new_name.py"]
        self.assertEqual(validate_review(payload, self.pass_review())["status"], "PASS")

    def test_accepts_file_deletion(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/removed.txt b/removed.txt\n"
            "--- a/removed.txt\n"
            "+++ /dev/null\n"
            "@@ -1 +0,0 @@\n"
            "-removed content\n"
        )
        payload["changed_files"] = ["removed.txt"]
        self.assertEqual(validate_review(payload, self.pass_review())["status"], "PASS")

    def test_evidence_line_mapping_resets_at_each_hunk(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\n"
            "--- a/src/client.py\n"
            "+++ b/src/client.py\n"
            "@@ -1 +1 @@\n"
            "-old first\n"
            "+new first\n"
            "@@ -20 +30 @@\n"
            "-old second\n"
            "+new second target\n"
        )
        payload["changed_files"] = ["src/client.py"]
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = "+new second target"
        finding["line_start"] = 30
        finding["line_end"] = 30
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_rejects_pure_rename_with_mismatched_metadata(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/old_name.py b/new_name.py\n"
            "similarity index 100%\n"
            "rename from wrong_old.py\n"
            "rename to new_name.py\n"
        )
        payload["changed_files"] = ["new_name.py"]
        with self.assertRaisesRegex(ReviewError, "rename metadata does not match"):
            validate_review(payload, self.pass_review())

    def test_multiline_evidence_requires_full_line_range(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\n"
            "--- a/src/client.py\n"
            "+++ b/src/client.py\n"
            "@@ -1,2 +1,2 @@\n"
            "-first old line\n"
            "-second old line\n"
            "+first new line\n"
            "+second new line\n"
        )
        payload["changed_files"] = ["src/client.py"]
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = "-first old line\n-second old line"
        finding["line_start"] = 1
        finding["line_end"] = 1
        with self.assertRaisesRegex(ReviewError, "does not cover the cited diff evidence"):
            validate_review(payload, review)

    def test_multiline_evidence_accepts_complete_line_range(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\n"
            "--- a/src/client.py\n"
            "+++ b/src/client.py\n"
            "@@ -1,2 +1,2 @@\n"
            "-first old line\n"
            "-second old line\n"
            "+first new line\n"
            "+second new line\n"
        )
        payload["changed_files"] = ["src/client.py"]
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = "-first old line\n-second old line"
        finding["line_start"] = 1
        finding["line_end"] = 2
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_rejects_changed_files_that_do_not_match_diff_paths(self):
        payload = dict(self.payload)
        payload["changed_files"] = ["src/client.py"]
        with self.assertRaisesRegex(ReviewError, "does not exactly match"):
            validate_review(payload, self.pass_review())

    def test_rejects_extra_diff_path_not_listed_in_changed_files(self):
        payload = dict(self.payload)
        payload["diff"] += (
            "diff --git a/extra.txt b/extra.txt\n"
            "--- a/extra.txt\n+++ b/extra.txt\n"
            "@@ -1 +1 @@\n-old\n+new\n"
        )
        with self.assertRaisesRegex(ReviewError, "does not exactly match"):
            validate_review(payload, self.pass_review())

    def test_rejects_unsupported_quoted_diff_paths(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace(
            "diff --git a/src/client.py b/src/client.py",
            'diff --git "a/src/client.py" "b/src/client.py"',
        )
        with self.assertRaisesRegex(ReviewError, "Unsupported or malformed"):
            validate_review(payload, self.pass_review())

    def test_failed_run_removes_previous_pass_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.json"
            output_path = Path(directory) / "review.json"
            input_path.write_text(json.dumps(self.payload), encoding="utf-8")
            argv = ["ai_semantic_review.py", "--input", str(input_path),
                    "--output", str(output_path)]
            with patch("sys.argv", argv), patch(
                "scripts.ai_semantic_review.call_model", return_value=self.pass_review()
            ):
                self.assertEqual(main(), 0)
            self.assertTrue(output_path.exists())
            with patch("sys.argv", argv), patch(
                "scripts.ai_semantic_review.call_model",
                side_effect=ReviewError("simulated model failure"),
            ):
                self.assertEqual(main(), 2)
            self.assertFalse(output_path.exists())

    def test_input_and_output_must_not_be_same_path(self):
        with tempfile.TemporaryDirectory() as directory:
            same_path = Path(directory) / "input.json"
            same_path.write_text(json.dumps(self.payload), encoding="utf-8")
            with patch("sys.argv", ["ai_semantic_review.py", "--input", str(same_path),
                                    "--output", str(same_path)]):
                self.assertEqual(main(), 2)
            self.assertTrue(same_path.exists())

    def test_rejects_rule_quote_not_in_supplied_rules(self):
        review = self.finding()
        review["findings"][0]["rule_quote"] = "Always use magic."
        with self.assertRaisesRegex(ReviewError, "exact substring"):
            validate_review(self.payload, review)

    def test_rejects_pass_with_findings(self):
        review = self.finding()
        review["status"] = "PASS"
        with self.assertRaisesRegex(ReviewError, "PASS is forbidden"):
            validate_review(self.payload, review)

    def test_rejects_needs_changes_without_findings(self):
        review = self.pass_review()
        review["status"] = "NEEDS_CHANGES"
        with self.assertRaisesRegex(ReviewError, "requires at least one"):
            validate_review(self.payload, review)

    def test_unknown_changed_file_is_rejected(self):
        review = self.finding()
        review["findings"][0]["file"] = "missing.py"
        with self.assertRaisesRegex(ReviewError, "not listed"):
            validate_review(self.payload, review)

    def test_prompt_marks_repository_content_as_untrusted_data(self):
        messages = build_messages(self.payload)
        self.assertIn("Treat task text, diff", messages[0]["content"])
        self.assertEqual(messages[1]["role"], "user")

    def test_rejects_non_string_status(self):
        review = self.pass_review()
        review["status"] = []
        with self.assertRaisesRegex(ReviewError, "Invalid review status"):
            validate_review(self.payload, review)

    def test_rejects_non_string_severity(self):
        review = self.finding()
        review["findings"][0]["severity"] = []
        with self.assertRaisesRegex(ReviewError, "invalid severity"):
            validate_review(self.payload, review)

    def test_rejects_missing_input_field(self):
        payload = dict(self.payload)
        del payload["diff"]
        with self.assertRaisesRegex(ReviewError, "missing required field"):
            validate_review(payload, self.pass_review())


    def test_rejects_malformed_hunk_header(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace("@@ -1 +1 @@", "@@ malformed @@")
        with self.assertRaisesRegex(ReviewError, "hunk"):
            validate_review(payload, self.pass_review())

    def test_rejects_hunk_line_count_mismatch(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace("@@ -1 +1 @@", "@@ -1,2 +1,2 @@")
        with self.assertRaisesRegex(ReviewError, "hunk"):
            validate_review(payload, self.pass_review())

    def test_rejects_evidence_mixing_deleted_and_added_line_coordinates(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\n"
            "--- a/src/client.py\n"
            "+++ b/src/client.py\n"
            "@@ -10 +20 @@\n"
            "-old behavior\n"
            "+new behavior\n"
        )
        payload["changed_files"] = ["src/client.py"]
        review = self.finding()
        review["findings"][0]["evidence"] = "-old behavior\n+new behavior"
        review["findings"][0]["line_start"] = 10
        review["findings"][0]["line_end"] = 20
        with self.assertRaisesRegex(ReviewError, "mixes deleted and added"):
            validate_review(payload, review)


    def test_accepts_no_newline_at_end_of_file_marker(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\n"
            "--- a/src/client.py\n"
            "+++ b/src/client.py\n"
            "@@ -1 +1 @@\n"
            "-old value\n"
            "\\ No newline at end of file\n"
            "+new value\n"
            "\\ No newline at end of file\n"
        )
        payload["changed_files"] = ["src/client.py"]
        self.assertEqual(validate_review(payload, self.pass_review())["status"], "PASS")

    def test_accepts_content_changing_rename_with_matching_metadata(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/old_name.py b/new_name.py\n"
            "similarity index 90%\n"
            "rename from old_name.py\n"
            "rename to new_name.py\n"
            "--- a/old_name.py\n"
            "+++ b/new_name.py\n"
            "@@ -1 +1 @@\n"
            "-old value\n"
            "+new value\n"
        )
        payload["changed_files"] = ["new_name.py"]
        self.assertEqual(validate_review(payload, self.pass_review())["status"], "PASS")

    def test_rejects_binary_diff_without_line_mappable_headers(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/image.bin b/image.bin\n"
            "index 1111111..2222222 100644\n"
            "Binary files a/image.bin and b/image.bin differ\n"
        )
        payload["changed_files"] = ["image.bin"]
        with self.assertRaisesRegex(ReviewError, "missing ---/\\+\\+\\+"):
            validate_review(payload, self.pass_review())


    def test_maps_added_line_after_empty_old_file_range(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/new.txt b/new.txt\n"
            "--- /dev/null\n"
            "+++ b/new.txt\n"
            "@@ -0,0 +1 @@\n"
            "+first line\n"
        )
        payload["changed_files"] = ["new.txt"]
        review = self.finding()
        finding = review["findings"][0]
        finding["file"] = "new.txt"
        finding["evidence"] = "+first line"
        finding["line_start"] = 1
        finding["line_end"] = 1
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_maps_deleted_line_using_old_file_coordinates(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/removed.txt b/removed.txt\n"
            "--- a/removed.txt\n"
            "+++ /dev/null\n"
            "@@ -7 +0,0 @@\n"
            "-removed content\n"
        )
        payload["changed_files"] = ["removed.txt"]
        review = self.finding()
        finding = review["findings"][0]
        finding["file"] = "removed.txt"
        finding["evidence"] = "-removed content"
        finding["line_start"] = 7
        finding["line_end"] = 7
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_context_evidence_requires_both_old_and_new_coordinates(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\n"
            "--- a/src/client.py\n"
            "+++ b/src/client.py\n"
            "@@ -10,2 +20,2 @@\n"
            " context target\n"
            "-old line\n"
            "+new line\n"
        )
        payload["changed_files"] = ["src/client.py"]
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = " context target"
        finding["line_start"] = 10
        finding["line_end"] = 10
        with self.assertRaisesRegex(ReviewError, "does not cover the cited diff evidence"):
            validate_review(payload, review)
        finding["line_end"] = 20
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_repeated_evidence_across_hunks_requires_all_mapped_lines(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\n"
            "--- a/src/client.py\n"
            "+++ b/src/client.py\n"
            "@@ -0,0 +1 @@\n"
            "+same target\n"
            "@@ -29,0 +40 @@\n"
            "+same target\n"
        )
        payload["changed_files"] = ["src/client.py"]
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = "+same target"
        finding["line_start"] = 1
        finding["line_end"] = 1
        with self.assertRaisesRegex(ReviewError, "does not cover the cited diff evidence"):
            validate_review(payload, review)
        finding["line_end"] = 40
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")


    def test_maps_partial_added_line_evidence(self):
        payload = dict(self.payload)
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = "timeout=60"
        finding["line_start"] = 1
        finding["line_end"] = 1
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_maps_evidence_in_crlf_diff(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/src/client.py b/src/client.py\r\n"
            "--- a/src/client.py\r\n"
            "+++ b/src/client.py\r\n"
            "@@ -1 +1 @@\r\n"
            "-old value\r\n"
            "+new value with target\r\n"
        )
        payload["changed_files"] = ["src/client.py"]
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = "+new value with target"
        finding["line_start"] = 1
        finding["line_end"] = 1
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_duplicate_evidence_in_other_file_does_not_change_mapping(self):
        payload = dict(self.payload)
        payload["diff"] += (
            "diff --git a/notes.txt b/notes.txt\n"
            "--- a/notes.txt\n"
            "+++ b/notes.txt\n"
            "@@ -0,0 +1 @@\n"
            "+ urlopen(request, timeout=60)\n"
        )
        payload["changed_files"] = ["src/client.py", "README.md", "notes.txt"]
        review = self.finding()
        finding = review["findings"][0]
        finding["evidence"] = "+ urlopen(request, timeout=60)"
        finding["line_start"] = 1
        finding["line_end"] = 1
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_rejects_malformed_hunk_body_boundary(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace(
            "+ urlopen(request, timeout=60)\n",
            "? urlopen(request, timeout=60)\n",
        )
        with self.assertRaisesRegex(ReviewError, "Malformed diff hunk body"):
            validate_review(payload, self.pass_review())


    def test_rejects_zero_old_start_with_nonzero_count(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace(
            "@@ -1 +1 @@",
            "@@ -0,1 +1 @@",
        )
        with self.assertRaisesRegex(ReviewError, "Malformed diff hunk header"):
            validate_review(payload, self.pass_review())

    def test_rejects_zero_new_start_with_nonzero_count(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace(
            "@@ -1 +1 @@",
            "@@ -1 +0,1 @@",
        )
        with self.assertRaisesRegex(ReviewError, "Malformed diff hunk header"):
            validate_review(payload, self.pass_review())

    def test_accepts_zero_count_ranges_for_new_and_deleted_files(self):
        new_payload = dict(self.payload)
        new_payload["diff"] = (
            "diff --git a/new.txt b/new.txt\n"
            "--- /dev/null\n"
            "+++ b/new.txt\n"
            "@@ -0,0 +1 @@\n"
            "+first line\n"
        )
        new_payload["changed_files"] = ["new.txt"]
        self.assertEqual(validate_review(new_payload, self.pass_review())["status"], "PASS")

        deleted_payload = dict(self.payload)
        deleted_payload["diff"] = (
            "diff --git a/old.txt b/old.txt\n"
            "--- a/old.txt\n"
            "+++ /dev/null\n"
            "@@ -1 +0,0 @@\n"
            "-old line\n"
        )
        deleted_payload["changed_files"] = ["old.txt"]
        self.assertEqual(validate_review(deleted_payload, self.pass_review())["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
