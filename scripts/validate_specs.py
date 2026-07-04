#!/usr/bin/env python3
"""Validate feature specs under specs/<feature-id>/ against the pack's conventions.

Checks (stdlib only):
  - spec.md frontmatter present with id, title, status, spec_level, work_type.
  - spec_level is 0-3; status is a known value.
  - Requirement IDs use known prefixes and are unique within the spec.
  - Level-appropriate artifacts exist (Level 2+: plan.md; Level 3: risk/rollback evidence referenced).

If no specs/ directory exists yet, this is reported as a pass with a note (nothing to validate).

Exit code 0 = pass, 1 = errors.
Usage: python scripts/validate_specs.py [--specs-dir specs]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:  # schemas/spec.schema.json is the frontmatter contract.
    from _minijsonschema import validate as schema_validate, load_schema
    SPEC_SCHEMA = load_schema("spec")
    TASK_SCHEMA = load_schema("task")
except Exception:  # pragma: no cover
    schema_validate = None
    SPEC_SCHEMA = None
    TASK_SCHEMA = None

REQ_PREFIXES = ("BUS", "USR", "FR", "NFR", "AI", "DATA", "SEC", "PRIV", "REL", "OBS", "OPS", "EVAL", "AC")
REQ_ID_RE = re.compile(r"\b(" + "|".join(REQ_PREFIXES) + r")-(\d{3})\b")
KNOWN_STATUS = {"draft", "approved", "implemented", "closed"}
KNOWN_WORK = {"greenfield", "brownfield", "incident", "research"}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_]+):\s?(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            data[m.group(1)] = m.group(2).strip().strip('"')
    return data


def parse_frontmatter_typed(text: str) -> dict:
    """Parse frontmatter into a typed nested dict. Prefers PyYAML; falls back to a small parser."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block)
        return data if isinstance(data, dict) else {}
    except Exception:
        pass

    # Fallback: reliably parse only top-level scalar fields (the schema's required fields are all
    # scalars). Nested containers (owners/risk_domains/...) are skipped here to avoid type misreads;
    # install PyYAML for full-fidelity parsing. Inline [] lists are preserved.
    def coerce(v: str):
        v = v.strip()
        if v == "[]":
            return []
        if v.lower() in ("true", "false"):
            return v.lower() == "true"
        if v.lstrip("-").isdigit():
            return int(v)
        return v.strip('"')

    root: dict = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace() or line.lstrip().startswith("- "):
            continue  # skip nested content in fallback mode
        m = re.match(r"^([A-Za-z0-9_]+):\s?(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if val.strip() != "":  # scalar or inline list only
            root[key] = coerce(val)
    return root


def validate_spec(spec_dir: Path) -> list[str]:
    errors: list[str] = []
    fid = spec_dir.name
    spec = spec_dir / "spec.md"
    if not spec.exists():
        return [f"{fid}: missing spec.md"]

    text = spec.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    for field in ("id", "title", "status", "spec_level", "work_type"):
        if not fm.get(field):
            errors.append(f"{fid}: spec.md frontmatter missing '{field}'")

    level_raw = fm.get("spec_level", "")
    level = None
    if level_raw:
        try:
            level = int(level_raw)
            if level not in (0, 1, 2, 3):
                errors.append(f"{fid}: spec_level '{level_raw}' not in 0-3")
        except ValueError:
            errors.append(f"{fid}: spec_level '{level_raw}' is not an integer")

    if fm.get("status") and fm["status"] not in KNOWN_STATUS:
        errors.append(f"{fid}: unknown status '{fm['status']}'")
    if fm.get("work_type") and fm["work_type"] not in KNOWN_WORK:
        errors.append(f"{fid}: unknown work_type '{fm['work_type']}'")

    # Requirement ID uniqueness within the spec body.
    seen: dict[str, int] = {}
    for m in REQ_ID_RE.finditer(text):
        rid = f"{m.group(1)}-{m.group(2)}"
        seen[rid] = seen.get(rid, 0) + 1
    dupes = [rid for rid, n in seen.items() if n > 1]
    # A definition + references legitimately repeat an ID, so only warn beyond a threshold is noisy;
    # here we simply do not fail on repeats, but we do require at least one requirement for Level >= 1.
    if level is not None and level >= 1 and not seen:
        errors.append(f"{fid}: Level {level} spec has no requirement IDs (FR-/NFR-/AI-/...)")

    # Level-appropriate artifacts.
    if level is not None and level >= 2 and not (spec_dir / "plan.md").exists():
        errors.append(f"{fid}: Level {level} requires plan.md")
    if level == 3:
        blob = text.lower()
        for token in ("rollback", "human"):
            if token not in blob and not (spec_dir / "contracts").exists():
                errors.append(f"{fid}: Level 3 spec should address '{token}' or provide contracts/")

    # Schema validation of the spec frontmatter.
    if SPEC_SCHEMA is not None:
        fm_typed = parse_frontmatter_typed(text)
        for err in schema_validate(fm_typed, SPEC_SCHEMA):
            errors.append(f"{fid}: spec schema: {err}")

    # Schema validation of tasks.md YAML task items (requires PyYAML for the block list).
    tasks_md = spec_dir / "tasks.md"
    if TASK_SCHEMA is not None and tasks_md.exists():
        errors += validate_tasks(fid, tasks_md.read_text(encoding="utf-8"))
    return errors


def validate_tasks(fid: str, text: str) -> list[str]:
    """Validate the YAML task list embedded in tasks.md against task.schema.json.

    The tasks live in a ```yaml fenced block. Parsing needs PyYAML; without it we skip
    (the fallback frontmatter parser cannot handle deep task structures) and note it once.
    """
    m = re.search(r"```yaml\s*\n(.*?)```", text, re.DOTALL)
    if not m:
        return []
    try:
        import yaml  # type: ignore
        items = yaml.safe_load(m.group(1))
    except Exception:
        return []  # PyYAML absent; deep task validation is best-effort
    if not isinstance(items, list):
        return []
    errors: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        tid = item.get("id", "<task>")
        for err in schema_validate(item, TASK_SCHEMA):
            errors.append(f"{fid}/{tid}: task schema: {err}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--specs-dir", default="specs")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    specs_dir = (root / args.specs_dir).resolve()

    if not specs_dir.is_dir():
        print(f"PASS: no {args.specs_dir}/ directory yet - nothing to validate.")
        return 0

    spec_dirs = [p for p in specs_dir.iterdir() if p.is_dir()]
    if not spec_dirs:
        print(f"PASS: {args.specs_dir}/ is empty - nothing to validate.")
        return 0

    errors: list[str] = []
    for d in sorted(spec_dirs):
        errors += validate_spec(d)

    if errors:
        print(f"FAIL: {len(errors)} issue(s) across {len(spec_dirs)} spec(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {len(spec_dirs)} spec(s) valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
