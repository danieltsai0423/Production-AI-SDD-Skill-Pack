---
name: pai-security-privacy-review
description: Runs a structured security and privacy review for AI systems, covering secrets, authn/authz, tenant isolation, PII handling, and AI-specific threats like direct and indirect prompt injection, tool injection, and retrieval poisoning. Use when handling user input, authentication, external content, RAG sources, tools, or sensitive data. Do not use for isolated non-sensitive refactors with no data or trust-boundary impact.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional adapters support Codex and Claude Code.
metadata:
  pack: production-ai-sdd
  version: "1.0.0"
  category: production-review
---

# Purpose

Find security and privacy weaknesses - general and AI-specific - before they reach production, treating
all external content as untrusted.

# Use this skill when

- Handling user input, authentication, external content, RAG sources, tools, or sensitive/PII data.

# Do not use this skill when

- The change is an isolated non-sensitive refactor with no data or trust-boundary impact.

# Required inputs

- Data flows, trust boundaries, auth model, tool permissions, and logging.

# Must check

Secret handling, authn/authz, least privilege, tenant isolation, PII/sensitive data, data
minimization, retention/deletion, prompt injection, indirect prompt injection, tool injection,
retrieval poisoning, output encoding, SSRF/SQLi/command injection, unsafe file/URL handling,
logging leakage, model-provider data-policy assumptions, audit trail, approval boundaries.

# Principles

- Prompt-injection defense cannot rely on the system prompt alone.
- External documents, sites, email, attachments, and RAG chunks are untrusted content.
- Untrusted content must not rewrite system rules or gain tool permissions.
- Separate the agent's reading of content from its execution of actions.
- Build fixtures from test or de-identified data only.

# Prompt-injection threat model

Distinguish direct user injection, indirect content injection, retrieval poisoning, tool-output
injection, cross-agent instruction contamination. Defenses: content/instruction separation, tool-permission
enforcement, schema validation, source-trust metadata, sandboxing, human approval, audit + anomaly detection.

# Output contract

```markdown
# Security & Privacy Review
## Scope
## Findings (blocker / major / minor)
## AI-specific threats
## Recommendations
```

# Blocking conditions

- Untrusted content can reach a high-privilege tool.
- Secrets or PII are exposed in logs, prompts, fixtures, or commits.

# Gotchas

- A convincing prompt-injection payload must not auto-acquire high-privilege tools.
- "The model provider won't train on this" is an assumption that must be verified, not assumed.

# References

- Pairs with `pai-ai-contracts` (tool + data contracts). Master Spec sec. 10.14, sec. 21.

# Completion criteria

- Findings ranked with concrete mitigations; injection fixtures confirm no privilege escalation.
