---
id: FEAT-030
title: Webhook event deduplication and idempotent replies
status: implemented
spec_level: 2
work_type: brownfield
owners:
  product: null
  engineering: null
  operations: null
risk_domains:
  - external-communication
data_classification: internal
human_approval_required: false
created_at: 2026-07-04
updated_at: 2026-07-04
related_changes: []
related_decisions: []
---

# Business outcome

Stop customers from receiving duplicate replies when the platform redelivers a webhook.

# Reliability requirements

- **REL-030** - Inbound events are deduplicated by platform event id; a redelivered event does not
  create a second task.
- **REL-031** - Messages from the same user are serialized so concurrent tasks cannot interleave.
- **REL-032** - Outbound replies are idempotent (keyed), so a retry cannot double-send.

# Observability requirements

- **OBS-030** - Duplicate-event count and dedup hits are logged and monitored.

# Acceptance criteria (Given / When / Then)

- **AC-030** - Given a redelivered webhook, When processed, Then exactly one reply is sent.
- **AC-031** - Given two rapid messages from one user, When processed, Then replies do not interleave.
