# Profile: Conversational AI

Overlay for chat/assistant systems on messaging channels (support bots, LINE/Messenger/web chat).
Apply *in addition to* the core SDD workflow; do not auto-load it for unrelated work.

**Apply when:** the system holds a multi-turn conversation, sends outbound messages to users, or
integrates a messaging channel.
**Not universal:** channel and stack specifics (a particular messenger, queue, or DB) stay here or in
`examples/`, never in canonical skills.

## Additional focus (Master Spec sec. 11.1)

- **Conversation state** — persist per-user/per-conversation state (auto-reply, awaiting-input,
  awaiting-human, human-active, paused, closed, error). Never infer full state from a single message.
- **Multi-message batching** — coalesce rapid consecutive messages before inference; serialize per
  user to avoid interleaved replies.
- **Human takeover** — when a human takes over, disable AI outbound (`ai_reply_enabled=false`); AI may
  draft internal suggestions only; high-risk cases require manual release.
- **Duplicate / echo events** — deduplicate by platform event id; a redelivered webhook must not
  produce a second reply.
- **Channel constraints** — respect per-channel message size, rate, formatting, and reply-window rules.
- **Conversation privacy** — redact PII in logs and prompts; retain transcripts per policy.
- **Tone & escalation** — define escalation triggers (explicit request, repeated failure, strong
  emotion, medical/refund/legal, low confidence, missing knowledge).
- **Outbound message policy** — no auto-send of sensitive content without approval.

## SDD adjustments

- **Specify:** add `AI-*` requirements for answerable scope, uncertainty behavior, and takeover; add
  `REL-*` for dedup/ordering; add `PRIV-*` for transcript handling.
- **Contracts:** author an [ai-behavior-contract](../templates/contracts/ai-behavior-contract.md),
  [human-oversight-contract](../templates/contracts/human-oversight-contract.md), and
  [reliability-contract](../templates/contracts/reliability-contract.md).
- **Reviews:** always run [pai-reliability-review](../skills/pai-reliability-review/) (webhooks,
  dedup, ordering) and [pai-security-privacy-review](../skills/pai-security-privacy-review/).
- **Evals:** measure correct-escalation rate, dedup correctness, and takeover-respect (AI silent when
  a human is active), not just "did it reply".

## Checklist

- [ ] Per-user state machine defined and persisted.
- [ ] Event dedup by platform id, verified with a redelivery test.
- [ ] Per-user serialization / batching under burst.
- [ ] Human takeover disables AI outbound and is testable.
- [ ] Escalation triggers enumerated and evaluated.
- [ ] PII redaction in logs/prompts.

## Common anti-patterns

- Replying twice to a redelivered webhook (no dedup).
- AI and human replying to the customer simultaneously.
- Deciding state from the latest message text alone.
- Blocking the webhook ack on full inference (see reliability profile / SOP async split).
