# Production AI SDD Skill Pack

> Spec-driven workflows, production architecture reviews, AI contracts, evaluations,
> reliability gates, and human-control patterns for Codex, Claude Code, and
> Agent Skills-compatible coding agents.

繁體中文說明見 [README.zh-TW.md](README.zh-TW.md)。

## What it is

A reusable, cross-agent [Agent Skills](https://agentskills.io) pack that turns real production-AI
engineering judgment into **triggerable procedures and repeatable templates**, backed by a growing
set of **deterministic gates** (validators today; secret scan and spec checks in this release; hooks
and CI expanding). It is designed to run the same canonical skills on both **Codex** and **Claude
Code**, and applies a **risk-tiered Spec-Driven Development (SDD)** lifecycle so that small edits stay
light while high-risk AI behavior gets contracts, evals, human oversight, and rollback.

> **Maturity:** core skills + templates + initial validators/gates. This is not yet the full
> production-grade v1.0 from the Master Spec (see [Status](#status) for what is still missing).

The full product specification and acceptance contract is
[`Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md`](Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md).

## Core skills (v1)

| Skill | Job |
|---|---|
| `pai-sdd-orchestrator` | Route a request through the right SDD steps at the right weight. |
| `pai-sdd-discovery` | Classify work type, risk (Level 0-3), scope, and existing evidence before coding. |
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
templates/       # spec / plan / tasks / verification templates
templates/contracts/  # AI-behavior / model-prompt / data / RAG / tool / oversight / reliability / eval / observability
scripts/         # validators, installer, secret scan, eval runner (Python 3.11+)
evals/trigger/   # trigger-eval cases (Appendix C scenarios)
.github/workflows/    # CI
AGENTS.md        # always-on working agreements (shared by Codex + Claude)
CLAUDE.md        # Claude Code adapter (imports AGENTS.md)
pack.yaml        # pack manifest
```

## Install (repo scope)

Copy the canonical `skills/` into each agent's discovery path with the installer (copy strategy works
on Windows, WSL2, macOS, and Linux):

```bash
python scripts/install.py --targets codex claude --scope repo        # writes .agents/skills and .claude/skills
python scripts/install.py --targets claude --scope user --dry-run    # preview a user-scope install
```

This writes each skill to `.agents/skills/<name>/` (Codex) and `.claude/skills/<name>/` (Claude Code)
and records an install manifest.

## Validate

```bash
python scripts/validate_skills.py     # format, references, duplicate names, hardcoded paths, non-ASCII
python scripts/validate_specs.py      # feature specs under specs/ (no-op until specs exist)
python scripts/run_trigger_evals.py   # trigger-eval cases: schema + referential + keyword smoke (static)
python scripts/scan_secrets.py        # gitleaks/detect-secrets if present, else stdlib fallback
```

These are format/consistency and safety checks. They do not yet measure live trigger precision/recall
or run output-quality evals against an agent (tracked follow-ups).

## Methodology

This pack is **Spec-Anchored**, not Spec-as-Source:

```text
Specification = intent, boundaries, contracts, acceptance criteria
Code          = actual system behavior
Tests / Evals = reproducible evidence of Spec<->Code consistency
Runtime       = evidence the production system is actually reliable
Observability = evidence problems are discoverable, traceable, recoverable
```

## Status

**Present in this release:** 17 core skills, SDD + contract templates, a copy-based installer
(`scripts/install.py`), an extended skill validator, a spec validator, a secret scanner, a trigger-eval
scaffold (Appendix C scenarios), and a CI workflow.

**Not yet implemented (tracked follow-ups):** Codex/Claude hooks, a full output/workflow eval suite with
live-agent scoring and precision/recall thresholds, JSON schemas, repository fixtures, `profiles/` and
`references/` per AI system type, `examples/`, `docs/`, hash-based adapter drift checks, and source-synthesis
artifacts from the SOP. See the Master Spec (sec. 7, sec. 14-sec. 16, sec. 26) for the full target.

This is a **core skill pack with initial enforcement**, not the full production-grade v1.0 defined by the
Master Spec's Definition of Done (sec. 25).

## License

MIT - see [LICENSE](LICENSE).
