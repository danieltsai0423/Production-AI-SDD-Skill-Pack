#!/usr/bin/env python3
"""Install the pack's deterministic hooks into a repository.

Does two things (both idempotent, both optional via flags):
  1. git pre-commit: writes .git/hooks/pre-commit to invoke hooks/common/pre_commit.py
     (secret guard + protected files + spec-required gate) unless one already exists.
  2. Claude Code settings: copies .claude/settings.example.json to .claude/settings.json if absent
     (never overwrites an existing settings.json; prints a merge hint instead).

Usage:
  python scripts/install_hooks.py                 # both, safe/no-clobber
  python scripts/install_hooks.py --git-only
  python scripts/install_hooks.py --dry-run
Exit code 0 = done, 1 = error.
"""
from __future__ import annotations

import argparse
import shutil
import stat
import subprocess
import sys
from pathlib import Path

PRE_COMMIT = """#!/bin/sh
# Installed by Production AI SDD Skill Pack (scripts/install_hooks.py)
exec python hooks/common/pre_commit.py
"""


def git_dir(root: Path) -> Path | None:
    try:
        p = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=root,
                           capture_output=True, text=True)
        if p.returncode == 0:
            gd = Path(p.stdout.strip())
            return gd if gd.is_absolute() else root / gd
    except FileNotFoundError:
        return None
    return None


def install_git_hook(root: Path, dry_run: bool) -> str:
    gd = git_dir(root)
    if gd is None:
        return "skip: not a git repository"
    hook = gd / "hooks" / "pre-commit"
    if hook.exists():
        return f"skip: {hook} already exists (leaving it untouched)"
    if dry_run:
        return f"[dry-run] would write {hook}"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(PRE_COMMIT, encoding="utf-8")
    hook.chmod(hook.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return f"installed: {hook}"


def install_claude_settings(root: Path, dry_run: bool) -> str:
    example = root / ".claude" / "settings.example.json"
    target = root / ".claude" / "settings.json"
    if not example.exists():
        return "skip: .claude/settings.example.json not found"
    if target.exists():
        return f"skip: {target} exists - merge hooks from settings.example.json manually"
    if dry_run:
        return f"[dry-run] would copy settings.example.json -> {target}"
    shutil.copyfile(example, target)
    return f"installed: {target}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--git-only", action="store_true")
    ap.add_argument("--claude-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent

    steps = []
    if not args.claude_only:
        steps.append(install_git_hook(root, args.dry_run))
    if not args.git_only:
        steps.append(install_claude_settings(root, args.dry_run))

    for s in steps:
        print(f"  {s}")
    print("\nEnforcement mode via PAI_SDD_ENFORCEMENT = strict | standard | advisory (default standard).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
