# Troubleshooting

## Skills don't trigger
- Confirm they're installed: `python scripts/sync_skills.py --check`. If missing, run `install.py`.
- Confirm the agent's discovery path (`.claude/skills/` or `.agents/skills/`).
- Be explicit once: "Use pai-sdd-orchestrator to ...". See [examples/](../examples/) for prompts.

## Mojibake / garbled characters
- Files are UTF-8; your console is likely cp950/Big5. Run `chcp 65001` and set `PYTHONUTF8=1`. See
  [windows-wsl2.md](windows-wsl2.md).

## `validate_specs` fails on dates
- Unquoted YAML dates parse as date objects; the validator normalizes them. If you hand-roll a
  parser, quote dates (`created_at: "2026-07-04"`).

## Hooks don't block
- Check `PAI_SDD_ENFORCEMENT` — `advisory` never blocks. Set `standard` or `strict`.
- For git, confirm `.git/hooks/pre-commit` exists and is executable (`install_hooks.py`).
- Claude Code: confirm the hooks block is in `.claude/settings.json`, not only the example file.

## Adapter drift in CI
- `sync_skills.py --check` failing means an installed copy differs from canonical `skills/`. Run
  `python scripts/sync_skills.py` to heal, or re-run `install.py`.

## Secret scan false positive
- Real fixture/example key? Add `# pragma: allowlist secret` on that line. Otherwise remove the
  secret and use an env var.
- For reliable coverage install `gitleaks`; the stdlib fallback is heuristic.

## PyYAML / jsonschema not installed
- Not required. The scripts fall back to stdlib parsing/validation. Install them for full fidelity:
  `pip install pyyaml jsonschema`.

## Quality gate is red
- Run `python scripts/run_quality_gate.py --mode standard` and read the per-check failure output; each
  check also runs standalone for a focused message.
