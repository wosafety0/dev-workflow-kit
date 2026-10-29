import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.verify_consumer_acceptance_report import verify_report as verify_standalone_report


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "reusable-acceptance.yml"
SHA = "a" * 40
WORKFLOW_SHA = "b" * 40
WORKFLOW_REF = "wosafety0/example/.github/workflows/ci.yml@refs/heads/main"
HARNESS_WORKFLOW_SHA = "c" * 40
HARNESS_WORKFLOW_REF = (
    "wosafety0/dev-workflow-kit/.github/workflows/reusable-acceptance.yml@"
    + HARNESS_WORKFLOW_SHA
)


def extract_inline_report_builder():
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    marker = "      - name: Build redacted consumer acceptance report"
    start = lines.index(marker)
    run_index = next(i for i in range(start, len(lines)) if lines[i] == "        run: |")
    heredoc_index = next(
        i for i in range(run_index + 1, len(lines))
        if lines[i] == "          python3 - <<'PY'"
    )
    code = []
    for line in lines[heredoc_index + 1:]:
        if line == "          PY":
            break
        if not line.strip():
            code.append("")
            continue
        if not line.startswith("          "):
            raise AssertionError("Unexpected YAML indentation in report builder")
        code.append(line[10:])
    else:
        raise AssertionError("Report builder heredoc terminator not found")
    return "\n".join(code) + "\n"


def extract_inline_verifier():
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    marker = "      - name: Verify consumer report identity and passing status"
    start = lines.index(marker)
    run_index = next(i for i in range(start, len(lines)) if lines[i] == "        run: |")
    heredoc_index = next(
        i for i in range(run_index + 1, len(lines))
        if lines[i] == "          python3 - <<'PY'"
    )
    code = []
    for line in lines[heredoc_index + 1:]:
        if line == "          PY":
            break
        if not line.strip():
            code.append("")
            continue
        if not line.startswith("          "):
            raise AssertionError("Unexpected YAML indentation in inline verifier")
        code.append(line[10:])
    else:
        raise AssertionError("Inline verifier heredoc terminator not found")
    return "\n".join(code) + "\n"


class ReusableAcceptanceWorkflowTests(unittest.TestCase):
    def test_checkout_does_not_persist_github_credentials_for_consumer_code(self):
        lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
        checkout_index = lines.index("      - name: Check out consuming repository")
        next_step = next(
            index for index in range(checkout_index + 1, len(lines))
            if lines[index].startswith("      - name: ")
        )
        checkout_block = lines[checkout_index:next_step]
        self.assertIn("          persist-credentials: false", checkout_block)

    def run_inline_report_builder(self, root):
        env = os.environ.copy()
        env.update({
            "CONSUMER_COMMIT_SHA": SHA,
            "CALLER_WORKFLOW_REF": WORKFLOW_REF,
            "CALLER_WORKFLOW_SHA": WORKFLOW_SHA,
            "HARNESS_WORKFLOW_REF": HARNESS_WORKFLOW_REF,
            "HARNESS_WORKFLOW_SHA": HARNESS_WORKFLOW_SHA,
            "RUNTIME_OUTCOME": "success",
            "TEST_OUTCOME": "success",
        })
        return subprocess.run(
            [sys.executable, "-c", extract_inline_report_builder()],
            cwd=root, env=env, capture_output=True, text=True, check=False,
        )

    def test_report_builder_rejects_symlinked_artifacts_directory(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            (root / "artifacts").symlink_to(Path(outside), target_is_directory=True)
            result = self.run_inline_report_builder(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unsafe acceptance report output directory", result.stderr)
            self.assertFalse((Path(outside) / "consumer-acceptance-report.json").exists())

    def test_report_builder_atomically_replaces_hardlinked_output_without_modifying_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            target = root / "consumer-source.txt"
            target.write_text("original consumer source", encoding="utf-8")
            output = artifacts / "consumer-acceptance-report.json"
            os.link(target, output)
            result = self.run_inline_report_builder(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "original consumer source")
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "passed")
            self.assertNotEqual(target.stat().st_ino, output.stat().st_ino)

    def run_inline_verifier_payload(self, payload=None, expected_sha=SHA,
                                    expected_ref=WORKFLOW_REF,
                                    expected_workflow_sha=WORKFLOW_SHA,
                                    expected_harness_ref=HARNESS_WORKFLOW_REF,
                                    expected_harness_sha=HARNESS_WORKFLOW_SHA):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            report_path = artifacts / "consumer-acceptance-report.json"
            if payload is not None:
                report_path.write_text(payload, encoding="utf-8")
            env = os.environ.copy()
            env.update({
                "EXPECTED_SHA": expected_sha,
                "EXPECTED_WORKFLOW_REF": expected_ref,
                "EXPECTED_WORKFLOW_SHA": expected_workflow_sha,
                "EXPECTED_HARNESS_WORKFLOW_REF": expected_harness_ref,
                "EXPECTED_HARNESS_WORKFLOW_SHA": expected_harness_sha,
            })
            return subprocess.run(
                [sys.executable, "-c", extract_inline_verifier()],
                cwd=root, env=env, capture_output=True, text=True, check=False,
            )

    def run_inline_verifier(self, report, **kwargs):
        return self.run_inline_verifier_payload(json.dumps(report), **kwargs)

    def test_actual_inline_verifier_accepts_matching_report(self):
        report = {
            "schema_version": 1,
            "consumer_commit_sha": SHA,
            "caller_workflow_ref": WORKFLOW_REF,
            "caller_workflow_sha": WORKFLOW_SHA,
            "harness_workflow_ref": HARNESS_WORKFLOW_REF,
            "harness_workflow_sha": HARNESS_WORKFLOW_SHA,
            "tests": {"runtime-validation": "passed", "consumer-acceptance-command": "passed"},
            "status": "passed",
        }
        result = self.run_inline_verifier(report)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("report verified", result.stdout.lower())

    def test_actual_inline_verifier_rejects_stale_sha_and_failed_tests(self):
        report = {
            "schema_version": 1,
            "consumer_commit_sha": SHA,
            "caller_workflow_ref": WORKFLOW_REF,
            "caller_workflow_sha": WORKFLOW_SHA,
            "harness_workflow_ref": HARNESS_WORKFLOW_REF,
            "harness_workflow_sha": HARNESS_WORKFLOW_SHA,
            "tests": {"runtime-validation": "passed", "consumer-acceptance-command": "failed"},
            "status": "failed",
        }
        stale = self.run_inline_verifier(report, expected_sha="c" * 40)
        self.assertEqual(stale.returncode, 1)
        self.assertIn("verification failed", stale.stdout.lower())
        failed = self.run_inline_verifier(report)
        self.assertEqual(failed.returncode, 1)
        self.assertNotIn("Traceback", failed.stderr)


    def test_actual_inline_verifier_rejects_workflow_identity_mismatches(self):
        report = {
            "schema_version": 1,
            "consumer_commit_sha": SHA,
            "caller_workflow_ref": WORKFLOW_REF,
            "caller_workflow_sha": WORKFLOW_SHA,
            "harness_workflow_ref": HARNESS_WORKFLOW_REF,
            "harness_workflow_sha": HARNESS_WORKFLOW_SHA,
            "tests": {"runtime-validation": "passed"},
            "status": "passed",
        }
        wrong_ref = self.run_inline_verifier(
            report, expected_ref="another/repo/.github/workflows/ci.yml@refs/heads/main"
        )
        self.assertEqual(wrong_ref.returncode, 1)
        wrong_workflow_sha = self.run_inline_verifier(
            report, expected_workflow_sha="d" * 40
        )
        self.assertEqual(wrong_workflow_sha.returncode, 1)
        wrong_harness_ref = self.run_inline_verifier(
            report, expected_harness_ref="wosafety0/dev-workflow-kit/.github/workflows/reusable-acceptance.yml@refs/heads/main"
        )
        self.assertEqual(wrong_harness_ref.returncode, 1)
        wrong_harness_sha = self.run_inline_verifier(
            report, expected_harness_sha="e" * 40
        )
        self.assertEqual(wrong_harness_sha.returncode, 1)

    def test_actual_inline_verifier_rejects_invalid_schema_and_test_sets(self):
        base = {
            "schema_version": 1,
            "consumer_commit_sha": SHA,
            "caller_workflow_ref": WORKFLOW_REF,
            "caller_workflow_sha": WORKFLOW_SHA,
            "harness_workflow_ref": HARNESS_WORKFLOW_REF,
            "harness_workflow_sha": HARNESS_WORKFLOW_SHA,
            "tests": {"runtime-validation": "passed"},
            "status": "passed",
        }
        cases = []
        empty_tests = dict(base, tests={})
        cases.append(empty_tests)
        missing_required_stage = dict(base, tests={"runtime-validation": "passed"})
        cases.append(missing_required_stage)
        unknown_stage = dict(base, tests={
            "runtime-validation": "passed",
            "consumer-acceptance-command": "passed",
            "unrecognized-stage": "passed",
        })
        cases.append(unknown_stage)
        extra_key = dict(base, unexpected="not allowed")
        cases.append(extra_key)
        boolean_version = dict(base, schema_version=True)
        cases.append(boolean_version)
        blank_test_name = dict(base, tests={"   ": "passed"})
        cases.append(blank_test_name)
        unknown_test_status = dict(base, tests={"runtime-validation": "skipped"})
        cases.append(unknown_test_status)
        for report in cases:
            with self.subTest(report=report):
                result = self.run_inline_verifier(report)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)

    def test_inline_and_standalone_verifiers_enforce_same_contract(self):
        valid = {
            "schema_version": 1,
            "consumer_commit_sha": SHA,
            "caller_workflow_ref": WORKFLOW_REF,
            "caller_workflow_sha": WORKFLOW_SHA,
            "harness_workflow_ref": HARNESS_WORKFLOW_REF,
            "harness_workflow_sha": HARNESS_WORKFLOW_SHA,
            "tests": {
                "runtime-validation": "passed",
                "consumer-acceptance-command": "passed",
            },
            "status": "passed",
        }
        cases = [valid]
        cases.append({key: value for key, value in valid.items() if key != "harness_workflow_sha"})
        cases.append(dict(valid, unexpected="not allowed"))
        cases.append(dict(valid, consumer_commit_sha="f" * 40))
        cases.append(dict(valid, caller_workflow_ref="other/repo/workflow.yml@refs/heads/main"))
        cases.append(dict(valid, harness_workflow_sha="f" * 40))
        cases.append(dict(valid, tests={"runtime-validation": "passed"}))
        cases.append(dict(valid, tests={
            "runtime-validation": "passed",
            "consumer-acceptance-command": "passed",
            "unexpected-stage": "passed",
        }))
        cases.append(dict(valid, tests={
            "runtime-validation": "passed",
            "consumer-acceptance-command": "failed",
        }, status="failed"))
        cases.append(dict(valid, schema_version=True))

        for report in cases:
            with self.subTest(report=report):
                standalone_valid = verify_standalone_report(
                    report, SHA, WORKFLOW_REF, WORKFLOW_SHA,
                    HARNESS_WORKFLOW_REF, HARNESS_WORKFLOW_SHA,
                )
                inline = self.run_inline_verifier(report)
                inline_valid = inline.returncode == 0
                self.assertEqual(
                    inline_valid, standalone_valid,
                    "inline and standalone verifier contract drifted: "
                    + inline.stdout + inline.stderr,
                )

    def test_actual_inline_verifier_rejects_duplicate_json_object_keys(self):
        duplicate_top_level = (
            '{"schema_version":1,"consumer_commit_sha":"' + SHA
            + '","caller_workflow_ref":"' + WORKFLOW_REF
            + '","caller_workflow_sha":"' + WORKFLOW_SHA
            + '","harness_workflow_ref":"' + HARNESS_WORKFLOW_REF
            + '","harness_workflow_sha":"' + HARNESS_WORKFLOW_SHA
            + '","tests":{"runtime-validation":"passed",'
            + '"consumer-acceptance-command":"passed"},'
            + '"status":"failed","status":"passed"}'
        )
        duplicate_nested = (
            '{"schema_version":1,"consumer_commit_sha":"' + SHA
            + '","caller_workflow_ref":"' + WORKFLOW_REF
            + '","caller_workflow_sha":"' + WORKFLOW_SHA
            + '","harness_workflow_ref":"' + HARNESS_WORKFLOW_REF
            + '","harness_workflow_sha":"' + HARNESS_WORKFLOW_SHA
            + '","tests":{"runtime-validation":"failed",'
            + '"runtime-validation":"passed",'
            + '"consumer-acceptance-command":"passed"},"status":"passed"}'
        )
        for payload in (duplicate_top_level, duplicate_nested):
            with self.subTest(payload=payload):
                result = self.run_inline_verifier_payload(payload)
                self.assertEqual(result.returncode, 1)
                self.assertIn("verification failed", result.stdout.lower())
                self.assertNotIn("Traceback", result.stderr)

    def test_actual_inline_verifier_fails_closed_for_missing_or_corrupt_report(self):
        missing = self.run_inline_verifier_payload()
        self.assertEqual(missing.returncode, 1)
        self.assertNotIn("Traceback", missing.stderr)
        corrupt = self.run_inline_verifier_payload("{not-json")
        self.assertEqual(corrupt.returncode, 1)
        self.assertNotIn("Traceback", corrupt.stderr)

    def test_workflow_does_not_require_verifier_script_from_consumer_checkout(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        verifier_source = source[source.index(
            "      - name: Verify consumer report identity and passing status"
        ):]
        self.assertIn("python3 - <<'PY'", verifier_source)
        self.assertNotIn("python3 scripts/verify_consumer_acceptance_report.py", source)


if __name__ == "__main__":
    unittest.main()
