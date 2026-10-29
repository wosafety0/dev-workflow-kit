#!/usr/bin/env python3
"""Run reviewed Harness task IDs without shell evaluation and emit a redacted report.

Configuration is validated by scripts.harness_config. The runner maps each allowed task
ID to fixed behavior; configuration cannot supply executable names or arbitrary arguments.
Task stdout/stderr are suppressed by default so secrets or private test payloads are not
copied into CI logs. The acceptance report contains status metadata only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from scripts.acceptance_report import AcceptanceReportError, build_acceptance_report
from scripts.harness_config import HarnessConfigError, validate_harness_config


class HarnessRunnerError(ValueError):
    """Raised when runner inputs or local project metadata are unsafe or incomplete."""


_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_MAX_TIMEOUT_SECONDS = 3600


def _resolve_inside_root(root: Path, value: str, field: str) -> Path:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise HarnessRunnerError(f"{field} must be a non-empty trimmed repository-relative path")
    candidate = Path(value)
    if (
        candidate.is_absolute()
        or not candidate.parts
        or candidate == Path(".")
        or any(part in {"", ".", ".."} for part in candidate.parts)
    ):
        raise HarnessRunnerError(f"{field} must be a safe repository-relative path")
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        raise HarnessRunnerError(f"{field} resolves outside the project root") from None
    return resolved


def _require_artifact_path(root: Path, path: Path, field: str) -> None:
    artifact_root = (root / "artifacts").resolve()
    try:
        path.relative_to(artifact_root)
    except ValueError:
        raise HarnessRunnerError(f"{field} must be inside the artifacts/ directory") from None
    if path == artifact_root or (path.exists() and path.is_dir()):
        raise HarnessRunnerError(f"{field} must identify a file inside artifacts/")


def _git_commit_sha(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise HarnessRunnerError("Could not determine the project Git commit SHA") from None
    sha = result.stdout.strip()
    if result.returncode != 0 or not _SHA_RE.fullmatch(sha):
        raise HarnessRunnerError("Project root must be a Git worktree with a valid HEAD commit")
    return sha.lower()


def _rules_pin(root: Path) -> str:
    contract = root / "docs" / "STABLE_ACCEPTANCE_CONTRACT.md"
    try:
        digest = hashlib.sha256(contract.read_bytes()).hexdigest()
    except OSError:
        raise HarnessRunnerError("Could not read docs/STABLE_ACCEPTANCE_CONTRACT.md") from None
    return f"sha256:{digest}"


def _task_argv(
    task_id: str,
    root: Path,
    review_input: Path | None,
    review_output: Path | None,
) -> list[str]:
    if task_id == "python-unittest":
        return [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    if task_id == "semantic-review":
        if review_input is None or review_output is None:
            raise HarnessRunnerError(
                "semantic-review requires both --review-input and --review-output"
            )
        script = root / "scripts" / "ai_semantic_review.py"
        if not script.is_file():
            raise HarnessRunnerError("semantic-review task requires scripts/ai_semantic_review.py")
        return [
            sys.executable,
            str(script),
            "--input",
            str(review_input),
            "--output",
            str(review_output),
        ]
    # This should be unreachable after validate_harness_config, but remain fail-closed
    # if the allowlist changes without a matching runner implementation.
    raise HarnessRunnerError(f"No reviewed runner implementation for task ID: {task_id}")


def _run_task(argv: list[str], root: Path, timeout_seconds: int) -> tuple[str, int | None]:
    try:
        result = subprocess.run(
            argv,
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "failed", None
    except OSError:
        return "failed", None
    return ("passed", result.returncode) if result.returncode == 0 else ("failed", result.returncode)


def _write_report(output_path: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    report = build_acceptance_report(metadata)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, output_path)
    except OSError:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except OSError:
                pass
        raise HarnessRunnerError("Could not write the acceptance report") from None
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Project root (default: current directory)")
    parser.add_argument("--config", required=True, help="Repository-relative Harness JSON config")
    parser.add_argument(
        "--report-output",
        default="artifacts/acceptance-report.json",
        help="Repository-relative redacted report output path",
    )
    parser.add_argument("--review-input", help="Repository-relative semantic-review input JSON")
    parser.add_argument("--review-output", help="Repository-relative semantic-review output JSON")
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=600,
        help=f"Per-task timeout in seconds (1-{_MAX_TIMEOUT_SECONDS}; default 600)",
    )
    args = parser.parse_args(argv)

    try:
        if not 1 <= args.timeout_seconds <= _MAX_TIMEOUT_SECONDS:
            raise HarnessRunnerError(
                f"timeout-seconds must be between 1 and {_MAX_TIMEOUT_SECONDS}"
            )
        root = Path(args.project_root).resolve()
        if not root.is_dir():
            raise HarnessRunnerError("project-root must be an existing directory")
        config_path = _resolve_inside_root(root, args.config, "config")
        report_path = _resolve_inside_root(root, args.report_output, "report-output")
        review_input = (
            _resolve_inside_root(root, args.review_input, "review-input")
            if args.review_input is not None else None
        )
        review_output = (
            _resolve_inside_root(root, args.review_output, "review-output")
            if args.review_output is not None else None
        )
        if review_input is not None and review_output is not None and review_input == review_output:
            raise HarnessRunnerError("review-input and review-output must be different paths")
        if review_output is not None and review_output == config_path:
            raise HarnessRunnerError("review-output must not overwrite config")
        for label, path in (
            ("config", config_path),
            ("review-input", review_input),
            ("review-output", review_output),
        ):
            if path is not None and path == report_path:
                raise HarnessRunnerError(f"report-output must not overwrite {label}")

        # Remove a prior report before config preflight. A blocked run must not leave
        # a previous PASS artifact available for downstream report-only consumers.
        _require_artifact_path(root, report_path, "report-output")
        try:
            report_path.unlink()
        except FileNotFoundError:
            pass

        try:
            raw_config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            raise HarnessRunnerError("Could not read a valid JSON Harness config") from None
        config = validate_harness_config(raw_config)

        wants_review = "semantic-review" in config["commands"]
        if wants_review and config["commands"][-1] != "semantic-review":
            raise HarnessRunnerError(
                "semantic-review must be the final configured task"
            )
        if wants_review and (review_input is None or review_output is None):
            raise HarnessRunnerError(
                "semantic-review requires both --review-input and --review-output"
            )
        if not wants_review and (review_input is not None or review_output is not None):
            raise HarnessRunnerError(
                "--review-input and --review-output are only valid when semantic-review is configured"
            )
        _require_artifact_path(root, report_path, "report-output")
        if review_output is not None:
            _require_artifact_path(root, review_output, "review-output")
        if review_input is not None and not review_input.is_file():
            raise HarnessRunnerError("review-input must identify an existing file")
        if review_output is not None:
            review_output.parent.mkdir(parents=True, exist_ok=True)
            # A skipped or blocked semantic-review must not expose a previous PASS artifact.
            try:
                review_output.unlink()
            except FileNotFoundError:
                pass

        # Preflight every task before executing any of them, avoiding partial execution if
        # a configured task lacks its required arguments or implementation.
        planned_tasks = [
            (task_id, _task_argv(task_id, root, review_input, review_output))
            for task_id in config["commands"]
        ]
        commit_sha = _git_commit_sha(root)
        rules_pin = _rules_pin(root)
        outcomes: dict[str, str] = {}
        failed = False
        for task_id, argv_for_task in planned_tasks:
            if failed:
                outcomes[task_id] = "not_run"
                print(f"Task {task_id}: not_run (an earlier task failed)")
                continue
            status, exit_code = _run_task(argv_for_task, root, args.timeout_seconds)
            outcomes[task_id] = status
            suffix = " (timeout or launch failure)" if exit_code is None and status == "failed" else (
                f" (exit {exit_code})" if exit_code not in (None, 0) else ""
            )
            print(f"Task {task_id}: {status}{suffix}")
            failed = status != "passed"

        metadata = {
            "commit_sha": commit_sha,
            "rules_pin": rules_pin,
            "tool_version": f"dev-workflow-kit/harness-runner@{commit_sha}",
            "tests": outcomes,
        }
        report = _write_report(report_path, metadata)
        print(f"Acceptance report written: {report_path.relative_to(root).as_posix()}")
        print(f"Acceptance status: {report['status']}")
        return 0 if report["status"] == "passed" else 1
    except (HarnessRunnerError, HarnessConfigError, AcceptanceReportError) as exc:
        print(f"Harness run blocked: {exc}", file=sys.stderr)
        return 2
    except OSError:
        print("Harness run blocked: filesystem operation failed", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
