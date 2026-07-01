---
name: pai-sdd-tasking
description: Breaks approved work into small tasks that are independently implementable, verifiable, and reversible, each with explicit path boundaries, linked requirements, verification, and rollback impact. Use after pai-sdd-plan for Level 2-3 work, or directly after a light Level 1 spec that needs no separate plan. Do not use before a plan or Level 1 spec exists, or for a single Level 0 edit.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Convert a plan into ordered, bounded tasks that each fit in one implementation context, carry their own
acceptance evidence, and can be rolled back independently.

# Use this skill when

- A plan (or a light Level 1 spec) is ready to be executed.

# Do not use this skill when

- No plan (Level 2-3) or light spec (Level 1) exists yet, or the change is a single Level 0 edit.

## Level 1 vs Level 2-3

At Level 1 there is no `plan.md`; derive tasks directly from the light `spec.md`. At Level 2-3, derive
tasks from `plan.md` and its contracts. Either way, do not invent a heavy plan just to run this skill.

# Required inputs

- `plan.md` (or Level 1 `spec.md`), contracts, and the requirement IDs to satisfy.

# Workflow

- [ ] 1. Derive tasks from the plan's components and contracts.
- [ ] 2. Give each task an ID, boundary (allowed/prohibited paths), linked requirements, verification, and rollback impact.
- [ ] 3. Order tasks: walking skeleton / hardest uncertainty first, then contracts, core behavior, integration, failure handling, observability, migration/release, docs.
- [ ] 4. Mark human-approval points for Level 3 tasks.
- [ ] 5. Save `tasks.md`.

## Task shape

```yaml
id: TASK-001
title: Add idempotent event persistence
depends_on: []
boundary:
  allowed_paths: [src/events/, tests/events/]
  prohibited_paths: [migrations/unrelated/]
requirements: [FR-003, REL-002]
verification: [unit-test, integration-test]
rollback_impact: low
status: pending
```

## Rules

- A task must be completable in an isolated context.
- No vague tasks ("finish backend", "handle errors").
- Every task carries acceptance evidence; Level 3 tasks mark human-approval points.

# Output contract

Use `templates/tasks.md`. Each task validates against the task shape above.

# Blocking conditions

- A task cannot be bounded or verified independently - return to `pai-sdd-plan`.

# Gotchas

- Ordering by convenience instead of by risk hides the hardest uncertainty until the end.
- Boundaries that overlap unrelated modules invite scope creep during implement.

# References

- Use `templates/tasks.md`; hand tasks to `pai-sdd-implement` one at a time. Master Spec sec. 10.6.

# Completion criteria

- `tasks.md` exists; every task is bounded, linked to requirements, and independently verifiable.
