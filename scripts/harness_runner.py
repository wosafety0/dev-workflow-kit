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
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

# Keep the documented ``python scripts/harness_runner.py`` entry point working.
# Direct script execution places scripts/ rather than the repository root on sys.path.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

class HarnessRunnerError(ValueError):
    """Raised when runner inputs or local project metadata are unsafe or incomplete."""


_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_MAX_TIMEOUT_SECONDS = 3600
_MAX_REVIEW_INPUT_BYTES = 4 * 1024 * 1024


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
            timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise HarnessRunnerError("Could not verify ignored Python source") from None
    if ignored.returncode != 0:
        raise HarnessRunnerError("Could not verify ignored Python source")
    root_environment_dirs = {".venv", "venv", "env", ".tox", "artifacts"}
    for raw_path in ignored.stdout.split(b"\0"):
        if not raw_path:
            continue
        ignored_path = Path(os.fsdecode(raw_path))
        if ignored_path.suffix not in {".py", ".pyc", ".so", ".pyd"}:
            continue
        parent_parts = ignored_path.parts[:-1]
        # Only recognized repository-root environments/artifacts are excluded.
        # A nested directory named "env" or ".venv-custom" may contain mutable
        # project code and must not silently bypass the ignored-source guard.
        if "__pycache__" in parent_parts or (
            parent_parts and parent_parts[0] in root_environment_dirs
        ):
            continue
        raise HarnessRunnerError("ignored Python source must not be executed")


def _load_trusted_helpers(root: Path):
    """Load project helper modules after source checks, bypassing repository pyc caches."""
    helper_paths = (
        ("scripts/harness_config.py", "Harness config module"),
        ("scripts/acceptance_report.py", "acceptance report module"),
    )
    for relative, label in helper_paths:
        source = _resolve_trusted_source(root, relative, label)
        if not source.is_file():
            raise HarnessRunnerError(f"{label} is missing")

    try:
        with tempfile.TemporaryDirectory(prefix="harness-import-cache-") as cache_dir:
            cache_path = Path(cache_dir).resolve()
            try:
                cache_path.relative_to(root.resolve())
            except ValueError:
                pass
            else:
                raise HarnessRunnerError("temporary Python import cache must be outside the project root")
            old_prefix = sys.pycache_prefix
            old_dont_write = sys.dont_write_bytecode
            sys.pycache_prefix = str(cache_path)
            sys.dont_write_bytecode = True
            try:
                loaded_modules = {}
                for module_name, relative in (
                    ("_harness_trusted_config", "scripts/harness_config.py"),
                    ("_harness_trusted_report", "scripts/acceptance_report.py"),
                ):
                    source_path = root / relative
                    spec = importlib.util.spec_from_file_location(module_name, source_path)
                    if spec is None or spec.loader is None:
                        raise ImportError("trusted helper module has no source loader")
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    loaded_modules[module_name] = module
                config_module = loaded_modules["_harness_trusted_config"]
                report_module = loaded_modules["_harness_trusted_report"]
            finally:
                sys.pycache_prefix = old_prefix
                sys.dont_write_bytecode = old_dont_write
    except Exception:
        raise HarnessRunnerError("Could not load trusted Harness helper modules") from None
    return report_module.build_acceptance_report, config_module.validate_harness_config


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
        return [sys.executable, "-I", "-S", "-m", "unittest", "discover", "-s", "tests", "-v"]
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
            "-I",
            "-S",
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


def _verify_review_diff_provenance(
    root: Path, review_input_bytes: bytes, base_commit: str
) -> None:
    """Bind caller-supplied review diff bytes to the current HEAD and an explicit base."""
    if not isinstance(base_commit, str) or not _SHA_RE.fullmatch(base_commit):
        raise HarnessRunnerError("--review-base-commit must be a full 40-character Git commit SHA")
    try:
        payload = json.loads(
            review_input_bytes.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (UnicodeError, ValueError):
        raise HarnessRunnerError("review-input must be valid UTF-8 JSON for provenance verification") from None
    if not isinstance(payload, dict) or not isinstance(payload.get("diff"), str):
        raise HarnessRunnerError("review-input must contain a string diff for provenance verification")
    if not isinstance(payload.get("changed_files"), list):
        raise HarnessRunnerError("review-input must contain changed_files for provenance verification")

    def run_git(*args: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=20,
            check=False,
        )

    try:
        head = run_git("rev-parse", "HEAD")
        if head.returncode != 0:
            raise HarnessRunnerError("Could not resolve source commit for review provenance")
        source_commit = head.stdout.decode("ascii", errors="strict").strip().lower()
        if not _SHA_RE.fullmatch(source_commit):
            raise HarnessRunnerError("Could not resolve source commit for review provenance")
        resolved_base = run_git("rev-parse", "--verify", f"{base_commit.lower()}^{{commit}}")
        if resolved_base.returncode != 0 or (
            resolved_base.stdout.decode("ascii", errors="strict").strip().lower() != base_commit.lower()
        ):
            raise HarnessRunnerError("--review-base-commit must identify an available Git commit")
        merge_base = run_git("merge-base", base_commit.lower(), source_commit)
        if merge_base.returncode != 0 or not _SHA_RE.fullmatch(
            merge_base.stdout.decode("ascii", errors="strict").strip()
        ):
            raise HarnessRunnerError("review base and source commit must share a Git merge base")
        expected = run_git(
            "diff",
            "--binary",
            "--full-index",
            "--no-ext-diff",
            "--no-textconv",
            "--no-color",
            "--no-renames",
            "--no-relative",
            "--diff-algorithm=myers",
            "--src-prefix=a/",
            "--dst-prefix=b/",
            f"{base_commit.lower()}...{source_commit}",
            "--",
        )
    except (OSError, subprocess.TimeoutExpired, UnicodeError):
        raise HarnessRunnerError("Could not verify semantic-review diff provenance") from None
    if expected.returncode != 0:
        raise HarnessRunnerError("Could not generate canonical Git diff for semantic-review provenance")
    try:
        supplied_diff = payload["diff"].encode("utf-8")
    except UnicodeEncodeError:
        raise HarnessRunnerError("review-input diff contains invalid Unicode") from None
    if supplied_diff != expected.stdout:
        raise HarnessRunnerError(
            "review-input diff does not exactly match the canonical Git diff from --review-base-commit to HEAD"
        )


def _write_report(
    output_path: Path,
    metadata: dict[str, Any],
    build_acceptance_report: Any,
) -> dict[str, Any]:
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
    parser.add_argument("--review-base-commit", help="Full Git commit SHA of the target base used to generate the review diff")
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

        # Verify source integrity before importing any project helper modules.
        commit_sha = _git_commit_sha(root)
        _reject_ignored_python_sources(root)
        build_acceptance_report, validate_harness_config = _load_trusted_helpers(root)

        try:
            raw_config = json.loads(
                config_path.read_text(encoding="utf-8"),
                object_pairs_hook=_reject_duplicate_json_keys,
            )
        except (OSError, UnicodeError, ValueError):
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
        if wants_review and not args.review_base_commit:
            raise HarnessRunnerError("semantic-review requires --review-base-commit")
        if not wants_review and (review_input is not None or review_output is not None or args.review_base_commit is not None):
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

        # Preflight every task before executing any of them, avoiding partial execution if
        # a configured task lacks its required arguments or implementation.
        planned_tasks = [
            (task_id, _task_argv(task_id, root, review_input, review_output))
            for task_id in config["commands"]
        ]
        if wants_review and review_input_bytes is not None:
            _verify_review_diff_provenance(root, review_input_bytes, args.review_base_commit)
            print(f"Semantic review diff provenance: verified against {args.review_base_commit.lower()}...HEAD")
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
                review_input_bytes if task_id == "semantic-review" else None
            )
            # Give every child a fresh private bytecode-cache prefix so it cannot
            # load ignored or poisoned .pyc files from project __pycache__ directories.
            with tempfile.TemporaryDirectory(prefix="harness-task-pycache-") as task_cache:
                task_cache_path = Path(task_cache).resolve()
                try:
                    task_cache_path.relative_to(root.resolve())
                except ValueError:
                    pass
                else:
                    raise HarnessRunnerError("temporary task bytecode cache must be outside the project root")
                isolated_argv = [
                    argv_for_task[0],
                    "-B",
                    "-X",
                    f"pycache_prefix={task_cache_path}",
                    *argv_for_task[1:],
                ]
                status, exit_code = _run_task(
                    isolated_argv, root, args.timeout_seconds, task_stdin
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
        report = _write_report(report_path, metadata, build_acceptance_report)
        print(f"Acceptance report written: {report_path.relative_to(root).as_posix()}")
        print(f"Acceptance status: {report['status']}")
        return 0 if report["status"] == "passed" else 1
    except (HarnessRunnerError, ValueError) as exc:
        _invalidate_safe_outputs(root, safe_outputs, (args.config, args.review_input))
        print(f"Harness run blocked: {exc}", file=sys.stderr)
        return 2
    except OSError:
        _invalidate_safe_outputs(root, safe_outputs, (args.config, args.review_input))
        print("Harness run blocked: filesystem operation failed", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
