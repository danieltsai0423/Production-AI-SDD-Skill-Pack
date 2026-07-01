@AGENTS.md

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This repository **is** the Production AI SDD Skill Pack — the canonical source of a reusable,
cross-agent Agent Skills pack that encodes a risk-tiered Spec-Driven Development lifecycle for
building production AI systems. It targets both Codex and Claude Code from one source.

- Authoritative spec: `Production_AI_SDD_Skill_Pack_Master_Spec_zh-TW.md` (product spec + acceptance contract).
- Domain source: `AI 系統與自動化專案開發 SOP.docx` (USER_SOP; binary — extract before use).
- Canonical skills live in `skills/<name>/SKILL.md`. Never hardcode a specific stack
  (Messenger/LINE/n8n/FastAPI/Celery/Redis/Pinecone/a cloud) as the universal solution;
  such specifics belong in `profiles/` or examples.

## Claude Code adapter rules

- Use plan mode for Level 2 and Level 3 work.
- Use isolated subagents for independent architecture, security, reliability, or verification reviews when supported.
- Before finishing, run the repository verification recipe or `/verify` equivalent when available.
- Treat Skills as procedures and this file as persistent facts; do not duplicate long workflows here.

## Editing the pack itself

- Skill names are lowercase-hyphenated, prefixed `pai-`, and the directory name must equal the frontmatter `name`.
- Keep each `SKILL.md` focused and under ~500 lines; move long standards to `references/`, long templates to `assets/`, deterministic logic to `scripts/`.
- Every `description` must state what the skill does, when to trigger, and when NOT to trigger.
- Validate skills with `python scripts/validate_skills.py` before committing.
- The Master Spec is the source of truth: full target tree in §7, core skill catalog in §10, phased plan in §26, Definition of Done in §25.
