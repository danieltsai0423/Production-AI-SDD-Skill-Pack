# Security policy

## Reporting a vulnerability

Please report security issues privately to the maintainer (see the repository owner on GitHub) rather
than opening a public issue. Include steps to reproduce and impact. We aim to acknowledge within a few
business days.

## The pack's own security posture

- **No secrets in the repo.** `scripts/scan_secrets.py` and the secret-guard hook block keys, tokens,
  private keys, and `.env` files. Fixtures and examples use synthetic data only; deliberate example
  keys are marked `# pragma: allowlist secret`.
- **Protected files.** The protected-file guard blocks casual edits to credentials, migrations,
  lockfiles, and generated specs.
- **Least privilege for agents.** The pack's guidance separates read/propose/approve/execute
  permissions and requires human approval for high-risk, irreversible actions (see
  `profiles/agent-tool-use.md` and the security/privacy review skill).

## AI-specific threats covered

The `pai-security-privacy-review` skill and `evals/safety/` cover direct and indirect prompt
injection, tool injection, retrieval poisoning, PII leakage, destructive operations, and cross-tenant
access. Safety fixtures assert that an injection attempt cannot obtain a high-privilege tool without
approval.

## Scope

This repository is a methodology/skills pack. It ships no runtime service; the security controls here
protect the pack and guide downstream systems that adopt it.
