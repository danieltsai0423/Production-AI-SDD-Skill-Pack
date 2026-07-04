---
id: CHG-001
title: Add pricing knowledge base with citations
target_spec: FEAT-010
status: implemented
risk_level: 2
created_at: 2026-07-04
updated_at: 2026-07-04
---

# Reason for change

Customers ask pricing questions the bot cannot currently answer; a new approved pricing KB exists.

# Current behavior

Retrieval covers the product KB only; pricing questions hit the empty-retrieval decline path.

# Target behavior

Index the approved pricing KB, retrieve across both sources, and cite the pricing source (FR-010,
DATA-010).

# Impact analysis

- Backward compatibility: additive source; existing answers unchanged.
- Data migration: new index namespace; prior index retained.
- API / event compatibility: none.
- Prompt / model / RAG drift: retrieval set changes -> regression evals required (EVAL-010).
- Documentation impact: update source registry.

# Rollout & rollback

- Rollout strategy: flag `pricing_kb` on a canary; compare citation-correctness vs baseline.
- Feature flag / parallel run: yes.
- Rollback: disable flag; prior index namespace still live.
- Regression evals required: retrieval recall@5, citation-correctness, decline-on-gap.
