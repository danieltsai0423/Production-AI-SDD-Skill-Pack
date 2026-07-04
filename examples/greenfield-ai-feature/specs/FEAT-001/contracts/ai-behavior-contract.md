# AI Behavior Contract - Human takeover (FEAT-001)

## Answerable scope
The AI reply worker handles routine support Q&A only. It does not make medical, refund, or legal
commitments (those are escalation triggers).

## Uncertainty behavior
- Below confidence threshold, or on an escalation trigger, the AI proposes takeover instead of
  replying (AI-002).
- It never fabricates an answer to fill a knowledge gap.

## Silence rule (hard)
- When the conversation is `human_active`, the AI produces **no customer-facing output** (FR-002,
  AI-001). It may produce internal drafts for the agent only (FR-004).

## Escalation triggers
Explicit request for a human; repeated failure; strong negative sentiment; medical/refund/legal
topic; low confidence; missing knowledge.

## Forbidden
- Sending any message while a human is active.
- Delivering an internal draft to the customer.
- Auto-resuming a high-risk conversation.

## Evaluation
- Escalation-proposal recall >= 0.90.
- Takeover-respect = 1.00 (no AI output while human-active).
