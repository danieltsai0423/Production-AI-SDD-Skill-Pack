# Examples

End-to-end worked SDD runs across several AI project types. Each is a real set of artifacts (spec,
plan, tasks, verification, and contracts where the risk level requires them) that a full run through
the `pai-*` skills produces. They double as output-eval fixtures.

| Example | Type | Level | Shows |
|---|---|---|---|
| [greenfield-ai-feature](greenfield-ai-feature/) | Conversational AI | 3 | Full greenfield run, human takeover, AI-behavior + human-oversight contracts |
| [brownfield-rag-change](brownfield-rag-change/) | RAG / knowledge | 2 | Change flow, spec delta, retrieval vs citation evals |
| [high-risk-agent-action](high-risk-agent-action/) | Agent tool use | 3 | Propose/approve/execute split, tool contract, injection safety evals |
| [webhook-reliability-fix](webhook-reliability-fix/) | Reliability / automation | 2 | Incident → dedup/idempotency fix with a regression test |

Every `spec.md` passes `python scripts/validate_specs.py --specs-dir examples/<name>/specs`, and every
Markdown link resolves. See each example's README for the per-skill example prompts.

Together these cover more than three distinct AI project types running the complete workflow
(Master Spec DoD sec. 25.3).
