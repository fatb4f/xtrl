# EXEC_PROMPT

```json
{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/examples/packet-000-foundation.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/packet-000-foundation/",
  "tasks": [
    "Validate the packet runner end-to-end using this contract."
  ],
  "acceptance_checks": [
    "python $CODEX_DATA/vendor/xtrl/tools/run_packet.py packets/examples/packet-000-foundation.json --repo-root /path/to/target"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt"
  ]
}
```

## Tasks
1) Validate the packet runner end-to-end using this contract.

## Acceptance checks
- `python $CODEX_DATA/vendor/xtrl/tools/run_packet.py packets/examples/packet-000-foundation.json --repo-root /path/to/target`

## Evidence
Required artifacts under `<repo_root>/out/packet-000-foundation/`:
- `summary.md`
- `raw/diffstat.txt`
