# Architecture of the pack

How the pieces fit together, and why the pack is split the way it is.

## Layers

| Layer | Where | Role |
|---|---|---|
| Persistent facts | `AGENTS.md`, `CLAUDE.md` | Always-on working agreements + risk routing |
| Procedures (judgment) | `skills/pai-*/SKILL.md` | Triggerable SDD + review procedures |
| Overlays | `profiles/` | Project-type-specific focus, applied on demand |
| Templates | `templates/`, `templates/contracts/` | Repeatable artifact shapes |
| Contracts of data | `schemas/*.json` | Machine-checkable frontmatter/eval structure |
| Determinism | `scripts/`, `hooks/` | What must be enforced, not just advised |
| Evidence | `evals/`, `examples/` | Fixtures, rubrics, worked runs |

## The core split (Master Spec sec. 5, ADR-006)

- **Skills** encode judgment: they decide *what* to do and *when*. They cannot enforce.
- **Scripts** encode deterministic checks with clear pass/fail (validators, drift, evals).
- **Hooks** wire scripts into the agent/git lifecycle so rules actually block.

This keeps advice where nuance is needed and enforcement where rules are crisp.

## Cross-agent strategy (ADR-002)

`skills/` is the single canonical source. `scripts/install.py` copies it into `.agents/skills/`
(Codex) and `.claude/skills/` (Claude Code). `scripts/sync_skills.py --check` fails CI if a copy
drifts from canonical, so the two agents can never silently diverge.

## Data flow of a change

```
request -> pai-sdd-discovery (risk level) -> specify/clarify -> plan (+ contracts, reviews)
        -> tasking -> implement -> verify (evidence) -> close
hooks (secret/protected/spec/verify) gate the lifecycle; evals gate AI-behavior changes.
```

See [sdd-workflow.md](sdd-workflow.md) for the step-by-step, [risk-classification.md](risk-classification.md)
for levels, and [hook-guide.md](hook-guide.md) for enforcement.
