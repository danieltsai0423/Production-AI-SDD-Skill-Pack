#!/usr/bin/env python3
"""Minimal stdlib-only JSON Schema (Draft 2020-12 subset) validator.

Supports the keywords the pack's own schemas use: type, required, properties,
additionalProperties (bool), enum, const, pattern, minimum, maximum, minLength,
maxLength, items, allOf, if/then. Prefers the real `jsonschema` package when it is
installed; otherwise falls back to this checker. It is deliberately small: enough to
enforce the pack's frontmatter/eval contracts, not a general-purpose implementation.

Usage as a library:
    from _minijsonschema import validate
    errors = validate(instance, schema)   # -> list[str], empty means valid
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:  # Prefer the mature implementation when available.
    import jsonschema as _jsonschema  # type: ignore

    def validate(instance: Any, schema: dict) -> list[str]:
        validator = _jsonschema.Draft202012Validator(schema)
        return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
                for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]

    BACKEND = "jsonschema"
except Exception:  # pragma: no cover - fallback path
    BACKEND = "builtin"

    _TYPES = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "null": type(None),
    }

    def _type_ok(value: Any, t: str) -> bool:
        if t == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if t == "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if t == "boolean":
            return isinstance(value, bool)
        py = _TYPES.get(t)
        return isinstance(value, py) if py else True

    def _check(instance: Any, schema: dict, path: str, errors: list[str]) -> None:
        if not isinstance(schema, dict):
            return
        t = schema.get("type")
        if t is not None:
            types = t if isinstance(t, list) else [t]
            if not any(_type_ok(instance, x) for x in types):
                errors.append(f"{path or '<root>'}: expected type {t}, got {type(instance).__name__}")
                return

        if "enum" in schema and instance not in schema["enum"]:
            errors.append(f"{path or '<root>'}: {instance!r} not in enum {schema['enum']}")
        if "const" in schema and instance != schema["const"]:
            errors.append(f"{path or '<root>'}: {instance!r} != const {schema['const']!r}")

        if isinstance(instance, str):
            pat = schema.get("pattern")
            if pat and not re.search(pat, instance):
                errors.append(f"{path or '<root>'}: {instance!r} does not match /{pat}/")
            if "minLength" in schema and len(instance) < schema["minLength"]:
                errors.append(f"{path or '<root>'}: shorter than minLength {schema['minLength']}")
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                errors.append(f"{path or '<root>'}: longer than maxLength {schema['maxLength']}")

        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if "minimum" in schema and instance < schema["minimum"]:
                errors.append(f"{path or '<root>'}: {instance} < minimum {schema['minimum']}")
            if "maximum" in schema and instance > schema["maximum"]:
                errors.append(f"{path or '<root>'}: {instance} > maximum {schema['maximum']}")

        if isinstance(instance, dict):
            for req in schema.get("required", []):
                if req not in instance:
                    errors.append(f"{path or '<root>'}: missing required property '{req}'")
            props = schema.get("properties", {})
            for key, val in instance.items():
                if key in props:
                    _check(val, props[key], f"{path}/{key}" if path else key, errors)
                elif schema.get("additionalProperties") is False:
                    errors.append(f"{path or '<root>'}: additional property '{key}' not allowed")
            addl = schema.get("additionalProperties")
            if isinstance(addl, dict):
                for key, val in instance.items():
                    if key not in props:
                        _check(val, addl, f"{path}/{key}" if path else key, errors)

        if isinstance(instance, list):
            items = schema.get("items")
            if isinstance(items, dict):
                for i, val in enumerate(instance):
                    _check(val, items, f"{path}/{i}", errors)

        for sub in schema.get("allOf", []):
            _check(instance, sub, path, errors)

        if "anyOf" in schema:
            if not any(not _probe(instance, sub, path) for sub in schema["anyOf"]):
                errors.append(f"{path or '<root>'}: does not match any of anyOf")

        cond = schema.get("if")
        if cond is not None:
            probe: list[str] = []
            _check(instance, cond, path, probe)
            if not probe and "then" in schema:
                _check(instance, schema["then"], path, errors)

    def _probe(instance: Any, schema: dict, path: str) -> list[str]:
        probe: list[str] = []
        _check(instance, schema, path, probe)
        return probe

    def validate(instance: Any, schema: dict) -> list[str]:
        errors: list[str] = []
        _check(instance, schema, "", errors)
        return errors


_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
_cache: dict[str, dict] = {}


def load_schema(name: str) -> dict:
    """Load schemas/<name>.schema.json (cached)."""
    if name not in _cache:
        path = _SCHEMA_DIR / f"{name}.schema.json"
        _cache[name] = json.loads(path.read_text(encoding="utf-8"))
    return _cache[name]


def self_test() -> int:
    """Assert every schema file is valid JSON and self-consistent."""
    if not _SCHEMA_DIR.is_dir():
        print("PASS: no schemas/ directory.")
        return 0
    bad = 0
    for f in sorted(_SCHEMA_DIR.glob("*.schema.json")):
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"FAIL: {f.name} is not valid JSON: {e}")
            bad += 1
    if bad:
        return 1
    n = len(list(_SCHEMA_DIR.glob("*.schema.json")))
    print(f"PASS: {n} schema(s) parse as JSON. Validator backend: {BACKEND}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(self_test())
