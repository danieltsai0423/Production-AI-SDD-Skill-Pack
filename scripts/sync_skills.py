#!/usr/bin/env python3
"""Sync canonical skills/ into installed adapter copies, or check for drift.

The canonical source of truth is skills/. Adapter copies live under .agents/skills/ (Codex) and
.claude/skills/ (Claude Code). This script keeps them consistent:

  --check   : compare each canonical skill's hash to its installed copy; exit 1 on any drift or
              missing/extra skill. Makes adapter consistency a CI-enforceable gate (read-only).
  (default) : re-copy canonical skills into the targets that already exist, healing drift.

Only targets that are already present are considered, so running --check in a fresh checkout that
has not installed adapters is a pass with a note. Use install.py to create adapters initially.

Usage:
  python scripts/sync_skills.py --check --targets codex claude
  python scripts/sync_skills.py --targets claude
Exit code 0 = in sync / synced, 1 = drift found (in --check) or error.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from install import TARGET_SUBDIR, base_dir, sha256_of_dir


def canonical_skills(skills_dir: Path) -> list[Path]:
    return sorted(p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def check_target(dest_root: Path, skills: list[Path]) -> list[str]:
    drift: list[str] = []
    canon_names = {s.name for s in skills}
    for skill in skills:
        dest = dest_root / skill.name
        if not dest.exists():
            drift.append(f"missing installed copy: {dest_root.name}/{skill.name}")
        elif sha256_of_dir(dest) != sha256_of_dir(skill):
            drift.append(f"drift: {dest_root.name}/{skill.name} differs from canonical skills/")
    if dest_root.is_dir():
        for extra in sorted(p for p in dest_root.iterdir() if p.is_dir()):
            if extra.name not in canon_names:
                drift.append(f"orphan: {dest_root.name}/{extra.name} has no canonical source")
    return drift


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--targets", nargs="+", choices=list(TARGET_SUBDIR), default=list(TARGET_SUBDIR))
    ap.add_argument("--scope", choices=["repo", "user"], default="repo")
    ap.add_argument("--check", action="store_true", help="report drift without modifying files")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        print("FAIL: skills/ not found")
        return 1
    skills = canonical_skills(skills_dir)

    present = {t: base_dir(args.scope, root) / TARGET_SUBDIR[t] for t in args.targets}
    present = {t: p for t, p in present.items() if p.is_dir()}
    if not present:
        print("PASS: no installed adapter copies found (nothing to sync). Run install.py first.")
        return 0

    if args.check:
        all_drift: list[str] = []
        for target, dest_root in present.items():
            all_drift += check_target(dest_root, skills)
        if all_drift:
            print(f"FAIL: {len(all_drift)} drift issue(s):")
            for d in all_drift:
                print(f"  - {d}")
            print("Run: python scripts/sync_skills.py  (to heal)")
            return 1
        print(f"PASS: {len(skills)} skill(s) in sync across {len(present)} target(s).")
        return 0

    healed = 0
    for target, dest_root in present.items():
        for skill in skills:
            dest = dest_root / skill.name
            if not dest.exists() or sha256_of_dir(dest) != sha256_of_dir(skill):
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(skill, dest)
                healed += 1
        for extra in sorted(p for p in dest_root.iterdir() if p.is_dir()):
            if extra.name not in {s.name for s in skills}:
                shutil.rmtree(extra)
                healed += 1
    print(f"PASS: synced {len(present)} target(s); {healed} change(s) applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
