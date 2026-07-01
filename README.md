# Production AI SDD Skill Pack

> Spec-driven workflows, production architecture reviews, AI contracts, evaluations,
> reliability gates, and human-control patterns for Codex, Claude Code, and
> Agent Skills-compatible coding agents.

繁體中文說明見 [README.zh-TW.md](README.zh-TW.md)。

## What it is

A reusable, cross-agent [Agent Skills](https://agentskills.io) pack that turns real production-AI
engineering judgment into **triggerable procedures, repeatable templates, and enforceable gates**.
It runs the same canonical skills on both **Codex** and **Claude Code**, and applies a
**risk-tiered Spec-Driven Development (SDD)** lifecycle so that small edits stay light while
high-risk AI behavior gets contracts, evals, human oversight, and rollback.

The full product specification and acceptance contract is
[`Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md`](Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md).

## Core skills (v1)

| Skill | Job |
|---|---|
| `pai-sdd-orchestrator` | Route a request through the right SDD steps at the right weight. |
| `pai-sdd-discovery` | Classify work type, risk (Level 0–3), scope, and existing evidence before coding. |
| `pai-sdd-specify` | Turn vague requirements into testable, solution-agnostic specs. |
| `pai-sdd-clarify` | Resolve ambiguities that affect architecture, risk, or acceptance. |
| `pai-sdd-plan` | Turn a confirmed spec into architecture, contracts, data flow, tests, and rollout. |
| `pai-sdd-tasking` | Break a plan into independently implementable, verifiable, reversible tasks. |
| `pai-sdd-implement` | Implement the minimum correct change within a single task boundary. |
| `pai-sdd-verify` | Prove the implementation meets the spec with reproducible evidence. |
| `pai-sdd-change` | Manage brownfield requirement/architecture changes and spec deltas. |
| `pai-sdd-close` | Finalize specs, evidence, docs, and operational handoff. |
| `pai-ai-architecture-review` | Review AI component boundaries, data/state, failure isolation, scalability. |
| `pai-ai-contracts` | Author AI behavior / model-prompt / data / RAG / tool / human-oversight contracts. |
| `pai-reliability-review` | Review events, queues, idempotency, retries, ordering, concurrency, recovery. |
| `pai-security-privacy-review` | Review AI-specific and general security/privacy, including prompt injection. |
| `pai-ai-evaluation` | Build repeatable, comparable, regression-ready evals for non-deterministic AI. |
| `pai-release-readiness` | Gate deployment across functionality, reliability, security, data, AI quality, ops. |
| `pai-incident-postmortem` | Turn incidents into permanent prevention, detection, and recovery improvements. |

## Repository layout

```text
skills/          # canonical cross-agent skills (source of truth)
templates/       # spec / plan / tasks / verification / contract templates
scripts/         # validators and installers (Python 3.11+)
AGENTS.md        # always-on working agreements (shared by Codex + Claude)
CLAUDE.md        # Claude Code adapter (imports AGENTS.md)
pack.yaml        # pack manifest
```

## Install (repo scope)

Copy or symlink the canonical `skills/` into each agent's discovery path:

- Codex: `.agents/skills/<skill-name>/SKILL.md`
- Claude Code: `.claude/skills/<skill-name>/SKILL.md`

On Windows/WSL2, prefer copying over symlinks. A cross-agent installer is planned; until then,
copy the `skills/` subdirectories into the paths above.

## Validate

```bash
python scripts/validate_skills.py
```

Checks that every skill directory name matches its frontmatter `name`, that required frontmatter
fields exist, and that `SKILL.md` files stay within the recommended size.

## Methodology

This pack is **Spec-Anchored**, not Spec-as-Source:

```text
Specification = intent, boundaries, contracts, acceptance criteria
Code          = actual system behavior
Tests / Evals = reproducible evidence of Spec↔Code consistency
Runtime       = evidence the production system is actually reliable
Observability = evidence problems are discoverable, traceable, recoverable
```

## Status

First version of the core skills and scaffold. Profiles, hooks, eval runners, fixtures, and the
cross-agent installer described in the Master Spec (§7, §14–§16) are planned follow-ups.

## License

MIT — see [LICENSE](LICENSE).
