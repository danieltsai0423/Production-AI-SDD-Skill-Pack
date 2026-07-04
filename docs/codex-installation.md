# Codex installation

## Install skills (repo scope)

```bash
python scripts/install.py --targets codex --scope repo
```

This copies `skills/` into `.agents/skills/<name>/` and writes an install manifest. Codex discovers
skills there. Use `--scope user` for `~/.agents/skills/`.

## Configuration

See [`.codex/config.example.toml`](../.codex/config.example.toml) for skill path, enforcement mode,
and command references.

## Wire the hooks

Codex hook APIs vary by version. The most portable enforcement path is the git pre-commit hook, which
runs the same guards as Claude Code:

```bash
python scripts/install_hooks.py --git-only
```

If your Codex build exposes a pre-tool hook, point it at `hooks/common/secret_guard.py` and
`hooks/common/protected_file_guard.py`. See [hook-guide.md](hook-guide.md).

## Verify

```bash
python scripts/validate_skills.py
python scripts/sync_skills.py --check --targets codex
```

## Update / uninstall

```bash
python scripts/sync_skills.py --targets codex
python scripts/uninstall.py --scope repo
```
