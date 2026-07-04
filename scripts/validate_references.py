#!/usr/bin/env python3
"""Validate that Markdown navigation links `[text](path)` across the repo resolve.

Scans Markdown files for real navigation links and checks that each relative target exists (relative
to the file, and as a fallback relative to the repo root). External URLs, anchors, mailto, and
`<placeholder>` tokens are ignored. Backticked bare paths are intentionally NOT treated as links -
they are frequently conceptual artifact names (e.g. `spec.md`) or planned directories mentioned in
prose; validate_skills.py already checks backticked repo paths inside skills/ where the context is
unambiguous.

Usage: python scripts/validate_references.py [--root .]
Exit code 0 = all links resolve, 1 = broken links found.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".agents", ".claude", ".codex", "workbench", "dist"}


def iter_markdown(root: Path):
    for p in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def candidate_targets(text: str) -> set[str]:
    return {m.group(1).strip() for m in MD_LINK_RE.finditer(text)}


def is_checkable(target: str) -> bool:
    if not target or target.startswith(("http://", "https://", "#", "mailto:")):
        return False
    if "<" in target or ">" in target or "*" in target:
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    repo = Path(__file__).resolve().parent.parent
    root = (repo / args.root).resolve()

    errors: list[str] = []
    checked = 0
    for md in iter_markdown(root):
        text = md.read_text(encoding="utf-8", errors="replace")
        for target in candidate_targets(text):
            if not is_checkable(target):
                continue
            clean = target.split("#", 1)[0].rstrip("/")
            if not clean:
                continue
            checked += 1
            if not (md.parent / clean).resolve().exists() and not (repo / clean).resolve().exists():
                errors.append(f"{md.relative_to(repo)}: broken link '{target}'")

    if errors:
        print(f"FAIL: {len(errors)} broken reference(s) ({checked} checked):")
        for e in sorted(errors):
            print(f"  - {e}")
        return 1
    print(f"PASS: {checked} reference(s) resolve across repo Markdown.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
