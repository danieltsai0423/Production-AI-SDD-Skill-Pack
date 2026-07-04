---
id: FEAT-010
title: RAG citation change - Plan
spec: spec.md
updated_at: 2026-07-04
---

# Architecture

Add a `pricing` index namespace; retrieval queries both namespaces and merges by score; the generator
must cite the winning chunks. Retrieval and generation stay separate components with separate evals.

# Failure strategy

- Empty/low-confidence merged retrieval -> decline (FR-011).
- Poisoned/instructional source text -> treated as data, never executed (AI-010).

# Domain reviews selected

- `pai-ai-architecture-review` (retrieval/generation boundary, source authority).
- `pai-ai-evaluation` (separate retrieval + citation evals).

# Rollout & rollback

- Flag `pricing_kb`, canary, compare to baseline; rollback by disabling the flag.
