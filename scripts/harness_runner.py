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
import threading
import time
from pathlib import Path
from typing import Any

from scripts.acceptance_report import AcceptanceReportError, build_acceptance_report
from scripts.ai_semantic_review import ReviewError, _validate_diff_integrity, validate_input
from scripts.harness_config import HarnessConfigError, validate_harness_config


class HarnessRunnerError(ValueError):
    """Raised when runner inputs or local project metadata are unsafe or incomplete."""


_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_MAX_TIMEOUT_SECONDS = 3600
_MAX_REVIEW_INPUT_BYTES = 4 * 1024 * 1024
_GIT_COMMAND_TIMEOUT_SECONDS = 10


def _git_environment() -> dict[str, str]:
    """Ignore replace refs so provenance is derived from the commit objects named by their SHAs."""
    environment = os.environ.copy()
    # Git provenance must not inherit repository redirection from the caller.
    # Git-specific caller settings can redirect object lookup or inject config.
    # Keep ordinary process environment (PATH, locale, etc.) intact.
    for name in tuple(environment):
        if name.startswith("GIT_"):
            environment.pop(name, None)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


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


def _reject_symlink_path(root: Path, value: str, field: str) -> None:
    """Reject symlinks in a repository-relative input or output path."""
    current = root / value
    while current != root:
        if current.is_symlink():
            raise HarnessRunnerError(f"{field} must not use symlinked paths")
        current = current.parent


def _resolve_trusted_source(root: Path, value: str, field: str) -> Path:
    """Resolve committed executable/rule inputs, excluding mutable symlink targets and artifacts."""
    resolved = _resolve_inside_root(root, value, field)
    candidate = root / value
    current = candidate
    while current != root:
        if current.is_symlink():
            raise HarnessRunnerError(f"{field} must not use symlinked source paths")
        current = current.parent

    if resolved.is_dir():
        for directory, subdirectories, filenames in os.walk(resolved, followlinks=False):
            entries = [Path(directory) / name for name in (*subdirectories, *filenames)]
            if any(entry.is_symlink() for entry in entries):
                raise HarnessRunnerError(f"{field} must not contain symlinked source paths")

    artifact_root = (root / "artifacts").resolve()
    try:
        resolved.relative_to(artifact_root)
    except ValueError:
        return resolved
    raise HarnessRunnerError(f"{field} must not resolve inside artifacts/")


def _require_tracked_config(root: Path, config_path: Path) -> None:
    """Require the config to be a committed file outside generated artifacts/."""
    artifact_root = (root / "artifacts").resolve()
    try:
        config_path.relative_to(artifact_root)
    except ValueError:
        pass
    else:
        raise HarnessRunnerError("config must not resolve inside artifacts/")

    try:
        relative = config_path.relative_to(root.resolve()).as_posix()
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD", "--", f":(literal){relative}"],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=10,
            check=False,
            env=_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        raise HarnessRunnerError("Could not verify tracked Harness config") from None
    if result.returncode != 0 or relative not in result.stdout.splitlines():
        raise HarnessRunnerError("config must be tracked by the current Git HEAD")


def _git_commit_sha(root: Path) -> str:
    """Require that the report's commit describes the exact checked-out source.

    Git status checks tracked changes and untracked files, excluding only generated
    artifacts/. Normal interpreter caches should be covered by the project's
    .gitignore. No filenames or file contents are included in error messages.
    """
    def run_git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=10,
            check=False,
            env=_git_environment(),
        )

    try:
        top = run_git("rev-parse", "--show-toplevel")
        result = run_git("rev-parse", "HEAD")
        status = run_git(
            "status", "--porcelain=v1", "--untracked-files=all",
            "--", ".", ":(exclude)artifacts",
        )
    except (OSError, subprocess.TimeoutExpired):
        raise HarnessRunnerError("Could not verify Git commit provenance") from None
    if top.returncode != 0 or not top.stdout.strip() or (
        Path(top.stdout.strip()).resolve() != root.resolve()
    ):
        raise HarnessRunnerError("project-root must be the Git repository root")
    sha = result.stdout.strip()
    if result.returncode != 0 or not _SHA_RE.fullmatch(sha):
        raise HarnessRunnerError("Project root must be a Git worktree with a valid HEAD commit")
    if status.returncode != 0:
        raise HarnessRunnerError("Could not verify clean Git worktree")
    if status.stdout:
        raise HarnessRunnerError(
            "Git worktree must be clean outside artifacts/ before acceptance"
        )
    return sha.lower()


def _rules_pin(root: Path) -> str:
    contract = _resolve_trusted_source(
        root, "docs/STABLE_ACCEPTANCE_CONTRACT.md", "stable acceptance contract"
    )
    if not contract.is_file():
        raise HarnessRunnerError("Could not read docs/STABLE_ACCEPTANCE_CONTRACT.md")
    try:
        digest = hashlib.sha256(contract.read_bytes()).hexdigest()
    except OSError:
        raise HarnessRunnerError("Could not read docs/STABLE_ACCEPTANCE_CONTRACT.md") from None
    return f"sha256:{digest}"


def _reject_ignored_python_sources(root: Path) -> None:
    """Reject ignored project Python sources before and after task execution."""
    try:
        ignored = subprocess.run(
            [
                "git", "ls-files", "--others", "--ignored", "--exclude-standard",
                "-z", "--", ".",
            ],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            timeout=10, check=False, env=_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        raise HarnessRunnerError("Could not verify ignored Python source") from None
    if ignored.returncode != 0:
        raise HarnessRunnerError("Could not verify ignored Python source")
    generated_or_environment_dirs = {
        ".venv", "venv", "env", ".tox", "artifacts", "__pycache__",
    }
    for raw_path in ignored.stdout.split(b"\0"):
        if not raw_path:
            continue
        ignored_path = Path(os.fsdecode(raw_path))
        if ignored_path.suffix != ".py":
            continue
        if any(
            part in generated_or_environment_dirs or part.startswith(".venv")
            for part in ignored_path.parts[:-1]
        ):
            continue
        raise HarnessRunnerError("ignored Python source must not be executed")


def _task_argv(
    task_id: str,
    root: Path,
    review_input: Path | None,
    review_output: Path | None,
) -> list[str]:
    if task_id == "python-unittest":
        tests_dir = _resolve_trusted_source(root, "tests", "tests directory")
        if not tests_dir.is_dir():
            raise HarnessRunnerError("python-unittest task requires a tests/ directory")
        return [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    if task_id == "semantic-review":
        if review_input is None or review_output is None:
            raise HarnessRunnerError(
                "semantic-review requires both --review-input and --review-output"
            )
        script = _resolve_trusted_source(root, "scripts/ai_semantic_review.py", "semantic-review script")
        if not script.is_file():
            raise HarnessRunnerError("semantic-review task requires scripts/ai_semantic_review.py")
        return [
            sys.executable,
            str(script),
            "--input",
            "-",
            "--output",
            str(review_output),
        ]
    # This should be unreachable after validate_harness_config, but remain fail-closed
    # if the allowlist changes without a matching runner implementation.
    raise HarnessRunnerError(f"No reviewed runner implementation for task ID: {task_id}")


def _run_task(
    argv: list[str],
    root: Path,
    timeout_seconds: int,
    stdin_data: bytes | None = None,
) -> tuple[str, int | None]:
    try:
        run_options: dict[str, Any] = {
            "cwd": root,
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "timeout": timeout_seconds,
            "check": False,
        }
        if stdin_data is not None:
            run_options["input"] = stdin_data
        result = subprocess.run(argv, **run_options)
    except subprocess.TimeoutExpired:
        return "failed", None
    except OSError:
        return "failed", None
    return ("passed", result.returncode) if result.returncode == 0 else ("failed", result.returncode)


def _git_text(root: Path, args: list[str], field: str) -> str:
    """Run a bounded-time Git metadata command without exposing its stderr."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=10,
            check=False,
            env=_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired):
        raise HarnessRunnerError(f"Could not verify {field}") from None
    if result.returncode != 0:
        raise HarnessRunnerError(f"Could not verify {field}")
    return result.stdout.strip()


def _git_bytes_bounded(root: Path, args: list[str], field: str) -> bytes:
    """Read bounded Git output with both a byte cap and a wall-clock timeout."""
    process: subprocess.Popen[bytes] | None = None
    reader: threading.Thread | None = None
    output_chunks: list[bytes] = []
    reader_errors: list[BaseException] = []
    oversized = threading.Event()
    total_bytes = 0
    timed_out = False

    def consume_stdout() -> None:
        nonlocal total_bytes
        assert process is not None and process.stdout is not None
        try:
            while total_bytes <= _MAX_REVIEW_INPUT_BYTES:
                chunk = process.stdout.read(
                    min(65536, _MAX_REVIEW_INPUT_BYTES + 1 - total_bytes)
                )
                if not chunk:
                    return
                output_chunks.append(chunk)
                total_bytes += len(chunk)
                if total_bytes > _MAX_REVIEW_INPUT_BYTES:
                    oversized.set()
                    return
        except (OSError, ValueError) as exc:
            reader_errors.append(exc)

    try:
        process = subprocess.Popen(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0,
            env=_git_environment(),
        )
        reader = threading.Thread(target=consume_stdout, name="harness-git-output", daemon=True)
        reader.start()
        deadline = time.monotonic() + _GIT_COMMAND_TIMEOUT_SECONDS
        while process.poll() is None:
            if oversized.is_set():
                try:
                    process.kill()
                except OSError:
                    pass
                break
            if time.monotonic() >= deadline:
                timed_out = True
                try:
                    process.kill()
                except OSError:
                    pass
                break
            time.sleep(0.01)

        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                timed_out = True

        reader.join(timeout=2)
        if reader.is_alive():
            if process.stdout is not None:
                try:
                    process.stdout.close()
                except (OSError, ValueError):
                    pass
            reader.join(timeout=2)

        if oversized.is_set():
            raise HarnessRunnerError(f"{field} exceeds the 4 MiB input limit")
        if timed_out or reader.is_alive():
            raise HarnessRunnerError(f"Could not verify {field}")
        if reader_errors:
            raise HarnessRunnerError(f"Could not verify {field}") from None
        if process.returncode != 0:
            raise HarnessRunnerError(f"Could not verify {field}")
        return b"".join(output_chunks)
    except HarnessRunnerError:
        raise
    except (OSError, subprocess.TimeoutExpired):
        if process is not None and process.poll() is None:
            try:
                process.kill()
            except OSError:
                pass
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass
        raise HarnessRunnerError(f"Could not verify {field}") from None
    finally:
        if process is not None and process.stdout is not None:
            try:
                process.stdout.close()
            except (OSError, ValueError):
                pass


def _resolve_git_commit(root: Path, value: str, field: str) -> str:
    """Require a full immutable commit SHA, not a branch name or abbreviated ref."""
    if not isinstance(value, str) or not _SHA_RE.fullmatch(value):
        raise HarnessRunnerError(f"{field} must be a full 40-character Git commit SHA")
    resolved = _git_text(
        root,
        ["rev-parse", "--verify", "--end-of-options", f"{value}^{{commit}}"],
        field,
    ).lower()
    if not _SHA_RE.fullmatch(resolved) or resolved != value.lower():
        raise HarnessRunnerError(f"{field} must identify an existing Git commit")
    return resolved


def _build_git_bound_review_input(
    root: Path,
    source_bytes: bytes,
    base_value: str,
    head_value: str,
    current_head: str,
) -> tuple[bytes, dict[str, Any]]:
    """Replace caller diff fields with a bounded diff derived from immutable Git commits."""
    base_sha = _resolve_git_commit(root, base_value, "review-base")
    head_sha = _resolve_git_commit(root, head_value, "review-head")
    if head_sha != current_head.lower():
        raise HarnessRunnerError("review-head must equal the checked-out Git HEAD")

    merge_base = _git_text(root, ["merge-base", base_sha, head_sha], "Git review merge-base").lower()
    if not _SHA_RE.fullmatch(merge_base):
        raise HarnessRunnerError("Could not verify Git review merge-base")

    diff_bytes = _git_bytes_bounded(
        root,
        [
            "-c", "core.quotePath=false", "diff",
            "--no-ext-diff", "--no-textconv", "--no-renames", "--no-color",
            "--unified=3", merge_base, head_sha, "--",
        ],
        "Git-generated semantic-review diff",
    )
    if not diff_bytes:
        raise HarnessRunnerError("Git base/head range contains no reviewable changes")
    try:
        diff = diff_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HarnessRunnerError("Git-generated semantic-review diff is not valid UTF-8") from None

    names_bytes = _git_bytes_bounded(
        root,
        ["diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--name-only", "-z",
         merge_base, head_sha, "--"],
        "Git review changed-file list",
    )
    try:
        changed_files = sorted(name.decode("utf-8") for name in names_bytes.split(b"\0") if name)
    except UnicodeDecodeError:
        raise HarnessRunnerError("Git review changed-file paths are not valid UTF-8") from None
    if not changed_files or len(changed_files) != len(set(changed_files)):
        raise HarnessRunnerError("Git review changed-file list is empty or ambiguous")

    try:
        payload = json.loads(
            source_bytes.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (UnicodeError, ValueError):
        raise HarnessRunnerError("review-input must be valid UTF-8 JSON for Git-bound review") from None
    if not isinstance(payload, dict):
        raise HarnessRunnerError("review-input must be a JSON object for Git-bound review")

    # In strict mode these fields are never trusted from the caller.
    payload["diff"] = diff
    payload["changed_files"] = changed_files
    try:
        validate_input(payload)
        _validate_diff_integrity(payload)
    except ReviewError:
        raise HarnessRunnerError(
            "Git-generated review diff failed semantic-review input validation"
        ) from None

    task_bytes = (json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    if len(task_bytes) > _MAX_REVIEW_INPUT_BYTES:
        raise HarnessRunnerError("Git-bound semantic-review input exceeds the 4 MiB input limit")

    provenance = {
        "base_sha": base_sha,
        "head_sha": head_sha,
        "merge_base_sha": merge_base,
        "diff_sha256": hashlib.sha256(diff_bytes).hexdigest(),
        "changed_files": changed_files,
    }
    return task_bytes, provenance


def _read_review_input(path: Path, field: str) -> bytes:
    """Read caller-supplied review input once so the exact bytes can be passed to the child."""
    try:
        with path.open("rb") as source:
            data = source.read(_MAX_REVIEW_INPUT_BYTES + 1)
    except OSError:
        raise HarnessRunnerError(f"Could not verify {field}") from None
    if len(data) > _MAX_REVIEW_INPUT_BYTES:
        raise HarnessRunnerError(f"{field} exceeds the 4 MiB input limit")
    return data


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


def _invalidate_safe_outputs(
    root: Path | None,
    outputs: list[tuple[Path, str]],
    protected_paths: tuple[str | None, ...],
) -> None:
    """Remove stale generated outputs on blocked runs without unlinking input aliases."""
    if root is None:
        return
    protected_resolved: set[Path] = set()
    aliasing_uncertain = False
    for value in protected_paths:
        if value is None:
            continue
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = root / candidate
        try:
            protected_resolved.add(candidate.resolve(strict=False))
        except (OSError, RuntimeError):
            # If aliasing cannot be ruled out, preserve outputs rather than risk input loss.
            aliasing_uncertain = True
            break
    if aliasing_uncertain:
        return

    for output, raw_output in outputs:
        try:
            _reject_symlink_path(root, raw_output, "generated output")
            _require_artifact_path(root, output, "generated output")
            if output.resolve(strict=False) in protected_resolved:
                continue
            output.unlink()
        except (HarnessRunnerError, OSError, RuntimeError, ValueError):
            # Cleanup is best-effort; never replace the original blocked-run error.
            pass


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
    parser.add_argument("--review-base", help="Optional full Git commit SHA for strict Git-bound semantic review")
    parser.add_argument("--review-head", help="Optional full Git commit SHA for strict Git-bound semantic review")
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=600,
        help=f"Per-task timeout in seconds (1-{_MAX_TIMEOUT_SECONDS}; default 600)",
    )
    args = parser.parse_args(argv)
    root: Path | None = None
    safe_outputs: list[tuple[Path, str]] = []

    try:
        if not 1 <= args.timeout_seconds <= _MAX_TIMEOUT_SECONDS:
            raise HarnessRunnerError(
                f"timeout-seconds must be between 1 and {_MAX_TIMEOUT_SECONDS}"
            )
        root = Path(args.project_root).resolve()
        if not root.is_dir():
            raise HarnessRunnerError("project-root must be an existing directory")
        report_path = _resolve_inside_root(root, args.report_output, "report-output")
        _reject_symlink_path(root, args.report_output, "report-output")
        _require_artifact_path(root, report_path, "report-output")
        safe_outputs.append((report_path, args.report_output))
        review_output = (
            _resolve_inside_root(root, args.review_output, "review-output")
            if args.review_output is not None else None
        )
        if args.review_output is not None and review_output is not None:
            _reject_symlink_path(root, args.review_output, "review-output")
            _require_artifact_path(root, review_output, "review-output")
            safe_outputs.append((review_output, args.review_output))

        # Resolve output paths first so later input/path errors can invalidate stale
        # generated artifacts. Cleanup protects any output that aliases an input path.
        config_path = _resolve_inside_root(root, args.config, "config")
        _reject_symlink_path(root, args.config, "config")
        review_input = (
            _resolve_inside_root(root, args.review_input, "review-input")
            if args.review_input is not None else None
        )
        if args.review_input is not None:
            _reject_symlink_path(root, args.review_input, "review-input")
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

        # Invalidate previous successful artifacts before config validation or task
        # execution, so a blocked run cannot leave a stale PASS for consumers.
        _require_artifact_path(root, report_path, "report-output")
        if review_output is not None:
            _require_artifact_path(root, review_output, "review-output")
        for output in (report_path, review_output):
            if output is not None:
                try:
                    output.unlink()
                except FileNotFoundError:
                    pass

        _require_tracked_config(root, config_path)


        try:
            raw_config = json.loads(
                config_path.read_text(encoding="utf-8"),
                object_pairs_hook=_reject_duplicate_json_keys,
            )
        except (OSError, UnicodeError, ValueError):
            raise HarnessRunnerError("Could not read a valid JSON Harness config") from None
        config = validate_harness_config(raw_config)

        wants_review = "semantic-review" in config["commands"]
        strict_review = args.review_base is not None or args.review_head is not None
        if strict_review and (args.review_base is None or args.review_head is None):
            raise HarnessRunnerError("--review-base and --review-head must be supplied together")
        if strict_review and not wants_review:
            raise HarnessRunnerError("--review-base and --review-head require semantic-review in config")
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
        review_input_bytes = (
            _read_review_input(review_input, "review-input")
            if review_input is not None else None
        )
        review_input_sha = (
            hashlib.sha256(review_input_bytes).hexdigest()
            if review_input_bytes is not None else None
        )
        if review_output is not None:
            review_output.parent.mkdir(parents=True, exist_ok=True)

        # Reject ignored project Python sources before planning or executing tasks.
        _reject_ignored_python_sources(root)

        # Preflight every task before executing any of them, avoiding partial execution if
        # a configured task lacks its required arguments or implementation.
        planned_tasks = [
            (task_id, _task_argv(task_id, root, review_input, review_output))
            for task_id in config["commands"]
        ]
        commit_sha = _git_commit_sha(root)
        review_task_bytes = review_input_bytes
        review_provenance: dict[str, Any] | None = None
        if strict_review:
            if review_input_bytes is None:
                raise HarnessRunnerError("Git-bound semantic-review requires --review-input")
            review_task_bytes, review_provenance = _build_git_bound_review_input(
                root, review_input_bytes, args.review_base, args.review_head, commit_sha
            )
        rules_pin = _rules_pin(root)
        outcomes: dict[str, str] = {}
        failed = False
        for task_id, argv_for_task in planned_tasks:
            if failed:
                outcomes[task_id] = "not_run"
                print(f"Task {task_id}: not_run (an earlier task failed)")
                continue
            if task_id == "semantic-review" and review_input is not None:
                # Earlier tests are trusted repository code, but they may still mutate
                # generated or tracked inputs. Do not review bytes different from those
                # validated during preflight.
                _reject_symlink_path(root, args.review_input, "review-input")
                current_review_input = _read_review_input(
                    review_input, "review-input"
                )
                if (
                    review_input_sha is None
                    or hashlib.sha256(current_review_input).hexdigest() != review_input_sha
                ):
                    raise HarnessRunnerError("review-input changed during task execution")
            task_stdin = (
                review_task_bytes if task_id == "semantic-review" else None
            )
            status, exit_code = _run_task(
                argv_for_task, root, args.timeout_seconds, task_stdin
            )
            outcomes[task_id] = status
            suffix = " (timeout or launch failure)" if exit_code is None and status == "failed" else (
                f" (exit {exit_code})" if exit_code not in (None, 0) else ""
            )
            print(f"Task {task_id}: {status}{suffix}")
            failed = status != "passed"

        # Tests or hooks may edit tracked/untracked source or move HEAD. Recheck
        # full source-tree cleanliness as well as the commit before reporting success.
        _reject_ignored_python_sources(root)
        post_task_sha = _git_commit_sha(root)
        if post_task_sha != commit_sha:
            raise HarnessRunnerError("Git HEAD changed during task execution")

        # Revalidate generated output paths immediately before report emission.
        _reject_symlink_path(root, args.report_output, "report-output")
        _require_artifact_path(root, report_path, "report-output")
        if args.review_output is not None:
            _reject_symlink_path(root, args.review_output, "review-output")
            if review_output is not None:
                _require_artifact_path(root, review_output, "review-output")

        metadata = {
            "commit_sha": commit_sha,
            "rules_pin": rules_pin,
            "tool_version": f"dev-workflow-kit/harness-runner@{commit_sha}",
            "tests": outcomes,
        }
        if review_provenance is not None:
            metadata["review_provenance"] = review_provenance
        report = _write_report(report_path, metadata)
        print(f"Acceptance report written: {report_path.relative_to(root).as_posix()}")
        print(f"Acceptance status: {report['status']}")
        return 0 if report["status"] == "passed" else 1
    except (HarnessRunnerError, HarnessConfigError, AcceptanceReportError) as exc:
        _invalidate_safe_outputs(root, safe_outputs, (args.config, args.review_input))
        print(f"Harness run blocked: {exc}", file=sys.stderr)
        return 2
    except OSError:
        _invalidate_safe_outputs(root, safe_outputs, (args.config, args.review_input))
        print("Harness run blocked: filesystem operation failed", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
