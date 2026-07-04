#!/usr/bin/env python3
"""git pre-commit orchestrator: secret guard + protected files + spec-required gate.

Installed to .git/hooks/pre-commit by scripts/install_hooks.py. Runs the staged-mode guards and the
spec-drift check; a non-zero result blocks the commit with actionable output. Respects
PAI_SDD_ENFORCEMENT (advisory never blocks).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

COMMON = Path(__file__).resolve().parent


def run(script: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(COMMON / script), *args]).returncode


def main() -> int:
    rc = 0
    rc |= run("secret_guard.py", "--staged")
    rc |= run("protected_file_guard.py", "--staged")
    rc |= run("spec_required_gate.py")
    if rc:
        print("\n[pai-sdd] pre-commit blocked. Resolve the issues above or set "
              "PAI_SDD_ENFORCEMENT=advisory to bypass intentionally.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
