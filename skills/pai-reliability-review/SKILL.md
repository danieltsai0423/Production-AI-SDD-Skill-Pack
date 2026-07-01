---
name: pai-reliability-review
description: Reviews asynchronous events, webhooks, queues, background jobs, agents, and external dependencies for acknowledgement time, idempotency, deduplication, ordering, concurrency, retries, timeouts, partial failure, and recovery. Use when adding or debugging webhooks, queues, background jobs, event consumers, outbound messaging, or duplicate processing. Do not use for request-response endpoints with no external event or asynchronous behavior.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: production-review
---

# Purpose

Ensure event-driven and asynchronous AI work survives retries, duplicates, concurrency, and partial
failure without duplicate side effects or lost work.

# Use this skill when

- Adding or debugging webhooks, queues, background jobs, event consumers, outbound messaging, or duplicate processing.

# Do not use this skill when

- The endpoint is pure request-response with no external event or async behavior.

# Required inputs

- The event/queue/job design, external dependencies, and side-effect points.

# Must check

Acknowledgement deadline, idempotency key, event deduplication, message ordering, concurrency
control, user/entity lock, retry eligibility, exponential backoff + jitter, max retry count,
dead-letter handling, timeout, circuit breaker, partial failure, poison message, replay,
data consistency, recovery point/time, fallback and manual operation.

# Webhook reference pattern

```text
Receive -> Authenticate/verify signature -> Normalize -> Persist event/deduplicate -> Enqueue ->
Acknowledge -> Process asynchronously -> Persist result -> Perform outbound action -> Record audit/metrics
```

This is a default reference, not a mandate: do not force a queue onto every low-latency endpoint with
no external deadline or dependency.

# Output contract

```markdown
# Reliability Review
## Scope
## Findings (blocker / major / minor)
## Failure & recovery gaps
## Recommendations
```

# Blocking conditions

- External events cause duplicate side effects with no idempotency/dedup.
- A critical path has no recovery or manual fallback.

# Gotchas

- "The provider won't retry" is an assumption, not a guarantee - design for at-least-once delivery.
- Concurrency for the same user/entity needs a lock, not just a stateless handler.

# References

- Pairs with `pai-ai-architecture-review`. Master Spec sec. 10.13, sec. 2.

# Completion criteria

- Findings ranked, with concrete idempotency/retry/ordering/recovery recommendations.
