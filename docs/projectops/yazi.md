# Yazi → just wiring (no logic in Yazi)

Yazi only launches `just` commands; ProjectOps logic stays in Justfile recipes.

## Keybindings
This repo ships a starter keymap in `dot_config/yazi/keymap.toml`:
- `g w` → `just wt` (worktree)
- `g s` → `just sess` (session)
- `g p` → `just -f "$CODEX_HOME/xtrl/Justfile" ctrl.preflight`
- `g c` → `just -f "$CODEX_HOME/xtrl/Justfile" ctrl.check` (hovered contract)
- `g m` → `just -f "$CODEX_HOME/xtrl/Justfile" ctrl.promote` (disabled by default)

## Notes
- The keymap assumes `CODEX_HOME` is set to the config root and that the generated
  Justfile lives at `$CODEX_HOME/xtrl/Justfile`.
- The `ctrl.check` binding passes the hovered path as the contract argument.
