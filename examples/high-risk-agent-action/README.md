# Example: High-risk agent action - Refund approval agent

A worked **Level 3** feature: an LLM agent that proposes refunds but never issues one without human
approval. Shows the read/propose/approve/execute permission split, idempotent execution, safety evals
(prompt injection cannot escalate to the refund tool), and human oversight.

**Profile:** [agent-tool-use](../../profiles/agent-tool-use.md)

## Example prompts

| Skill | Prompt |
|---|---|
| `pai-sdd-orchestrator` | "Add an agent that can approve small refunds automatically." (→ discovery flags Level 3) |
| `pai-ai-contracts` | "Write the tool and human-oversight contracts for the refund agent." |
| `pai-security-privacy-review` | "Review the refund agent for tool injection and privilege escalation." |
| `pai-release-readiness` | "Gate the refund agent for release." |

## Artifacts

```
specs/FEAT-020/
├── spec.md
├── plan.md
├── tasks.md
├── verification.md
└── contracts/
    ├── tool-contract.md
    └── human-oversight-contract.md
```

## Outcome

The "approve small refunds automatically" request was down-scoped: the agent *proposes*, a human
*approves*, execution is idempotent and audited. Safety evals prove a prompt-injection attempt cannot
reach the refund tool. See `verification.md`.
