# SDD workflow

The risk-tiered Spec-Driven Development lifecycle the pack runs. Start at
[`pai-sdd-orchestrator`](../skills/pai-sdd-orchestrator/) or
[`pai-sdd-discovery`](../skills/pai-sdd-discovery/) for any non-trivial work.

## Steps

1. **Discovery** (`pai-sdd-discovery`) — classify work type + risk level (0-3), inspect repo, pick the
   minimum sufficient workflow.
2. **Specify** (`pai-sdd-specify`) — testable, solution-agnostic requirements with IDs + acceptance
   criteria. (Level 1-3)
3. **Clarify** (`pai-sdd-clarify`) — resolve ambiguities that affect architecture/risk/acceptance.
   (Level 2-3)
4. **Plan** (`pai-sdd-plan`) — architecture, contracts, data flow, failure strategy, rollout; select
   domain reviews. (Level 2-3)
5. **Tasking** (`pai-sdd-tasking`) — reversible, path-bounded tasks with requirement links. (Level 1-3)
6. **Implement** (`pai-sdd-implement`) — the minimum correct change for one task, test-first where
   deterministic.
7. **Verify** (`pai-sdd-verify`) — trace requirements to reproducible evidence; PASS/CONDITIONAL/FAIL.
8. **Close** (`pai-sdd-close`) — reconcile specs, evidence, docs, operational handoff.

Brownfield changes go through [`pai-sdd-change`](../skills/pai-sdd-change/) (spec delta). Incidents go
through [`pai-incident-postmortem`](../skills/pai-incident-postmortem/).

## Flows (Master Spec sec. 9)

- **Greenfield:** discovery → specify → clarify → plan → tasking → implement → verify → close.
- **Brownfield:** discovery → change (delta + impact) → plan/tasking → implement → verify → close.
- **Incident:** contain → postmortem (root cause) → change → verify.

## Worked runs

See [examples/](../examples/): a greenfield L3 feature, a brownfield RAG change, a high-risk agent,
and a webhook reliability fix — each with real spec/plan/tasks/verification artifacts.

## Artifacts per level

See [risk-classification.md](risk-classification.md). Level 0 needs only a diff + validation; Level 3
adds risk, AI-behavior, human-oversight, evals, observability, rollback, and a runbook.
