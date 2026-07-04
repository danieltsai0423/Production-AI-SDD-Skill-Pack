# Deterministic hooks

Skills are procedural guidance; they cannot *enforce* anything. These hooks are the deterministic
half (Master Spec sec. 14). They are plain, fast, stdlib-only Python scripts that run the same way
for Codex, Claude Code, and a git pre-commit hook.

## Gates

| Gate | Script | When | Blocks on |
|---|---|---|---|
| A. Secret guard | `common/secret_guard.py` | PreToolUse (Write/Edit/Bash), pre-commit `--staged` | AWS/Google/Slack/GitHub/OpenAI/Anthropic keys, private keys, hardcoded secrets, `.env` |
| B. Protected file guard | `common/protected_file_guard.py` | PreToolUse (Write/Edit), pre-commit `--staged` | credentials, `*.pem/*.key`, migrations, lockfiles, generated specs, install manifest |
| C+E. Spec-required / drift | `common/spec_required_gate.py` | Stop, pre-commit | spec-worthy change (API/schema, migration, model/prompt, contract, auth) without an accompanying spec/change |
| D. Verification gate | `common/verification_gate.py` | Stop | configured verify command fails; or (strict) source changed with no tests |

`common/pre_commit.py` chains A + B + C for git. `common/_hooklib.py` holds the shared payload/mode/
decision helpers.

## Enforcement modes

Set `PAI_SDD_ENFORCEMENT`:

- `strict` — blocks on everything above, plus unverified source changes and contract/migration
  changes lacking a plan/verification.
- `standard` (default) — blocks on secrets, protected files, and missing specs for spec-worthy
  changes; warns on unverified source.
- `advisory` — never blocks; prints the same messages so you can adopt gradually.

Every block prints an actionable message (what tripped, and how to fix it).

## Wiring

- **Claude Code:** copy `.claude/settings.example.json` to `.claude/settings.json`
  (or run `python scripts/install_hooks.py`). It wires PreToolUse + Stop.
- **git:** `python scripts/install_hooks.py` writes `.git/hooks/pre-commit` (no-clobber).
- **Codex:** see `.codex/config.example.toml`; the git pre-commit path is the most portable.

## Tests

`python scripts/test_hooks.py` feeds crafted payloads to each guard and asserts the block/allow
decision and that messages are actionable (Master Spec DoD sec. 25.4).
