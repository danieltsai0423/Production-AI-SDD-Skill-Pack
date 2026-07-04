---
id: FEAT-020
title: Refund agent - Plan
spec: spec.md
updated_at: 2026-07-04
---

# Architecture

Read/propose/approve/execute are four separate capabilities with separate identities:

```
agent (read tools + propose_refund)  ->  proposal (pending)
                                          |
human approver (execute_refund, authz) -> idempotent execution -> audit
```

The agent identity has no binding to `execute_refund`. Execution is a separate service call keyed by
an idempotency key.

# Contracts

- [tool-contract](contracts/tool-contract.md) - tool registry, permission tiers, idempotency.
- [human-oversight-contract](contracts/human-oversight-contract.md) - approval authority, audit,
  rollback.

# Failure strategy

- Duplicate approval event -> idempotency key makes execution a no-op (REL-020).
- Injection via order/message content -> treated as data; tool set is fixed (SEC-021, AI-020).

# Domain reviews selected

- `pai-security-privacy-review` (tool injection, privilege escalation) - required.
- `pai-reliability-review` (idempotency, partial failure) - required.
- `pai-ai-evaluation` + safety fixtures (injection cannot reach execute_refund).

# Rollout & rollback

- Flag `refund_agent`, canary with low amount cap; all executions human-approved.
- Rollback: disable flag; pending proposals remain, none auto-execute.
