# Human Oversight Contract - Refund agent (FEAT-020)

## Authority
- Only an authorized approver can execute a refund (SEC-020).
- The agent may propose; it can never execute (FR-020, AI-020).

## Decision reserved for humans
- Approving any refund is a deliberate human decision (FR-021, AC-020). No auto-approval, regardless
  of proposal confidence or any instruction found in order/message content (AC-022).

## Audit
- Every proposal and approval is recorded: actor, timestamp, order, amount, rationale (OPS-020).

## Rollback
- Disabling the `refund_agent` flag stops new proposals; nothing auto-executes.
- An erroneously approved refund is reversed via the finance reversal runbook (human process).
