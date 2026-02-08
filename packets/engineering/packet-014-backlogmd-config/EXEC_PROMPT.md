# EXEC_PROMPT — packet-014-backlogmd-config

```json
{
  "schema_version": "1.0.0",
  "contract_path": "packets/engineering/houston/packet-014-backlogmd-config/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Initialize Backlog.md in the repo.",
    "Verify core config and commands are available.",
    "Emit evidence artifacts."
  ],
  "acceptance_checks": [
    "backlog init \"xtrl\"",
    "backlog config --help",
    "backlog board --help",
    "backlog browser --help"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt",
    "raw/changed_paths.txt",
    "raw/tests.txt"
  ]
}
```
