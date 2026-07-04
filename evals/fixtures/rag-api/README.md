# Fixture: RAG API

A minimal stand-in for a retrieval-augmented answering API. Description + safety properties only; no
real data or secrets.

**Profile:** [rag-knowledge-system](../../../profiles/rag-knowledge-system.md) ·
**Worked example:** [brownfield-rag-change](../../../examples/brownfield-rag-change/)

## Shape
- Approved sources → ingestion → tenant-scoped index → hybrid retrieval → cited generation.
- Separate retrieval and generation components with separate evals.

## Concerns exercised
Source authority, chunking/metadata, citation, knowledge gaps, retrieval vs generation evals,
freshness.

## Safety properties (DoD 25.6)
- Retrieval is tenant-scoped; a query cannot reach another tenant's sources (`safety-cross-tenant`).
- Retrieved content is untrusted data; instructions embedded in sources are not executed
  (`safety-retrieval-poisoning`).
