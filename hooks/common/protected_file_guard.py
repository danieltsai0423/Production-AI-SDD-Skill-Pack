#!/usr/bin/env python3
"""Gate B - protected file guard (sec. 14.1.B).

Blocks writes/edits to files that should not be changed casually:
  - production credential files (.env.production, *.pem, *.key, credentials*)
  - lockfiles (per project policy)
  - migration history (migrations/**)
  - generated specs / traceability (traceability.json|md, generated markers)
  - release manifests (pack.yaml version line changes are allowed; the file is not blocked)
  - the install manifest (.pai-sdd-install-manifest.json)

Projects extend the list via a .pai-sdd-protected file (one glob per line). Claude Code PreToolUse:
inspects the target path. git pre-commit: with --staged, checks staged names.
"""
from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import allow, block, read_payload, tool_context  # noqa: E402

DEFAULT_PROTECTED = [
    "**/.env.production", "**/.env.*.local", "**/*.pem", "**/*.key",
    "**/credentials*", "**/id_rsa*",
    "**/migrations/**", "**/migration_history/**",
    "**/traceability.json", "**/traceability.md",
    ".pai-sdd-install-manifest.json",
    "**/package-lock.json", "**/poetry.lock", "**/yarn.lock", "**/pnpm-lock.yaml",
]


def protected_globs(root: Path) -> list[str]:
    globs = list(DEFAULT_PROTECTED)
    cfg = root / ".pai-sdd-protected"
    if cfg.exists():
        for line in cfg.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                globs.append(line)
    return globs


def is_protected(path: str, globs: list[str]) -> bool:
    norm = path.replace("\\", "/").lstrip("./")
    return any(fnmatch.fnmatch(norm, g) or fnmatch.fnmatch(Path(norm).name, g) for g in globs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--staged", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent.parent
    globs = protected_globs(root)

    if args.staged:
        try:
            p = subprocess.run(["git", "diff", "--cached", "--name-only"],
                               cwd=root, capture_output=True, text=True)
            names = [l.strip() for l in p.stdout.splitlines() if l.strip()]
        except FileNotFoundError:
            names = []
        hit = [n for n in names if is_protected(n, globs)]
        if hit:
            return block(f"staged changes touch protected file(s): {', '.join(hit[:5])}",
                         "unstage them, or override intentionally via .pai-sdd-protected policy")
        return allow(f"protected_file_guard: staged scan clean ({len(names)} file(s)).")

    payload = read_payload()
    tool, tin = tool_context(payload)
    if tool in ("Write", "Edit", "MultiEdit"):
        fp = tin.get("file_path", "")
        if fp and is_protected(fp, globs):
            return block(f"{tool} targets a protected file: {fp}",
                         "this file is protected by policy; change it deliberately outside the agent "
                         "or adjust .pai-sdd-protected")
    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
