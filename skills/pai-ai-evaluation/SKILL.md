---
name: pai-ai-evaluation
description: Builds repeatable, comparable, regression-ready evaluations for non-deterministic AI behavior, using fixed datasets, tiered scoring, calibrated rubrics, and risk-based thresholds. Use for any Level 2-3 AI feature and before shipping prompt, model, retrieval, tool-schema, or knowledge changes. Do not use for deterministic logic covered by ordinary tests, or for Level 0-1 edits with no AI behavior.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: production-review
---

# Purpose

Give non-deterministic AI behavior a measurable, regression-capable evaluation so quality can be
compared across prompt/model/retrieval/tool changes.

# Use this skill when

- Any Level 2/3 AI feature, or before shipping a prompt/model/retrieval/tool-schema/knowledge change.

# Do not use this skill when

- The behavior is deterministic and covered by ordinary tests, or the edit is Level 0/1 with no AI behavior.

# Required inputs

- The AI behavior contract, representative inputs, and reference answers where available.

# Evaluation dimensions

Task success · correctness · groundedness · relevance · completeness · refusal accuracy · escalation
accuracy · tool selection · tool-argument correctness · schema compliance · hallucination rate ·
safety · latency · cost · retrieval quality · user experience.

# Eval hierarchy (prefer the strongest applicable)

1. Deterministic assertions
2. Reference-answer comparison
3. Rule-based scoring
4. Structured human rubric
5. LLM-as-judge (with rubric + calibration cases)
6. Online metrics / A-B test

# Requirements

- Every Level 2/3 AI feature has a fixed regression dataset.
- LLM-as-judge needs an explicit rubric and calibration cases.
- Preserve failure examples, not just average scores.
- Prompt/model/RAG changes run the same benchmark set.
- Thresholds are set by risk, never arbitrarily.

# Separate-component evals

- RAG: retrieval quality, context assembly, generation quality, citation correctness, end-to-end success.
- Tool agent: intent/plan, tool selection, argument generation, permission behavior, result handling, final response.

# Output contract

An eval suite (cases + thresholds) plus a results report per dimension, including retained failure cases.

# Blocking conditions

- A risk-relevant threshold is missed and not mitigated.
- No regression dataset exists for a Level 2/3 AI feature.

# Gotchas

- An average score can hide catastrophic failures — keep and review the failing examples.
- LLM-as-judge without calibration is not evidence.

# References

- Feeds `pai-sdd-verify` and `pai-release-readiness`. Master Spec §10.15, §16, §20.

# Completion criteria

- Fixed dataset, calibrated scoring, risk-based thresholds, and a results report with failures retained.
