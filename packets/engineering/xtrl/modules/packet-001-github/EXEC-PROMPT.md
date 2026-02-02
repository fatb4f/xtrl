{
  "schema_version": "1.0.0",
  "contract_path": "$CODEX_STATE/xtrl/packets/engineering/packet-012-github-module/contract.json",
  "worktree_root": "$CODEX_STATE/xtrl/worktrees/packet-012-github-module/",
  "tasks": [
    "Add tools/github/ module that wraps gh operations behind a small API (shell-out wrapper + error normalization).",
    "Add cache helper(s) anchored at $CODEX_STATE/xtrl/cache/github with TTL support, plus --offline and --dry-run behaviors (no network in offline).",
    "Extend schemas/contract.schema.json to support a github block usable by packets (at minimum: issue + pr metadata request shapes; keep additive and schema-valid).",
    "Add offline tests + fixtures (tests/smoke_github_module.py) that validate: schema accepts github block, offline mode never hits network, cache read/write paths stay under CODEX_STATE, and outputs are deterministic."
  ],
  "acceptance_checks": [
    "python tests/smoke_xdg_paths.py",
    "python tests/smoke_github_module.py",
    "python -m compileall xtrl tools"
  ],
  "evidence": [
    "summary.md",
    "raw/diffstat.txt",
    "raw/git-diff.patch",
    "raw/test.log",
    "raw/lint.log",
    "raw/schema-validate.log"
  ]
}

