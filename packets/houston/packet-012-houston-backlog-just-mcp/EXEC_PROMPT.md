# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/houston/packet-012-houston-backlog-just-mcp/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/packet-012-houston-backlog-just-mcp/",
  "tasks": [
    "Add ctrl.backlog.hydrate and ctrl.backlog.sync recipes to templates/Justfile.tmpl (rendered surface).",
    "Mirror the same recipes into dot_config/codex/just/xtrl.just (dotfiles-friendly surface).",
    "Update ctrl.help output to include the new backlog commands.",
    "Update dot_config/codex/xtrl/MCP.md to document the two backlog commands and note that xtrl just render must be re-run for MCP surface updates.",
    "Keep cache-root invariants: recipes must pass --codex-state through to the tool; the tool must derive cache under $CODEX_STATE/xtrl/cache/houston (no repo-local state)."
  ],
  "acceptance_checks": [
    "python ./xtrl just render --out /tmp/xtrl.Justfile",
    "just -f /tmp/xtrl.Justfile --list | grep -q 'ctrl\\.backlog\\.hydrate'",
    "just -f /tmp/xtrl.Justfile --list | grep -q 'ctrl\\.backlog\\.sync'",
    "grep -n 'ctrl.backlog.hydrate' -n templates/Justfile.tmpl",
    "grep -n 'ctrl.backlog.sync' -n templates/Justfile.tmpl"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

Deterministic promoted commit message

Use exactly:

feat(houston): add ctrl.backlog.{hydrate,sync} (packet-012)

Optional trailers:

Packet: packet-012-houston-backlog-just-mcp

Evidence: <repo_root>/out/packet-012-houston-backlog-just-mcp/

Recipe behavior requirements (for implementation)

When adding the recipes, require:

Guard: fail if XTRL_ROOT is unset.

Tool entrypoint: call the backlog tool (expected to exist after backlog core lands) and pass --codex-state.

Parameters (minimum):

codex_state=""

ttl_minutes="60" (hydrate)

offline="0" (hydrate/sync)

out="backlog.md" (sync)

The recipes should NOT write to repo-local .codex/ or .quint/ paths.

---

## Notes for the implementation (what the recipes should look like)

When you execute this packet, implement the recipe bodies so they:
- only **invoke** the tool (no logic in Just)
- pass `--codex-state` through
- rely on the tool to place cached state under `"$CODEX_STATE/xtrl/cache/houston"` and to update/render `backlog.md`

If you want the exact recipe text included in the packet tasks, tell me whether the tool entrypoint is intended to be:
- `python "$XTRL_ROOT/tools/houston/backlog.py" hydrate|sync ...` **(single entrypoint)**, or
- separate scripts (e.g., `hydrate.py` + `render.py`).
