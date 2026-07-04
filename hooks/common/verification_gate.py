#!/usr/bin/env python3
"""Gate D - verification gate (sec. 14.1.D).

Runs before the agent stops. Two behaviors:
  1. If a project verification command is configured (env PAI_SDD_VERIFY_CMD, or a .pai-sdd-verify
     file containing the command), run it. Non-zero exit blocks the stop with the command output so
     the agent keeps fixing. This is the "execute the minimum necessary verification" path.
  2. Otherwise, statically check the working tree: if source files changed but no test/eval files
     changed, warn (standard/advisory) or block once (strict), pointing at pai-sdd-verify. It never
     runs an expensive suite it was not told about (sec. 14.2).

Runnable as a Claude Code Stop hook (no stdin needed) or manually.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import mode  # noqa: E402

SOURCE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".rb", ".php", ".rs", ".cs", ".kt"}
TEST_MARKERS = ("test_", "_test", ".test.", ".spec.", "/tests/", "/test/", "spec_", "_spec")


def changed(root: Path) -> list[str]:
    try:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
        if p.returncode != 0:
            return []
    except FileNotFoundError:
        return []
    out = []
    for line in p.stdout.splitlines():
        if len(line) > 3:
            out.append(line[3:].strip().split(" -> ")[-1])
    return out


def is_test(path: str) -> bool:
    low = path.replace("\\", "/").lower()
    return any(m in low for m in TEST_MARKERS)


def verify_command(root: Path) -> str | None:
    cmd = os.environ.get("PAI_SDD_VERIFY_CMD")
    if cmd:
        return cmd
    cfg = root / ".pai-sdd-verify"
    if cfg.exists():
        line = cfg.read_text(encoding="utf-8").strip()
        return line or None
    return None


def main() -> int:
    root = Path(__file__).resolve().parent.parent.parent

    cmd = verify_command(root)
    if cmd:
        print(f"[pai-sdd] verification_gate: running `{cmd}`", file=sys.stderr)
        result = subprocess.run(cmd, cwd=root, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print((result.stdout + result.stderr)[-4000:], file=sys.stderr)
            print(f"[pai-sdd] BLOCKED: verification command failed (exit {result.returncode}).\n"
                  f"          Fix: make `{cmd}` pass, or update the spec/tests, before stopping.",
                  file=sys.stderr)
            return 2
        print("[pai-sdd] verification_gate: verification command passed.", file=sys.stderr)
        return 0

    files = changed(root)
    source = [f for f in files if Path(f).suffix in SOURCE_EXT and not is_test(f)]
    tests = [f for f in files if is_test(f)]
    if source and not tests:
        msg = (f"[pai-sdd] {len(source)} source file(s) changed with no test/eval changes "
               f"(e.g. {source[0]}).")
        fix = ("          Run pai-sdd-verify, add/execute tests or evals, or set PAI_SDD_VERIFY_CMD "
               "so this gate can run them.")
        if mode() == "strict":
            print(msg + "\n[pai-sdd] BLOCKED (strict): unverified source change.\n" + fix, file=sys.stderr)
            return 2
        print(msg + "\n" + fix, file=sys.stderr)
        return 0
    print("[pai-sdd] verification_gate: no unverified source changes detected.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
