# Codex xtrl

xtrl is a repo-agnostic execution surface that keeps config, state, and vendor
data in distinct XDG roots. It provides packet templates, execution tooling, and
evidence conventions while keeping all runtime state out of the target
repositories.

## XDG layout (canonical)
- `CODEX_HOME` = `$XDG_CONFIG_HOME/codex` (config only)
- `CODEX_STATE` = `$XDG_STATE_HOME/codex` (runtime state + evidence)
- `CODEX_DATA` = `$XDG_DATA_HOME/codex` (vendor checkouts)

State root:
```
$CODEX_STATE/xtrl/{packets,out,worktrees}/...
```

Vendor checkout:
```
$CODEX_DATA/vendor/xtrl
```
See `docs/projectops/xdg-layout.md` for details.

Binding ProjectOps paths: `docs/drr/DRR-0001-projectops-naming-paths.md`
Repo backlog: `backlog.md`

## Export surface (skills-pack)
`skills-pack/` is the subtree-importable export surface for `$CODEX_HOME/skills/`:
- `skills-pack/xtrl.packet-runner/`
- `skills-pack/xtrl.packet-template/`

`skills/` remains as a compatibility layer (symlinks to `skills-pack/`).

## Global-only roots (no repo-local .codex/.quint)
xtrl must not create or depend on repo-local `./.codex/` or `./.quint/`.
All runtime artifacts live under the xtrl state root in `$CODEX_STATE`.
A compatibility alias may expose `$CODEX_STATE/ctrlex/` or
`$CODEX_STATE/plant-a/` if you are still migrating existing work.

## Install via chezmoi subtree (example)
From your chezmoi source directory:
```bash
git subtree add --prefix "$CODEX_HOME/skills/xtrl.packet-runner" /path/to/codex-plant-a skills-pack/xtrl.packet-runner --squash
git subtree add --prefix "$CODEX_HOME/skills/xtrl.packet-template" /path/to/codex-plant-a skills-pack/xtrl.packet-template --squash
```

## Run a packet (target-aware)
```bash
bash $CODEX_HOME/skills/xtrl.packet-runner/scripts/run_packet.sh \
  packets/examples/packet-000-foundation.json \
  --repo-root /path/to/target
```

## Evidence output
Evidence bundles are written under:
```
<repo_root>/out/<packet_id>/
```

## Install wrappers (repo-shipped)
Copy the repo-shipped wrappers into your PATH and mark them executable:
```bash
install -m 755 scripts/install/xtrl ~/.local/bin/xtrl
install -m 755 scripts/install/xtrl-just-mcp ~/.local/bin/xtrl-just-mcp
```

## CLI & Just integration
The `xtrl` CLI aggregates the Python tooling so you can run the canonical
commands without walking into a repo:

```bash
xtrl preflight --repo-root /path/to/repo
xtrl run-packet --repo-root /path/to/repo packets/examples/<packet>.json
xtrl collect-evidence --repo-root /path/to/repo packets/examples/<packet>.json
```

Use `xtrl just render --out "$CODEX_HOME/xtrl/Justfile"` to generate the Justfile
watched by `just-mcp`, and `xtrl just install-mcp` to print the MCP stanza that
runs `just-mcp --watch-dir "$CODEX_HOME/xtrl:xtrl"`.

The launcher at `~/.local/bin/xtrl-just-mcp` watches `$CODEX_HOME/xtrl`
(alias `xtrl`), so MCP tools are published as `just_<recipe>@xtrl`.

## Control surface (ctrl.*)
The control surface is a set of `just` recipes prefixed with `ctrl.` that act as
the public actuator API for MCP and Yazi:
- `ctrl.help`, `ctrl.list`, `ctrl.paths`, `ctrl.doctor`
- `ctrl.preflight`, `ctrl.exec`, `ctrl.check`, `ctrl.evidence`
- `ctrl.promote` (deny-by-default)

See `docs/projectops/yazi.md` for the Yazi → just wiring.
