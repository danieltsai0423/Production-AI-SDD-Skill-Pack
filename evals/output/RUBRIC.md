# Artifact quality rubric (0-4)

Master Spec sec. 16.4. Each major artifact (spec, plan, tasks, verification) is scored per dimension
on a 0-4 scale. Core artifacts do not pass on the average alone: key fields have a hard fail.

| Score | Meaning |
|---|---|
| 0 | Missing or wrong |
| 1 | Vague / generic |
| 2 | Partially usable |
| 3 | Specific and largely complete |
| 4 | Directly executable, verifiable, aligned with repository evidence |

## Dimensions (sec. 16.2)

- **Completeness** — all required sections present.
- **Specificity** — concrete, not hand-wavy ("natural/correct/nice" is a fail).
- **Testability** — requirements map to acceptance criteria and evidence.
- **Repository grounding** — no hallucinated repo facts.
- **Risk coverage** — failure, security, and (for AI) behavior boundaries addressed.
- **Internal consistency** — requirements, tasks, and verification agree.

## Hard-fail fields (cannot be averaged away)

- Spec: acceptance criteria present and measurable; AI behavior boundaries for AI features.
- Plan: failure strategy and rollback present.
- Tasks: path boundaries and requirement links present.
- Verification: requirement-by-requirement evidence and an explicit PASS/CONDITIONAL/FAIL decision.

## Scope of the automated runner

`scripts/run_output_evals.py` enforces the **structural** subset of this rubric (required sections,
requirement-ID kinds, no hallucination markers) deterministically. Full calibrated 0-4 scoring of
generated prose requires a live agent plus human review and is a tracked follow-up.
