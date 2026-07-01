---
contract: observability
id: OBSC-000
feature: FEAT-000
version: "1.0.0"
status: draft
updated_at: 2026-07-02
---

# Observability Contract

## Correlation
- Request / event ID:
- Trace ID:
- User / tenant pseudonymous ID:

## AI-specific signals
- Prompt / model / knowledge version:
- Retrieval document IDs:
- Tool calls:
- Latency breakdown (retrieval / inference / tools):
- Token / cost:
- Retry / fallback:
- Human takeover / approval:
- Safety / refusal decision:
- Final status:

## Metrics
- Business / AI outcome metrics (not just application errors):
- Latency percentiles (p50 / p95 / p99), not only average:

## Prohibited
- No unnecessary full PII in logs.
- No secrets in logs.

## Alerting
<what triggers an alert and who receives it>
