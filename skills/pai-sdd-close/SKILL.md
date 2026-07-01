---
name: pai-sdd-close
description: Finalizes a piece of work by reconciling specs, evidence, documentation, and operational handoff before it is considered done. Use at the end of Level 1-3 work after verification passes. Do not use as a substitute for verification, or for Level 0 edits.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Ensure nothing dangling remains: specs, contracts, ADRs, evidence, runbooks, and follow-ups are all
consistent before the work is closed.

# Use this skill when

- Verification has passed and the work is ready to be finalized.

# Do not use this skill when

- Verification has not passed, or the change is Level 0.

# Required inputs

- Verification Report, spec/contracts/ADRs, and operational docs.

# Workflow (checklist)

- [ ] 1. All task statuses are consistent.
- [ ] 2. Spec, contracts, and ADRs are updated.
- [ ] 3. Verification evidence is reproducible.
- [ ] 4. Known limitations are recorded.
- [ ] 5. Runbook, rollback, and monitors are complete.
- [ ] 6. Change is archived.
- [ ] 7. Release notes are generated.
- [ ] 8. Unfinished items are tracked as follow-ups.

# Output contract

A close-out summary listing updated artifacts, reproducible evidence locations, known limitations,
and tracked follow-ups.

# Blocking conditions

- Verification evidence cannot be reproduced.
- A Level 3 change lacks a runbook, rollback, or monitor.

# Gotchas

- Closing without recording known limitations pushes hidden risk to operations.
- Follow-ups left only in chat are lost — file them as tracked items.

# References

- Master Spec §10.10, §25 (Definition of Done).

# Completion criteria

- Close-out checklist satisfied; artifacts consistent; follow-ups tracked.
