# Verification Report

## Scope
- Change: FEAT-001 Human takeover for AI conversations
- Commit / diff: (example) feature branch `feat/human-takeover`
- Spec version: spec.md @ approved 2026-07-04

## Requirement evidence
| Requirement | Evidence | Result |
|---|---|---|
| FR-001 | unit: state persists; integration: takeover visible to worker | pass |
| FR-002 | integration: worker aborts send while human-active | pass |
| FR-003 | unit: high-risk blocks auto-release; manual release works | pass |
| FR-004 | unit: draft stored separately, not delivered | pass |
| AI-001 | integration: send-time re-check aborts on stale enable | pass |
| AI-002 | ai-eval: low-confidence proposes takeover (18/18 cases) | pass |
| NFR-001 | integration: state change seen by worker in < 2s (p95 0.8s) | pass |
| DATA-001 | log inspection: PII redacted in transcripts | pass |
| PRIV-001 | unit: internal draft never enters outbound path | pass |
| SEC-001 | unit: unauthorized state change rejected (403) | pass |
| REL-001 | integration: redelivered webhook during takeover -> no dup | pass |

## Commands executed
| Command | Result | Evidence location |
|---|---|---|
| `pytest tests/conversation tests/reply_worker` | 41 passed | CI log |
| `python evals/run.py --suite takeover` | 36/36 pass | eval report |

## AI eval results
| Metric | Threshold | Actual | Result |
|---|---:|---:|---|
| Escalation-proposal recall | 0.90 | 1.00 | pass |
| Takeover-respect (AI silent when human-active) | 1.00 | 1.00 | pass |

## Runtime verification
- Startup: worker boots, reads state store.
- Representative scenario: takeover → customer receives only the agent's messages.
- Failure scenario: retry during transition → single outbound (dedup verified).

## Risks and limitations
- Last-writer-wins on simultaneous takeover (accepted for v1; audited).
- Auto-release timeout tuning deferred to canary feedback.

## Final decision
- PASS
