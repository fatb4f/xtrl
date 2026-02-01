# xtrl MCP tools

This document covers exposing the xtrl execution surface via `just-mcp` so Codex can
invoke the CLI recipes from any repo.

## Install `just-mcp`
Use `binstall justmcp just-mcp` (preferred) or download a release from
https://github.com/justmcp/just-mcp/releases and put the binary on your `PATH`.

## Generate the watched Justfile
Every time the recipes change, rerun:

```bash
xtrl just render --out $CODEX_HOME/Justfile
```

The generated file defines the migrated `preflight`, `enter_work`, `run_packet`,
`collect_evidence`, and `doctor` recipes via the installed `xtrl` CLI.

## Print the MCP config stanza
Call the helper to emit the `[mcp_servers]` snippet that points at the global watch
dir:

```bash
xtrl just install-mcp
```

Copy the output into `~/.codex/config.toml` (or your Codex config) so the stdio
server can launch `just-mcp --watch-dir "$CODEX_HOME:xtrl"`.

## Wrapper CLI
Install the bundled wrapper at `$CODEX_HOME/bin/xtrl` (see `dot_config/codex/bin/xtrl`) so both
the exported Justfile and the MCP server invoke a stable executable instead of
relying on user `PATH`.

## Start the MCP server
```bash
$CODEX_HOME/bin/xtrl-just-mcp
```
This watches `$CODEX_HOME` (named `xtrl`), so `just-mcp` discovers `$CODEX_HOME/Justfile`
and advertises recipes as tools named `just_<recipe>@xtrl` (e.g., `just_preflight@xtrl`).

## Refresh available tools
`just-mcp` exposes an `admin_sync` tool to force a reload:

```bash
just-mcp admin_sync
```

## Smoke checks
1. Doctor the current repo without the MCP server:
   ```bash
   just -f $CODEX_HOME/Justfile doctor repo_root=/path/to/repo
   ```
2. Run the preflight recipe to confirm it works:
   ```bash
   just -f $CODEX_HOME/Justfile preflight repo_root=/path/to/repo
   ```
3. Verify tool discovery:
   ```bash
   just-mcp --watch-dir "$CODEX_HOME:xtrl" --list-tools
   ```
   Look for entries like `just_preflight@xtrl`, `just_run_packet@xtrl`, etc.

All recipes operate on the target repo via `--repo-root` and emit artifacts under
`$CODEX_STATE/xtrl/{packets,out,worktrees}`. Legacy `ctrlex` or `plant-a` roots are
only referenced when the canonical `xtrl` directories are missing.
