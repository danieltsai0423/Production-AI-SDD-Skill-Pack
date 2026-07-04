---
id: FEAT-001
title: Human takeover for AI conversations
status: approved
spec_level: 3
work_type: greenfield
owners:
  product: null
  engineering: null
  operations: null
risk_domains:
  - external-communication
  - personal-data
data_classification: confidential
human_approval_required: true
created_at: 2026-07-04
updated_at: 2026-07-04
related_changes: []
related_decisions: []
---

# Business outcome

Let human agents take over an AI-handled conversation cleanly, so high-risk or failing cases reach a
person without the customer receiving conflicting AI and human replies. Improves resolution quality
and reduces escalation-handling errors.

# Users / actors

- End customer on a messaging channel.
- Human support agent using the back office.
- AI reply worker.

# Current problem

The bot replies to every inbound message. When an agent intervenes, the AI can still reply in
parallel, producing contradictory messages and duplicated outbound sends.

# Scope

## In scope
- Per-conversation state with an explicit human-active mode.
- Disabling AI outbound while a human is active.
- Manual release back to AI, plus optional inactivity auto-release (non-high-risk only).

## Out of scope
- Agent routing/assignment logic.
- Analytics dashboards.

# User journeys

1. Agent opens a conversation and clicks "Take over" → AI stops replying → agent chats directly.
2. Agent resolves and clicks "Release" → AI resumes (unless flagged high-risk).
3. High-risk case → only manual release is allowed.

# Functional requirements

- **FR-001** - An agent can set a conversation to human-active; the state persists across messages.
- **FR-002** - While human-active, the AI reply worker must not send any outbound message.
- **FR-003** - An agent can release a conversation back to AI; high-risk cases require manual release.
- **FR-004** - AI may generate internal draft suggestions for the agent, never sent to the customer.

# Non-functional requirements

- **NFR-001** - Takeover state change is visible to the reply worker within 2s.

# AI behavior requirements

- **AI-001** - The reply worker checks conversation state immediately before sending and aborts if
  human-active.
- **AI-002** - On low confidence or an escalation trigger, the AI proposes takeover rather than
  replying.

# Data

- **DATA-001** - Transcripts are confidential; redact PII in logs; retain per policy.
- **PRIV-001** - Internal AI drafts are stored separately and never delivered to the customer.

# Security

- **SEC-001** - Only authorized agents can change takeover state (authz enforced server-side).

# Reliability

- **REL-001** - Outbound sends are idempotent and deduplicated by message id, so a retry during a
  state transition cannot double-send.

# Failure scenarios

- State write succeeds but worker read is stale → worker must re-check at send time (AI-001).
- Two agents take over simultaneously → last-writer-wins with an audit entry.

# Acceptance criteria (Given / When / Then)

- **AC-001** - Given a conversation, When an agent takes over, Then the next AI attempt sends nothing.
- **AC-002** - Given a human-active high-risk case, When inactivity elapses, Then AI does NOT
  auto-resume.
- **AC-003** - Given a redelivered webhook during takeover, When processed, Then no duplicate outbound
  is sent.

# Success metrics

- Zero simultaneous AI+human customer replies in a 2-week canary.
- 100% of high-risk cases require manual release.

# Human responsibility

The support agent is accountable for the conversation while human-active; releasing a high-risk case
is a deliberate human decision.
