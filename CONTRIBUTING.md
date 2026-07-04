# Contributing

Thanks for improving the Production AI SDD Skill Pack.

## Ground rules

- `skills/` is the canonical source; never edit `.agents/skills/` or `.claude/skills/` (generated).
- Keep specific stacks (a messenger, queue, DB, cloud) out of canonical skills — they belong in
  `profiles/` or `examples/`.
- Every behavior change updates the relevant spec/tests/evals/docs.

## Before you open a PR

Run the full gate:

```bash
python scripts/run_quality_gate.py --mode standard
```

or the pieces:

```bash
python scripts/validate_skills.py
python scripts/validate_specs.py
python scripts/validate_references.py
python scripts/run_trigger_evals.py
python scripts/run_workflow_evals.py
python scripts/run_output_evals.py
python scripts/run_safety_evals.py
python scripts/test_hooks.py
python scripts/scan_secrets.py
```

## Adding a skill

See [docs/skill-authoring-guide.md](docs/skill-authoring-guide.md). Update `pack.yaml`, add a trigger
case, and keep `SKILL.md` under ~500 lines.

## Adding a profile / example / eval

- Profile: follow the existing overlay structure; link the relevant contracts and reviews.
- Example: produce real artifacts that pass `validate_specs`.
- Eval: add a case to the appropriate `evals/*/cases.yaml`; fixtures must contain no real secrets.

## Commits

Small, reversible changes. Explain assumptions, tests run, and rollback impact.
