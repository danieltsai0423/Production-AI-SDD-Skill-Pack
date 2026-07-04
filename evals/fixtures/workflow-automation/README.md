# Fixture: Workflow Automation

A minimal stand-in for a low-code/n8n-style automation. Description + safety properties only; no real
credentials.

**Profile:** [workflow-automation](../../../profiles/workflow-automation.md) ·
**Worked example:** [webhook-reliability-fix](../../../examples/webhook-reliability-fix/)

## Shape
- Exported workflow artifact → third-party API calls → error workflow → retry/resume.
- Per-environment credentials referenced by id (never embedded).

## Concerns exercised
Exported artifacts, credential references, node/version pinning, error workflow, retry/resume, item
cardinality, manual replay, environment promotion, observability.

## Safety properties (DoD 25.6)
- Credentials are referenced by id; the fixture contains no real secrets.
- Manual replay is idempotent; a re-run does not double-send or double-charge.
