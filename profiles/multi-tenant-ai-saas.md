# Profile: Multi-tenant AI SaaS

Overlay for AI products serving multiple isolated customers from shared infrastructure. Apply in
addition to the core SDD workflow. Almost always Level 3 due to cross-tenant risk.

**Apply when:** one deployment serves multiple tenants whose data and config must stay isolated.
**Not universal:** a specific tenancy or billing stack is an example, not the universal solution.

## Additional focus (Master Spec sec. 11.9)

- **Tenant isolation** — enforced at data, retrieval, and cache layers; a query can never cross
  tenants. This is a hard-fail security property.
- **Config / prompt isolation** — per-tenant prompts/config cannot leak between tenants.
- **Per-tenant knowledge base** — retrieval is scoped to the tenant's own sources.
- **Usage quota** — per-tenant rate/usage limits.
- **Cost attribution** — attribute model/API cost per tenant.
- **Audit** — per-tenant audit trail of sensitive actions.
- **Data residency** — honor per-tenant data-location requirements.

## SDD adjustments

- **Specify:** add `SEC-*` for isolation (hard-fail), `PRIV-*` for residency, `OPS-*` for
  quota/cost attribution, `OBS-*` for per-tenant audit.
- **Contracts:** author a [data-contract](../templates/contracts/data-contract.md),
  [observability-contract](../templates/contracts/observability-contract.md), and, if agents are
  used, [tool-contract](../templates/contracts/tool-contract.md).
- **Reviews:** always run [pai-security-privacy-review](../skills/pai-security-privacy-review/)
  (tenant isolation, cross-tenant retrieval) and
  [pai-ai-architecture-review](../skills/pai-ai-architecture-review/).
- **Safety evals:** cross-tenant access attempts must fail (DoD sec. 25.6).

## Checklist

- [ ] Tenant id enforced on every data + retrieval + cache access.
- [ ] Cross-tenant access eval that must fail.
- [ ] Per-tenant prompt/config isolation.
- [ ] Per-tenant quota + cost attribution.
- [ ] Per-tenant audit trail.
- [ ] Data-residency handling where required.

## Common anti-patterns

- Tenant id passed but not enforced at the query/cache layer.
- A shared cache keyed without tenant, leaking answers across tenants.
- Retrieval that can reach another tenant's documents.
- No per-tenant cost/usage visibility.
