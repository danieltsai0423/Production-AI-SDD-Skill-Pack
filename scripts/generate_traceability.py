#!/usr/bin/env python3
"""Generate a traceability report linking requirements -> tasks -> verification evidence.

For each specs/<feature-id>/, this reads:
  - spec.md          : requirement IDs (FR-/NFR-/AI-/DATA-/SEC-/...)
  - tasks.md         : task items and their `requirements:` links
  - verification.md  : requirement rows and their evidence/result

and emits a machine-readable JSON plus a human-readable Markdown table, flagging requirements that
have no task and/or no verification evidence. Traceability chain (sec. 12.4):
    Requirement -> Task -> Verification Evidence

If no specs/ exist, this is a pass with a note.

Usage: python scripts/generate_traceability.py [--specs-dir specs] [--out-dir specs]
Exit code 0 = generated (or nothing to do), 1 = gaps found when --strict.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQ_PREFIXES = ("BUS", "USR", "FR", "NFR", "AI", "DATA", "SEC", "PRIV", "REL", "OBS", "OPS", "EVAL", "AC")
REQ_ID_RE = re.compile(r"\b((?:" + "|".join(REQ_PREFIXES) + r")-\d{3,})\b")


def requirements_in(text: str) -> list[str]:
    seen: list[str] = []
    for m in REQ_ID_RE.finditer(text):
        if m.group(1) not in seen:
            seen.append(m.group(1))
    return seen


def task_links(tasks_md: str) -> dict[str, list[str]]:
    """Map requirement id -> [task ids] using the YAML task block if PyYAML is present."""
    out: dict[str, list[str]] = {}
    m = re.search(r"```yaml\s*\n(.*?)```", tasks_md, re.DOTALL)
    if not m:
        return out
    try:
        import yaml  # type: ignore
        items = yaml.safe_load(m.group(1)) or []
    except Exception:
        return out
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        tid = item.get("id", "?")
        for req in item.get("requirements", []) or []:
            out.setdefault(req, []).append(tid)
    return out


def verification_evidence(ver_md: str) -> dict[str, str]:
    """Map requirement id -> result token from the verification.md requirement table."""
    out: dict[str, str] = {}
    for line in ver_md.splitlines():
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        m = REQ_ID_RE.search(cells[0])
        if m:
            out[m.group(1)] = cells[-1] if len(cells) > 1 else ""
    return out


def build(feature_dir: Path) -> dict:
    spec = (feature_dir / "spec.md")
    reqs = requirements_in(spec.read_text(encoding="utf-8")) if spec.exists() else []
    tasks = task_links((feature_dir / "tasks.md").read_text(encoding="utf-8")) \
        if (feature_dir / "tasks.md").exists() else {}
    ver = verification_evidence((feature_dir / "verification.md").read_text(encoding="utf-8")) \
        if (feature_dir / "verification.md").exists() else {}
    rows = []
    for r in reqs:
        rows.append({
            "requirement": r,
            "tasks": tasks.get(r, []),
            "verification": ver.get(r, ""),
            "gap": (not tasks.get(r)) or (not ver.get(r)),
        })
    return {"feature": feature_dir.name, "requirements": rows}


def to_markdown(report: dict) -> str:
    lines = [f"# Traceability - {report['feature']}", "",
             "| Requirement | Tasks | Verification | Gap |", "|---|---|---|---|"]
    for row in report["requirements"]:
        lines.append(f"| {row['requirement']} | {', '.join(row['tasks']) or '-'} "
                     f"| {row['verification'] or '-'} | {'YES' if row['gap'] else ''} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--specs-dir", default="specs")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any requirement has a gap")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    specs_dir = (root / args.specs_dir).resolve()
    if not specs_dir.is_dir():
        print(f"PASS: no {args.specs_dir}/ directory - nothing to trace.")
        return 0

    features = [p for p in sorted(specs_dir.iterdir()) if p.is_dir() and (p / "spec.md").exists()]
    if not features:
        print("PASS: no feature specs found.")
        return 0

    gaps = 0
    for fdir in features:
        report = build(fdir)
        (fdir / "traceability.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        (fdir / "traceability.md").write_text(to_markdown(report), encoding="utf-8")
        n_gap = sum(1 for r in report["requirements"] if r["gap"])
        gaps += n_gap
        print(f"  {fdir.name}: {len(report['requirements'])} requirement(s), {n_gap} gap(s) "
              f"-> {fdir.name}/traceability.md")

    if args.strict and gaps:
        print(f"FAIL: {gaps} requirement(s) missing a task or verification evidence.")
        return 1
    print(f"PASS: traceability generated for {len(features)} feature(s) ({gaps} gap(s) noted).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
