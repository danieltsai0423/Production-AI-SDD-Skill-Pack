# Migration guide

## Adopting the pack in an existing repo

1. Install skills for your agent(s):
   ```bash
   python scripts/install.py --targets codex claude --scope repo
   ```
2. Add the working agreements: commit `AGENTS.md` (and `CLAUDE.md` for Claude Code) to your repo, or
   import the pack's rules into your existing ones.
3. Turn on enforcement gradually:
   ```bash
   PAI_SDD_ENFORCEMENT=advisory python scripts/install_hooks.py
   ```
   Advisory prints findings without blocking. Move to `standard`, then `strict`, as the team adjusts.
4. Start using specs for spec-worthy changes (`specs/<FEAT-id>/`). The spec-required gate will point
   these out.

## Upgrading the pack

```bash
git pull                                   # update the canonical pack
python scripts/sync_skills.py              # re-sync installed adapter copies
python scripts/sync_skills.py --check      # confirm no drift
```

Semantic versioning (Master Spec sec. 23): breaking skill/schema changes bump the major version. Check
[`CHANGELOG.md`](../CHANGELOG.md) before a major upgrade.

## Rolling back

- Skills: `python scripts/uninstall.py --scope repo` removes installed copies; canonical `skills/`
  stays in git.
- Hooks: delete `.git/hooks/pre-commit` and remove the hooks block from `.claude/settings.json`, or
  set `PAI_SDD_ENFORCEMENT=advisory`.
