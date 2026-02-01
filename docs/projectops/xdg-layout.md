# XDG layout for xtrl

## Goals
- Keep config small and declarative.
- Keep runtime state under XDG state.
- Keep vendor checkouts under XDG data.

## Canonical roots
- `CODEX_HOME` → `$XDG_CONFIG_HOME/codex` (config only)
- `CODEX_STATE` → `$XDG_STATE_HOME/codex` (runtime state + evidence)
- `CODEX_DATA` → `$XDG_DATA_HOME/codex` (vendor checkouts)

Defaults if XDG variables are not set:
- `XDG_CONFIG_HOME`: `$HOME/.config`
- `XDG_STATE_HOME`: `$HOME/.local/state`
- `XDG_DATA_HOME`: `$HOME/.local/share`

## State layout
All runtime artifacts live under:
```
$CODEX_STATE/xtrl/{packets,out,worktrees,log}/...
```
Legacy roots (`ctrlex`, `plant-a`) are only checked under `CODEX_STATE`.

## Vendor layout
The recommended vendor checkout is:
```
$CODEX_DATA/vendor/xtrl
```
Wrapper fallback order:
1) `XTRL_ROOT` (explicit)
2) `CTRLEX_ROOT` (compat)
3) `$CODEX_DATA/vendor/xtrl`
4) `$CODEX_DATA/vendor/ctrlex`
5) `$CODEX_HOME/skills/vendor/xtrl`
6) `$CODEX_HOME/skills/vendor/ctrlex`

## Generated Justfile
The generated Justfile is config output (not source) and lives at:
```
$CODEX_HOME/xtrl/Justfile
```
Use `xtrl just render --out "$CODEX_HOME/xtrl/Justfile"` to generate it.

## MCP launcher
Run MCP via the wrapper:
```
~/.local/bin/xtrl-just-mcp
```
This watches:
```
$CODEX_HOME/xtrl
```
so just-mcp registers recipes from the generated Justfile.

## CLI overrides
All xtrl tools accept these overrides:
- `--codex-home` for config root
- `--codex-state` for state root

Use these in smoke tests to ensure state does not write under `CODEX_HOME`.
