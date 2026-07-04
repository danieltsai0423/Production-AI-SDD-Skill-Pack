#!/usr/bin/env python3
"""Gate C + E - spec-required / spec-drift gate (sec. 14.1.C, 14.1.E).

Delegates to scripts/check_spec_drift.py, which deterministically maps changed paths to spec-worthy
surfaces (API/schema, migrations, model/prompt, contracts, auth/tenant, external messaging) and
verifies an accompanying spec/change artifact exists. Runnable as a Claude Code Stop hook (no stdin
needed) or a git pre-commit hook.

Enforcement mode comes from PAI_SDD_ENFORCEMENT and is passed through to the drift checker.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import mode  # noqa: E402


def main() -> int:
    root = Path(__file__).resolve().parent.parent.parent
    checker = root / "scripts" / "check_spec_drift.py"
    if not checker.exists():
        print("[pai-sdd] spec_required_gate: check_spec_drift.py not found; skipping.", file=sys.stderr)
        return 0
    result = subprocess.run([sys.executable, str(checker), "--mode", mode()],
                            cwd=root, capture_output=True, text=True)
    out = (result.stdout + result.stderr).strip()
    # Drift checker returns 2 when not a git repo -> treat as a non-blocking skip.
    if result.returncode == 2:
        print("[pai-sdd] spec_required_gate: not a git repo; skipping.", file=sys.stderr)
        return 0
    if result.returncode != 0:
        print(out, file=sys.stderr)
        print("[pai-sdd] BLOCKED: add or update the spec/change for this surface "
              "(pai-sdd-specify / pai-sdd-change).", file=sys.stderr)
        return 2
    print(out, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
