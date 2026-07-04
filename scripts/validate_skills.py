#!/usr/bin/env python3
"""Validate the canonical skills in skills/ against the Agent Skills format.

Checks (stdlib only, no external dependencies):
  errors (exit 1):
    - Each skill dir contains a SKILL.md.
    - Frontmatter parses and has required fields: name, description, license, compatibility.
    - Frontmatter `name` equals the directory name and is lowercase-hyphenated.
    - No two skills declare the same frontmatter `name`.
    - `description` states what/when-to-use/when-not (heuristic).
    - Backticked or linked relative repo paths (templates/, references/, assets/, scripts/) exist.
    - No unsafe hardcoded absolute paths (C:\\..., /home/..., /Users/...).
    - Every skill in pack.yaml exists and vice versa.
  warnings (do not fail):
    - SKILL.md over the recommended 500-line size.
    - Non-ASCII characters (mojibake risk under legacy Windows codepages).

Exit code 0 = pass (warnings allowed), 1 = errors found.
Usage: python scripts/validate_skills.py [--skills-dir skills] [--pack pack.yaml] [--strict]
       --strict treats warnings as errors.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:  # schemas/skill-manifest.schema.json is the frontmatter contract.
    from _minijsonschema import validate as schema_validate, load_schema
    SKILL_SCHEMA = load_schema("skill-manifest")
except Exception:  # pragma: no cover
    schema_validate = None
    SKILL_SCHEMA = None

REQUIRED_FIELDS = ("name", "description", "license", "compatibility")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_LINES = 500
REL_PREFIXES = ("templates/", "references/", "assets/", "scripts/")
HARDCODED_PATH_RE = re.compile(r"(?:[A-Za-z]:\\Users\\|/home/|/Users/|/root/)")
# Relative paths in backticks or markdown links, excluding placeholders with < >.
BACKTICK_PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+)`")
MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip("\n")
    data: dict[str, str] = {}
    current_key: str | None = None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s?(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            current_key = m.group(1)
            data[current_key] = m.group(2).strip().strip('"')
        elif current_key and line.startswith((" ", "\t")):
            data[current_key] = (data[current_key] + " " + line.strip()).strip()
    return data


def parse_frontmatter_nested(text: str) -> dict | None:
    """Parse frontmatter into a nested dict (one level of indentation) for schema checks."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    root: dict = {}
    cur_map: dict | None = None
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        m = re.match(r"^([A-Za-z0-9_]+):\s?(.*)$", line.strip())
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip().strip('"')
        if indent == 0:
            if val == "":
                cur_map = {}
                root[key] = cur_map
            else:
                root[key] = val
                cur_map = None
        elif cur_map is not None:
            cur_map[key] = val
    return root


def load_pack_skills(pack_path: Path) -> list[str]:
    if not pack_path.exists():
        return []
    names: list[str] = []
    in_skills = False
    for line in pack_path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^skills:\s*$", line):
            in_skills = True
            continue
        if in_skills:
            m = re.match(r"^\s*-\s*(\S+)\s*$", line)
            if m:
                names.append(m.group(1))
            elif line and not line.startswith((" ", "\t", "-")):
                break
    return names


def find_referenced_paths(text: str) -> set[str]:
    refs: set[str] = set()
    for m in BACKTICK_PATH_RE.finditer(text):
        refs.add(m.group(1))
    for m in MD_LINK_RE.finditer(text):
        refs.add(m.group(1))
    out: set[str] = set()
    for r in refs:
        if "<" in r or ">" in r or r.startswith(("http://", "https://", "#")):
            continue
        if r.startswith(REL_PREFIXES):
            out.add(r.rstrip("/"))
    return out


def validate(skills_dir: Path, pack_path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    found: set[str] = set()
    names_seen: dict[str, str] = {}

    if not skills_dir.is_dir():
        return [f"skills directory not found: {skills_dir}"], warnings

    for skill_path in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        dir_name = skill_path.name
        found.add(dir_name)
        md = skill_path / "SKILL.md"
        if not md.exists():
            errors.append(f"{dir_name}: missing SKILL.md")
            continue

        text = md.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        if line_count > MAX_LINES:
            warnings.append(f"{dir_name}: SKILL.md is {line_count} lines (recommended <= {MAX_LINES})")

        non_ascii = sorted({c for c in text if ord(c) > 127})
        if non_ascii:
            sample = ", ".join(f"U+{ord(c):04X}" for c in non_ascii[:8])
            warnings.append(f"{dir_name}: SKILL.md has non-ASCII chars ({sample}) - mojibake risk")

        for m in HARDCODED_PATH_RE.finditer(text):
            errors.append(f"{dir_name}: unsafe hardcoded absolute path near '{m.group(0)}'")

        for ref in sorted(find_referenced_paths(text)):
            if not (root / ref).exists():
                errors.append(f"{dir_name}: references missing path '{ref}'")

        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{dir_name}: SKILL.md has no parseable frontmatter")
            continue

        if SKILL_SCHEMA is not None:
            nested = parse_frontmatter_nested(text) or {}
            for err in schema_validate(nested, SKILL_SCHEMA):
                errors.append(f"{dir_name}: schema: {err}")

        for field in REQUIRED_FIELDS:
            if not fm.get(field):
                errors.append(f"{dir_name}: frontmatter missing '{field}'")

        name = fm.get("name", "")
        if name != dir_name:
            errors.append(f"{dir_name}: frontmatter name '{name}' != directory name")
        if name and not NAME_RE.match(name):
            errors.append(f"{dir_name}: name '{name}' is not lowercase-hyphenated")
        if name in names_seen:
            errors.append(f"{dir_name}: duplicate skill name '{name}' (also in {names_seen[name]})")
        elif name:
            names_seen[name] = dir_name

        desc = fm.get("description", "")
        if desc:
            if len(desc) < 40:
                errors.append(f"{dir_name}: description is too short to express trigger boundaries")
            if "do not" not in desc.lower():
                errors.append(f"{dir_name}: description should state when NOT to trigger")
            if "use " not in desc.lower():
                errors.append(f"{dir_name}: description should state when to use the skill")

    pack_skills = load_pack_skills(pack_path)
    for name in pack_skills:
        if name not in found:
            errors.append(f"pack.yaml lists '{name}' but skills/{name}/ does not exist")
    if pack_skills:
        for name in sorted(found):
            if name not in pack_skills:
                errors.append(f"skills/{name}/ exists but is not listed in pack.yaml")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skills-dir", default="skills")
    ap.add_argument("--pack", default="pack.yaml")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    skills_dir = (root / args.skills_dir).resolve()
    pack_path = (root / args.pack).resolve()

    errors, warnings = validate(skills_dir, pack_path, root)
    count = len([p for p in skills_dir.iterdir() if p.is_dir()]) if skills_dir.is_dir() else 0

    for w in warnings:
        print(f"  warn: {w}")

    if args.strict and warnings:
        errors += [f"(strict) {w}" for w in warnings]

    if errors:
        print(f"FAIL: {len(errors)} issue(s) across {count} skill(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {count} skill(s) valid ({len(warnings)} warning(s)). Format checks only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
