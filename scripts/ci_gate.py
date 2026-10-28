"""Fail CI unless the named test step completed successfully."""
from __future__ import annotations

import sys


def gate_passes(outcome: str) -> bool:
    """Only the exact GitHub Actions outcome 'success' opens the gate."""
    return outcome == "success"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python scripts/ci_gate.py <test-step-outcome>", file=sys.stderr)
        return 2
    outcome = args[0]
    if not gate_passes(outcome):
        print(f"Offline contract tests did not pass (outcome: {outcome}).", file=sys.stderr)
        return 1
    print("Offline contract-test gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
