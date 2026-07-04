# Profile: Document Intelligence

Overlay for document extraction/understanding (OCR, invoices, forms, contracts). Apply in addition
to the core SDD workflow.

**Apply when:** the system extracts structured data or answers from documents.
**Not universal:** a specific OCR/vendor is an example, not the universal solution.

## Additional focus (Master Spec sec. 11.7)

- **OCR quality** — track OCR confidence; low quality routes to human verification.
- **Layout / table extraction** — handle multi-column, tables, and forms explicitly.
- **Document trust boundary** — treat document content as untrusted input (indirect prompt
  injection); do not execute instructions found in documents.
- **Page-level provenance** — every extracted field traces to a page/region for audit.
- **PII** — classify and redact personal data; restrict access.
- **Human verification** — low-confidence or high-impact fields require human confirmation.

## SDD adjustments

- **Specify:** add `DATA-*` for classification/provenance/retention, `AI-*` for
  extraction-uncertainty behavior, `SEC-*` for the document trust boundary.
- **Contracts:** author a [data-contract](../templates/contracts/data-contract.md) and
  [ai-behavior-contract](../templates/contracts/ai-behavior-contract.md).
- **Reviews:** run [pai-security-privacy-review](../skills/pai-security-privacy-review/) (indirect
  injection, PII) and, for pipelines, [pai-reliability-review](../skills/pai-reliability-review/).
- **Evals:** field-level accuracy, provenance correctness, and confidence calibration.

## Checklist

- [ ] OCR confidence tracked; low → human verification.
- [ ] Table/layout extraction handled and tested.
- [ ] Document content treated as untrusted (no instruction execution).
- [ ] Page/region provenance per extracted field.
- [ ] PII classification + redaction.

## Common anti-patterns

- Executing instructions embedded in a document ("ignore previous...").
- Extracted fields with no provenance, impossible to audit.
- Auto-accepting low-confidence OCR into a system of record.
