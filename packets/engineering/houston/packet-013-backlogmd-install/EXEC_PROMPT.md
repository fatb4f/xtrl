# EXEC_PROMPT — packet-013-backlogmd-install

```json
{
  "schema_version": "1.0.0",
  "contract_path": "packets/engineering/houston/packet-013-backlogmd-install/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Install Backlog.md CLI via npm.",
    "Verify CLI responds to --help/--version and MCP help.",
    "Emit evidence artifacts."
  ],
  "acceptance_checks": [
    "NPM_CONFIG_PREFIX="$HOME/.local" npm i -g backlog.md",
    "backlog --help",
    "backlog --version",
    "backlog mcp start --help"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt",
    "raw/changed_paths.txt",
    "raw/tests.txt"
  ]
}
```
