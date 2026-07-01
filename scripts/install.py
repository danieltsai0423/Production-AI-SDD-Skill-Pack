#!/usr/bin/env python3
"""Install the canonical skills/ into agent discovery paths (copy strategy).

Copies each skills/<name>/ into the chosen targets and writes an install manifest so a later
uninstall or drift check can reason about what was placed. Copy is used (not symlink) so the same
command works on Windows, WSL2, macOS, and Linux.

Targets:
  codex  -> .agents/skills/<name>/   (repo scope) or ~/.agents/skills/<name>/ (user scope)
  claude -> .claude/skills/<name>/   (repo scope) or ~/.claude/skills/<name>/ (user scope)

Usage:
  python scripts/install.py --targets codex claude --scope repo --mode copy
  python scripts/install.py --targets claude --scope user --dry-run

Exit code 0 = success, 1 = error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

TARGET_SUBDIR = {"codex": ".agents/skills", "claude": ".claude/skills"}


def sha256_of_dir(path: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(path.rglob("*")):
        if f.is_file():
            h.update(f.relative_to(path).as_posix().encode())
            h.update(f.read_bytes())
    return h.hexdigest()


def base_dir(scope: str, root: Path) -> Path:
    return root if scope == "repo" else Path.home()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--targets", nargs="+", choices=list(TARGET_SUBDIR), required=True)
    ap.add_argument("--scope", choices=["repo", "user"], default="repo")
    ap.add_argument("--mode", choices=["copy"], default="copy",
                    help="only copy is supported for cross-platform reliability")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        print("FAIL: skills/ not found")
        return 1

    skills = sorted(p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    manifest = {
        "pack": "production-ai-sdd-skill-pack",
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "scope": args.scope,
        "mode": args.mode,
        "targets": {},
    }

    for target in args.targets:
        dest_root = base_dir(args.scope, root) / TARGET_SUBDIR[target]
        entries = []
        print(f"\n{target}: {dest_root}")
        for skill in skills:
            dest = dest_root / skill.name
            digest = sha256_of_dir(skill)
            action = "copy"
            if dest.exists():
                # Do not clobber a skill we did not place / that differs unexpectedly.
                action = "overwrite" if sha256_of_dir(dest) != digest else "unchanged"
            print(f"  [{'dry-run' if args.dry_run else action}] {skill.name}")
            if not args.dry_run:
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(skill, dest)
            entries.append({"skill": skill.name, "sha256": digest, "action": action})
        manifest["targets"][target] = {"path": str(dest_root), "skills": entries}

    if args.dry_run:
        print("\nDry run: no files written, no manifest saved.")
        return 0

    manifest_path = base_dir(args.scope, root) / ".pai-sdd-install-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nPASS: installed {len(skills)} skill(s) to {len(args.targets)} target(s).")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
