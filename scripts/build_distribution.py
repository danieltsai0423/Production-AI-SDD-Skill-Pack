#!/usr/bin/env python3
"""Build a distributable archive of the pack (sec. 15, sec. 23.3).

Packages the redistributable parts of the pack (canonical skills, templates, schemas, profiles,
agent rule files, installer/validators, and the pack manifest) into
dist/production-ai-sdd-skill-pack-<version>.zip and writes a SHA256SUMS file. Development-only
content (evals fixtures, workbench, generated adapter copies, git metadata) is excluded.

Version is read from pack.yaml.

Usage: python scripts/build_distribution.py [--out-dir dist]
Exit code 0 = built, 1 = error.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path

INCLUDE_DIRS = ["skills", "templates", "schemas", "profiles", "scripts", "docs", "hooks"]
INCLUDE_FILES = ["AGENTS.md", "CLAUDE.md", "pack.yaml", "README.md", "README.zh-TW.md",
                 "LICENSE", "CHANGELOG.md"]
EXCLUDE_PARTS = {"__pycache__", ".git", ".agents", ".claude", ".codex", "workbench", "dist"}


def pack_version(root: Path) -> str:
    m = re.search(r"^version:\s*(\S+)", (root / "pack.yaml").read_text(encoding="utf-8"), re.MULTILINE)
    return m.group(1) if m else "0.0.0"


def iter_files(root: Path):
    for d in INCLUDE_DIRS:
        base = root / d
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if f.is_file() and not any(part in EXCLUDE_PARTS for part in f.parts):
                yield f
    for name in INCLUDE_FILES:
        f = root / name
        if f.is_file():
            yield f


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default="dist")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    version = pack_version(root)
    out_dir = (root / args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    archive = out_dir / f"production-ai-sdd-skill-pack-{version}.zip"
    files = list(iter_files(root))
    if not files:
        print("FAIL: nothing to package.")
        return 1

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.relative_to(root).as_posix())

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (out_dir / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")

    print(f"PASS: packaged {len(files)} file(s) -> {archive.relative_to(root)}")
    print(f"  version: {version}")
    print(f"  sha256:  {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
