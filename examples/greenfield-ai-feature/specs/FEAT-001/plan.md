---
id: FEAT-001
title: Human takeover - Plan
spec: spec.md
updated_at: 2026-07-04
---

# Architecture

Add an explicit conversation-state field (`ai_reply_enabled`, `human_active`, `risk_flag`) owned by
the conversation service. The reply worker becomes state-aware: it re-reads state immediately before
sending and aborts if `human_active`.

```
inbound -> webhook (ack fast) -> dedup -> queue -> reply worker
                                                     |-- read conversation state at send time
                                                     |-- if human_active: abort (draft only)
back office -> takeover/release -> conversation service (authz) -> state
```

# Components & responsibilities

- **Conversation service:** owns state, enforces authz on state changes (SEC-001), writes audit.
- **Reply worker:** state check at send time (AI-001), idempotent send (REL-001).
- **Back office:** takeover/release actions; shows internal AI drafts.

# Contracts

- [ai-behavior-contract](contracts/ai-behavior-contract.md) - answerable scope, escalation, silence
  while human-active.
- [human-oversight-contract](contracts/human-oversight-contract.md) - takeover/release authority,
  high-risk manual release.

# Failure strategy

- Stale read → re-check at send time; the send is the transaction boundary.
- Retry during transition → idempotency key dedup (REL-001).
- Simultaneous takeover → last-writer-wins + audit (C-004).

# Domain reviews selected

- `pai-reliability-review` (dedup, ordering, send-time race).
- `pai-security-privacy-review` (authz on state change, transcript PII).
- `pai-ai-evaluation` (escalation-correctness and takeover-respect evals).

# Test & eval strategy

- Unit: state transitions, authz, idempotency key.
- Integration: takeover → worker aborts send.
- Eval: escalation trigger → proposes takeover; human-active → AI silent.

# Rollout & rollback

- Feature flag `human_takeover`. Canary on a small cohort for 2 weeks (AC metrics).
- Rollback: disable flag → worker ignores state, reverts to prior behavior; no schema rollback needed
  (additive fields).
