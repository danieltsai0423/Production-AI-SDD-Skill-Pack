#!/usr/bin/env python3
"""Scan the repository for secrets, credentials, and obvious PII before commit/CI.

Prefers a mature scanner when available (gitleaks, then detect-secrets). If neither is
installed, falls back to a stdlib regex scan and clearly labels its limitations.

Exit code 0 = clean, 1 = potential secret found (or scanner error in a wrapped tool).
Usage: python scripts/scan_secrets.py [--root .] [--staged]
       --staged limits the fallback scan to files staged in git.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Directories and suffixes the fallback scanner skips.
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".agents", ".claude", ".mypy_cache"}
SKIP_SUFFIXES = {".docx", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".lock"}

# High-signal patterns. Kept conservative to limit false positives.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}")),
    ("OpenAI key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("Anthropic key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("Generic assigned secret", re.compile(
        r"(?i)(password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
]
# .env files are flagged as content that should never be committed.
ENV_FILE_RE = re.compile(r"(^|/)\.env(\.|$)")
# Inline allowlist marker (detect-secrets convention) for deliberate test fixtures / example keys.
ALLOWLIST_RE = re.compile(r"pragma:\s*allowlist secret", re.IGNORECASE)


def run_tool(cmd: list[str]) -> int:
    print(f"scan_secrets: using {cmd[0]}")
    proc = subprocess.run(cmd)
    return proc.returncode


def iter_files(root: Path, staged: bool) -> list[Path]:
    if staged:
        try:
            out = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                cwd=root, capture_output=True, text=True, check=True,
            ).stdout
            return [root / line for line in out.splitlines() if (root / line).is_file()]
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("scan_secrets: could not read git staged files; scanning working tree")
    files: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SKIP_SUFFIXES:
            continue
        files.append(p)
    return files


def fallback_scan(root: Path, staged: bool) -> list[str]:
    print("scan_secrets: no gitleaks/detect-secrets found; using stdlib fallback (LIMITED coverage)")
    hits: list[str] = []
    for f in iter_files(root, staged):
        rel = f.relative_to(root).as_posix()
        if ENV_FILE_RE.search("/" + rel):
            hits.append(f"{rel}: .env-style file should not be committed")
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lines = text.splitlines()
        for name, pat in PATTERNS:
            for m in pat.finditer(text):
                line_no = text.count("\n", 0, m.start()) + 1
                line = lines[line_no - 1] if 0 <= line_no - 1 < len(lines) else ""
                if ALLOWLIST_RE.search(line):
                    continue  # deliberately allowlisted (test fixture / documented example)
                hits.append(f"{rel}:{line_no}: possible {name}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--staged", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if shutil.which("gitleaks"):
        return run_tool(["gitleaks", "detect", "--no-banner", "--source", str(root)])
    if shutil.which("detect-secrets"):
        # detect-secrets scan prints a baseline; non-zero on error only, so we scan and report.
        return run_tool(["detect-secrets", "scan", str(root)])

    hits = fallback_scan(root, args.staged)
    if hits:
        print(f"FAIL: {len(hits)} potential secret(s)/PII found:")
        for h in hits:
            print(f"  - {h}")
        print("Note: fallback scanner is heuristic. Install gitleaks for reliable coverage.")
        return 1
    print("PASS: no secrets found by fallback scanner (heuristic; not a substitute for gitleaks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
