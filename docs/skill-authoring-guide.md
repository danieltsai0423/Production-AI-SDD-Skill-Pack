# Skill authoring guide

How to add or edit a `pai-*` skill so it passes validation and triggers correctly.

## Rules

- Name is lowercase-hyphenated, `pai-` prefixed; the **directory name must equal** the frontmatter
  `name`.
- `description` must state **what** the skill does, **when to trigger**, and **when NOT to** (the
  validator checks for a "use..." and a "do not..." clause, min length 40).
- Keep `SKILL.md` focused and under ~500 lines. Move long standards to `references/`, long templates
  to `assets/`, deterministic logic to `scripts/`.
- Frontmatter follows [`schemas/skill-manifest.schema.json`](../schemas/skill-manifest.schema.json):
  `name`, `description`, `license`, `compatibility`, `metadata.{pack,version,category}`
  (`category` ∈ `sdd-core` | `production-review`).

## Structure (Master Spec sec. 35)

Purpose · Use when · Do not use when · Required inputs · Workflow · Output contract · Blocking
conditions · Gotchas · References · Completion criteria.

## Before committing

```bash
python scripts/validate_skills.py     # format, references, schema, duplicate names, hardcoded paths
python scripts/run_trigger_evals.py   # add a trigger case in evals/trigger/cases.yaml
```

Add the skill to `pack.yaml` (the validator checks skills/ ↔ pack.yaml agree) and, if it changes
routing, add a case to `evals/workflow/cases.yaml`.

## Boundaries

If a new skill overlaps an existing one, add a "Boundary with related skills" section to both (see
`pai-sdd-verify` ↔ `pai-release-readiness`) so triggering stays unambiguous.
