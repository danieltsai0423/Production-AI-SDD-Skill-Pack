# Example: Greenfield AI feature - Human takeover for AI conversations

A worked, end-to-end SDD run for a **Level 3** conversational-AI feature. It shows how the pack
routes a request through discovery → specify → clarify → plan → tasking → implement → verify → close,
and which contracts and reviews a high-risk feature pulls in.

**Profile:** [conversational-ai](../../profiles/conversational-ai.md)

## Example prompts (per skill)

| Skill | Prompt that triggers it |
|---|---|
| `pai-sdd-orchestrator` | "Build a human-takeover feature so agents can take over an AI chat." |
| `pai-sdd-discovery` | "Classify the risk and scope of adding human takeover to our support bot." |
| `pai-sdd-specify` | "Write a testable spec for human takeover of AI conversations." |
| `pai-sdd-clarify` | "What must we decide before building takeover?" |
| `pai-sdd-plan` | "Turn the takeover spec into architecture, contracts, and rollout." |
| `pai-sdd-tasking` | "Break the takeover plan into reversible tasks." |
| `pai-sdd-verify` | "Prove the takeover feature meets its spec." |
| `pai-ai-contracts` | "Author the AI-behavior and human-oversight contracts for takeover." |
| `pai-reliability-review` | "Review dedup and ordering for the takeover message path." |
| `pai-security-privacy-review` | "Review transcript privacy for takeover." |

## Artifacts

```
specs/FEAT-001/
├── spec.md            # testable requirements + acceptance criteria
├── clarifications.md  # decisions that unblocked planning
├── plan.md            # architecture, contracts, failure strategy, rollout
├── tasks.md           # reversible, path-bounded tasks
├── verification.md    # requirement -> evidence -> decision
└── contracts/
    ├── ai-behavior-contract.md
    └── human-oversight-contract.md
```

## Outcome

Level 3 classification pulled in reliability + security/privacy reviews, an AI-behavior contract, a
human-oversight contract, evals for escalation correctness, and a staged rollout with rollback. See
`verification.md` for the requirement-by-requirement evidence and the final decision.
