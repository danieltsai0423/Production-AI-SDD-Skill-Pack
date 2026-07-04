# Codex hook wiring

The canonical guards live in `hooks/common/` and are agent-agnostic. Codex discovers skills under
`.agents/skills/` (installed via `python scripts/install.py --targets codex`).

Because Codex hook APIs vary by version, the most portable enforcement path is the **git pre-commit
hook**, which runs the same guards as Claude Code's PreToolUse/Stop hooks:

```bash
python scripts/install_hooks.py --git-only     # writes .git/hooks/pre-commit
```

See [`.codex/config.example.toml`](../../.codex/config.example.toml) for the command references. If
your Codex build exposes a pre-tool hook, point it at:

```
python hooks/common/secret_guard.py
python hooks/common/protected_file_guard.py
```

Enforcement mode is read from `PAI_SDD_ENFORCEMENT` (strict | standard | advisory).
