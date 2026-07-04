# Example: Brownfield RAG change - Add a new knowledge source with citations

A worked **Level 2 brownfield** change to an existing RAG answering system: add an approved knowledge
source and require citations. Shows the change flow (`pai-sdd-change`) with a spec delta, impact
analysis, and regression evals rather than a greenfield spec.

**Profile:** [rag-knowledge-system](../../profiles/rag-knowledge-system.md)

## Example prompts

| Skill | Prompt |
|---|---|
| `pai-sdd-change` | "We need to add the new pricing KB to the RAG bot and cite it." |
| `pai-ai-architecture-review` | "Review the retrieval-vs-generation boundary for the new source." |
| `pai-ai-evaluation` | "Add retrieval and citation regression evals for the pricing KB." |

## Artifacts

```
specs/FEAT-010/
├── spec.md              # existing system spec (updated)
├── change-proposal.md   # CHG-001 spec delta + impact + rollback
├── plan.md
├── tasks.md
└── verification.md
```

## Outcome

The change was scoped as a spec delta, evaluated for retrieval/citation regression, and rolled out
behind a flag with the prior index retained for rollback. See `verification.md`.
