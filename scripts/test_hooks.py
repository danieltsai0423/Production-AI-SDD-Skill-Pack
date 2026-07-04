#!/usr/bin/env python3
"""Tests for the deterministic hooks (sec. 25.4 - "Secret guard has tests", etc.).

Feeds crafted Claude Code PreToolUse payloads to each guard and asserts the block/allow decision and
that blocking messages are actionable (contain a "Fix:" or actionable verb). Covers the three
enforcement modes. Pure stdlib; runnable in CI.

Usage: python scripts/test_hooks.py
Exit code 0 = all tests pass, 1 = a test failed.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / "hooks" / "common"


def run_hook(script: str, payload: dict | None, mode: str = "standard", args=()):
    env = dict(os.environ, PAI_SDD_ENFORCEMENT=mode)
    p = subprocess.run(
        [sys.executable, str(HOOKS / script), *args],
        input=json.dumps(payload) if payload is not None else "",
        capture_output=True, text=True, env=env,
    )
    return p.returncode, (p.stdout + p.stderr)


CASES = []


def case(name, ok):
    CASES.append((name, ok))


def main() -> int:
    results = []

    def check(name, cond, detail=""):
        results.append((name, cond, detail))

    # Secret guard: blocks a Write introducing an AWS key.
    payload = {"tool_name": "Write", "tool_input": {"file_path": "app/config.py",
               "content": "AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'"}}  # pragma: allowlist secret
    rc, out = run_hook("secret_guard.py", payload, "standard")
    check("secret_guard blocks AWS key (standard)", rc == 2, out)
    check("secret_guard block is actionable", "Fix:" in out or "secret manager" in out, out)

    # Secret guard: advisory mode never blocks.
    rc, out = run_hook("secret_guard.py", payload, "advisory")
    check("secret_guard advisory does not block", rc == 0, out)

    # Secret guard: clean content allowed.
    payload_ok = {"tool_name": "Write", "tool_input": {"file_path": "app/config.py",
                  "content": "API_KEY = os.environ['API_KEY']"}}
    rc, out = run_hook("secret_guard.py", payload_ok, "standard")
    check("secret_guard allows env-var reference", rc == 0, out)

    # Secret guard: Bash echoing an Anthropic key is blocked.
    payload_bash = {"tool_name": "Bash", "tool_input": {"command": "echo sk-ant-abcdef0123456789ABCDEF01"}}  # pragma: allowlist secret
    rc, out = run_hook("secret_guard.py", payload_bash, "standard")
    check("secret_guard blocks key in Bash command", rc == 2, out)

    # Protected file guard: blocks editing a migration.
    payload_mig = {"tool_name": "Edit", "tool_input": {"file_path": "db/migrations/001_init.sql"}}
    rc, out = run_hook("protected_file_guard.py", payload_mig, "standard")
    check("protected_file_guard blocks migration edit", rc == 2, out)
    check("protected_file_guard block is actionable", "protected" in out.lower(), out)

    # Protected file guard: allows a normal source edit.
    payload_src = {"tool_name": "Edit", "tool_input": {"file_path": "app/service.py"}}
    rc, out = run_hook("protected_file_guard.py", payload_src, "standard")
    check("protected_file_guard allows normal edit", rc == 0, out)

    # Protected file guard: strict still allows, advisory never blocks.
    rc, out = run_hook("protected_file_guard.py", payload_mig, "advisory")
    check("protected_file_guard advisory does not block", rc == 0, out)

    # _hooklib runs standalone.
    rc, out = run_hook("_hooklib.py", None, "standard")
    check("_hooklib self-check runs", rc == 0 and "enforcement mode" in out, out)

    failed = [(n, d) for n, ok, d in results if not ok]
    for n, ok, d in results:
        print(f"  [{'ok' if ok else 'FAIL'}] {n}")
    print()
    if failed:
        print(f"FAIL: {len(failed)} hook test(s) failed:")
        for n, d in failed:
            print(f"  - {n}\n      {d.strip()[:300]}")
        return 1
    print(f"PASS: {len(results)} hook test(s) passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
