---
name: pai-sdd-clarify
description: Resolves the ambiguities that would affect architecture, risk, or acceptance before planning, recording decisions and assumptions in the spec rather than in chat. Use when a Level 2-3 spec has open questions about product, data, AI behavior, integration, permissions, operations, compliance, or acceptance. Do not use for trivial edits or when the spec is already unambiguous.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Remove the specific ambiguities that change architecture, risk, or acceptance - before design starts -
and persist the resulting decisions so they are not lost in conversation.

# Use this skill when

- A Level 2/3 spec has open questions that materially affect design or risk.

# Do not use this skill when

- The spec is unambiguous, or ambiguity is cosmetic and can be safely assumed.

# Required inputs

- The draft `spec.md`, repository evidence, and any stakeholder constraints.

# Workflow

- [ ] 1. Classify each ambiguity: product, data, AI behavior, integration, permission, operational, compliance, acceptance.
- [ ] 2. Try to answer from the repository/docs first.
- [ ] 3. For safe cases, record an explicit assumption.
- [ ] 4. For irreversible/high-risk unknowns, mark as a blocker.
- [ ] 5. For non-blocking unknowns, record as open question / follow-up.
- [ ] 6. Update the spec and write `clarifications.md`.

## Resolution strategy

Prefer evidence over asking. Ask the user only when a critical, high-risk ambiguity cannot be resolved
from available evidence. Never leave a resolved answer only in chat - write it into the spec.

# Output contract

`clarifications.md` records, per item: Question ID, decision/assumption, source/decision owner,
affected requirements, date, and revisit condition.

# Blocking conditions

- An irreversible or high-risk decision cannot be made safely from available evidence and has no owner.

# Gotchas

- Assumptions must be explicit and traceable, not silent defaults.
- A single unclear permission or data-classification question can flip the whole risk Level.

# References

- Use `templates/clarifications.md`. Feed decisions back into `spec.md`. Master Spec sec. 10.4.

# Completion criteria

- `clarifications.md` exists; the spec reflects the decisions; blockers are escalated with owners.
