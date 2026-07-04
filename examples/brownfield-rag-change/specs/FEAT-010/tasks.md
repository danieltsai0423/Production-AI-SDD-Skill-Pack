---
id: FEAT-010
title: RAG citation change - Tasks
plan: plan.md
updated_at: 2026-07-04
---

# Tasks

```yaml
- id: TASK-010
  title: Ingest approved pricing KB into a new index namespace with metadata
  depends_on: []
  boundary:
    allowed_paths: ["src/ingestion/", "src/retrieval/"]
    prohibited_paths: []
  requirements: [DATA-010]
  verification: [unit-test, integration-test]
  human_approval: false
  rollback_impact: low
  status: done
- id: TASK-011
  title: Merge retrieval across namespaces and enforce citations in generation
  depends_on: [TASK-010]
  boundary:
    allowed_paths: ["src/retrieval/", "src/generation/"]
    prohibited_paths: []
  requirements: [FR-010, FR-011, AI-010]
  verification: [integration-test, ai-eval]
  human_approval: false
  rollback_impact: medium
  status: done
- id: TASK-012
  title: Retrieval + citation regression evals behind the pricing_kb flag
  depends_on: [TASK-011]
  boundary:
    allowed_paths: ["evals/", "src/config/"]
    prohibited_paths: []
  requirements: [EVAL-010, AC-010, AC-011]
  verification: [ai-eval]
  human_approval: false
  rollback_impact: low
  status: done
```
