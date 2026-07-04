# Risk classification

The pack sizes ceremony to risk. Discovery assigns a level; the level determines required artifacts.

| Level | Applies to | Required artifacts |
|---|---|---|
| **0 Direct** | typo/format/comment, safe config, behavior-preserving refactor | diff + targeted validation + completion note |
| **1 Light Spec** | small feature, single module, low data risk | `spec.md`, `tasks.md`, `verification.md` |
| **2 Full Spec** | cross-module, new API/DB/queue/integration, architecture trade-offs | + `brief.md`, `clarifications.md`, `plan.md`, `contracts/` |
| **3 High-Risk AI** | external AI communication, real-effect tools, sensitive data, payments/deletions, critical concurrency | + risk, ai-behavior, human-oversight, security-privacy, evals, observability, rollback, runbook |

## How to classify

Ask (from `pai-sdd-discovery`):
- Does it change external AI behavior or send messages to real users? → ≥ 3
- Does it use tools with real side effects (payments, deletions, data changes)? → 3
- Does it touch sensitive/personal data, auth, or tenant isolation? → ≥ 2, often 3
- Cross-module, new API/DB/queue, or architecture trade-off? → 2
- Single small module, low data risk? → 1
- Behavior-preserving / trivial? → 0

When in doubt, pick the higher level; you can always down-scope in clarify.

## Signals that force Level 3

External communication, real-effect tools, sensitive data, payments/deletions, critical concurrency.
These pull in the security/privacy review, an AI-behavior + human-oversight contract, safety evals,
and a rollback plan (see the [agent-tool-use](../profiles/agent-tool-use.md) and
[multi-tenant-ai-saas](../profiles/multi-tenant-ai-saas.md) profiles).

## Enforcement

The [spec-required gate](hook-guide.md) flags spec-worthy changes (API/schema, migration,
model/prompt, contracts, auth) that arrive without a spec/change artifact.
