#!/usr/bin/env python3
"""Run STATIC safety-eval checks over evals/safety/cases.yaml (sec. 16.1.5, DoD sec. 25.6).

This does NOT run adversarial prompts against a live agent. It verifies the safety suite is
well-formed and wired to real defenses: each case names a known attack category, references an
existing skill and (optional) fixture, and declares the capability the attack must NOT obtain. Live
adversarial execution is a tracked follow-up.

Checks (fail -> exit 1):
  - Each case has id, category, attack, expected_defense, must_not_obtain, expected_skills (list).
  - category is one of the known safety categories (covering sec. 16.1.5).
  - Every expected skill exists under skills/.
  - Any referenced fixture exists under evals/fixtures/.
  - The required categories (injection, tool-misuse, pii, destructive, cross-tenant) are all present.

Usage: python scripts/run_safety_evals.py [--cases evals/safety/cases.yaml]
Exit code 0 = pass, 1 = malformed suite.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

KNOWN_CATEGORIES = {
    "prompt-injection", "tool-misuse", "pii-leakage", "destructive-operation",
    "unsupported-decision", "cross-tenant-access", "retrieval-poisoning",
}
REQUIRED_CATEGORIES = {
    "prompt-injection", "tool-misuse", "pii-leakage", "destructive-operation", "cross-tenant-access",
}

try:
    from _minijsonschema import validate as schema_validate, load_schema
    EVAL_SCHEMA = load_schema("eval-case")
except Exception:  # pragma: no cover
    schema_validate = None
    EVAL_SCHEMA = None


def load_cases(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or []
    except Exception:
        pass
    cases: list[dict] = []
    cur: dict | None = None
    key: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("- "):
            if cur is not None:
                cases.append(cur)
            cur = {}
            key = None
            raw = "  " + raw[2:]
        if cur is None:
            continue
        mi = re.match(r"^\s+-\s+(.*)$", raw)
        mk = re.match(r"^\s+([A-Za-z0-9_]+):\s*(.*)$", raw)
        if mk:
            k, v = mk.group(1), mk.group(2).strip()
            if v in ("", "[]"):
                cur[k] = []
                key = k if v == "" else None
            elif v.startswith("["):
                cur[k] = [x.strip().strip('"') for x in v.strip("[]").split(",") if x.strip()]
                key = None
            else:
                cur[k] = v.strip().strip('"')
                key = None
        elif mi and key:
            cur[key].append(mi.group(1).strip().strip('"'))
    if cur is not None:
        cases.append(cur)
    return cases


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", default="evals/safety/cases.yaml")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    cases_path = (root / args.cases).resolve()
    skills = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    fixtures_dir = root / "evals" / "fixtures"

    if not cases_path.exists():
        print(f"PASS: no safety cases at {args.cases} - nothing to check.")
        return 0

    cases = load_cases(cases_path)
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_categories: set[str] = set()

    for i, case in enumerate(cases):
        cid = case.get("id") or f"<index {i}>"
        for field in ("id", "category", "attack", "expected_defense", "must_not_obtain", "expected_skills"):
            if not case.get(field):
                errors.append(f"{cid}: missing '{field}'")
        if cid in seen_ids:
            errors.append(f"{cid}: duplicate id")
        seen_ids.add(cid)
        cat = case.get("category")
        if cat:
            if cat not in KNOWN_CATEGORIES:
                errors.append(f"{cid}: unknown category '{cat}'")
            else:
                seen_categories.add(cat)
        if not isinstance(case.get("expected_skills"), list):
            errors.append(f"{cid}: 'expected_skills' must be a list")
        for name in case.get("expected_skills") or []:
            if name not in skills:
                errors.append(f"{cid}: references unknown skill '{name}'")
        fixture = case.get("fixture")
        if fixture and not (fixtures_dir / fixture).is_dir():
            errors.append(f"{cid}: references missing fixture 'evals/fixtures/{fixture}'")
        print(f"  safety {cid}: category={cat} must_not_obtain=\"{case.get('must_not_obtain','')[:40]}\"")

    missing = REQUIRED_CATEGORIES - seen_categories
    if missing:
        errors.append(f"missing required safety categories: {sorted(missing)}")

    print()
    if errors:
        print(f"FAIL: {len(errors)} issue(s) across {len(cases)} safety case(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {len(cases)} safety case(s) well-formed and wired to defenses (static checks only).")
    print("Note: live adversarial execution against an agent is a tracked follow-up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
