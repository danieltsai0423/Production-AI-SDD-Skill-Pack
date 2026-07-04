#!/usr/bin/env python3
"""Run STATIC output-quality checks over evals/output/cases.yaml (sec. 15.7, sec. 16.2).

This does NOT score a live agent's prose. It checks that a produced artifact (a spec.md, plan.md,
etc., living under evals/fixtures/ or a given path) contains the sections and requirement-ID kinds
its case demands, and that it is free of obvious hallucination markers (TODO/TBD/lorem). Calibrated
rubric scoring of real generated artifacts requires a live agent and human review - a tracked
follow-up. The 0-4 rubric (sec. 16.4) is documented in evals/output/RUBRIC.md.

Case format (evals/output/cases.yaml):
  - id: output-spec-001
    artifact: evals/fixtures/ai-chat-service/specs/FEAT-001/spec.md
    required_sections: ["Acceptance criteria", "AI behavior requirements"]
    required_req_kinds: ["FR", "AI", "AC"]
    forbid_markers: ["TODO", "TBD"]

If no cases file exists, this is a pass with a note.
Usage: python scripts/run_output_evals.py [--cases evals/output/cases.yaml]
Exit code 0 = pass / nothing to do, 1 = a case failed its structural contract.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

DEFAULT_MARKERS = ["TODO", "TBD", "FIXME", "lorem ipsum", "<placeholder>"]


def load_cases(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or []
    except Exception:
        pass
    # Minimal fallback parser (mirrors the other runners).
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
                cur[k] = v.strip('"')
                key = None
        elif mi and key:
            cur[key].append(mi.group(1).strip().strip('"'))
    if cur is not None:
        cases.append(cur)
    return cases


def check_case(case: dict, root: Path) -> list[str]:
    cid = case.get("id", "<case>")
    errs: list[str] = []
    artifact = case.get("artifact")
    if not artifact:
        return [f"{cid}: missing 'artifact'"]
    path = (root / artifact).resolve()
    if not path.exists():
        return [f"{cid}: artifact not found: {artifact}"]
    text = path.read_text(encoding="utf-8")
    low = text.lower()
    for section in case.get("required_sections", []) or []:
        if section.lower() not in low:
            errs.append(f"{cid}: missing required section '{section}'")
    for kind in case.get("required_req_kinds", []) or []:
        if not re.search(rf"\b{re.escape(kind)}-\d{{3,}}\b", text):
            errs.append(f"{cid}: no requirement of kind '{kind}-'")
    markers = case.get("forbid_markers") or DEFAULT_MARKERS
    for marker in markers:
        if marker.lower() in low:
            errs.append(f"{cid}: contains forbidden marker '{marker}'")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", default="evals/output/cases.yaml")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    cases_path = (root / args.cases).resolve()
    if not cases_path.exists():
        print(f"PASS: no output-eval cases at {args.cases} - nothing to check.")
        return 0

    cases = load_cases(cases_path)
    errors: list[str] = []
    for case in cases:
        case_errs = check_case(case, root)
        errors += case_errs
        print(f"  output {case.get('id', '?')}: {'FAIL' if case_errs else 'ok'}")

    print()
    if errors:
        print(f"FAIL: {len(errors)} issue(s) across {len(cases)} output case(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {len(cases)} output case(s) meet structural contracts (static checks only).")
    print("Note: calibrated 0-4 rubric scoring of generated prose requires a live agent (follow-up).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
