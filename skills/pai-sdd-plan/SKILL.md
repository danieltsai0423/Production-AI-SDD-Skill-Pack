---
name: pai-sdd-plan
description: Turns a confirmed AI system spec into technical architecture, contracts, data flow, failure strategy, tests, and rollout, and selects the domain reviews the change needs. Use for Level 2-3 work after the spec and clarifications are settled. Do not use before requirements are agreed or for Level 0-1 edits that need no architecture decisions.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Translate an agreed spec into an executable technical plan: architecture, contracts, data/state, failure
handling, security/privacy, observability, tests, migration, deployment, rollback, and decision records.

# Use this skill when

- The Level 2/3 spec and clarifications are settled and design decisions are needed.

# Do not use this skill when

- Requirements are not yet agreed, or the change needs no architecture decisions.

# Required inputs

- `spec.md`, `clarifications.md`, current architecture, existing patterns and constraints.

# Workflow

- [ ] 1. Describe current state and target architecture with component boundaries.
- [ ] 2. Define data flow and sync/async boundaries.
- [ ] 3. Specify API/event contracts, state model, and persistence.
- [ ] 4. Define failure strategy, security/privacy, and observability.
- [ ] 5. Define test strategy, migration, deployment, and rollback.
- [ ] 6. Note cost/latency implications and write decision records (alternatives + consequences).
- [ ] 7. Select domain reviews and run them.

## Select domain reviews

Call the ones the change touches:

- `pai-ai-architecture-review` — new/changed component boundaries or data/state ownership.
- `pai-ai-contracts` — model/prompt/RAG/tool/data/human-oversight behavior.
- `pai-reliability-review` — events, queues, background jobs, external dependencies.
- `pai-security-privacy-review` — sensitive data, auth, tenancy, untrusted content.
- `pai-ai-evaluation` — any non-deterministic AI behavior.

## Rules

- Prefer existing repository patterns unless the spec requires change.
- Attack the largest uncertainty and irreversible risk first.
- Give every third-party API/model/workflow a fallback and an owner.
- Each architecture decision records alternatives and consequences.

# Output contract

Use `templates/plan.md`, plus contract files under `specs/<feature-id>/contracts/` and
decision records under `decisions/`.

# Blocking conditions

- A required domain review surfaces an unmitigated high risk.
- No viable fallback/ownership exists for a critical external dependency.

# Gotchas

- Do not invent a new architecture when an existing pattern satisfies the spec.
- A plan without a rollback path is not done for Level 3.

# References

- Use `templates/plan.md`; invoke the domain-review skills above. Master Spec §10.5, §13, §19.

# Completion criteria

- `plan.md`, contracts, and decision records exist; selected reviews passed or logged mitigations.
