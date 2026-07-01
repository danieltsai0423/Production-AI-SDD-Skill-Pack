---
name: pai-sdd-change
description: Manages brownfield requirement, architecture, and behavior changes as a spec delta with impact analysis, compatibility, migration, and rollback, then merges the approved delta into the canonical spec. Use when changing an existing AI system's behavior, contracts, model/prompt/RAG, or data. Do not use for greenfield features (use pai-sdd-specify) or for Level 0 edits.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Handle changes to an existing system as a bounded delta - not a full rewrite - with explicit
compatibility, migration, and rollback analysis, then reconcile it into the canonical spec.

# Use this skill when

- Modifying existing behavior, APIs, contracts, model/prompt/RAG config, or data in a live system.

# Do not use this skill when

- Building a new greenfield feature, or making a Level 0 edit.

# Required inputs

- Current spec/behavior, the requested change, and the affected code/tests/runtime.

# Workflow

- [ ] 1. Scan current repository, spec, tests, and runtime assumptions; write a current-state summary.
- [ ] 2. Write the change proposal (reason, current vs target behavior).
- [ ] 3. Write a spec delta (not a rewrite).
- [ ] 4. Analyze backward compatibility, data migration, API/event compatibility, and prompt/model/RAG drift.
- [ ] 5. Define rollout, rollback, feature-flag/parallel-run, and documentation impact.
- [ ] 6. Implement and verify; then merge the approved delta into the canonical spec and archive the change.

## Change package

```text
changes/<change-id>/
+-- proposal.md
+-- impact.md
+-- spec-delta.md
+-- design.md
+-- tasks.md
+-- verification.md
\-- decisions/
```

# Output contract

Use `templates/change-proposal.md` and `templates/spec-delta.md`; produce the change package above.

# Blocking conditions

- An irreversible migration has no rollback.
- Backward-incompatible behavior change has no rollout/mitigation plan.

# Gotchas

- Do not just delete the old behavior (e.g. removing a review UI) - analyze impact and risk escalation first.
- Prompt/model/RAG changes are behavior changes even when code is untouched; run regression evals.

# References

- Use `pai-ai-evaluation` for regression, `pai-release-readiness` before rollout. Master Spec sec. 9.2, sec. 10.9, sec. 20.3.

# Completion criteria

- Change package complete; delta merged into canonical spec; traceability updated; change archived.
