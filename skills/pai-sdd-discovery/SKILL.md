---
name: pai-sdd-discovery
description: Classifies AI software work by type and risk (Level 0-3), inspects repository context, and selects the minimum sufficient SDD workflow before any code is written. Use before implementing new AI features, cross-module changes, architecture changes, risky automation, or when requirements are unclear. Do not use for trivial formatting-only edits or pure concept explanations.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Decide what kind of work this is, how risky it is, what evidence already exists, and the minimum
workflow needed — before editing code. It prevents both over-engineering trivial edits and
under-specifying dangerous ones.

# Use this skill when

- Starting any non-trivial change, or at the beginning of `pai-sdd-orchestrator`.
- Requirements, scope, or risk are unclear.

# Do not use this skill when

- The edit is formatting/comment-only (Level 0 can be handled directly).
- The request is purely explanatory.

# Required inputs

- Root instructions (`AGENTS.md`/`CLAUDE.md`), existing specs/changes/ADRs, related code, tests,
  and deployment/runtime docs.

Inspect the repository before asking the user. Never classify from the prompt alone.

# Workflow

- [ ] 1. Read root instructions and any active specs/changes/ADRs.
- [ ] 2. Identify code ownership, related modules, tests, and deployment.
- [ ] 3. Determine work type: greenfield / brownfield / incident / research spike.
- [ ] 4. Determine Level 0–3 using the risk table.
- [ ] 5. List assumptions, unknowns, dependencies, and affected interfaces.
- [ ] 6. Emit the Discovery Report.

## Risk classification

- Level 0: typo/format/comment, safe config, behavior-preserving refactor.
- Level 1: small feature, single module, low data risk.
- Level 2: cross-module, new API/DB/queue/external integration, architecture trade-offs.
- Level 3: external AI communication, tools with real-world effect, sensitive/PII/medical/legal/
  financial/minors data, payments/refunds/deletions/permission changes, high-concurrency critical services.

# Output contract

```markdown
# Discovery Report

## Classification
- Work type:
- SDD level:
- Risk rationale:

## Existing evidence
- Relevant specs / code / tests / runtime docs:

## Impact surface
- Components / APIs & events / Data / Models-prompts-RAG / Users & operations:

## Unknowns
- Critical:
- Non-critical:

## Recommended workflow
- Required artifacts:
- Required reviews:
- Suggested validation:
```

# Blocking conditions

- Cannot determine ownership or blast radius of the change.
- Critical unknowns that make safe implementation impossible.

# Gotchas

- A simple new API that executes a payment is still Level 3.
- A prompt-only change may not touch code yet still change production behavior — do not mark it Level 0.

# References

- Master Spec §5.2 (risk levels), §10.2. Hand back to `pai-sdd-orchestrator` with the chosen Level.

# Completion criteria

- Discovery Report exists with a defensible Level and required-artifact list.
- Assumptions and critical unknowns are explicit.
