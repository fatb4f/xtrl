# DRR-0001 — ProjectOps Naming + Paths (xtrl)

Status: ACCEPTED
Date: 2026-02-01

## Decisions (binding)

### D1 — ID derivation
IDs are filesystem-derived and stable.

- Canonical pattern: `<id>-<slug>` (recommended)
- Stable legacy names allowed if unambiguous (e.g., `packet-000-foundation`)

### D2 — Worktree base path
`CODEX_STATE := ${CODEX_STATE:-$XDG_STATE_HOME/codex}`

Worktrees live at:
- `$CODEX_STATE/xtrl/worktrees/<repo>/<packet_id>/`

### D3 — Session naming
- `<repo>-<packet_id>`

### D4 — `just wt` implementation
- `lazyworktree`

### D5 — Gate/evidence SSOT location
Out dir:
- `$CODEX_STATE/xtrl/out/<repo>/<packet_id>/`

Minimum files expected in out dir:
- `contract.json`
- `exec-prompt.md`
- `packet.json`
- `summary.md`
- `commands.log`

## Hard invariants (non-negotiable)
- `CODEX_HOME := ${CODEX_HOME:-$XDG_CONFIG_HOME/codex}` is config-only
- No repo-local roots: deny `.codex/` and `.quint/` anywhere in target repos
- Strict clean gate: `git status --porcelain` must be empty (untracked counts as dirty)
- All git ops must be `git -C <repo_root> …`

## Follow-ups (explicit)
- Update `dot_config/**` and `skills-pack/**` to stop referencing CODEX_HOME state paths
