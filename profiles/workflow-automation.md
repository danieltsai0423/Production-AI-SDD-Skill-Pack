# Profile: Workflow Automation / n8n / Low-code

Overlay for automation built on workflow engines and low-code platforms. Apply in addition to the
core SDD workflow.

**Apply when:** logic lives in exported workflow artifacts (n8n, Make, Zapier-like) or a low-code
platform rather than only in application code.
**Not universal:** a specific platform is an example, not the universal solution.

## Additional focus (Master Spec sec. 11.4)

- **Exported workflow artifacts** — the workflow JSON/export is a versioned artifact; review it in PRs.
- **Credential references** — credentials referenced by id, never embedded in the export.
- **Node version & dependency** — pin node/plugin versions; record them.
- **Error workflow** — every production workflow has an error/failure path, not just the happy path.
- **Retry & resume** — bounded retries with backoff; resumable from a known point.
- **Item cardinality / merge semantics** — be explicit about 1:1 vs 1:many item expansion and merges.
- **Manual replay** — support safe manual re-run of a failed item without duplicate side effects.
- **Environment promotion** — dev → staging → prod with per-environment credentials and configs.
- **Observability** — execution logs, failure alerts, and run history.

## SDD adjustments

- **Specify:** add `REL-*` for retry/resume/cardinality, `SEC-*` for credential handling, `OPS-*`
  for environment promotion and replay.
- **Contracts:** author a [reliability-contract](../templates/contracts/reliability-contract.md) and
  [observability-contract](../templates/contracts/observability-contract.md).
- **Reviews:** run [pai-reliability-review](../skills/pai-reliability-review/) (retry, ordering,
  duplicate side effects) and [pai-security-privacy-review](../skills/pai-security-privacy-review/)
  for credentials.
- **Protected files:** treat exported workflow artifacts and credential maps as protected.

## Checklist

- [ ] Workflow export committed and reviewed as an artifact.
- [ ] Credentials referenced by id; none embedded in export.
- [ ] Error workflow + bounded retry + resume point.
- [ ] Idempotent side effects; safe manual replay.
- [ ] Item cardinality/merge semantics documented.
- [ ] Per-environment config; promotion process defined.

## Common anti-patterns

- Credentials hardcoded inside an exported workflow JSON.
- No error path — failures vanish silently.
- Manual replay that re-sends messages / re-charges (no idempotency).
- Editing production workflows directly with no promotion or version history.
