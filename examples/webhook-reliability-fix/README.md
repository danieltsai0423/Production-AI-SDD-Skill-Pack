# Example: Webhook reliability fix - Stop duplicate replies

A worked **Level 2 brownfield** reliability fix for the classic duplicate-reply incident (the SOP's
own five-whys example): a redelivered webhook caused a second customer reply because there was no
event deduplication. Shows the incident → change → verification path.

**Profile:** [conversational-ai](../../profiles/conversational-ai.md) +
[workflow-automation](../../profiles/workflow-automation.md)

## Example prompts

| Skill | Prompt |
|---|---|
| `pai-incident-postmortem` | "Customers got duplicate replies; find the root cause and prevent it." |
| `pai-reliability-review` | "Review our webhook path for dedup, ordering, and idempotency." |
| `pai-sdd-change` | "Add event dedup to the webhook consumer." |

## Artifacts

```
specs/FEAT-030/
├── spec.md
├── plan.md
├── tasks.md
└── verification.md
```

## Outcome

Root cause: webhook redelivery + no event dedup + a design that only handled the single-success path.
Fix: dedup by event id, per-user serialization, idempotent send, and a redelivery regression test so
it cannot recur. See `verification.md`.
