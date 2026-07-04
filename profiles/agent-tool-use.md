# Profile: Agent Tool Use

Overlay for LLM agents that call tools with real side effects. Apply in addition to the core SDD
workflow. Tool-using agents with real effects are almost always Level 3.

**Apply when:** the model can invoke tools that read or change external state (APIs, DBs, messages,
money, deletions).
**Not universal:** a specific agent framework or tool SDK belongs in `examples/`, never in canonical
skills.

## Additional focus (Master Spec sec. 11.3)

- **Tool registry** — explicit, enumerated tools; no dynamic/arbitrary capability.
- **Permission tiers** — separate read, propose, approve, execute, publish (AGENTS.md rule).
- **Read vs write tools** — write/irreversible tools gated behind approval.
- **Plan / approve / execute split** — the agent proposes; a human or policy approves; execution is
  a separate, auditable step.
- **Idempotency** — every write tool call carries an idempotency key; retries never double-apply.
- **Compensation** — define undo/compensation for reversible effects; block on irreversible ones.
- **Tool result validation** — validate tool outputs (schema, ranges) before acting on them.
- **Loop / budget limits** — max steps, token, and cost budgets; stop and escalate on exhaustion.
- **Sandbox** — least privilege; no ambient credentials beyond the task scope.

## SDD adjustments

- **Specify:** add `AI-*` for tool boundaries, `SEC-*` for permission tiers, `REL-*` for
  idempotency/compensation, `OPS-*` for budgets.
- **Contracts:** author a [tool-contract](../templates/contracts/tool-contract.md) and
  [human-oversight-contract](../templates/contracts/human-oversight-contract.md).
- **Reviews:** always run [pai-security-privacy-review](../skills/pai-security-privacy-review/)
  (tool injection, privilege escalation) and [pai-reliability-review](../skills/pai-reliability-review/)
  (idempotency, partial failure).
- **Evals + safety fixtures:** prompt-injection and tool-misuse cases must NOT obtain a
  high-privilege tool without approval (DoD sec. 25.6).

## Checklist

- [ ] Enumerated tool registry with per-tool permission tier.
- [ ] Write/irreversible tools require explicit approval.
- [ ] Idempotency key on every write; retry-safe.
- [ ] Step/token/cost budgets with escalation.
- [ ] Tool output validation before use.
- [ ] Safety evals: injection cannot escalate to write tools.

## Common anti-patterns

- One agent identity with full read+write+delete authority.
- Auto-executing a proposed destructive action with no approval step.
- Retrying a failed write without an idempotency key (double charge / double send).
- Trusting tool output or retrieved instructions as commands (injection).
