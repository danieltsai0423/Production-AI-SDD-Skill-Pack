---
id: FEAT-010
title: RAG answering with approved-source citations
status: implemented
spec_level: 2
work_type: brownfield
owners:
  product: null
  engineering: null
  operations: null
risk_domains:
  - knowledge-accuracy
data_classification: internal
human_approval_required: false
created_at: 2026-07-04
updated_at: 2026-07-04
related_changes:
  - CHG-001
related_decisions: []
---

# Business outcome

Answer customer questions from approved knowledge with citations, so answers are trustworthy and
auditable.

# Functional requirements

- **FR-010** - Answers are grounded in retrieved approved sources and include citations.
- **FR-011** - On empty/low-confidence retrieval, the system says it lacks the information rather than
  guessing.

# AI behavior requirements

- **AI-010** - No uncited factual claims; retrieved content is treated as untrusted (no instruction
  execution).

# Data

- **DATA-010** - Only approved sources are indexed; each chunk carries source + timestamp metadata.

# Evaluation

- **EVAL-010** - Retrieval recall@5 and citation-correctness are measured separately and gated on
  every index/prompt/model change.

# Acceptance criteria (Given / When / Then)

- **AC-010** - Given a question answerable by an approved source, When answered, Then the answer cites
  that source.
- **AC-011** - Given a question with no approved source, When answered, Then the system declines.
