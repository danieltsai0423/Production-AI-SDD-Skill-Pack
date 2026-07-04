---
id: FEAT-001
title: Human takeover - Tasks
plan: plan.md
updated_at: 2026-07-04
---

# Task ordering

1. Walking skeleton / hardest uncertainty (send-time state race)
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
  title: Add conversation state fields and send-time re-check in the reply worker
  depends_on: []
  boundary:
    allowed_paths: ["src/conversation/", "src/reply_worker/"]
    prohibited_paths: ["src/billing/"]
  requirements: [FR-002, AI-001, NFR-001]
  verification: [unit-test, integration-test]
  human_approval: false
  rollback_impact: medium
  status: done
- id: TASK-002
  title: Takeover/release endpoints with server-side authz and audit
  depends_on: [TASK-001]
  boundary:
    allowed_paths: ["src/conversation/", "src/backoffice/"]
    prohibited_paths: []
  requirements: [FR-001, FR-003, SEC-001]
  verification: [unit-test, integration-test]
  human_approval: false
  rollback_impact: medium
  status: done
- id: TASK-003
  title: Idempotent outbound send with message-id dedup
  depends_on: [TASK-001]
  boundary:
    allowed_paths: ["src/reply_worker/"]
    prohibited_paths: []
  requirements: [REL-001, AC-003]
  verification: [unit-test, integration-test]
  human_approval: false
  rollback_impact: low
  status: done
- id: TASK-004
  title: Internal AI draft suggestions (stored separately, never delivered)
  depends_on: [TASK-002]
  boundary:
    allowed_paths: ["src/reply_worker/", "src/backoffice/"]
    prohibited_paths: []
  requirements: [FR-004, PRIV-001]
  verification: [unit-test]
  human_approval: false
  rollback_impact: low
  status: done
- id: TASK-005
  title: High-risk manual-release rule + inactivity auto-release for normal cases
  depends_on: [TASK-002]
  boundary:
    allowed_paths: ["src/conversation/"]
    prohibited_paths: []
  requirements: [FR-003, AC-002]
  verification: [unit-test, ai-eval]
  human_approval: true
  rollback_impact: medium
  status: done
- id: TASK-006
  title: Escalation + takeover-respect evals and canary rollout flag
  depends_on: [TASK-003, TASK-004, TASK-005]
  boundary:
    allowed_paths: ["evals/", "src/config/"]
    prohibited_paths: []
  requirements: [AI-002, AC-001]
  verification: [ai-eval, integration-test]
  human_approval: true
  rollback_impact: low
  status: done
```
