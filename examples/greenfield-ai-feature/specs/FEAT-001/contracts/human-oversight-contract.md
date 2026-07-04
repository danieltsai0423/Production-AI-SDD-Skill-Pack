# Human Oversight Contract - Human takeover (FEAT-001)

## Authority
- Only authorized support agents can change takeover state (SEC-001, server-side authz).
- Taking over makes the agent accountable for the conversation until release.

## Decisions reserved for humans
- Releasing a **high-risk** conversation back to AI is always a manual human decision (FR-003,
  AC-002). No timer may auto-release it.

## Auto-release (non-high-risk only)
- Normal conversations may auto-resume AI after a configurable inactivity timeout.

## Audit
- Every takeover/release writes an audit entry (actor, timestamp, conversation, risk flag).
- Simultaneous takeover resolves last-writer-wins, both recorded.

## Rollback
- Disabling the `human_takeover` flag reverts to prior behavior; audit history is retained.
