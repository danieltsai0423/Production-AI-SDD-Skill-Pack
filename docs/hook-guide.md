# Hook guide

The deterministic enforcement layer. Full reference: [`hooks/README.md`](../hooks/README.md).

## The five gates

| Gate | Script | Blocks |
|---|---|---|
| A Secret guard | `hooks/common/secret_guard.py` | keys/tokens/private keys/.env in writes or commits |
| B Protected files | `hooks/common/protected_file_guard.py` | credentials, migrations, lockfiles, generated specs |
| C+E Spec-required/drift | `hooks/common/spec_required_gate.py` | spec-worthy change with no spec/change artifact |
| D Verification | `hooks/common/verification_gate.py` | failing verify command; (strict) unverified source |

## Modes

`PAI_SDD_ENFORCEMENT` = `strict` | `standard` (default) | `advisory`. Advisory never blocks; it prints
the same actionable messages so teams can adopt gradually.

## Install

```bash
python scripts/install_hooks.py            # git pre-commit (no-clobber) + Claude settings copy
python scripts/install_hooks.py --git-only
```

- **Claude Code:** wires PreToolUse + Stop via `.claude/settings.json` (from
  [`.claude/settings.example.json`](../.claude/settings.example.json)).
- **git:** `.git/hooks/pre-commit` runs secret + protected + spec gates on staged changes.
- **Codex:** see [`.codex/config.example.toml`](../.codex/config.example.toml); git pre-commit is the
  most portable path.

## Configure

- `PAI_SDD_VERIFY_CMD` — command the verification gate runs before stop.
- `.pai-sdd-protected` — extra protected-path globs.

## Tests

`python scripts/test_hooks.py` — 10 assertions on block/allow + actionable messages (DoD 25.4).
