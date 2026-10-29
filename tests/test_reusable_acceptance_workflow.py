import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "reusable-acceptance.yml"
SHA = "a" * 40
WORKFLOW_SHA = "b" * 40
WORKFLOW_REF = "wosafety0/example/.github/workflows/ci.yml@refs/heads/main"


def extract_inline_verifier():
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    marker = "      - name: Verify consumer report identity and passing status"
    start = lines.index(marker)
    run_index = next(i for i in range(start, len(lines)) if lines[i] == "        run: |")
    code = []
    for line in lines[run_index + 1:]:
        if line == "          PY":
            break
        if not line.startswith("          "):
            raise AssertionError("Unexpected YAML indentation in inline verifier")
        code.append(line[10:])
    else:
        raise AssertionError("Inline verifier heredoc terminator not found")
    return "\n".join(code) + "\n"


class ReusableAcceptanceWorkflowTests(unittest.TestCase):
    def run_inline_verifier(self, report, expected_sha=SHA):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            (artifacts / "consumer-acceptance-report.json").write_text(
                json.dumps(report), encoding="utf-8"
            )
            env = os.environ.copy()
            env.update({
                "EXPECTED_SHA": expected_sha,
                "EXPECTED_WORKFLOW_REF": WORKFLOW_REF,
                "EXPECTED_WORKFLOW_SHA": WORKFLOW_SHA,
            })
            return subprocess.run(
                [sys.executable, "-c", extract_inline_verifier()],
                cwd=root, env=env, capture_output=True, text=True, check=False,
            )

    def test_actual_inline_verifier_accepts_matching_report(self):
        report = {
            "schema_version": 1,
            "consumer_commit_sha": SHA,
            "caller_workflow_ref": WORKFLOW_REF,
            "caller_workflow_sha": WORKFLOW_SHA,
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
            "tests": {"runtime-validation": "passed", "consumer-acceptance-command": "failed"},
            "status": "failed",
        }
        stale = self.run_inline_verifier(report, expected_sha="c" * 40)
        self.assertEqual(stale.returncode, 1)
        self.assertIn("verification failed", stale.stdout.lower())
        failed = self.run_inline_verifier(report)
        self.assertEqual(failed.returncode, 1)
        self.assertNotIn("Traceback", failed.stderr)

    def test_workflow_does_not_require_verifier_script_from_consumer_checkout(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        verifier_source = source[source.index(
            "      - name: Verify consumer report identity and passing status"
        ):]
        self.assertIn("python3 - <<'PY'", verifier_source)
        self.assertNotIn("python3 scripts/verify_consumer_acceptance_report.py", source)


if __name__ == "__main__":
    unittest.main()
