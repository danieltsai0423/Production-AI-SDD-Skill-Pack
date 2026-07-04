# Profile: RAG / Knowledge System

Overlay for retrieval-augmented generation and knowledge-base answering. Apply in addition to the
core SDD workflow.

**Apply when:** the system retrieves from a knowledge source to ground generation, cites sources, or
maintains an ingestion pipeline.
**Not universal:** a specific vector DB, embedding model, or reranker belongs in `examples/`/profiles,
never in canonical skills.

## Additional focus (Master Spec sec. 11.2)

- **Source authority** — only approved sources feed answers; track source ownership and trust level.
- **Ingestion pipeline** — versioned, reproducible ingestion; know what is indexed and when.
- **Chunking & metadata** — chunk strategy and metadata (source, section, timestamp, permissions).
- **Hybrid retrieval / reranking** — combine lexical + semantic; rerank; measure retrieval quality
  separately from generation.
- **Freshness** — define staleness limits and re-index triggers.
- **Citation** — answers cite retrieved sources; uncited claims are a defect.
- **Knowledge gaps** — when retrieval is empty/low-confidence, say so or escalate; never fabricate.
- **Separate evals** — evaluate retrieval (recall@k, precision) and generation (faithfulness,
  citation correctness) independently.

## SDD adjustments

- **Specify:** add `AI-*` for grounding/citation/uncertainty, `DATA-*` for source classification and
  retention, `EVAL-*` for retrieval and generation thresholds.
- **Contracts:** author a [rag-contract](../templates/contracts/rag-contract.md),
  [data-contract](../templates/contracts/data-contract.md), and
  [evaluation-contract](../templates/contracts/evaluation-contract.md).
- **Reviews:** run [pai-ai-architecture-review](../skills/pai-ai-architecture-review/) (retrieval vs
  generation boundary) and [pai-security-privacy-review](../skills/pai-security-privacy-review/) for
  retrieval poisoning and per-document permissions.
- **Evals:** fixed question set with known-answer and known-gap cases; regression on every
  prompt/model/index change.

## Checklist

- [ ] Approved-source list and ingestion versioning.
- [ ] Chunk + metadata schema (incl. access control).
- [ ] Retrieval eval (recall@k) separate from generation eval (faithfulness/citation).
- [ ] Empty/low-confidence retrieval path (escalate or "I don't know").
- [ ] Freshness / re-index policy.
- [ ] Indirect prompt-injection defense on retrieved content.

## Common anti-patterns

- Answering confidently from an empty retrieval (hallucinated grounding).
- Evaluating only end-to-end, so retrieval regressions hide behind a good generator.
- Indexing unapproved or unpermissioned documents.
- Treating retrieved text as trusted instructions (injection via poisoned sources).
