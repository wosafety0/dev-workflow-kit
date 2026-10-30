import unittest

from scripts.acceptance_report import AcceptanceReportError, build_acceptance_report


class AcceptanceReportTests(unittest.TestCase):
    def valid_metadata(self):
        return {
            "commit_sha": "a" * 40,
            "rules_pin": "sha256:" + "b" * 64,
            "tool_version": "dev-workflow-kit/0.1.0",
            "tests": {"unit": "passed", "policy": "passed"},
        }

    def test_builds_deterministic_allowlisted_report(self):
        metadata = self.valid_metadata()
        report = build_acceptance_report(metadata)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(list(report["tests"]), ["policy", "unit"])
        self.assertEqual(report["commit_sha"], "a" * 40)
        self.assertEqual(set(report), {
            "schema_version", "commit_sha", "rules_pin", "tool_version", "tests", "status"
        })

    def test_git_bound_provenance_uses_schema_v2_and_binds_head_to_report_commit(self):
        metadata = self.valid_metadata()
        metadata["review_provenance"] = {
            "base_sha": "b" * 40,
            "head_sha": "a" * 40,
            "merge_base_sha": "c" * 40,
            "diff_sha256": "d" * 64,
            "changed_files": ["src/z.py", "src/a.py"],
        }
        report = build_acceptance_report(metadata)
        self.assertEqual(report["schema_version"], 2)
        self.assertEqual(report["review_provenance"]["head_sha"], report["commit_sha"])
        self.assertEqual(report["review_provenance"]["changed_files"], ["src/a.py", "src/z.py"])

    def test_git_bound_provenance_allows_internal_spaces_in_valid_paths(self):
        metadata = self.valid_metadata()
        metadata["review_provenance"] = {
            "base_sha": "b" * 40,
            "head_sha": "a" * 40,
            "merge_base_sha": "c" * 40,
            "diff_sha256": "d" * 64,
            "changed_files": ["src/my file.py"],
        }
        report = build_acceptance_report(metadata)
        self.assertEqual(
            report["review_provenance"]["changed_files"], ["src/my file.py"]
        )

    def test_git_bound_provenance_rejects_mismatched_head_or_unsafe_paths(self):
        mutations = (
            lambda p: p.update(head_sha="e" * 40),
            lambda p: p.update(diff_sha256="not-a-digest"),
            lambda p: p.update(changed_files=["../outside.py"]),
            lambda p: p.update(changed_files=["C:/outside.py"]),
            lambda p: p.update(changed_files=["C:relative.py"]),
            lambda p: p.update(changed_files=["src/" + chr(0x85) + "a.py"]),
            lambda p: p.update(changed_files=["src/a.py", "src/a.py"]),
        )
        for mutate in mutations:
            metadata = self.valid_metadata()
            provenance = {
                "base_sha": "b" * 40,
                "head_sha": "a" * 40,
                "merge_base_sha": "c" * 40,
                "diff_sha256": "d" * 64,
                "changed_files": ["src/a.py"],
            }
            mutate(provenance)
            metadata["review_provenance"] = provenance
            with self.subTest(provenance=provenance), self.assertRaises(AcceptanceReportError):
                build_acceptance_report(metadata)

    def test_normalizes_commit_sha_case(self):
        metadata = self.valid_metadata()
        metadata["commit_sha"] = "A" * 40
        self.assertEqual(build_acceptance_report(metadata)["commit_sha"], "a" * 40)

    def test_rejects_missing_or_unknown_root_fields(self):
        for mutate in ("missing", "extra"):
            metadata = self.valid_metadata()
            if mutate == "missing":
                del metadata["rules_pin"]
            else:
                metadata["token"] = "must-not-leak"
            with self.subTest(mutate=mutate), self.assertRaises(AcceptanceReportError):
                build_acceptance_report(metadata)

    def test_rejects_malformed_commit_sha(self):
        for sha in ("", "1234", "g" * 40, " " + "a" * 40):
            metadata = self.valid_metadata()
            metadata["commit_sha"] = sha
            with self.subTest(sha=sha), self.assertRaises(AcceptanceReportError):
                build_acceptance_report(metadata)

    def test_rejects_malformed_rules_pin(self):
        for value in (
            "sha256:",
            "sha256:rules-v1",
            "sha256:" + "g" * 64,
            "SHA256:" + "b" * 64,
            "sha256:" + "b" * 63,
        ):
            metadata = self.valid_metadata()
            metadata["rules_pin"] = value
            with self.subTest(value=value), self.assertRaisesRegex(
                AcceptanceReportError, "lowercase SHA-256 digest"
            ):
                build_acceptance_report(metadata)

    def test_rejects_empty_or_untrimmed_required_text(self):
        for field in ("rules_pin", "tool_version"):
            for value in ("", "  ", " value "):
                metadata = self.valid_metadata()
                metadata[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(AcceptanceReportError):
                    build_acceptance_report(metadata)

    def test_missing_tests_fail_closed(self):
        for tests in ({}, None, [], "passed"):
            metadata = self.valid_metadata()
            metadata["tests"] = tests
            with self.subTest(tests=tests), self.assertRaises(AcceptanceReportError):
                build_acceptance_report(metadata)

    def test_any_non_pass_status_fails_overall_report(self):
        for status in ("failed", "skipped", "not_run"):
            metadata = self.valid_metadata()
            metadata["tests"]["policy"] = status
            report = build_acceptance_report(metadata)
            self.assertEqual(report["tests"]["policy"], status)
            self.assertEqual(report["status"], "failed")

    def test_rejects_unknown_test_status_and_bad_name(self):
        for name, status in (("unit", "success"), ("", "passed"), (" unit", "passed"), ("unit", True)):
            metadata = self.valid_metadata()
            metadata["tests"] = {name: status}
            with self.subTest(name=name, status=status), self.assertRaises(AcceptanceReportError):
                build_acceptance_report(metadata)

    def test_rejects_non_object_input(self):
        with self.assertRaisesRegex(AcceptanceReportError, "JSON object"):
            build_acceptance_report([])

    def test_does_not_mutate_input(self):
        metadata = self.valid_metadata()
        original = {**metadata, "tests": dict(metadata["tests"])}
        build_acceptance_report(metadata)
        self.assertEqual(metadata, original)


if __name__ == "__main__":
    unittest.main()
