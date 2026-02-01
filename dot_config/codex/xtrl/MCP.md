# xtrl MCP tools

This document covers exposing the xtrl execution surface via `just-mcp` so Codex can
invoke the CLI recipes from any repo.

## Install `just-mcp`
Use `binstall justmcp just-mcp` (preferred) or download a release from
https://github.com/justmcp/just-mcp/releases and put the binary on your `PATH`.

## Generate the watched Justfile
Every time the recipes change, rerun:

```bash
xtrl just render --out $CODEX_HOME/xtrl/Justfile
```

The generated file defines the migrated `preflight`, `enter_work`, `run_packet`,
`collect_evidence`, `doctor`, and `ctrl.*` recipes via the installed `xtrl` CLI.
`ctrl.list` and `ctrl.evidence` also expect `XTRL_ROOT` to be set (the launcher
exports it by default).

## Print the MCP config stanza
Call the helper to emit the `[mcp_servers]` snippet that points at the global watch
dir:

```bash
xtrl just install-mcp
```

Copy the output into `~/.codex/config.toml` (or your Codex config) so the stdio
server can launch `just-mcp --watch-dir "$CODEX_HOME/xtrl:xtrl"`.

## Wrapper CLI
Install the bundled wrapper at `~/.local/bin/xtrl` (see `scripts/install/xtrl`) so both
the exported Justfile and the MCP server invoke a stable executable instead of
relying on user `PATH`.

## Start the MCP server
```bash
~/.local/bin/xtrl-just-mcp
```
This watches `$CODEX_HOME/xtrl` (named `xtrl`), so `just-mcp` discovers
`$CODEX_HOME/xtrl/Justfile` and advertises recipes as tools named
`just_<recipe>@xtrl` (e.g., `just_ctrl.preflight@xtrl`).

## Refresh available tools
`just-mcp` exposes an `admin_sync` tool to force a reload:

```bash
just-mcp admin_sync
```

## Smoke checks
1. Doctor the current repo without the MCP server:
   ```bash
   just -f $CODEX_HOME/xtrl/Justfile doctor repo_root=/path/to/repo
   ```
2. Run the preflight recipe to confirm it works:
   ```bash
   just -f $CODEX_HOME/xtrl/Justfile ctrl.preflight repo_root=/path/to/repo
   ```
3. Verify tool discovery:
   ```bash
   just-mcp --watch-dir "$CODEX_HOME/xtrl:xtrl" --list-tools
   ```
   Look for entries like `just_ctrl.preflight@xtrl`, `just_ctrl.exec@xtrl`, etc.

All recipes operate on the target repo via `--repo-root` and emit artifacts under
`$CODEX_STATE/xtrl/{packets,out,worktrees}`. Legacy `ctrlex` or `plant-a` roots are
only referenced when the canonical `xtrl` directories are missing.
