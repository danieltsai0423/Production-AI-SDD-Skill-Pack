#!/usr/bin/env python3
"""Validate the canonical skills in skills/ against the Agent Skills format.

Checks (stdlib only, no external dependencies):
  - Each skill dir contains a SKILL.md.
  - Frontmatter parses and has required fields: name, description, license, compatibility.
  - Frontmatter `name` equals the directory name and is lowercase-hyphenated.
  - `description` states what/when-to-use/when-not (heuristic: mentions "Use when"/"Use " and "Do not").
  - SKILL.md stays within the recommended size (<= 500 lines).
  - Every skill listed in pack.yaml exists, and vice versa.

Exit code 0 = pass, 1 = failures found.
Usage: python scripts/validate_skills.py [--skills-dir skills] [--pack pack.yaml]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("name", "description", "license", "compatibility")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_LINES = 500


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse a minimal top-level YAML frontmatter block into a flat dict of strings."""
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
        # Only capture top-level `key: value` pairs (no leading indentation).
        m = re.match(r"^([A-Za-z0-9_]+):\s?(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            current_key = m.group(1)
            data[current_key] = m.group(2).strip().strip('"')
        elif current_key and line.startswith((" ", "\t")):
            # Continuation of a folded/multi-line value.
            data[current_key] = (data[current_key] + " " + line.strip()).strip()
    return data


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


def validate(skills_dir: Path, pack_path: Path) -> list[str]:
    errors: list[str] = []
    found: set[str] = set()

    if not skills_dir.is_dir():
        return [f"skills directory not found: {skills_dir}"]

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
            errors.append(f"{dir_name}: SKILL.md is {line_count} lines (recommended <= {MAX_LINES})")

        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{dir_name}: SKILL.md has no parseable frontmatter")
            continue

        for field in REQUIRED_FIELDS:
            if not fm.get(field):
                errors.append(f"{dir_name}: frontmatter missing '{field}'")

        name = fm.get("name", "")
        if name != dir_name:
            errors.append(f"{dir_name}: frontmatter name '{name}' != directory name")
        if name and not NAME_RE.match(name):
            errors.append(f"{dir_name}: name '{name}' is not lowercase-hyphenated")

        desc = fm.get("description", "")
        if desc:
            if len(desc) < 40:
                errors.append(f"{dir_name}: description is too short to express trigger boundaries")
            if "do not use" not in desc.lower() and "do not" not in desc.lower():
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

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skills-dir", default="skills")
    ap.add_argument("--pack", default="pack.yaml")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    skills_dir = (root / args.skills_dir).resolve()
    pack_path = (root / args.pack).resolve()

    errors = validate(skills_dir, pack_path)
    count = len([p for p in skills_dir.iterdir() if p.is_dir()]) if skills_dir.is_dir() else 0

    if errors:
        print(f"FAIL: {len(errors)} issue(s) across {count} skill(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {count} skill(s) valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
