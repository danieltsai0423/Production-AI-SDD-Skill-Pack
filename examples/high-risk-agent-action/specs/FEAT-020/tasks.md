---
id: FEAT-020
title: Refund agent - Tasks
plan: plan.md
updated_at: 2026-07-04
---

# Tasks

```yaml
- id: TASK-020
  title: Read tools + propose_refund tool for the agent (no execute binding)
  depends_on: []
  boundary:
    allowed_paths: ["src/agent/", "src/tools/"]
    prohibited_paths: ["src/payments/execute/"]
  requirements: [FR-020, AI-020]
  verification: [unit-test, integration-test]
  human_approval: false
  rollback_impact: low
  status: done
- id: TASK-021
  title: Human approval workflow + authorized execute_refund with idempotency
  depends_on: [TASK-020]
  boundary:
    allowed_paths: ["src/payments/", "src/backoffice/"]
    prohibited_paths: []
  requirements: [FR-021, FR-022, SEC-020, REL-020, OPS-020]
  verification: [unit-test, integration-test]
  human_approval: true
  rollback_impact: high
  status: done
- id: TASK-022
  title: Safety evals - injection cannot escalate to execute_refund
  depends_on: [TASK-021]
  boundary:
    allowed_paths: ["evals/safety/"]
    prohibited_paths: []
  requirements: [SEC-021, AC-020, AC-021, AC-022]
  verification: [ai-eval]
  human_approval: true
  rollback_impact: low
  status: done
```
