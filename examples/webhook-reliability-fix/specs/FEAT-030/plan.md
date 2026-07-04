---
id: FEAT-030
title: Webhook dedup - Plan
spec: spec.md
updated_at: 2026-07-04
---

# Architecture

At the webhook boundary: ack fast, compute/verify an event id, check a dedup store, and only then
enqueue. Per-user serialization via a user-scoped lock/key. Outbound send carries an idempotency key.

```
platform -> webhook (ack) -> event-id -> dedup store check
   already processed? -> drop
   new?              -> record -> enqueue (per-user serialized) -> reply (idempotent send)
```

# Failure strategy

- Redelivered event -> dedup drop (REL-030).
- Concurrent user messages -> serialized (REL-031).
- Send retry -> idempotency key (REL-032).

# Domain reviews selected

- `pai-reliability-review` (dedup, ordering, idempotency, recovery) - required.

# Rollout & rollback

- Deploy behind a config toggle; monitor duplicate-event count (OBS-030). Rollback = toggle off.
