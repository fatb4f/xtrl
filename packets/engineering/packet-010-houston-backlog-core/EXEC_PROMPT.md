# EXEC_PROMPT — packet-010-houston-backlog-core

```json
{
  "schema_version": "1.0.0",
  "contract_path": "packets/engineering/packet-010-houston-backlog-core/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees",
  "tasks": [
    "Create xtrl-owned Houston backlog SSOT under data/houston/ (index packet + minimal README).",
    "Add deterministic renderer tool under tools/houston/ that generates backlog.md (or data/houston/backlog.md).",
    "Add/update tests for deterministic rendering; keep existing smoke_xdg_paths test passing."
  ],
  "acceptance_checks": [
    "python tests/smoke_xdg_paths.py",
    "python -m compileall tools"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt",
    "raw/changed_paths.txt",
    "raw/tests.txt"
  ]
}

Acceptance checks

python tests/smoke_xdg_paths.py

python -m compileall tools

Evidence

Required artifacts under $CODEX_STATE/xtrl/out/packet-010-houston-backlog-core/:

summary.md

raw/diffstat.txt

raw/changed_paths.txt

raw/tests.txt
