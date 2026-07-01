#!/usr/bin/env python3
"""Run STATIC trigger-eval checks over evals/trigger/cases.yaml.

This does NOT run a live agent. It validates that the eval suite is well-formed and internally
consistent, and reports a keyword-overlap smoke signal between each prompt and the descriptions of
its expected skills. Real precision/recall requires executing an agent against these prompts, which
is a tracked follow-up.

Checks (fail -> exit 1):
  - Each case has id, prompt, expected_skills (list), must_not_trigger (list), rationale.
  - Case ids are unique.
  - Every named skill (expected or must_not) exists under skills/.
  - No skill appears in both expected_skills and must_not_trigger of the same case.

Reports (informational):
  - For each expected skill, whether the prompt shares meaningful keywords with its description.

Usage: python scripts/run_trigger_evals.py [--cases evals/trigger/cases.yaml]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

STOP = set("a an the to and or of for with in on at is it be by an as this that add new use using make".split())


def load_cases(path: Path) -> list[dict]:
    """Try PyYAML; fall back to a parser targeted at this file's structure."""
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        return data or []
    except Exception:
        pass
    cases: list[dict] = []
    cur: dict | None = None
    pending_list_key: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("- "):
            if cur is not None:
                cases.append(cur)
            cur = {}
            pending_list_key = None
            raw = "  " + raw[2:]  # normalize first key onto the record indent
        if cur is None:
            continue
        m_item = re.match(r"^\s+-\s+(.*)$", raw)
        m_kv = re.match(r"^\s+([A-Za-z0-9_]+):\s*(.*)$", raw)
        if m_kv:
            key, val = m_kv.group(1), m_kv.group(2).strip()
            if val == "" :
                cur[key] = []
                pending_list_key = key
            elif val == "[]":
                cur[key] = []
                pending_list_key = None
            else:
                cur[key] = val.strip().strip('"')
                pending_list_key = None
        elif m_item and pending_list_key is not None:
            cur[pending_list_key].append(m_item.group(1).strip().strip('"'))
    if cur is not None:
        cases.append(cur)
    return cases


def load_skill_descriptions(skills_dir: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for d in skills_dir.iterdir():
        md = d / "SKILL.md"
        if not md.exists():
            continue
        text = md.read_text(encoding="utf-8")
        m = re.search(r"^description:\s*(.*)$", text, re.MULTILINE)
        out[d.name] = m.group(1).strip() if m else ""
    return out


def keywords(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", s.lower()) if w not in STOP}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", default="evals/trigger/cases.yaml")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    cases_path = (root / args.cases).resolve()
    skills_dir = (root / "skills").resolve()

    if not cases_path.exists():
        print(f"FAIL: cases file not found: {cases_path}")
        return 1

    cases = load_cases(cases_path)
    descriptions = load_skill_descriptions(skills_dir)
    known = set(descriptions)

    errors: list[str] = []
    seen_ids: set[str] = set()

    for i, case in enumerate(cases):
        cid = case.get("id") or f"<index {i}>"
        for field in ("id", "prompt", "rationale"):
            if not case.get(field):
                errors.append(f"{cid}: missing '{field}'")
        for field in ("expected_skills", "must_not_trigger"):
            if not isinstance(case.get(field), list):
                errors.append(f"{cid}: '{field}' must be a list")
        if cid in seen_ids:
            errors.append(f"{cid}: duplicate case id")
        seen_ids.add(cid)

        expected = case.get("expected_skills") or []
        forbidden = case.get("must_not_trigger") or []
        for name in list(expected) + list(forbidden):
            if name not in known:
                errors.append(f"{cid}: references unknown skill '{name}'")
        overlap = set(expected) & set(forbidden)
        if overlap:
            errors.append(f"{cid}: skill(s) in both expected and must_not_trigger: {sorted(overlap)}")

        # Informational keyword-overlap smoke signal.
        pk = keywords(case.get("prompt", ""))
        for name in expected:
            if name in descriptions:
                shared = pk & keywords(descriptions[name])
                flag = "ok" if shared else "weak"
                print(f"  smoke[{flag}] {cid} -> {name}: shared={sorted(shared)[:6]}")

    print()
    if errors:
        print(f"FAIL: {len(errors)} issue(s) across {len(cases)} case(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {len(cases)} trigger case(s) well-formed and consistent (static checks only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
