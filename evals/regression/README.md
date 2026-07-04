# Regression evals & policy

Master Spec sec. 20.3. Non-deterministic AI behavior regresses silently, so changes to the
AI-affecting components must re-run a fixed evaluation set before shipping.

## Re-run triggers

Re-run the relevant suites when any of these change:

- Prompt text or prompt-assembly logic
- Model or model version
- Retrieval: index, chunking, embedding, or reranker
- Tool schema or permission tiers
- Knowledge base content

## Suites

| Suite | Runner | Gate |
|---|---|---|
| Trigger | `scripts/run_trigger_evals.py` | schema + referential (static) |
| Workflow | `scripts/run_workflow_evals.py` | routing/artifact/gate (static) |
| Output | `scripts/run_output_evals.py` | required sections + req kinds (static) |
| Safety | `scripts/run_safety_evals.py` | wired to defenses (static) |

## Baseline comparison

Each feature keeps a baseline of its key metrics (see the worked examples' `verification.md`:
escalation recall, citation-correctness, injection-to-execute = 0, etc.). A change may not ship if a
gated metric drops below its threshold, even if the overall average looks fine (hard-fail fields,
sec. 16.4).

## What is still static (tracked follow-up)

These runners check structure and wiring deterministically. Live precision/recall and calibrated
0-4 prose scoring require executing an agent against the fixtures/prompts and human review; that
harness is the primary remaining follow-up toward the Master Spec's full quality bar (sec. 25.3).
