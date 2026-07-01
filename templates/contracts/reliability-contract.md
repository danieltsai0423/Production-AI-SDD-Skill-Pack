---
contract: reliability
id: RELC-000
feature: FEAT-000
version: "1.0.0"
status: draft
updated_at: 2026-07-02
---

# Reliability Contract

## Ingress
- Acknowledgement deadline:
- Signature/auth verification:

## Idempotency & dedup
- Idempotency key:
- Deduplication window/store:

## Ordering & concurrency
- Ordering guarantee:
- Entity-scoped lock:

## Retry
- Eligible failures:
- Backoff + jitter:
- Max attempts / dead-letter:

## Failure handling
- Timeout:
- Circuit breaker:
- Partial failure behavior:
- Poison message handling:

## Recovery
- Replay procedure:
- Recovery point / recovery time objective:
- Fallback / manual operation:

## Consistency
<data consistency guarantees across the async boundary>
