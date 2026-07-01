---
name: pai-sdd-implement
description: Implements the minimum correct change for a single approved task within its path boundary, test-first where behavior is deterministic, without scope creep or hidden failures. Use when executing one task from tasks.md. Do not use to design architecture, to implement multiple tasks at once, or to add unspecified features.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Make the smallest correct change that satisfies one task and its linked requirements, staying inside the
task boundary and leaving reproducible evidence.

# Use this skill when

- Executing a single task from `tasks.md`.

# Do not use this skill when

- Designing architecture, batching multiple tasks, or adding features the spec did not approve.

# Required inputs

- One task, its linked requirements, the plan, and relevant references.

# Workflow

- [ ] 1. Read the single task, its requirements, plan, and references.
- [ ] 2. Check git status and existing changes.
- [ ] 3. Find or create a failing test / verification case.
- [ ] 4. Implement the minimum change.
- [ ] 5. Run targeted tests.
- [ ] 6. Check the boundary — revert any unrelated changes.
- [ ] 7. Self-review, then update the task's implementation notes.
- [ ] 8. Have an independent reviewer or fresh context verify before moving on.

## Rules

- Deterministic behavior: RED → GREEN → REFACTOR.
- AI quality: combine fixed datasets, rubric, threshold, and failure analysis — not unit tests alone.

# Must avoid

- Adding features without spec approval.
- Relaxing error requirements to make a test pass.
- Editing unrelated files or hiding failing tests.
- Mocking away the integration that actually needs verifying.
- Swallowing all errors in a fallback with no alerting.

# Blocking conditions

- The task cannot be implemented within its boundary.
- A required test/verification cannot be established.

# Gotchas

- "Tests pass" on a single happy path is not completion.
- Fresh-context verification catches boundary drift the author cannot see.

# References

- Hand off to `pai-sdd-verify` for evidence collection. Master Spec §10.7, §5.3.

# Completion criteria

- Minimum change implemented; targeted tests pass; boundary respected; notes and evidence recorded.
