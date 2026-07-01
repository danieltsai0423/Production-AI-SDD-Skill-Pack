---
contract: evaluation
id: EVALC-000
feature: FEAT-000
version: "1.0.0"
status: draft
updated_at: 2026-07-02
---

# Evaluation Contract

## Dimensions in scope
<task success, correctness, groundedness, refusal accuracy, tool selection, schema compliance,
hallucination rate, safety, latency, cost, retrieval quality, ...>

## Regression dataset
- Location:
- Size / composition:
- Ownership / update policy:

## Scoring method (per dimension)
- Deterministic assertion / reference comparison / rule-based / human rubric / LLM-as-judge / online
- Rubric + calibration cases (if LLM-as-judge):

## Thresholds
| Metric | Threshold | Rationale (risk-based) |
|---|---:|---|

## Failure retention
<where failing examples are stored and reviewed>

## Regression triggers
<which changes force a re-run: prompt, model, params, tool schema, retrieval config, chunking,
knowledge source, safety policy, output schema>
