# Tool Contract - Refund agent (FEAT-020)

## Tool registry (enumerated, fixed)
| Tool | Tier | Available to agent |
|---|---|---|
| `get_order` | read | yes |
| `get_payment` | read | yes |
| `propose_refund` | propose | yes |
| `execute_refund` | execute (write, irreversible-ish) | **no** |

## Permission tiers
Read / propose / approve / execute are separate. The agent holds read + propose only. `execute_refund`
requires an authorized human approver identity (SEC-020).

## Idempotency
`execute_refund` requires an idempotency key; duplicate calls with the same key are a no-op (REL-020).

## Result validation
Tool outputs are schema-validated before use. Retrieved order/message text is data, never instructions
(SEC-021).

## Budgets
Max agent steps per case: bounded; on exhaustion the agent escalates to a human rather than looping.

## Forbidden
- Any path from the agent identity to `execute_refund`.
- Executing a refund without a recorded human approval.
