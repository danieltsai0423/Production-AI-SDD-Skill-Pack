---
name: pai-ai-architecture-review
description: Reviews an AI application's component boundaries, data and state ownership, sync/async split, failure isolation, scalability, and vendor lock-in, flagging common production anti-patterns. Use during planning for Level 2-3 work that adds or changes AI components, orchestration, tools, or data flow. Do not use for pure prompt-wording tweaks or Level 0-1 edits with no architectural impact.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: production-review
---

# Purpose

Assess whether an AI system's structure is sound: clear boundaries, correct sync/async split, isolated
failures, and no reliance on brittle single-prompt or single-fallback designs.

# Use this skill when

- Planning Level 2/3 work that adds or changes AI components, orchestration, tools, or data flow.

# Do not use this skill when

- The change is a prompt-wording tweak or a Level 0/1 edit with no architectural impact.

# Required inputs

- The plan/spec, current architecture, and data/state ownership.

# Review dimensions

User/business flow · system boundaries · model boundary · orchestration boundary · tool boundary ·
data & state ownership · sync/async split · failure isolation · scalability · portability · vendor
lock-in · cost · latency · observability · testability.

# Anti-patterns to flag

- All logic stuffed into a single agent prompt.
- Webhook synchronously waiting on long AI inference.
- Workflow state stored only in conversation text.
- LLM deciding deterministic authorization.
- External event handling with no idempotency.
- Tool invocation with no schema, timeout, retries, or permission.
- Knowledge base / prompt / model updated without versioning.
- n8n / low-code flows with no export, versioning, tests, or error path.
- Only `/health`, no dependency readiness.
- A single fallback hiding all failures.

# Output contract

```markdown
# Architecture Review
## Scope
## Findings (blocker / major / minor)
## Anti-patterns detected
## Recommendations
## Risks and limitations
```

# Blocking conditions

- An unmitigated blocker anti-pattern in a Level 3 path (e.g. LLM-controlled authorization on real actions).

# Gotchas

- Reviewers must read the plan/diff independently, not inherit the implementer's conclusions.
- Not every low-latency endpoint needs a queue — flag the anti-pattern, not the pattern's absence.

# References

- Pairs with `pai-reliability-review` and `pai-ai-contracts`. Master Spec §10.11, §19.

# Completion criteria

- Findings ranked blocker/major/minor with concrete recommendations and residual risks.
