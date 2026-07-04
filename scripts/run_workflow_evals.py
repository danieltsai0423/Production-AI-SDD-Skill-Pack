#!/usr/bin/env python3
"""Run STATIC workflow-compliance checks over evals/workflow/cases.yaml.

This does NOT run a live agent. It validates realistic prompts against the pack's routing
contract: expected skills exist, required template artifacts exist, and the selected skills/templates
contain the gate terms needed for the scenario. Live agent loading, precision/recall, and output
quality scoring remain separate follow-ups.

Checks (fail -> exit 1):
  - Each case has id, category, prompt, expected_work_type, expected_level, expected_skills,
    must_not_trigger, required_artifacts, required_gate_terms, and rationale.
  - Categories cover positive, negative, and ambiguous workflow behavior.
  - Expected levels are 0-3 and known skill names are referenced.
  - Required artifacts map to templates/.
  - Level 3 cases include human oversight, rollback, evaluation, and audit gate terms.
  - Ambiguous cases include pai-sdd-clarify and do not go straight to pai-sdd-implement.
  - Negative cases do not expect skills or artifacts.

Usage: python scripts/run_workflow_evals.py [--cases evals/workflow/cases.yaml]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:  # schemas/ drives the structural contract; degrade gracefully if unavailable.
    from _minijsonschema import validate as schema_validate, load_schema
    EVAL_SCHEMA = load_schema("eval-case")
except Exception:  # pragma: no cover
    schema_validate = None
    EVAL_SCHEMA = None

CATEGORIES = {"positive", "negative", "ambiguous"}
REQUIRED_CATEGORIES = {"positive", "negative", "ambiguous"}
KNOWN_WORK = {"greenfield", "brownfield", "incident", "research"}
LEVEL3_REQUIRED_TERMS = {"human", "rollback", "evaluation", "audit"}


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
            raw = "  " + raw[2:]
        if cur is None:
            continue
        m_item = re.match(r"^\s+-\s+(.*)$", raw)
        m_kv = re.match(r"^\s+([A-Za-z0-9_]+):\s*(.*)$", raw)
        if m_kv:
            key, val = m_kv.group(1), m_kv.group(2).strip()
            if val == "":
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


def load_skill_texts(skills_dir: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for d in skills_dir.iterdir():
        md = d / "SKILL.md"
        if md.exists():
            out[d.name] = md.read_text(encoding="utf-8")
    return out


def artifact_path(root: Path, artifact: str) -> Path:
    return root / "templates" / artifact


def read_artifact(root: Path, artifact: str) -> str:
    path = artifact_path(root, artifact)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def contains_term(corpus: str, term: str) -> bool:
    return term.lower() in corpus.lower()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", default="evals/workflow/cases.yaml")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    cases_path = (root / args.cases).resolve()
    skills_dir = (root / "skills").resolve()

    if not cases_path.exists():
        print(f"FAIL: cases file not found: {cases_path}")
        return 1

    cases = load_cases(cases_path)
    skill_texts = load_skill_texts(skills_dir)
    known_skills = set(skill_texts)
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_categories: set[str] = set()

    for i, case in enumerate(cases):
        cid = case.get("id") or f"<index {i}>"
        for field in (
            "id",
            "category",
            "prompt",
            "expected_work_type",
            "expected_level",
            "expected_skills",
            "must_not_trigger",
            "required_artifacts",
            "required_gate_terms",
            "rationale",
        ):
            if field not in case or case.get(field) in (None, ""):
                errors.append(f"{cid}: missing '{field}'")

        if cid in seen_ids:
            errors.append(f"{cid}: duplicate case id")
        seen_ids.add(cid)

        if EVAL_SCHEMA is not None:
            for err in schema_validate(case, EVAL_SCHEMA):
                errors.append(f"{cid}: schema: {err}")

        category = case.get("category")
        if category:
            if category not in CATEGORIES:
                errors.append(f"{cid}: unknown category '{category}'")
            else:
                seen_categories.add(category)

        work_type = case.get("expected_work_type")
        if work_type and work_type not in KNOWN_WORK:
            errors.append(f"{cid}: unknown expected_work_type '{work_type}'")

        try:
            level = int(case.get("expected_level"))
        except (TypeError, ValueError):
            errors.append(f"{cid}: expected_level must be an integer 0-3")
            level = -1
        if level not in (0, 1, 2, 3):
            errors.append(f"{cid}: expected_level '{case.get('expected_level')}' not in 0-3")

        for field in ("expected_skills", "must_not_trigger", "required_artifacts", "required_gate_terms"):
            if not isinstance(case.get(field), list):
                errors.append(f"{cid}: '{field}' must be a list")

        expected = case.get("expected_skills") or []
        forbidden = case.get("must_not_trigger") or []
        artifacts = case.get("required_artifacts") or []
        gate_terms = case.get("required_gate_terms") or []

        for name in list(expected) + list(forbidden):
            if name not in known_skills:
                errors.append(f"{cid}: references unknown skill '{name}'")
        overlap = set(expected) & set(forbidden)
        if overlap:
            errors.append(f"{cid}: skill(s) in both expected and must_not_trigger: {sorted(overlap)}")

        for artifact in artifacts:
            if not artifact_path(root, artifact).exists():
                errors.append(f"{cid}: required artifact template missing 'templates/{artifact}'")

        corpus = "\n".join(skill_texts.get(name, "") for name in expected)
        corpus += "\n" + "\n".join(read_artifact(root, artifact) for artifact in artifacts)
        for term in gate_terms:
            if not contains_term(corpus, term):
                errors.append(f"{cid}: required gate term '{term}' not found in selected skills/templates")

        if category == "negative":
            if expected:
                errors.append(f"{cid}: negative case should not expect skills")
            if artifacts:
                errors.append(f"{cid}: negative case should not require artifacts")
        if category == "ambiguous":
            if "pai-sdd-clarify" not in expected:
                errors.append(f"{cid}: ambiguous case should trigger pai-sdd-clarify")
            if "pai-sdd-implement" not in forbidden:
                errors.append(f"{cid}: ambiguous case should forbid direct pai-sdd-implement")
        if level == 3:
            missing = LEVEL3_REQUIRED_TERMS - set(gate_terms)
            if missing:
                errors.append(f"{cid}: Level 3 case missing required gate term(s): {sorted(missing)}")

        print(
            f"  workflow {cid}: category={category} level={level} "
            f"skills={len(expected)} artifacts={len(artifacts)} gates={len(gate_terms)}"
        )

    missing_categories = REQUIRED_CATEGORIES - seen_categories
    if missing_categories:
        errors.append(f"missing workflow case categories: {sorted(missing_categories)}")

    print()
    if errors:
        print(f"FAIL: {len(errors)} issue(s) across {len(cases)} workflow case(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    counts = {c: sum(1 for case in cases if case.get("category") == c) for c in sorted(CATEGORIES)}
    print(f"PASS: {len(cases)} workflow case(s) satisfy static routing/artifact/gate contracts.")
    print("Categories: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    print("Note: static workflow checks only; live-agent execution is still required for precision/recall.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
