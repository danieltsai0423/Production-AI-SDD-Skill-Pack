---
name: pai-ai-contracts
description: Authors the formal contracts an AI system cannot express in natural-language prompts alone - AI behavior, model/prompt, data, RAG, tool, and human-oversight contracts. Use during planning for Level 2-3 AI features that communicate externally, use tools, retrieve knowledge, or handle sensitive data. Do not use for deterministic non-AI code or Level 0-1 edits.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: production-review
---

# Purpose

Make the implicit explicit: define allowed/disallowed AI behavior, model/prompt versioning, data and RAG
guarantees, tool permissions and side effects, and human-oversight triggers as versioned contracts.

# Use this skill when

- Planning Level 2/3 AI features involving external communication, tools, retrieval, or sensitive data.

# Do not use this skill when

- The code is deterministic and non-AI, or the edit is Level 0/1.

# Required inputs

- The spec/plan and the AI behavior, model, data, retrieval, and tools involved.

# Contract types

- **A. AI Behavior** — allowed/disallowed behavior, uncertainty & refusal & escalation behavior, tone/format, external-communication boundary.
- **B. Model & Prompt** — capability requirement vs implementation choice, prompt version, parameters, context budget, structured-output schema, fallback, cost/latency budget.
- **C. Data** — input/output schema, ownership, classification, retention, redaction, quality assumptions, validation.
- **D. RAG** — source authority, indexing, metadata, retrieval method, citation requirement, no-result behavior, freshness, evaluation.
- **E. Tool** — purpose, input/output schema, permission, preconditions, idempotency, timeout, retry, compensation/rollback, audit event, read/write/destructive classification.
- **F. Human Oversight** — trigger, owner, pause/resume behavior, approval SLA, conflict prevention, audit trail.

# Output contract

One file per applicable contract under `specs/<feature-id>/contracts/`, using the corresponding template.

# Rules

- Separate **capability requirement** ("supports structured output in the target language") from
  **implementation choice** ("currently uses model X vN"). Never write a specific model name as a permanent requirement.
- Every tool that writes or is destructive requires permission scope, idempotency, and human approval where impactful.

# Blocking conditions

- A high-risk tool has no permission model, idempotency, or human-approval path.

# Gotchas

- Natural-language prompt rules are not a contract — schema, permissions, and audit must be explicit.
- Uncertainty and refusal behavior are contract terms, not afterthoughts.

# References

- Pairs with `pai-security-privacy-review` and `pai-ai-evaluation`. Master Spec §10.12, §13.

# Completion criteria

- Each applicable contract exists, versioned, with capability/implementation separated and audit defined.
