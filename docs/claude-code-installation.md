# Claude Code installation

## Install skills (project scope)

```bash
python scripts/install.py --targets claude --scope repo
```

This copies `skills/` into `.claude/skills/<name>/` and writes an install manifest. Claude Code
discovers the skills there. Use `--scope user` to install to `~/.claude/skills/` instead.

## Wire the hooks (optional but recommended)

```bash
python scripts/install_hooks.py            # copies .claude/settings.example.json -> settings.json
```

Sets `PAI_SDD_ENFORCEMENT` and registers PreToolUse (secret + protected-file guards) and Stop
(spec-required + verification gates). See [hook-guide.md](hook-guide.md).

## Verify

```bash
python scripts/validate_skills.py
python scripts/sync_skills.py --check --targets claude   # confirm the copy matches canonical
```

The 17 `pai-*` skills should now be triggerable. Try: "Use pai-sdd-orchestrator to plan a human
takeover feature." See [examples/](../examples/) for per-skill prompts.

## Update / uninstall

```bash
python scripts/sync_skills.py --targets claude   # re-sync after canonical changes
python scripts/uninstall.py --scope repo         # remove installed copies + manifest
```

Windows/WSL2 notes: [windows-wsl2.md](windows-wsl2.md).
