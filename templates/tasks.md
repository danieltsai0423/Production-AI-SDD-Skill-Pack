---
id: FEAT-000
title: <feature title> - Tasks
plan: plan.md
updated_at: 2026-07-01
---

# Task ordering

1. Walking skeleton / hardest uncertainty
2. Contracts and test harness
3. Core domain behavior
4. Integration
5. Failure handling
6. Observability
7. Migration / release
8. Documentation

# Tasks

```yaml
- id: TASK-001
  title: <imperative, specific>
  depends_on: []
  boundary:
    allowed_paths: []
    prohibited_paths: []
  requirements: []          # e.g. FR-003, REL-002
  verification: []          # e.g. unit-test, integration-test, ai-eval
  human_approval: false     # true for Level 3 impactful actions
  rollback_impact: low      # low | medium | high
  status: pending           # pending | in_progress | done
```
