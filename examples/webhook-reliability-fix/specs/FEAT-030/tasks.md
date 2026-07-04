---
id: FEAT-030
title: Webhook dedup - Tasks
plan: plan.md
updated_at: 2026-07-04
---

# Tasks

```yaml
- id: TASK-030
  title: Event-id dedup store check at the webhook boundary
  depends_on: []
  boundary:
    allowed_paths: ["src/webhook/", "src/dedup/"]
    prohibited_paths: []
  requirements: [REL-030, OBS-030]
  verification: [unit-test, integration-test]
  human_approval: false
  rollback_impact: low
  status: done
- id: TASK-031
  title: Per-user serialization for enqueued tasks
  depends_on: [TASK-030]
  boundary:
    allowed_paths: ["src/queue/"]
    prohibited_paths: []
  requirements: [REL-031, AC-031]
  verification: [integration-test]
  human_approval: false
  rollback_impact: medium
  status: done
- id: TASK-032
  title: Idempotent outbound send + redelivery regression test
  depends_on: [TASK-030]
  boundary:
    allowed_paths: ["src/reply/", "tests/"]
    prohibited_paths: []
  requirements: [REL-032, AC-030]
  verification: [unit-test, integration-test]
  human_approval: false
  rollback_impact: low
  status: done
```
