---
name: pai-release-readiness
description: Gates deployment by confirming functionality, code quality, tests, AI evals, data/migration, security, reliability, observability, cost, rollback, human operation, and documentation are ready, and issues PASS / CONDITIONAL_PASS / FAIL. Use before deploying Level 2-3 AI changes. Do not use for Level 0-1 edits or as a substitute for verification and evals.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: production-review
---

# Purpose

Make a defensible go/no-go release decision across every readiness category, not just "tests pass".

# Use this skill when

- About to deploy a Level 2/3 AI change.

# Do not use this skill when

- The change is Level 0/1, or verification/evals have not been run yet.

# Required inputs

- Verification Report, eval results, migration/rollback plan, and operational docs.

# Gate categories

Requirements/scope · code quality · tests · AI evals · data/migration · security/privacy · reliability ·
observability · cost/capacity · rollback · human operation · documentation · approval.

# Release result

- `PASS`
- `CONDITIONAL_PASS` — must name an owner, deadline, and mitigation for each open item.
- `FAIL`

# Prohibited

- Shipping an irreversible migration with no rollback.
- Fully rolling out a critical AI flow with no human backup.
- Shipping a prompt/model change with no regression eval.

# Output contract

```markdown
# Release Readiness
## Result: PASS / CONDITIONAL_PASS / FAIL
## Gate results
| Category | Status | Evidence | Owner/mitigation |
## Open conditions (for CONDITIONAL_PASS)
```

# Blocking conditions

- Any prohibited case above is present.

# Gotchas

- CONDITIONAL_PASS without owner + deadline + mitigation is really a FAIL.
- Observability that tracks only average latency (no percentiles, no AI outcome metrics) is not ready.

# References

- Consumes `pai-sdd-verify` and `pai-ai-evaluation` output. Master Spec §10.16, §22, §24.

# Completion criteria

- Every gate category assessed with evidence; explicit result; conditions have owners and deadlines.
