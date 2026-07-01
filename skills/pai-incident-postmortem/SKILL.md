---
name: pai-incident-postmortem
description: Turns an AI system incident into permanent prevention, detection, and recovery improvements via containment, evidence preservation, blameless root-cause analysis, regression tests, monitors, and spec/runbook updates. Use when a production AI system misbehaves, duplicates actions, leaks data, or fails. Do not use for planned changes (use pai-sdd-change) or routine feature work.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: production-review
---

# Purpose

Convert an incident into lasting improvement - not a symptom patch - with a blameless root cause and
corrective actions that prevent, detect, or recover.

# Use this skill when

- A production AI system misbehaves, duplicates actions, leaks data, or fails.

# Do not use this skill when

- This is planned change work (use `pai-sdd-change`) or routine feature development.

# Required inputs

- Timeline, affected systems, logs/evidence, and impact.

# Workflow (incident loop)

- [ ] 1. Contain.
- [ ] 2. Preserve evidence.
- [ ] 3. Restore service / switch to fallback.
- [ ] 4. Root-cause analysis.
- [ ] 5. Fix.
- [ ] 6. Add regression test / monitor / guardrail.
- [ ] 7. Update spec and runbook.
- [ ] 8. Verify recurrence prevention.

# Root-cause principles

- Distinguish trigger, root cause, and contributing factor.
- Never end at "human error" as the final root cause.
- Each corrective action maps to at least one of: prevent, detect, recover.

# Output contract (postmortem)

Incident summary, timeline, customer/business impact, detection, containment, root cause,
contributing factors, what worked/failed, corrective actions, regression tests, monitoring updates,
spec/runbook updates, owners and deadlines.

# Blocking conditions

- The corrective actions do not prevent recurrence (no test/monitor/guardrail added).

# Gotchas

- "The provider retried the webhook" is a trigger, not a root cause - fix idempotency/dedup.
- A postmortem with no regression test invites the same incident again.

# References

- Feeds `pai-sdd-change` for the durable fix and `pai-ai-evaluation` for regression coverage. Master Spec sec. 9.3, sec. 10.17.

# Completion criteria

- Postmortem complete; corrective actions mapped to prevent/detect/recover with owners; recurrence prevention verified.
