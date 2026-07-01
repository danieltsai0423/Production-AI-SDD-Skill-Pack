---
contract: rag
id: RAGC-000
feature: FEAT-000
version: "1.0.0"
status: draft
updated_at: 2026-07-02
---

# RAG Contract

## Authoritative source
<which corpus is the source of truth; who owns ingestion>

## Update cadence
<how often the index is refreshed>

## Chunk & metadata contract
- Chunking strategy:
- Required metadata (source id, tenant, timestamp, permissions):

## Retrieval strategy
- Method (vector / hybrid / rerank):
- Filtering / tenant boundary:
- Top-k / thresholds:

## Citation / provenance
<required citation format; page/section-level provenance>

## No-result behavior
<what the system does when retrieval returns nothing relevant>

## Freshness
<max acceptable staleness>

## Evaluation
- Retrieval quality dataset:
- Reindex / rollback procedure:
