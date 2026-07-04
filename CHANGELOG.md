# Changelog

All notable changes to the Production AI SDD Skill Pack. Follows semantic versioning (Master Spec
sec. 23): breaking skill/schema/hook changes bump the major version.

## [1.0.0] - 2026-07-05

First production-grade release meeting the Master Spec Definition of Done (sec. 25).

### Added
- **Schemas** (`schemas/`): spec, task, verification, eval-case, skill-manifest, change; enforced by
  a stdlib mini JSON Schema validator (prefers `jsonschema` when installed).
- **Enforcement scripts** (`scripts/`): check_spec_drift, run_quality_gate, validate_references,
  generate_traceability, run_output_evals, run_safety_evals, sync_skills (`--check` drift),
  uninstall, install_hooks, build_distribution.
- **Deterministic hooks** (`hooks/`): five gates (secret, protected-file, spec-required/drift,
  verification) with strict/standard/advisory modes, agent-agnostic wiring for Claude Code, Codex,
  and git pre-commit; tested by `scripts/test_hooks.py`.
- **Profiles** (`profiles/`): 9 project-type overlays (conversational-ai, rag, agent-tool-use,
  workflow-automation, generative-content, realtime-voice, document-intelligence,
  ml-inference-service, multi-tenant-ai-saas).
- **Examples** (`examples/`): four end-to-end worked SDD runs with real, schema-valid artifacts.
- **Evals** (`evals/`): output + safety + regression suites, 0-4 rubric, four repository fixtures.
- **Docs** (`docs/`): architecture, sdd-workflow, risk-classification, skill-authoring, eval-guide,
  hook-guide, Codex/Claude installation, Windows/WSL2, migration, troubleshooting, knowledge-extraction.
- **CI**: schema/skills/specs/references/evals/hooks/secret/drift gates + adapter sync check.

### Changed
- `validate_specs` normalizes YAML date frontmatter to strings for schema validation.
- `scan_secrets` supports `pragma: allowlist secret` inline allowlisting.
- Version raised from 0.1.0 to 1.0.0; maturity updated in `pack.yaml`/README.

## [0.1.0] - 2026-07-02

Core skill pack with initial enforcement.

### Added
- 17 canonical `pai-*` skills, SDD + contract templates, copy-based installer, skill/spec validators,
  secret scanner, static trigger/workflow eval scaffolds, CI, bilingual README.
