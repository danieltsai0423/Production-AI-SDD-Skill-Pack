---
name: pai-sdd-verify
description: Verifies that an implementation satisfies the spec (not just that it compiles) by tracing requirements to reproducible evidence across tests, contracts, runtime, AI evals, and security. Use before declaring any Level 1-3 work complete. Do not use as a substitute for writing the tests, and do not treat a single happy path or an LLM judge as sufficient proof.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Prove spec compliance with reproducible evidence and issue a PASS / CONDITIONAL PASS / FAIL decision.

# Use this skill when

- Before declaring Level 1-3 work complete, or before a release gate.

# Do not use this skill when

- Nothing has been implemented yet, or the change is Level 0 (targeted validation suffices).

# Required inputs

- The change/diff, spec version, tasks, and available test/eval commands.

# Workflow (verification layers)

- [ ] 1. Requirements traceability (each requirement -> evidence).
- [ ] 2. Static validation.
- [ ] 3. Unit tests.
- [ ] 4. Integration tests.
- [ ] 5. Contract tests.
- [ ] 6. E2E / runtime verification (startup, health, representative + failure scenario).
- [ ] 7. AI evals against fixed datasets and thresholds.
- [ ] 8. Security / privacy checks.
- [ ] 9. Reliability / failure injection.
- [ ] 10. Release-readiness summary.

# Output contract

```markdown
# Verification Report

## Scope
- Change / commit-diff / spec version:

## Requirement evidence
| Requirement | Evidence | Result |

## Commands executed
| Command | Result | Evidence location |

## AI eval results
| Metric | Threshold | Actual | Result |

## Runtime verification
- Startup / health / representative scenario / failure scenario:

## Risks and limitations

## Final decision
- PASS / CONDITIONAL PASS / FAIL
```

# Blocking conditions

- A required requirement has no evidence.
- A critical test/eval fails and is not fixed.

# Gotchas

- "No tests" is not "no problems found".
- One happy path is not full verification; an LLM-as-judge is not the sole quality evidence.

# Boundary with related skills

- This skill proves the change meets its spec. `pai-release-readiness` does not re-verify; it makes a
  deploy go/no-go decision using this skill's Verification Report plus operational readiness.

# References

- Feed the result into `pai-release-readiness` / `pai-sdd-close`. Master Spec sec. 10.8, sec. 20.

# Completion criteria

- Verification Report exists with per-requirement evidence and an explicit final decision.
