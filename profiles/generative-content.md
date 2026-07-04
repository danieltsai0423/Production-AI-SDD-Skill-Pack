# Profile: Generative Content

Overlay for systems that generate publishable content (SEO articles, social posts, marketing copy).
Apply in addition to the core SDD workflow.

**Apply when:** the system drafts content intended for publication or external audiences.
**Not universal:** a specific CMS or channel is an example, not the universal solution.

## Additional focus (Master Spec sec. 11.5)

- **Brand voice** — enforce tone/style; encode it in the prompt contract, verify in evals.
- **Source grounding** — claims grounded in approved material (e.g. approved product/therapy
  knowledge), not invented.
- **Human review** — draft → human preview → edit → approve → publish; no direct auto-publish of
  sensitive content.
- **Claims & compliance** — no unverifiable medical/financial/legal claims; compliance review where
  regulated.
- **Plagiarism / copyright** — originality and licensing checks.
- **Publication approval** — an explicit approval gate before anything goes live.
- **Performance feedback** — capture engagement metrics for optimization, but keep them out of the
  source-of-truth knowledge so feedback cannot contaminate future grounding.

## SDD adjustments

- **Specify:** add `AI-*` for voice/grounding/forbidden-claims, `DATA-*` for source approval,
  `OPS-*` for the approval/publish workflow.
- **Contracts:** author an [ai-behavior-contract](../templates/contracts/ai-behavior-contract.md)
  and [human-oversight-contract](../templates/contracts/human-oversight-contract.md).
- **Reviews:** run [pai-security-privacy-review](../skills/pai-security-privacy-review/) for
  sensitive claims and data handling.
- **Evals:** score brand-voice adherence, factual grounding, forbidden-claim avoidance, and format.

## Checklist

- [ ] Brand-voice spec + eval.
- [ ] Grounding to approved sources; uncited claims flagged.
- [ ] Human preview/approve/publish gate.
- [ ] Forbidden-claim (medical/financial/legal) checks.
- [ ] Originality/copyright check.
- [ ] Performance metrics stored separately from grounding truth.

## Common anti-patterns

- Auto-publishing generated content with no human approval.
- Exaggerated or unverifiable claims (esp. medical).
- Feeding engagement data back in as "facts", drifting the knowledge base.
