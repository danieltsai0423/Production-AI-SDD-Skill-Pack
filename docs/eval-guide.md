# Eval guide

How the pack evaluates non-deterministic AI behavior, and what is enforced today vs. tracked.

## Eval layers (Master Spec sec. 16.1)

| Layer | Question | Runner | Status |
|---|---|---|---|
| Trigger | Right skill selected? | `run_trigger_evals.py` | static (schema + referential) |
| Workflow | Procedure followed? | `run_workflow_evals.py` | static (routing/artifact/gate) |
| Output | Artifact good enough? | `run_output_evals.py` | static (sections + req kinds) |
| Safety | High-risk blocked/escalated? | `run_safety_evals.py` | static (wired to defenses) |
| Outcome | Did the skill improve results? | — | live-agent follow-up |

## Rubric

Artifacts are scored 0-4 across completeness, specificity, testability, grounding, risk coverage,
and consistency; core fields hard-fail (see [`evals/output/RUBRIC.md`](../evals/output/RUBRIC.md)).

## Fixtures

Four repository fixtures (`evals/fixtures/`) — ai-chat-service, rag-api, workflow-automation,
tool-using-agent — plus the worked [examples/](../examples/) act as artifact fixtures. Fixtures carry
**no real secrets** and declare safety properties (DoD 25.6).

## Regression

Re-run the suites on any prompt/model/retrieval/tool/knowledge change; gate on baseline thresholds
(see [`evals/regression/README.md`](../evals/regression/README.md)).

## What is static vs. live

The runners deterministically check structure, wiring, and consistency. **Live** precision/recall and
calibrated prose scoring require driving an agent against the prompts/fixtures with human review —
the primary remaining follow-up toward Master Spec sec. 25.3.
