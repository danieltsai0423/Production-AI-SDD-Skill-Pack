---
contract: model-prompt
id: MPC-000
feature: FEAT-000
version: "1.0.0"
status: draft
updated_at: 2026-07-02
---

# Model & Prompt Contract

Keep capability requirement separate from implementation choice. Never write a specific model name
as a permanent requirement.

## Capability requirement
<provider-neutral; e.g. "supports structured JSON output and the target language at <= X ms p95">

## Current implementation mapping
- Model / version: <current choice>
- Provider: <current choice>

## Prompt
- Prompt ID / version:
- Input variables:
- Context assembly:

## Parameters
- Temperature / top_p / max_tokens / stop:

## Output schema
<JSON schema or structure; validation rule>

## Budgets
- Token budget:
- Latency budget (p50 / p95):
- Cost budget:

## Fallback strategy
<what happens on timeout, schema failure, provider outage>

## Change & evaluation policy
<which changes require re-running the regression eval set>
