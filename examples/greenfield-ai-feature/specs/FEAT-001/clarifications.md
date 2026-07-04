---
id: FEAT-001
title: Human takeover - Clarifications
updated_at: 2026-07-04
---

# Resolved

- **C-001 (state authority):** The conversation record is the single source of takeover state, not
  the message stream. → Decision: reply worker reads state at send time (FR-002, AI-001).
- **C-002 (auto-release):** Should AI auto-resume after inactivity? → Decision: yes for normal cases
  (configurable timeout), never for high-risk (AC-002).
- **C-003 (internal drafts):** Are AI suggestions shown to the agent during takeover? → Decision: yes,
  stored separately, never delivered to the customer (FR-004, PRIV-001).
- **C-004 (concurrency):** Two agents taking over at once? → Decision: last-writer-wins + audit entry;
  no hard lock needed for v1.

# Assumptions

- The messaging channel provides a stable per-conversation id.
- Outbound sends already carry a message id usable for dedup (REL-001).

# Deferred

- Agent assignment/routing (out of scope this feature).
