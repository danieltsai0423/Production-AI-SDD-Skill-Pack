#!/usr/bin/env python3
"""Remove installed adapter skill copies recorded in the install manifest.

Reads .pai-sdd-install-manifest.json (repo or user scope), removes each skill directory it recorded
under each target, and deletes the manifest. Only skills the manifest recorded are removed, so a
skill placed by something else is left alone. Supports --dry-run.

Usage:
  python scripts/uninstall.py --scope repo
  python scripts/uninstall.py --scope user --dry-run
Exit code 0 = success (including nothing-to-do), 1 = error.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from install import base_dir


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scope", choices=["repo", "user"], default="repo")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    manifest_path = base_dir(args.scope, root) / ".pai-sdd-install-manifest.json"
    if not manifest_path.exists():
        print(f"PASS: no manifest at {manifest_path} - nothing to uninstall.")
        return 0

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: manifest is not valid JSON: {e}")
        return 1

    removed = 0
    for target, info in manifest.get("targets", {}).items():
        dest_root = Path(info.get("path", ""))
        for entry in info.get("skills", []):
            dest = dest_root / entry["skill"]
            if dest.exists():
                print(f"  [{'dry-run' if args.dry_run else 'remove'}] {target}: {dest}")
                if not args.dry_run:
                    shutil.rmtree(dest)
                removed += 1

    if args.dry_run:
        print(f"\nDry run: would remove {removed} skill copy(ies); manifest kept.")
        return 0

    manifest_path.unlink()
    print(f"\nPASS: removed {removed} skill copy(ies) and manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
