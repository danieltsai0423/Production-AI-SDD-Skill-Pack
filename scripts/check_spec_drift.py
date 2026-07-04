#!/usr/bin/env python3
"""Heuristic spec-drift gate (sec. 14 gate E, sec. 15.4).

Flags changes that touch spec-worthy surfaces (API/schema, DB migrations, model/prompt config,
contracts, tool permissions, auth/tenant isolation, external messaging) but arrive WITHOUT an
accompanying spec or change artifact in the same diff. It is a fast, deterministic heuristic - it
never lets an LLM judgment be the only gate, and it can be tuned per enforcement mode.

This is intentionally conservative: it maps changed paths to spec-worthiness and checks whether the
same change set also updates a spec (specs/**/spec.md, change-proposal, spec-delta) or references an
approved active spec. Semantic/AST mapping can be layered on later.

Modes:
  advisory : always exit 0; print findings.
  standard : exit 1 if spec-worthy change lacks an accompanying spec/change (default).
  strict   : standard, plus require a plan.md/verification.md when contracts or migrations change.

Change set source (first non-empty wins):
  --base <ref>  -> git diff --name-only <ref>...HEAD
  otherwise     -> staged + unstaged vs HEAD (git status --porcelain)

Usage: python scripts/check_spec_drift.py [--mode standard] [--base origin/main]
Exit code 0 = pass, 1 = drift under the active mode, 2 = not a git repo / git error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

SPEC_WORTHY = [
    (re.compile(r"(^|/)contracts?/"), "contract"),
    (re.compile(r"(^|/)migrations?/|\.sql$"), "database-migration"),
    (re.compile(r"openapi|\.proto$|(^|/)schemas?/.*\.(json|yaml|yml)$"), "api-schema"),
    (re.compile(r"prompt|(^|/)prompts?/|\.prompt(\.|$)"), "model-prompt"),
    (re.compile(r"model[_-]?config|llm[_-]?config"), "model-config"),
    (re.compile(r"auth|tenant|permission|rbac|acl"), "auth-tenant"),
    (re.compile(r"webhook|messaging|notif"), "external-messaging"),
]
SPEC_ARTIFACT = re.compile(r"(specs?/.*/(spec|plan|clarifications|verification)\.md$"
                           r"|change-proposal|spec-delta|(^|/)CHG-)")
# Paths that are the pack's own tooling, never product surfaces - exempt from the gate.
EXEMPT = re.compile(r"^(scripts/|schemas/|templates/|skills/|profiles/|docs/|evals/|hooks/|examples/"
                    r"|\.github/|README|CHANGELOG|CONTRIBUTING|SECURITY|AGENTS|CLAUDE|pack\.yaml"
                    r"|LICENSE|Makefile|pyproject|\.gitignore)")


def git(args: list[str], root: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
        return p.returncode, p.stdout
    except FileNotFoundError:
        return 127, ""


def changed_files(root: Path, base: str | None) -> tuple[list[str], int]:
    if base:
        code, out = git(["diff", "--name-only", f"{base}...HEAD"], root)
        if code != 0:
            return [], code
        return [l.strip() for l in out.splitlines() if l.strip()], 0
    code, out = git(["status", "--porcelain"], root)
    if code != 0:
        return [], code
    files = []
    for line in out.splitlines():
        if len(line) > 3:
            files.append(line[3:].strip().split(" -> ")[-1])
    return files, 0


def classify(files: list[str]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for f in files:
        if EXEMPT.match(f):
            continue
        for rx, label in SPEC_WORTHY:
            if rx.search(f.lower()):
                hits.setdefault(label, []).append(f)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["advisory", "standard", "strict"], default="standard")
    ap.add_argument("--base", default=None)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent

    files, code = changed_files(root, args.base)
    if code == 127:
        print("SKIP: git not found.")
        return 2
    if code not in (0,):
        print("SKIP: not a git repository or git error.")
        return 2
    if not files:
        print("PASS: no changed files to evaluate.")
        return 0

    hits = classify(files)
    has_spec_artifact = any(SPEC_ARTIFACT.search(f) for f in files)

    if not hits:
        print(f"PASS: {len(files)} changed file(s); none are spec-worthy surfaces.")
        return 0

    print("Spec-worthy changes detected:")
    for label, fs in sorted(hits.items()):
        print(f"  - {label}: {', '.join(sorted(set(fs))[:5])}")

    problems: list[str] = []
    if not has_spec_artifact:
        problems.append("spec-worthy change has no accompanying spec/change artifact in the diff")
    if args.mode == "strict" and ("contract" in hits or "database-migration" in hits):
        if not any(re.search(r"(plan|verification)\.md$", f) for f in files):
            problems.append("strict: contract/migration change requires plan.md or verification.md")

    if not problems:
        print("PASS: spec-worthy change is accompanied by a spec/change artifact.")
        return 0

    for p in problems:
        print(f"  DRIFT: {p}")
    if args.mode == "advisory":
        print("advisory mode: not failing. Add a spec/change (pai-sdd-specify / pai-sdd-change).")
        return 0
    print("Action: add or update the spec/change for this surface, or run pai-sdd-change.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
