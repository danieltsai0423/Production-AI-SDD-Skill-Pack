---
name: pai-sdd-specify
description: Turns vague AI feature requirements into a testable, solution-agnostic specification with IDs, acceptance criteria, and AI-specific behavior boundaries. Use after discovery for Level 1-3 work when defining what to build and how it will be accepted. Do not use for implementation planning (use pai-sdd-plan) or for Level 0 edits.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Convert an ambiguous request into an acceptance-ready specification that is decoupled from any
particular framework, so implementation and verification have a stable contract.

# Use this skill when

- Discovery classified the work as Level 1-3.
- The team needs agreed, testable requirements before design.

# Do not use this skill when

- The work is Level 0, or you are choosing a technical solution (use `pai-sdd-plan`).

# Required inputs

- Discovery Report, business goal, affected users, related code/specs.

# Workflow

- [ ] 1. Capture business outcome, users/actors, and the current problem.
- [ ] 2. Define in-scope / out-of-scope and user journeys.
- [ ] 3. Write functional (`FR-*`), non-functional (`NFR-*`), and AI (`AI-*`) requirements with IDs.
- [ ] 4. Define failure scenarios, acceptance criteria (Given/When/Then), and measurable success metrics.
- [ ] 5. Record data classification and human responsibility.
- [ ] 6. Fill `templates/spec.md` and save under `specs/<feature-id>/spec.md`.

## Rules

- Requirements describe **what/why**, not the framework.
- Acceptance criteria use Given/When/Then; AI quality must be measurable, never "natural/correct/nice".
- Every requirement has an ID (`BUS-`, `USR-`, `FR-`, `NFR-`, `AI-`, `DATA-`, `SEC-`, `PRIV-`, `REL-`, `OBS-`, `OPS-`, `EVAL-`).

## AI-specific requirements to define

- Answerable vs non-answerable scope; behavior under uncertainty.
- Tool-use boundaries; human takeover conditions.
- Latency and cost expectations; data sources and citation requirements.
- Acceptable vs unacceptable error types.

# Output contract

Use `templates/spec.md`. Every requirement is uniquely identified and testable.

# Blocking conditions

- Critical requirements contradict each other and cannot be resolved from evidence.
- AI quality cannot be expressed measurably - escalate to `pai-sdd-clarify`.

# Gotchas

- Do not smuggle a chosen technology into requirements; keep capability vs implementation separate.
- "The AI should be helpful" is not a requirement - define observable, measurable behavior.

# References

- Use `templates/spec.md`. For unresolved ambiguity, hand to `pai-sdd-clarify`. Master Spec sec. 10.3, sec. 12.

# Completion criteria

- `spec.md` exists with IDs, Given/When/Then acceptance, measurable metrics, and AI boundaries.
