# Claude Code hook wiring

The canonical guards live in `hooks/common/`. Claude Code wires them via `.claude/settings.json`.

Use the ready example at [`.claude/settings.example.json`](../../.claude/settings.example.json):

```bash
python scripts/install_hooks.py          # copies it to .claude/settings.json if absent
```

It registers:

- **PreToolUse** on `Write|Edit|MultiEdit|Bash` → `secret_guard.py`
- **PreToolUse** on `Write|Edit|MultiEdit` → `protected_file_guard.py`
- **Stop** → `spec_required_gate.py`, `verification_gate.py`

Blocking is signalled with exit code 2 and an actionable message on stderr, which Claude Code feeds
back to the agent. Set `PAI_SDD_ENFORCEMENT` in the settings `env` block.
