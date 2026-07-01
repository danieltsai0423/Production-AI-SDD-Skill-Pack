# Production AI Engineering Working Agreements

These are the always-on rules for any coding agent working in a repository that uses the
Production AI SDD Skill Pack. Keep this file short; procedures live in the `pai-*` skills.

- Inspect repository instructions, current specs, tests, and active changes before editing code.
- Classify non-trivial work with `pai-sdd-discovery` before implementation.
- Use the minimum sufficient specification level; do not create ceremony for trivial edits.
- Never claim completion without reproducible evidence.
- Treat model, prompt, retrieval, tools, data, and runtime behavior as separate versioned components.
- For external events, evaluate acknowledgement time, idempotency, retries, ordering, concurrency, and recovery.
- For tool-using AI, separate read, propose, approve, execute, and publish permissions.
- Do not expose secrets, credentials, private data, or production records in prompts, logs, fixtures, or commits.
- High-risk AI behavior requires explicit human oversight, rollback, auditability, and evaluation criteria.
- Update relevant specs, tests, evals, and operational documentation with behavior changes.
- Prefer small reversible changes and preserve existing behavior unless the specification changes it.
- Report assumptions, tests run, evidence, known limitations, and rollback impact.

## Risk levels (routing)

| Level | Applies to | Required artifacts |
|---|---|---|
| 0 Direct | typo/format/comment, safe config, behavior-preserving refactor | diff + targeted validation + completion note |
| 1 Light Spec | small feature, single module, low data risk | `spec.md`, `tasks.md`, `verification.md` |
| 2 Full Spec | cross-module, new API/DB/queue/integration, architecture trade-offs | + `brief.md`, `clarifications.md`, `plan.md`, `contracts/` |
| 3 High-Risk AI | external AI communication, real-effect tools, sensitive data, payments/deletions, critical concurrency | + risk, ai-behavior, human-oversight, security-privacy, evals, observability, rollback, runbook |

Start every non-trivial task at `pai-sdd-orchestrator` or `pai-sdd-discovery`.
