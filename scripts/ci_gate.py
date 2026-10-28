"""Fail CI unless every required orchestration stage completed successfully."""
from __future__ import annotations

import sys

_REQUIRED_STAGES = ("tests", "report", "artifact")


def gate_passes(*outcomes: str) -> bool:
    """Only exact success for tests, report generation, and artifact upload opens the gate."""
    return len(outcomes) == len(_REQUIRED_STAGES) and all(
        outcome == "success" for outcome in outcomes
    )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != len(_REQUIRED_STAGES):
        print(
            "Usage: python scripts/ci_gate.py <test-outcome> <report-outcome> <artifact-outcome>",
            file=sys.stderr,
        )
        return 2

    failed_stages = [
        stage for stage, outcome in zip(_REQUIRED_STAGES, args) if outcome != "success"
    ]
    if failed_stages:
        print(
            "Acceptance gate closed; unsuccessful required stage(s): "
            + ", ".join(failed_stages),
            file=sys.stderr,
        )
        return 1

    print("Acceptance orchestration gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
