# Profile: Realtime Voice

Overlay for realtime voice / speech systems (voice agents, IVR, live transcription). Apply in
addition to the core SDD workflow.

**Apply when:** the system processes streaming audio in near-real-time or holds a spoken conversation.
**Not universal:** a specific STT/TTS vendor is an example, not the universal solution.

## Additional focus (Master Spec sec. 11.6)

- **Barge-in** — the user can interrupt; the system must stop speaking and listen.
- **Latency budget** — end-to-end budget (STT + inference + TTS); define and monitor it.
- **Streaming failure** — partial/dropped streams have a defined recovery, not a hang.
- **Transcript accuracy** — track word error rate; low confidence changes behavior.
- **Consent** — record/process only with consent; capture it.
- **Recording retention** — retention and deletion policy for audio and transcripts.
- **Fallback to text / human** — degrade to text or a human on repeated failure or low confidence.

## SDD adjustments

- **Specify:** add `NFR-*` for latency budget, `AI-*` for barge-in/uncertainty, `PRIV-*` for consent
  and retention, `REL-*` for stream recovery.
- **Contracts:** author a [reliability-contract](../templates/contracts/reliability-contract.md),
  [data-contract](../templates/contracts/data-contract.md), and
  [human-oversight-contract](../templates/contracts/human-oversight-contract.md).
- **Reviews:** run [pai-reliability-review](../skills/pai-reliability-review/) (streaming, timeouts)
  and [pai-security-privacy-review](../skills/pai-security-privacy-review/) (consent, retention).
- **Evals:** measure latency percentiles, WER, barge-in responsiveness, and fallback correctness.

## Checklist

- [ ] Latency budget defined + monitored (p50/p95).
- [ ] Barge-in interrupts TTS reliably.
- [ ] Stream failure recovery (no hangs).
- [ ] Consent captured; retention/deletion policy enforced.
- [ ] Low-confidence → text/human fallback.

## Common anti-patterns

- No barge-in — the bot talks over the user.
- Unbounded latency with no fallback, leaving dead air.
- Recording without consent or retention limits.
