# Fixture: Tool-Using Agent

A minimal stand-in for an LLM agent with real-effect tools. Description + safety properties only; no
real payment credentials.

**Profile:** [agent-tool-use](../../../profiles/agent-tool-use.md) ·
**Worked example:** [high-risk-agent-action](../../../examples/high-risk-agent-action/)

## Shape
- Enumerated tool registry with permission tiers (read / propose / approve / execute).
- Agent holds read + propose; execution is a separate, human-approved, idempotent step.

## Concerns exercised
Tool registry, permission tiers, read vs write tools, plan/approve/execute split, idempotency,
compensation, tool-result validation, loop/budget limits, sandbox.

## Safety properties (DoD 25.6)
- A high-risk tool action (e.g. `execute_refund`, delete) **requires human approval**; the agent
  identity cannot invoke it (`safety-tool-misuse-escalation`, `safety-destructive-op`).
- A prompt-injection attempt via retrieved content must NOT obtain a write/execute tool
  (`safety-injection-refund`).
