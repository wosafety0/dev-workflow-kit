import json
import tempfile
import unittest
from io import StringIO
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

    def test_rejects_rule_quote_spanning_global_and_project_instruction_boundary(self):
        review = self.finding()
        review["findings"][0]["rule_quote"] = (
            "不得将未验证结果声明为成功。\n网络请求必须设置明确超时。"
        )
        with self.assertRaisesRegex(ReviewError, "not an exact substring"):
            validate_review(self.payload, review)

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


    def test_duplicate_input_json_keys_fail_closed_before_model_call(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.json"
            output_path = Path(directory) / "review.json"
            raw = json.dumps(self.payload).replace('"task":', '"task": "", "task":', 1)
            input_path.write_text(raw, encoding="utf-8")
            output_path.write_text('{"status":"PASS"}', encoding="utf-8")
            argv = ["ai_semantic_review.py", "--input", str(input_path),
                    "--output", str(output_path)]
            with patch("sys.argv", argv), patch(
                "scripts.ai_semantic_review.call_model"
            ) as model, patch("sys.stderr", new_callable=StringIO) as stderr:
                self.assertEqual(main(), 2)
            self.assertIn("duplicate JSON object key", stderr.getvalue())
            model.assert_not_called()
            self.assertFalse(output_path.exists())


    def test_input_and_output_must_not_be_same_path(self):
        with tempfile.TemporaryDirectory() as directory:
            same_path = Path(directory) / "input.json"
            same_path.write_text(json.dumps(self.payload), encoding="utf-8")
            with patch("sys.argv", ["ai_semantic_review.py", "--input", str(same_path),
                                    "--output", str(same_path)]):
                self.assertEqual(main(), 2)
            self.assertTrue(same_path.exists())


    def test_rejects_symlink_output_without_touching_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "input.json"
            target_path = root / "important.txt"
            output_path = root / "review.json"
            input_path.write_text(json.dumps(self.payload), encoding="utf-8")
            target_path.write_text("preserve this file\n", encoding="utf-8")
            try:
                output_path.symlink_to(target_path)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable in this environment")
            argv = ["ai_semantic_review.py", "--input", str(input_path),
                    "--output", str(output_path)]
            with patch("sys.argv", argv), patch(
                "scripts.ai_semantic_review.call_model"
            ) as model, patch("sys.stderr", new_callable=StringIO) as stderr:
                self.assertEqual(main(), 2)
            self.assertIn("symlinked paths", stderr.getvalue())
            self.assertEqual(target_path.read_text(encoding="utf-8"), "preserve this file\n")
            self.assertTrue(output_path.is_symlink())
            model.assert_not_called()

    def test_rejects_symlinked_input_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target_path = root / "real-input.json"
            input_path = root / "input.json"
            output_path = root / "review.json"
            target_path.write_text(json.dumps(self.payload), encoding="utf-8")
            try:
                input_path.symlink_to(target_path)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable in this environment")
            with patch("sys.argv", ["ai_semantic_review.py", "--input", str(input_path),
                                    "--output", str(output_path)]), patch(
                "scripts.ai_semantic_review.call_model"
            ) as model, patch("sys.stderr", new_callable=StringIO) as stderr:
                self.assertEqual(main(), 2)
            self.assertIn("symlinked paths", stderr.getvalue())
            self.assertFalse(output_path.exists())
            model.assert_not_called()


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


    def test_rejects_duplicate_file_sections(self):
        payload = dict(self.payload)
        one_section = (
            "diff --git a/duplicate.txt b/duplicate.txt\n"
            "--- a/duplicate.txt\n"
            "+++ b/duplicate.txt\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
        )
        payload["diff"] = one_section + one_section
        payload["changed_files"] = ["duplicate.txt"]
        with self.assertRaisesRegex(ReviewError, "duplicate file sections"):
            validate_review(payload, self.pass_review())

    def test_rejects_diff_header_path_spoofing(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace(
            "diff --git a/src/client.py b/src/client.py",
            "diff --git a/src/client.py b/other.py",
        )
        with self.assertRaisesRegex(ReviewError, "new-file header does not match"):
            validate_review(payload, self.pass_review())

    def test_rejects_rename_from_path_header_mismatch(self):
        payload = dict(self.payload)
        payload["diff"] = (
            "diff --git a/old_name.py b/new_name.py\n"
            "similarity index 100%\n"
            "rename from other_name.py\n"
            "rename to new_name.py\n"
        )
        payload["changed_files"] = ["new_name.py"]
        with self.assertRaisesRegex(ReviewError, "rename metadata does not match"):
            validate_review(payload, self.pass_review())


    def test_rejects_parent_traversal_changed_file_path(self):
        payload = dict(self.payload)
        payload["changed_files"] = ["../client.py", "README.md"]
        with self.assertRaisesRegex(ReviewError, "changed_files contains an unsafe path"):
            validate_review(payload, self.pass_review())

    def test_rejects_absolute_changed_file_path(self):
        payload = dict(self.payload)
        payload["changed_files"] = ["/src/client.py", "README.md"]
        with self.assertRaisesRegex(ReviewError, "changed_files contains an unsafe path"):
            validate_review(payload, self.pass_review())

    def test_rejects_backslash_changed_file_path(self):
        payload = dict(self.payload)
        payload["changed_files"] = [r"src\\client.py", "README.md"]
        with self.assertRaisesRegex(ReviewError, "changed_files contains an unsafe path"):
            validate_review(payload, self.pass_review())

    def test_rejects_control_characters_in_changed_file_path(self):
        payload = dict(self.payload)
        payload["changed_files"] = ["src/client.py\\x00", "README.md"]
        with self.assertRaisesRegex(ReviewError, "changed_files contains an unsafe path"):
            validate_review(payload, self.pass_review())


    def test_rejects_extremely_large_hunk_line_numbers(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace(
            "@@ -1 +1 @@",
            "@@ -999999999999999999999999999999999999999999 +1 @@",
            1,
        )
        with self.assertRaisesRegex(ReviewError, "line range|evidence|hunk"):
            validate_review(payload, self.pass_review())

    def test_rejects_changed_file_path_with_repeated_separator(self):
        payload = dict(self.payload)
        payload["changed_files"] = ["src//client.py", "README.md"]
        with self.assertRaisesRegex(ReviewError, "unsafe path"):
            validate_review(payload, self.pass_review())

    def test_rejects_diff_path_with_parent_traversal(self):
        payload = dict(self.payload)
        payload["diff"] = payload["diff"].replace(
            "a/src/client.py b/src/client.py",
            "a/../client.py b/../client.py",
            1,
        ).replace(
            "--- a/src/client.py",
            "--- a/../client.py",
            1,
        ).replace(
            "+++ b/src/client.py",
            "+++ b/../client.py",
            1,
        )
        payload["changed_files"] = ["../client.py", "README.md"]
        with self.assertRaisesRegex(ReviewError, "unsafe path|path|changed_files"):
            validate_review(payload, self.pass_review())

    def test_rejects_excessively_long_changed_file_path(self):
        payload = dict(self.payload)
        long_path = "a" * 5000 + ".py"
        payload["changed_files"] = [long_path, "README.md"]
        payload["diff"] = payload["diff"].replace(
            "a/src/client.py b/src/client.py",
            f"a/{long_path} b/{long_path}",
            1,
        ).replace(
            "--- a/src/client.py",
            f"--- a/{long_path}",
            1,
        ).replace(
            "+++ b/src/client.py",
            f"+++ b/{long_path}",
            1,
        )
        with self.assertRaisesRegex(ReviewError, "path is too long"):
            validate_review(payload, self.pass_review())


    def test_rejects_hunk_header_with_unbounded_decimal_integer(self):
        payload = dict(self.payload)
        huge_number = "9" * 5000
        payload["diff"] = payload["diff"].replace(
            "@@ -1 +1 @@",
            f"@@ -{huge_number} +1 @@",
            1,
        )
        with self.assertRaisesRegex(ReviewError, "Malformed diff hunk header|line range"):
            validate_review(payload, self.pass_review())


    def test_checked_in_semantic_review_example_has_grounded_negative_finding(self):
        example = Path(__file__).resolve().parents[1] / "examples" / "semantic-review-negative-input.json"
        payload = json.loads(example.read_text(encoding="utf-8"))
        review = {
            "status": "NEEDS_CHANGES",
            "summary": "The addition function was changed to subtraction without authorization.",
            "checked_scope": ["arithmetic behavior"],
            "limitations": ["Only the supplied diff was reviewed."],
            "findings": [{
                "severity": "medium",
                "title": "Addition changed to subtraction",
                "file": "src/example.py",
                "line_start": 2,
                "line_end": 2,
                "rule_ref": "R1",
                "rule_quote": "Preserve the documented arithmetic behavior of each function.",
                "evidence": "return a - b",
                "rationale": "The changed implementation no longer performs addition.",
                "recommendation": "Restore addition unless the task explicitly requires subtraction.",
            }],
        }
        self.assertEqual(validate_review(payload, review)["status"], "NEEDS_CHANGES")

    def test_model_missing_configuration_fails_closed(self):
        from scripts.ai_semantic_review import call_model
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ReviewError, "not configured"):
                call_model(self.payload)

    def test_model_network_failure_fails_closed_without_leaking_key(self):
        import urllib.error
        from scripts.ai_semantic_review import call_model
        config = {"AI_REVIEW_API_BASE": "https://example.invalid/v1",
                  "AI_REVIEW_API_KEY": "SECRET_TEST_TOKEN",
                  "AI_REVIEW_MODEL": "test-model"}
        with patch.dict("os.environ", config, clear=True), patch(
            "scripts.ai_semantic_review.urllib.request.build_opener"
        ) as opener_builder:
            opener_builder.return_value.open.side_effect = urllib.error.URLError("SECRET_TEST_TOKEN")
            with self.assertRaises(ReviewError) as caught:
                call_model(self.payload)
        self.assertIn("review cannot pass", str(caught.exception))
        self.assertNotIn("SECRET_TEST_TOKEN", str(caught.exception))

    def test_model_timeout_fails_closed(self):
        from scripts.ai_semantic_review import call_model
        config = {"AI_REVIEW_API_BASE": "https://example.invalid/v1",
                  "AI_REVIEW_API_KEY": "test-key",
                  "AI_REVIEW_MODEL": "test-model"}
        with patch.dict("os.environ", config, clear=True), patch(
            "scripts.ai_semantic_review.urllib.request.build_opener"
        ) as opener_builder:
            opener_builder.return_value.open.side_effect = TimeoutError("simulated timeout")
            with self.assertRaisesRegex(ReviewError, "review cannot pass"):
                call_model(self.payload)

    def test_model_malformed_responses_fail_closed(self):
        from unittest.mock import MagicMock
        from scripts.ai_semantic_review import call_model
        config = {"AI_REVIEW_API_BASE": "https://example.invalid/v1",
                  "AI_REVIEW_API_KEY": "test-key",
                  "AI_REVIEW_MODEL": "test-model"}
        responses = [
            b"not-json",
            b"{}",
            b'{"choices":[]}',
            b'{"choices":[{"message":{"content":"not-json"}}]}',
            b'{"choices":[{"message":{"content":null}}]}',
            b'{"choices":[],"choices":[{"message":{"content":"{}"}}]}',
            b'{"choices":[{"message":{"content":"{\"status\":\"PASS\",\"status\":\"NEEDS_CHANGES\"}"}}]}',
        ]
        for raw in responses:
            with self.subTest(raw=raw):
                response = MagicMock()
                response.__enter__.return_value.read.return_value = raw
                with patch.dict("os.environ", config, clear=True), patch(
                    "scripts.ai_semantic_review.urllib.request.build_opener"
                ) as opener_builder:
                    opener_builder.return_value.open.return_value = response
                    with self.assertRaises(ReviewError):
                        call_model(self.payload)

    def test_model_valid_response_is_parsed(self):
        from unittest.mock import MagicMock
        from scripts.ai_semantic_review import call_model
        config = {"AI_REVIEW_API_BASE": "https://example.invalid/v1",
                  "AI_REVIEW_API_KEY": "test-key",
                  "AI_REVIEW_MODEL": "test-model"}
        raw = json.dumps({"choices": [{"message": {
            "content": json.dumps(self.pass_review())
        }}]}).encode("utf-8")
        response = MagicMock()
        response.__enter__.return_value.read.return_value = raw
        with patch.dict("os.environ", config, clear=True), patch(
            "scripts.ai_semantic_review.urllib.request.build_opener"
        ) as opener_builder:
            opener_builder.return_value.open.return_value = response
            self.assertEqual(call_model(self.payload)["status"], "PASS")



    def test_model_response_size_is_bounded_and_fails_closed(self):
        from unittest.mock import MagicMock
        from scripts.ai_semantic_review import MAX_MODEL_RESPONSE_BYTES, call_model

        config = {
            "AI_REVIEW_API_BASE": "https://example.invalid/v1",
            "AI_REVIEW_API_KEY": "test-key",
            "AI_REVIEW_MODEL": "test-model",
        }
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"x" * (MAX_MODEL_RESPONSE_BYTES + 1)
        with patch.dict("os.environ", config, clear=True), patch(
            "scripts.ai_semantic_review.urllib.request.build_opener"
        ) as opener_builder:
            opener_builder.return_value.open.return_value = response
            with self.assertRaisesRegex(ReviewError, "size limit"):
                call_model(self.payload)
        response.__enter__.return_value.read.assert_called_once_with(
            MAX_MODEL_RESPONSE_BYTES + 1
        )

    def test_provider_config_validation_is_offline(self):
        from scripts.ai_semantic_review import validate_model_config
        with patch("scripts.ai_semantic_review.urllib.request.urlopen") as network:
            endpoint, key, model = validate_model_config({
                "AI_REVIEW_API_BASE": "https://example.invalid/v1/",
                "AI_REVIEW_API_KEY": "test-key",
                "AI_REVIEW_MODEL": "test-model",
            })
        self.assertEqual(endpoint, "https://example.invalid/v1/chat/completions")
        self.assertEqual((key, model), ("test-key", "test-model"))
        network.assert_not_called()

    def test_provider_config_allows_http_only_for_literal_loopback_ips(self):
        from scripts.ai_semantic_review import validate_model_config

        for base, expected in (
            ("http://127.0.0.1:1235/v1", "http://127.0.0.1:1235/v1/chat/completions"),
            ("http://[::1]:1235/v1", "http://[::1]:1235/v1/chat/completions"),
        ):
            with self.subTest(base=base):
                endpoint, key, model = validate_model_config({
                    "AI_REVIEW_API_BASE": base,
                    "AI_REVIEW_API_KEY": "test-key",
                    "AI_REVIEW_MODEL": "test-model",
                })
                self.assertEqual(endpoint, expected)
                self.assertEqual((key, model), ("test-key", "test-model"))


    def test_call_model_uses_local_loopback_http_without_proxy(self):
        import threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        from scripts.ai_semantic_review import call_model

        response_body = json.dumps({
            "choices": [{
                "message": {"content": json.dumps(self.pass_review())}
            }]
        }).encode("utf-8")

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                self.server.received_auth = self.headers.get("Authorization")
                length = int(self.headers.get("Content-Length", "0"))
                self.rfile.read(length)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response_body)))
                self.end_headers()
                self.wfile.write(response_body)

            def log_message(self, _format, *_args):
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            config = {
                "AI_REVIEW_API_BASE": f"http://127.0.0.1:{server.server_port}/v1",
                "AI_REVIEW_API_KEY": "test-loopback-key",
                "AI_REVIEW_MODEL": "test-model",
                "HTTP_PROXY": "http://127.0.0.1:1",
                "HTTPS_PROXY": "http://127.0.0.1:1",
                "http_proxy": "http://127.0.0.1:1",
                "https_proxy": "http://127.0.0.1:1",
                "ALL_PROXY": "http://127.0.0.1:1",
                "all_proxy": "http://127.0.0.1:1",
                "NO_PROXY": "",
                "no_proxy": "",
            }
            # Keep Windows-required environment such as SystemRoot for SSLContext setup.
            with patch.dict("os.environ", config, clear=False):
                review = call_model(self.payload)
            self.assertEqual(review["status"], "PASS")
            self.assertEqual(server.received_auth, "Bearer test-loopback-key")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


    def test_https_model_requests_install_redirect_rejection_handler(self):
        from unittest.mock import MagicMock
        from scripts.ai_semantic_review import _NoRedirectHandler, call_model

        raw = json.dumps({"choices": [{"message": {
            "content": json.dumps(self.pass_review())
        }}]}).encode("utf-8")
        response = MagicMock()
        response.__enter__.return_value.read.return_value = raw
        config = {
            "AI_REVIEW_API_BASE": "https://model.example.invalid/v1",
            "AI_REVIEW_API_KEY": "test-key",
            "AI_REVIEW_MODEL": "test-model",
        }
        with patch.dict("os.environ", config, clear=True), patch(
            "scripts.ai_semantic_review.urllib.request.build_opener"
        ) as opener_builder:
            opener_builder.return_value.open.return_value = response
            review = call_model(self.payload)

        self.assertEqual(review["status"], "PASS")
        handlers = opener_builder.call_args.args
        redirect_handler = next(
            (handler for handler in handlers if isinstance(handler, _NoRedirectHandler)),
            None,
        )
        self.assertIsNotNone(redirect_handler)
        self.assertIsNone(redirect_handler.redirect_request(
            None, None, 302, "Found", {"Location": "https://attacker.invalid/collect"},
            "https://attacker.invalid/collect",
        ))


    def test_call_model_rejects_redirect_without_forwarding_authorization(self):
        import threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        from scripts.ai_semantic_review import call_model

        destination_hits = []

        class DestinationHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                destination_hits.append(self.headers.get("Authorization"))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"{}")

            def log_message(self, _format, *_args):
                return

        destination = ThreadingHTTPServer(("127.0.0.1", 0), DestinationHandler)

        class RedirectHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(302)
                self.send_header(
                    "Location",
                    f"http://127.0.0.1:{destination.server_port}/collect",
                )
                self.send_header("Content-Length", "0")
                self.end_headers()

            def log_message(self, _format, *_args):
                return

        source = ThreadingHTTPServer(("127.0.0.1", 0), RedirectHandler)
        threads = [
            threading.Thread(target=server.serve_forever, daemon=True)
            for server in (destination, source)
        ]
        for thread in threads:
            thread.start()
        try:
            config = {
                "AI_REVIEW_API_BASE": f"http://127.0.0.1:{source.server_port}/v1",
                "AI_REVIEW_API_KEY": "redirect-test-secret",
                "AI_REVIEW_MODEL": "test-model",
            }
            with patch.dict("os.environ", config, clear=True):
                with self.assertRaisesRegex(ReviewError, "Model request failed"):
                    call_model(self.payload)
            self.assertEqual(destination_hits, [])
        finally:
            for server in (source, destination):
                server.shutdown()
                server.server_close()
            for thread in threads:
                thread.join(timeout=2)


    def test_provider_config_rejects_unsafe_endpoints(self):
        from scripts.ai_semantic_review import validate_model_config
        invalid = [
            "http://example.invalid/v1",
            "https://user:password@example.invalid/v1",
            "https://example.invalid/v1?token=secret",
            "https://example.invalid/v1#fragment",
            "https://example.invalid:invalid/v1",
            "file:///tmp/model",
            "https://example.invalid/v1\nX-Injected: yes",
        ]
        for base in invalid:
            with self.subTest(base=base):
                with self.assertRaises(ReviewError):
                    validate_model_config({
                        "AI_REVIEW_API_BASE": base,
                        "AI_REVIEW_API_KEY": "test-key",
                        "AI_REVIEW_MODEL": "test-model",
                    })

    def test_provider_config_rejects_invalid_model_and_key(self):
        from scripts.ai_semantic_review import validate_model_config
        valid = {
            "AI_REVIEW_API_BASE": "https://example.invalid/v1",
            "AI_REVIEW_API_KEY": "test-key",
            "AI_REVIEW_MODEL": "test-model",
        }
        for field, bad in [
            ("AI_REVIEW_API_KEY", "key\nInjected: value"),
            ("AI_REVIEW_MODEL", "bad\nmodel"),
            ("AI_REVIEW_MODEL", "bad model"),
        ]:
            with self.subTest(field=field):
                config = dict(valid)
                config[field] = bad
                with self.assertRaises(ReviewError):
                    validate_model_config(config)



if __name__ == "__main__":
    unittest.main()
