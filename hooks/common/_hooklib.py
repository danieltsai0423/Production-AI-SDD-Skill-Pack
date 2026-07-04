#!/usr/bin/env python3
"""Shared helpers for the pack's deterministic hooks (sec. 14).

Design principles (sec. 14.2):
  - Fast, predictable, locally reproducible.
  - Deterministic rules live here (scripts); judgment lives in skills/reviewers.
  - Failure messages must be actionable.
  - Three enforcement modes: strict | standard | advisory (env PAI_SDD_ENFORCEMENT).

These hooks are agent-agnostic. They accept the Claude Code hook JSON payload on stdin when present,
and otherwise fall back to CLI/git usage so the same file works as a Codex hook or a git pre-commit
hook. Blocking is signalled with exit code 2 and an actionable message on stderr, which Claude Code
feeds back to the agent; in advisory mode nothing blocks (exit 0) but the message is still printed.
"""
from __future__ import annotations

import json
import os
import sys

VALID_MODES = ("strict", "standard", "advisory")


def mode() -> str:
    m = os.environ.get("PAI_SDD_ENFORCEMENT", "standard").lower()
    return m if m in VALID_MODES else "standard"


def read_payload() -> dict:
    """Read a Claude Code hook JSON payload from stdin if available; else return {}."""
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def tool_context(payload: dict) -> tuple[str, dict]:
    """Extract (tool_name, tool_input) from a PreToolUse payload."""
    return payload.get("tool_name", ""), payload.get("tool_input", {}) or {}


def allow(note: str = "") -> int:
    if note:
        print(note, file=sys.stderr)
    return 0


def block(reason: str, fix: str = "") -> int:
    """Block under strict/standard; warn-only under advisory. Message is always actionable."""
    lines = [f"[pai-sdd] BLOCKED: {reason}"]
    if fix:
        lines.append(f"          Fix: {fix}")
    msg = "\n".join(lines)
    if mode() == "advisory":
        print(f"[pai-sdd] advisory (not blocking): {reason}", file=sys.stderr)
        return 0
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    # Tiny self-check so the module is runnable/verifiable in isolation.
    print(f"enforcement mode: {mode()}")
    print(f"valid modes: {VALID_MODES}")
