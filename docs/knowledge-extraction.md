# Knowledge Extraction (Phase 0)

Source synthesis of the domain SOP into reusable engineering knowledge, per Master Spec sec. 26
Phase 0. It records what was generalized into the pack, what is deliberately kept project-specific,
and where the generalization boundary lies.

- **Primary source:** `AI 系統與自動化專案開發 SOP.docx` (USER_SOP), extracted to
  `workbench/source-analysis/sop-fulltext.md` (git-ignored working copy).
- **Rule:** the SOP is one organization's project-specific playbook. Generalizable *methods* inform
  skills/profiles; concrete *stacks* (a specific messenger, queue, DB, or platform) stay in
  `profiles/` and `examples/`, never in canonical skills.

## 1. Reusable patterns (generalized into the pack)

| SOP method | Generalized into |
|---|---|
| Confirm the business problem before choosing tech | `pai-sdd-discovery`, AGENTS.md |
| Ship a minimum viable, verifiable slice first; expand later | Risk-tiered SDD, `pai-sdd-tasking` ordering (walking skeleton first) |
| AI output is never trusted as correct; add a verification mechanism sized to risk | `pai-sdd-verify`, `pai-ai-evaluation`, AGENTS.md "Evidence before completion" |
| "AI proposes, human decides" for medical/PII/payment/booking/data changes | Level 3 human oversight, `human-oversight-contract`, `pai-security-privacy-review` |
| Fix root cause, add a test/monitor so it cannot recur | `pai-incident-postmortem`, spec-drift + verification gates |
| Decouple fast webhook ack from slow inference (ack → dedup → queue → async → reply) | `pai-reliability-review`, `reliability-contract`, `profiles/conversational-ai` |
| Event dedup by platform id; per-user lock/serialization | `pai-reliability-review`, `profiles/conversational-ai` |
| Explicit conversation state machine; don't infer state from one message | `profiles/conversational-ai` |
| Human takeover disables AI outbound; high-risk needs manual release | `human-oversight-contract`, `profiles/conversational-ai` |
| Structured (JSON) AI output + schema/enum/required validation + retry → human | `pai-ai-contracts` (model-prompt/tool contracts), `profiles/rag/agent` |
| Bounded retry with backoff, max attempts, dead-letter, then human | `reliability-contract`, `pai-reliability-review` |
| Separate retrieval evals from generation evals; fixed regression set | `profiles/rag-knowledge-system`, `pai-ai-evaluation` |
| Prompt must state role, allowed data, forbidden inference, escalation, forbidden content | `model-prompt-contract`, `ai-behavior-contract` |
| Cross-team communication via impact language, demos, acceptance lists | `pai-sdd-specify` acceptance criteria; docs/sdd-workflow |
| Staged rollout: local → dev → internal → small real users → full | `pai-release-readiness` |
| Definition of done = confirmed + tested + exceptions + logs + human backup + docs + owner | `pai-sdd-close`, `pai-release-readiness` |

## 2. Project-specific patterns (do NOT generalize)

These are valid for the source organization but must stay out of canonical skills. They appear only
as illustrative examples in `profiles/` and `examples/`:

- Specific stack: FastAPI (webhook ack), Celery (async inference), Redis (queue/lock/dedup),
  PostgreSQL/Supabase (state), n8n (integration), a specific LLM/RAG vendor.
- Specific channels: LINE, Facebook Messenger.
- Specific domain: aesthetic-clinic / therapy content, appointment and refund flows.
- Specific business metrics: appointment conversion rate, therapy content approval rate.

> Generalization boundary: the *shape* (ack-fast + async + dedup + per-user lock + human takeover) is
> reusable; the *components* (FastAPI/Celery/Redis/LINE) are one instantiation and are never presented
> as the universal solution (CLAUDE.md rule).

## 3. Anti-patterns (encoded as things the pack warns/blocks on)

- Coding before the requirement/problem is confirmed.
- Adopting new tech into production just because it is new.
- Treating AI output as correct without verification.
- Letting slow tasks block the webhook / main service.
- Ignoring duplicate events, concurrency, and state management.
- Human and AI replying to the customer simultaneously.
- Shipping without logging/monitoring.
- Reporting risk only at the deadline.
- Fixing the symptom but not the root cause.
- A system only its author can understand or maintain.

## 4. Incidents (illustrative, from the SOP's own five-whys example)

- **Duplicate customer reply:** platform redelivered a webhook → same task ran twice → no event
  dedup → original design only handled the single-success path. Remediation: event id + dedup record
  + a redelivery regression test. Encoded in `profiles/conversational-ai`, `pai-reliability-review`,
  and the `pai-incident-postmortem` root-cause discipline.

## 5. Decision principles (adopted into routing / precedence)

1. Safety, data protection, and irreversible-risk first.
2. Explicit user need and approved spec next.
3. Verifiable facts of the existing repository.
4. Product principles of the Master Spec.
5. Generalizable methods from the SOP.
6. Official Agent Skills / Codex / Claude Code specs.
7. Tool convenience last.

(Matches Master Spec sec. 27; the SOP's "confirm problem → size risk → verify → human for
high-risk" ordering reinforces it.)

## 6. What was intentionally left out

- Company-internal tool names, credentials, and real customer data (never ingested).
- Kanban/board and staffing conventions (org-specific process, not engineering method).
- Vendor-specific API details (belong in each project's own docs).
