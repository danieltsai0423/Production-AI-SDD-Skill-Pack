---
name: pai-sdd-orchestrator
description: Coordinates the full risk-tiered Spec-Driven Development lifecycle for AI software work so the user does not have to remember individual skill names. Use when asked to build, plan, or deliver an AI feature, a cross-module change, an architecture change, or any risky AI behavior. Do not use for explaining concepts, pure copy/formatting edits, or when the user explicitly asks for one specific sub-skill.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: sdd-core
---

# Purpose

Drive an AI engineering task through the minimum sufficient SDD workflow — discovery, specify,
clarify, plan, tasking, implement, verify, close — selecting domain reviews by risk. It prevents
the two common failures: skipping specification on risky work, and burying trivial edits in ceremony.

# Use this skill when

- The user says "build / develop / plan / deliver an AI feature".
- Work spans multiple modules, adds an API/DB/queue/integration, or changes architecture.
- The change involves high-risk AI behavior (external communication, real-effect tools, sensitive data).

# Do not use this skill when

- The request is purely explanatory ("what is a vector DB?").
- The change is copy/format only, or the user explicitly invokes a single sub-skill.

# Required inputs

- Repository root and existing instructions (`AGENTS.md`/`CLAUDE.md`), specs, tests, active changes.
- The user's goal and any constraints.

If inputs are missing, inspect the repository before asking the user. Record safe assumptions explicitly.

# Workflow

Progress:

- [ ] 1. Run discovery (`pai-sdd-discovery`) to classify work type and Level 0–3.
- [ ] 2. Derive required artifacts from the Level.
- [ ] 3. Check for an active spec/change; continue it instead of starting a new one.
- [ ] 4. Run specify → clarify → plan → tasking in order, skipping steps the Level does not require.
- [ ] 5. During plan, select domain reviews (architecture, contracts, reliability, security-privacy, evaluation).
- [ ] 6. During implement, restrict each iteration to a single task boundary.
- [ ] 7. During verify, collect reproducible evidence.
- [ ] 8. During close, update spec, change archive, and runbook.

## Step routing by Level

- Level 0: skip specify/plan; go straight to a bounded implement + targeted verify.
- Level 1: specify (light) → tasking → implement → verify.
- Level 2: full specify → clarify → plan (+ selected reviews) → tasking → implement → verify → close.
- Level 3: Level 2 plus mandatory risk assessment, AI behavior + human-oversight + security-privacy
  contracts, evals, observability, and rollback before implementation is approved.

# Blocking conditions

- Level 2/3 has unresolved contradictions in critical requirements.
- A high-risk operation has no owner, approval, or rollback.
- Tests or verification method cannot be established.
- Production data is required with no safe handling path.

# Gotchas

- Do not classify from the prompt alone — inspect the repository (a "simple" endpoint that triggers
  a payment is still Level 3).
- Do not re-run discovery from scratch if an active spec/change already covers this work.

# References

- Use `pai-sdd-discovery` first; hand off to the specific lifecycle skill for each phase.
- The Master Spec §5 (methodology), §9 (lifecycle), §10 (catalog) define the authoritative flow.

# Completion criteria

- The task reached the phase its Level requires, with evidence.
- Spec/change artifacts and runbook are updated.
- Open risks and follow-ups are recorded.
