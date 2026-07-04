# Windows / WSL2

The pack is developed and tested on Windows 11 and works on WSL2, macOS, and Linux. A few
Windows-specific notes.

## Encoding (important)

All pack files are UTF-8. Legacy Windows consoles default to a regional code page (e.g. cp950/Big5),
which can *display* UTF-8 punctuation as mojibake even though the files are fine. This was the root
cause of a false "corruption" review finding. To avoid it:

```powershell
chcp 65001                 # switch the console to UTF-8
$env:PYTHONUTF8 = "1"      # force Python UTF-8 mode
```

The validators intentionally keep skill/text files ASCII-clean where practical and warn on non-ASCII
to reduce this risk.

## Installation uses copy, not symlink

`install.py` copies skills (never symlinks), so it works identically on Windows without admin rights
or Developer Mode. `.agents/skills/`, `.claude/skills/`, and the install manifest are git-ignored.

## Line endings

Git may convert LF↔CRLF on checkout (you will see warnings). This is harmless; the scripts are
stdlib Python and run under both `python` (Windows) and `python3`.

## Running

```powershell
python scripts/run_quality_gate.py --mode standard
```

Under WSL2, use your Linux Python and the same commands; paths and hooks behave like Linux.

## Optional dependencies

Everything runs on the stdlib. Installing `pyyaml` and `jsonschema` improves spec/frontmatter
fidelity but is not required (the scripts fall back gracefully). See
[troubleshooting.md](troubleshooting.md).
