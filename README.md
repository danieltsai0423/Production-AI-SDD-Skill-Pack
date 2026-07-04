# Production AI SDD Skill Pack

> Spec-driven workflows, production architecture reviews, AI contracts, evaluations,
> reliability gates, and human-control patterns for Codex, Claude Code, and
> Agent Skills-compatible coding agents.

繁體中文說明見 [README.zh-TW.md](README.zh-TW.md)。

## What it is

A reusable, cross-agent [Agent Skills](https://agentskills.io) pack that turns real production-AI
engineering judgment into **triggerable procedures and repeatable templates**, backed by
**deterministic gates** (schema-checked artifacts, validators, a secret scanner, five enforcement
hooks, and CI). It runs the same canonical skills on both **Codex** and **Claude Code**, and applies a
**risk-tiered Spec-Driven Development (SDD)** lifecycle so that small edits stay light while high-risk
AI behavior gets contracts, evals, human oversight, and rollback.

> **Maturity:** production-grade v1.0 - meets the Master Spec Definition of Done (sec. 25). The one
> tracked follow-up is live-agent precision/recall and calibrated prose scoring; the eval runners
> enforce structure and wiring deterministically today (see [Status](#status)).

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
skills/          # 17 canonical cross-agent skills (source of truth)
profiles/        # 9 project-type overlays (conversational, RAG, agent, ...)
templates/       # spec / plan / tasks / verification + 9 contract templates
schemas/         # JSON schemas: spec, task, verification, eval-case, skill-manifest, change
scripts/         # validators, installer, hooks installer, drift check, eval runners (Python 3.11+)
hooks/           # 5 deterministic gates (secret, protected-file, spec-required, verification)
evals/           # trigger / workflow / output / safety cases, rubric, 4 fixtures
examples/        # 4 end-to-end worked SDD runs (real artifacts)
docs/            # architecture, workflow, install, hooks, evals, Windows/WSL2, troubleshooting
.github/workflows/    # validate + evals + release CI
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
python scripts/run_quality_gate.py --mode standard   # runs everything below + drift, one exit code
```

Or individually:

```bash
python scripts/_minijsonschema.py     # JSON schemas parse
python scripts/validate_skills.py     # format, references, schema, duplicate names, hardcoded paths
python scripts/validate_specs.py      # feature specs: frontmatter + task schema
python scripts/validate_references.py # Markdown links resolve
python scripts/run_trigger_evals.py   # trigger cases (static)
python scripts/run_workflow_evals.py  # workflow cases (static)
python scripts/run_output_evals.py    # artifact structure vs rubric (static)
python scripts/run_safety_evals.py    # safety cases wired to defenses (static)
python scripts/test_hooks.py          # hook block/allow tests
python scripts/scan_secrets.py        # gitleaks/detect-secrets if present, else stdlib fallback
```

These enforce structure, wiring, and safety deterministically. Live trigger precision/recall and
calibrated output-quality scoring against an agent remain a tracked follow-up.

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

**Present in v1.0:** 17 core skills; 9 project profiles; SDD + 9 contract templates; 6 JSON schemas
wired into the validators; a copy-based installer, hooks installer, adapter drift check, uninstall,
and distribution builder; five deterministic enforcement hooks (secret, protected-file,
spec-required/drift, verification) with tests; trigger/workflow/output/safety eval suites, a 0-4
rubric, and four repository fixtures; four end-to-end worked examples with real artifacts; eleven docs
(incl. Windows/WSL2); Phase 0 knowledge-extraction from the SOP; and validate/evals/release CI.

**Tracked follow-up:** live-agent trigger precision/recall and calibrated 0-4 prose scoring against a
running agent. The eval runners enforce structure, wiring, and safety deterministically; the live
scoring harness is the remaining step and is intentionally not faked.

This release meets the Master Spec Definition of Done (sec. 25). See
[docs/](docs/) and the Master Spec (sec. 7, sec. 14-16, sec. 25-26) for the full target.

## License

MIT - see [LICENSE](LICENSE).
