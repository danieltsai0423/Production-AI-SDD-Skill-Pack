#!/usr/bin/env python3
"""Orchestrate the repository quality gate (sec. 15.5).

Runs the deterministic checks in sequence, collects their results, and emits a JSON report and a
Markdown summary, with an exit code that reflects the enforcement mode. This is the single entry
point a CI job or a Stop hook can call.

Checks run:
  - validate JSON schemas parse
  - validate_skills
  - validate_specs
  - validate_references
  - run_trigger_evals
  - run_workflow_evals
  - scan_secrets
  - check_spec_drift (mode-aware)

Modes:
  advisory : report only; exit 0 regardless.
  standard : exit 1 if any blocking check fails (default).
  strict   : standard + treat warnings/drift as failures.

Usage: python scripts/run_quality_gate.py [--mode standard] [--change CHG-001] [--json out.json]
Exit code 0 = pass (or advisory), 1 = gate failure, 2 = harness error.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def run(name: str, argv: list[str]) -> dict:
    try:
        p = subprocess.run([sys.executable, str(SCRIPTS / name), *argv],
                           capture_output=True, text=True)
    except Exception as e:  # pragma: no cover
        return {"check": name, "exit": 2, "ok": False, "output": str(e)}
    return {"check": name, "exit": p.returncode, "ok": p.returncode == 0,
            "output": (p.stdout + p.stderr).strip()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["advisory", "standard", "strict"], default="standard")
    ap.add_argument("--change", default=None, help="active change id, for the report only")
    ap.add_argument("--json", default=None, help="write the JSON report to this path")
    args = ap.parse_args()

    drift_mode = "strict" if args.mode == "strict" else ("advisory" if args.mode == "advisory" else "standard")
    checks = [
        ("_minijsonschema.py", []),
        ("validate_skills.py", ["--strict"] if args.mode == "strict" else []),
        ("validate_specs.py", []),
        ("validate_references.py", []),
        ("run_trigger_evals.py", []),
        ("run_workflow_evals.py", []),
        ("run_output_evals.py", []),
        ("run_safety_evals.py", []),
        ("test_hooks.py", []),
        ("scan_secrets.py", []),
        ("check_spec_drift.py", ["--mode", drift_mode]),
    ]

    results = [run(name, argv) for name, argv in checks]
    # check_spec_drift returns 2 when not a git repo; treat as non-blocking skip.
    for r in results:
        if r["check"] == "check_spec_drift.py" and r["exit"] == 2:
            r["ok"] = True
            r["skipped"] = True

    failed = [r for r in results if not r["ok"]]
    report = {
        "pack": "production-ai-sdd-skill-pack",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "change": args.change,
        "decision": "PASS" if not failed else ("ADVISORY" if args.mode == "advisory" else "FAIL"),
        "checks": results,
    }

    print(f"# Quality gate ({args.mode}) - {report['decision']}\n")
    for r in results:
        status = "ok" if r["ok"] else "FAIL"
        tag = " (skipped)" if r.get("skipped") else ""
        print(f"  [{status}] {r['check']}{tag}")
    if failed and args.mode != "advisory":
        print("\nFailures:")
        for r in failed:
            print(f"\n--- {r['check']} (exit {r['exit']}) ---")
            print(r["output"])

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nJSON report: {args.json}")

    if args.mode == "advisory":
        return 0
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
