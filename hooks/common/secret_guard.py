#!/usr/bin/env python3
"""Gate A - secret and sensitive-data guard (sec. 14.1.A).

Blocks obvious secret leaks before they are written or committed:
  - Claude Code PreToolUse: inspects Write/Edit content and Bash commands on stdin.
  - git pre-commit / CLI: with --staged, scans staged diff content.

Detects AWS keys, Google API keys, Slack/GitHub/OpenAI/Anthropic tokens, private-key blocks,
generic assigned secrets, and attempts to add a .env file. This is a fast guard, not a replacement
for a full scanner; the deep scan is scripts/scan_secrets.py (Stop/CI). Actionable on block.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import allow, block, read_payload, tool_context  # noqa: E402

PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Google API key"),
    (re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"), "Slack token"),
    (re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}"), "GitHub token"),
    (re.compile(r"\bsk-ant-[0-9A-Za-z_\-]{20,}"), "Anthropic API key"),
    (re.compile(r"\bsk-[0-9A-Za-z]{32,}"), "OpenAI API key"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "private key block"),
    (re.compile(r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
     "hardcoded secret assignment"),
]


def scan(text: str) -> list[str]:
    hits = []
    for rx, label in PATTERNS:
        if rx.search(text):
            hits.append(label)
    return hits


def staged_text(root: Path) -> str:
    try:
        p = subprocess.run(["git", "diff", "--cached", "--unified=0"],
                           cwd=root, capture_output=True, text=True)
        return p.stdout if p.returncode == 0 else ""
    except FileNotFoundError:
        return ""


def staged_names(root: Path) -> list[str]:
    try:
        p = subprocess.run(["git", "diff", "--cached", "--name-only"],
                           cwd=root, capture_output=True, text=True)
        return [l.strip() for l in p.stdout.splitlines() if l.strip()] if p.returncode == 0 else []
    except FileNotFoundError:
        return []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--staged", action="store_true", help="scan git staged diff (pre-commit mode)")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent.parent

    if args.staged:
        names = staged_names(root)
        for n in names:
            if Path(n).name == ".env" or n.endswith("/.env"):
                return block(f"attempting to commit an env file: {n}",
                             "remove it from the index and add it to .gitignore")
        hits = scan(staged_text(root))
        if hits:
            return block(f"staged changes contain: {', '.join(sorted(set(hits)))}",
                         "remove the secret, use env vars / a secret manager, then re-stage")
        return allow(f"secret_guard: staged scan clean ({len(names)} file(s)).")

    payload = read_payload()
    tool, tin = tool_context(payload)
    corpus = ""
    if tool in ("Write", "Edit", "MultiEdit"):
        fp = tin.get("file_path", "")
        if Path(fp).name == ".env":
            return block(f"writing an env file: {fp}", "keep secrets out of the repo; use .gitignore")
        corpus = " ".join(str(tin.get(k, "")) for k in ("content", "new_string", "new_str"))
    elif tool in ("Bash",):
        corpus = str(tin.get("command", ""))
    if corpus:
        hits = scan(corpus)
        if hits:
            return block(f"{tool} would introduce: {', '.join(sorted(set(hits)))}",
                         "do not hardcode secrets; reference an env var or secret manager")
    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
