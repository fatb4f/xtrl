# xtrl backlog

Planning SSOT lives in `./backlog/`.

This file is a summary/export view only.

## Backlog tasks by area/milestone
### ops
- P0
  - pkt-evidence-0001-xtrl-ops-v0-2-contract-schema-adoption: xtrl-ops v0.2 contract schema adoption (To Do)
  - pkt-evidence-0002-implement-evidencecapsule-v0-2-layout: Implement EvidenceCapsule v0.2 layout (To Do)
  - pkt-evidence-0003-align-evidence-json-with-v0-2-schema: Align evidence.json with v0.2 schema (To Do)
  - pkt-exec-0001-enforce-action-only-execution: Enforce ACTION-only execution (To Do)
- P1
  - pkt-exec-0002-enforce-budgets-time-diff-iteration: Enforce budgets (time/diff/iteration) (To Do)
  - pkt-exec-0003-enforce-allowed-paths-during-execution: Enforce allowed paths during execution (To Do)
  - pkt-paths-0001-update-out-dir-to-include-repo-namespace: Update OUT_DIR to include repo namespace (To Do)
  - pkt-policy-0001-normalize-modes-and-reasoncodes: Normalize Modes and ReasonCodes (To Do)
- P2
  - pkt-actuator-0001-enforce-actuator-chain-requirements: Enforce actuator chain requirements (To Do)
  - pkt-backlog-0002-worktree-visibility: Worktree visibility (To Do)
  - pkt-skills-0001-validate-skills-pack-layout-and-compatibility-symlink: Validate skills-pack layout and compatibility symlink (To Do)
  - pkt-state-layout-0001-validate-ensure-state-subtrees: Validate/ensure state subtrees (To Do)
## Consolidated backlog (raw)

```json
{
  "components": {
    "items": [
      {
        "derived_p": "P0",
        "id": "quint",
        "notes": [
          "Needs small persistent index to avoid losing project memory."
        ],
        "optional": [],
        "requires": [
          "SSOT:SPEC.md",
          "SSOT:OPS.md",
          "BACKLOG:BACKLOG.md",
          "pointer:last_evidence (EvidenceCapsule id/path/hash | none)",
          "pointer:last_gate (GateDecision id/path | none)"
        ],
        "role": "epistemic control + governance index",
        "writes": [
          "work_order:WorkOrder",
          "state_index:{active_backlog_item,last_run_id,last_gate_decision,last_evidence_ptr}"
        ]
      },
      {
        "derived_p": "P0",
        "id": "chatgpt_cli",
        "notes": [
          "Transport/interaction surface; not authority for persistent state beyond emitted artifacts."
        ],
        "optional": [
          "bridge:proposal.json",
          "bridge:tick_decision.json",
          "evidence_inputs (for observers)"
        ],
        "requires": [
          "work_order:WorkOrder (or ability to generate from Quint)"
        ],
        "role": "planner/runtime router surface",
        "writes": [
          "work_order:WorkOrder (if producing it)"
        ]
      },
      {
        "derived_p": "P2",
        "id": "observer_a",
        "notes": [
          "If inputs missing => degrade to NOTES_ONLY/deny."
        ],
        "optional": [],
        "requires": [
          "preflight_snapshot",
          "active_block",
          "window_flags",
          "timer_phase",
          "latest_o_tests (or not_run)"
        ],
        "role": "neuro legality/intensity (optional)",
        "writes": [
          "tick_decision:TickDecision"
        ]
      },
      {
        "derived_p": "P2",
        "id": "observer_b",
        "notes": [],
        "optional": [
          "packet_stub:PacketStub"
        ],
        "requires": [
          "evidence_inputs (trace/test outputs/counterexample OR EvidenceCapsule)",
          "failing_invariant_details (optional)"
        ],
        "role": "work/learning (optional)",
        "writes": [
          "proposal:Proposal"
        ]
      },
      {
        "derived_p": "P2",
        "id": "coordinator",
        "notes": [
          "Outputs: EXECUTE|DEFER|RESET|NOTES_ONLY|CLOSE."
        ],
        "optional": [
          "degraded_action_text"
        ],
        "requires": [
          "observer_a:TickDecision",
          "observer_b:Proposal (optional depending on a_outcome)",
          "rules:veto_degrade_rules"
        ],
        "role": "mechanical intersection (optional)",
        "writes": [
          "tick_decision.json"
        ]
      },
      {
        "derived_p": "P1",
        "id": "ralph",
        "notes": [
          "Authority is derived from evidence references."
        ],
        "optional": [],
        "requires": [
          "work_order:WorkOrder",
          "run:EvidenceCapsule",
          "SSOT:SPEC.md (gate semantics)",
          "SSOT:evidence schema (EvidenceCapsule validity rules)"
        ],
        "role": "execution governance gatekeeper",
        "writes": [
          "gate_decision:GateDecision{work_order_id,run_id,decision,reason_codes,rationale}"
        ]
      },
      {
        "derived_p": "P0",
        "id": "xtrl",
        "notes": [
          "P1 adds evidence SSOT + action/VAR enforcement and stronger gating."
        ],
        "optional": [],
        "requires": [
          "target:repo_root (absolute)",
          "wiring:codex_home (config root)",
          "wiring:state_home (runtime state root)",
          "intent:WorkOrder and/or packet contract/handoff",
          "deny_fast:git_clean",
          "deny_fast:no_forbidden_roots"
        ],
        "role": "global controller/executor substrate",
        "writes": [
          "state:out/<repo_key>/<packet_id>/{evidence.json,logs,check_outputs,artifacts_hashes,...}",
          "optional:worktrees/<repo_key>/<packet_id>/..."
        ]
      },
      {
        "derived_p": "P0",
        "id": "codex_cli",
        "notes": [
          "Does not own acceptance; evidence + gate do."
        ],
        "optional": [],
        "requires": [
          "cwd:repo_or_worktree_path",
          "instructions:WorkOrder/Handoff",
          "local_tool_access (shell, git, tests, etc.)",
          "optional:mcp_connection (just-mcp)"
        ],
        "role": "execution engine (actuator)",
        "writes": [
          "repo_changes (as allowed)",
          "execution outputs (captured by xtrl into EvidenceCapsule)"
        ]
      },
      {
        "derived_p": "P0",
        "id": "just",
        "notes": [
          "Invokes xtrl; no persistent state."
        ],
        "optional": [],
        "requires": [
          "generated_justfile",
          "PATH resolves xtrl"
        ],
        "role": "actuator UX",
        "writes": []
      },
      {
        "derived_p": "P0",
        "id": "just_mcp",
        "notes": [
          "Exposes tools; no persistent state."
        ],
        "optional": [],
        "requires": [
          "watch_root containing generated Justfile",
          "mcp_session_stdio"
        ],
        "role": "MCP projection of just",
        "writes": []
      },
      {
        "derived_p": "P0",
        "id": "ssot_docs",
        "notes": [],
        "optional": [],
        "requires": [
          "versioned_git_storage"
        ],
        "role": "SSOT documents and schemas",
        "writes": [
          "versioned_revisions referenced by WorkOrder/EvidenceCapsule/GateDecision"
        ]
      },
      {
        "derived_p": "P0",
        "id": "backlog",
        "notes": [
          "Without link fields backlog becomes narrative-only."
        ],
        "optional": [],
        "requires": [
          "items:{deliverables,exit_criteria,required_evidence}"
        ],
        "role": "operational backlog state",
        "writes": [
          "backlog_state:{active_item_id,item_status,last_evidence_run_id,last_gate_decision}"
        ]
      }
    ],
    "schema_version": "xtrl.components/v1",
    "updated": "2026-02-02"
  },
  "contracts": {
    "projectops_ssot": {
      "gate_log_ssot": "$XDG_STATE_HOME/xtrl/out/<repo_key>/<packet_id>/",
      "id_derivation": "<id>-<slug>",
      "session_name": "<repo>-<id>",
      "worktree_base": "$XDG_STATE_HOME/xtrl/worktrees/<repo_key>/<packet_id>/",
      "wt_selector": "lazyworktree"
    },
    "reasoncodes": {
      "note": "Reasoncode taxonomy becomes canonical when pkt-0007 delivers machine-checkable denial reasoncodes.",
      "source_packet": "pkt-0007-root-preflight-enforce",
      "status": "planned"
    },
    "xdg": {
      "config_root": "$XDG_CONFIG_HOME/codex/xtrl",
      "executables_root": "~/.local/bin",
      "generated_justfile_path": "$CODEX_HOME/xtrl/Justfile",
      "mcp_watch_dir": "$CODEX_HOME/xtrl:xtrl",
      "state_root": "$XDG_STATE_HOME/xtrl",
      "state_subdirs": [
        "out",
        "worktrees",
        "logs",
        "cache"
      ],
      "vendor_root": "$XDG_DATA_HOME/codex/vendor/xtrl",
      "vendor_symlink_under_config": "$XDG_CONFIG_HOME/codex/xtrl/vendor"
    }
  },
  "derived_mappings": {
    "artifact_to_packets": {
      "DRR-0001 committed": {
        "derived_p": "P0",
        "produced_by_packets": [
          "pkt-0001-projectops-drr"
        ]
      },
      "evidence schema + required outputs (summary.md, commands.log)": {
        "derived_p": "P1",
        "produced_by_packets": [
          "pkt-0006-evidence-ssot"
        ]
      },
      "generated Justfile template in-repo": {
        "derived_p": "P0",
        "finalized_by_packets": [
          "pkt-0004-render-install-surface"
        ],
        "produced_by_packets": [
          "pkt-0002-xdg-split"
        ]
      },
      "install wrappers in-repo": {
        "derived_p": "P0",
        "finalized_by_packets": [
          "pkt-0004-render-install-surface"
        ],
        "produced_by_packets": [
          "pkt-0002-xdg-split"
        ]
      },
      "migration manifests for legacy .codex data": {
        "derived_p": "P0",
        "produced_by_packets": [
          "pkt-0008-legacy-codex-migration"
        ]
      },
      "root-preflight denial reasoncodes": {
        "derived_p": "P1",
        "produced_by_packets": [
          "pkt-0007-root-preflight-enforce"
        ]
      }
    },
    "next_focus": {
      "definition_of_done": [
        "rg finds no executable references to $CODEX_HOME/xtrl/(out|worktrees|packets)",
        "end-to-end smoke test uses --codex-state successfully"
      ],
      "next_packet": "pkt-0003-consistency-sweep"
    },
    "packet_registry": [
      {
        "blocks": [
          "pkt-0002-xdg-split"
        ],
        "criticality": "required",
        "deliverables": [
          "docs/drr/DRR-0001-projectops-naming-paths.md"
        ],
        "depends_on": [],
        "exit_criteria": [
          "DRR committed on main",
          "DRR referenced from README or docs index (optional)"
        ],
        "id": "pkt-0001-projectops-drr",
        "stage": "P0",
        "status": "done",
        "title": "Lock ProjectOps decisions (DRR-0001)",
        "type": "packet"
      },
      {
        "blocks": [
          "pkt-0003-consistency-sweep"
        ],
        "criticality": "required",
        "deliverables": [
          "tools path resolution: codex_home vs codex_state",
          "repo-shipped wrappers + Justfile template",
          "docs: XDG layout",
          "smoke test asserting no state under CODEX_HOME"
        ],
        "depends_on": [
          "pkt-0001-projectops-drr"
        ],
        "exit_criteria": [
          "tests/smoke_xdg_paths.py passes",
          "state outputs default under CODEX_STATE/xtrl"
        ],
        "id": "pkt-0002-xdg-split",
        "stage": "P0",
        "status": "done",
        "title": "Enforce XDG split (CODEX_STATE owns runtime output)",
        "type": "packet"
      },
      {
        "blocks": [
          "pkt-0004-render-install-surface"
        ],
        "criticality": "required",
        "deliverables": [
          "update skills-pack/** scripts to pass --codex-state and write state to CODEX_STATE",
          "update dot_config/codex/** snippets to reflect CODEX_STATE/CODEX_DATA",
          "mechanical grep/rg guard: deny executable refs to $CODEX_HOME/xtrl/(out|worktrees|packets)"
        ],
        "depends_on": [
          "pkt-0002-xdg-split"
        ],
        "exit_criteria": [
          "rg finds no executable references to $CODEX_HOME/xtrl/(out|worktrees|packets)",
          "end-to-end smoke test uses --codex-state successfully"
        ],
        "id": "pkt-0003-consistency-sweep",
        "notes": [
          "Leave legacy mentions only in explicitly marked docs if unavoidable."
        ],
        "stage": "P0",
        "status": "planned",
        "title": "Sweep remaining CODEX_HOME-as-state refs (skills-pack/**, dot_config/**)",
        "type": "packet"
      },
      {
        "blocks": [
          "pkt-0005-ctrl-surface"
        ],
        "criticality": "supporting",
        "deliverables": [
          "install scripts produce stable PATH wrappers (recommended: ~/.local/bin)",
          "xtrl just render writes $CODEX_HOME/xtrl/Justfile deterministically",
          "mcp launcher watches $CODEX_HOME/xtrl and registers tools from generated Justfile"
        ],
        "depends_on": [
          "pkt-0003-consistency-sweep"
        ],
        "exit_criteria": [
          "tools register under just-mcp from $CODEX_HOME/xtrl/Justfile",
          "commands run from any cwd with explicit repo_root targeting"
        ],
        "id": "pkt-0004-render-install-surface",
        "stage": "P0",
        "status": "planned",
        "title": "Verify install + render surfaces (MCP watch root stable)",
        "type": "packet"
      },
      {
        "blocks": [
          "gate-is_implemented",
          "pkt-0006-evidence-ssot",
          "pkt-0007-root-preflight-enforce"
        ],
        "criticality": "required",
        "deliverables": [
          "ctrl.help",
          "ctrl.list",
          "ctrl.doctor",
          "ctrl.paths",
          "ctrl.preflight",
          "ctrl.exec",
          "ctrl.check",
          "ctrl.evidence",
          "ctrl.promote (deny-by-default initially)"
        ],
        "depends_on": [
          "pkt-0004-render-install-surface"
        ],
        "exit_criteria": [
          "ctrl.* discoverable via MCP",
          "downstream callers (Yazi/MCP) can use ctrl.* only",
          "ctrl.preflight enforces strict gates (clean + forbidden roots)"
        ],
        "id": "pkt-0005-ctrl-surface",
        "stage": "P0",
        "status": "planned",
        "title": "Layer 1 public actuator surface: ctrl.*",
        "type": "packet"
      },
      {
        "blocks": [
          "gate-is_implemented",
          "pkt-0010-action-exec"
        ],
        "criticality": "required",
        "deliverables": [
          "evidence.json schema/fields (ComplianceReport SSOT)",
          "OUT_DIR layout standard (XDG state rooted)",
          "required files: summary.md, commands.log",
          "ctrl.evidence generates and ctrl.check validates SSOT"
        ],
        "depends_on": [
          "pkt-0005-ctrl-surface"
        ],
        "exit_criteria": [
          "ctrl.evidence always produces required files in OUT_DIR",
          "ctrl.check fails fast when required evidence missing or malformed"
        ],
        "id": "pkt-0006-evidence-ssot",
        "stage": "P1",
        "status": "planned",
        "title": "Evidence SSOT: ComplianceReport (evidence.json) + required outputs",
        "type": "packet"
      },
      {
        "blocks": [
          "gate-is_implemented",
          "pkt-0008-legacy-codex-migration"
        ],
        "criticality": "required",
        "deliverables": [
          "root-preflight scans tracked + untracked for .codex/.quint",
          "strict clean gate: git status --porcelain must be empty",
          "machine-checkable reasoncodes for denials"
        ],
        "depends_on": [
          "pkt-0005-ctrl-surface"
        ],
        "exit_criteria": [
          "consistent denial reasoncodes emitted",
          "ctrl.preflight denies forbidden roots deterministically"
        ],
        "id": "pkt-0007-root-preflight-enforce",
        "stage": "P1",
        "status": "planned",
        "title": "Enforce root-preflight: deny repo-local roots + strict clean gate everywhere",
        "type": "packet"
      },
      {
        "blocks": [
          "pkt-0009-decontaminate-repos"
        ],
        "criticality": "required",
        "deliverables": [
          "inventory tool/report per repo: packets/out/worktrees",
          "migrate .codex/packets -> $CODEX_STATE/xtrl/packets/<repo>/...",
          "migrate .codex/out -> $CODEX_STATE/xtrl/out/<repo>/...",
          "worktree salvage/discard plan + manifests (hashes, mappings)"
        ],
        "depends_on": [
          "pkt-0007-root-preflight-enforce"
        ],
        "exit_criteria": [
          "migration manifest produced for each repo",
          "no data loss for selected salvage set",
          "migrated artifacts are addressable under CODEX_STATE"
        ],
        "id": "pkt-0008-legacy-codex-migration",
        "stage": "P0",
        "status": "planned",
        "title": "Migrate legacy repo-local .codex packets/out; triage worktrees",
        "type": "packet"
      },
      {
        "blocks": [
          "gate-is_implemented"
        ],
        "criticality": "required",
        "deliverables": [
          "delete repo-local .codex/ directories after migration",
          "update docs/scripts that refer to .codex defaults",
          "ensure CI/preflight blocks reintroduction"
        ],
        "depends_on": [
          "pkt-0008-legacy-codex-migration"
        ],
        "exit_criteria": [
          "find <repo> -name .codex -o -name .quint returns nothing",
          "root-preflight passes on all target repos"
        ],
        "id": "pkt-0009-decontaminate-repos",
        "stage": "P0",
        "status": "planned",
        "title": "Remove repo-local .codex/ from target repos; update references",
        "type": "packet"
      },
      {
        "blocks": [
          "pkt-0010-action-exec"
        ],
        "criticality": "supporting",
        "deliverables": [
          "pydantic models + validators",
          "typed parsing and error taxonomy",
          "unit tests covering invalid inputs"
        ],
        "depends_on": [],
        "exit_criteria": [
          "invalid contracts/packets rejected with stable reasoncodes",
          "tests pass in CI"
        ],
        "id": "pkt-0011-pydantic-models",
        "stage": "P1",
        "status": "planned",
        "title": "Pydantic authoritative models (Packet/Contract/ResolvedCtx/ComplianceReport)",
        "type": "packet"
      },
      {
        "blocks": [
          "gate-is_implemented"
        ],
        "criticality": "required",
        "deliverables": [
          "ACTION argv-only execution (no arbitrary shell)",
          "{VAR} allowlist substitution rules",
          "ctrl.exec gated on evidence.ok==true (when SSOT present)"
        ],
        "depends_on": [
          "pkt-0006-evidence-ssot",
          "pkt-0011-pydantic-models"
        ],
        "exit_criteria": [
          "unapproved ACTION denied with ACTION_NOT_AUTHORIZED reasoncode",
          "disallowed {VAR} denied deterministically",
          "exec blocked when evidence.ok != true"
        ],
        "id": "pkt-0010-action-exec",
        "stage": "P1",
        "status": "planned",
        "title": "ACTION-based exec + {VAR} allowlist substitution (deny-by-default)",
        "type": "packet"
      },
      {
        "blocks": [],
        "criticality": "gate",
        "deliverables": [
          "mechanical checks proving predicate fields true"
        ],
        "depends_on": [
          "pkt-0005-ctrl-surface",
          "pkt-0006-evidence-ssot",
          "pkt-0007-root-preflight-enforce",
          "pkt-0009-decontaminate-repos",
          "pkt-0010-action-exec"
        ],
        "exit_criteria": [
          "all prerequisite packets complete",
          "predicate must_be_true satisfied",
          "target repos contain no repo-local roots"
        ],
        "id": "gate-is_implemented",
        "stage": "GATE",
        "status": "planned",
        "title": "GATE: spec is_implemented == true",
        "type": "gate"
      }
    ],
    "predicate_to_packets": {
      "action_exec_enforced": {
        "closure_packets": [],
        "derived_p": "P1",
        "satisfied_by_packets": [
          "pkt-0010-action-exec"
        ]
      },
      "codex_home_config_only": {
        "closure_packets": [],
        "derived_p": "P0",
        "satisfied_by_packets": [
          "pkt-0002-xdg-split",
          "pkt-0003-consistency-sweep"
        ]
      },
      "ctrl_surface_stable": {
        "closure_packets": [
          "pkt-0004-render-install-surface"
        ],
        "derived_p": "P0",
        "satisfied_by_packets": [
          "pkt-0005-ctrl-surface"
        ]
      },
      "deny_repo_local_roots": {
        "closure_packets": [
          "pkt-0008-legacy-codex-migration"
        ],
        "derived_p": "P1",
        "satisfied_by_packets": [
          "pkt-0007-root-preflight-enforce",
          "pkt-0009-decontaminate-repos"
        ]
      },
      "evidence_ssot_present": {
        "closure_packets": [],
        "derived_p": "P1",
        "satisfied_by_packets": [
          "pkt-0006-evidence-ssot"
        ]
      },
      "state_written_under_codex_state": {
        "closure_packets": [],
        "derived_p": "P0",
        "satisfied_by_packets": [
          "pkt-0002-xdg-split",
          "pkt-0003-consistency-sweep"
        ]
      },
      "strict_clean_gate": {
        "closure_packets": [],
        "derived_p": "P1",
        "satisfied_by_packets": [
          "pkt-0007-root-preflight-enforce"
        ]
      },
      "target_repos_decontaminated": {
        "closure_packets": [
          "pkt-0007-root-preflight-enforce"
        ],
        "derived_p": "P0+P1",
        "satisfied_by_packets": [
          "pkt-0008-legacy-codex-migration",
          "pkt-0009-decontaminate-repos"
        ]
      },
      "vars_allowlist_enforced": {
        "closure_packets": [],
        "derived_p": "P1",
        "satisfied_by_packets": [
          "pkt-0010-action-exec"
        ]
      },
      "xdg_split_enforced": {
        "closure_packets": [
          "pkt-0003-consistency-sweep"
        ],
        "derived_p": "P0",
        "satisfied_by_packets": [
          "pkt-0002-xdg-split"
        ]
      }
    }
  },
  "generated_at": "2026-02-02T08:50:22-05:00",
  "packet_dag": {
    "backlog_fold_suggestion": {
      "GATE": [
        "gate-is_implemented"
      ],
      "P0": [
        "pkt-0003-consistency-sweep",
        "pkt-0004-render-install-surface",
        "pkt-0005-ctrl-surface",
        "pkt-0008-legacy-codex-migration",
        "pkt-0009-decontaminate-repos"
      ],
      "P1": [
        "pkt-0006-evidence-ssot",
        "pkt-0007-root-preflight-enforce",
        "pkt-0011-pydantic-models",
        "pkt-0010-action-exec"
      ]
    },
    "edges": [
      {
        "from": "pkt-0001-projectops-drr",
        "to": "pkt-0002-xdg-split"
      },
      {
        "from": "pkt-0002-xdg-split",
        "to": "pkt-0003-consistency-sweep"
      },
      {
        "from": "pkt-0003-consistency-sweep",
        "to": "pkt-0004-render-install-surface"
      },
      {
        "from": "pkt-0004-render-install-surface",
        "to": "pkt-0005-ctrl-surface"
      },
      {
        "from": "pkt-0005-ctrl-surface",
        "to": "pkt-0006-evidence-ssot"
      },
      {
        "from": "pkt-0005-ctrl-surface",
        "to": "pkt-0007-root-preflight-enforce"
      },
      {
        "from": "pkt-0007-root-preflight-enforce",
        "to": "pkt-0008-legacy-codex-migration"
      },
      {
        "from": "pkt-0008-legacy-codex-migration",
        "to": "pkt-0009-decontaminate-repos"
      },
      {
        "from": "pkt-0006-evidence-ssot",
        "to": "pkt-0010-action-exec"
      },
      {
        "from": "pkt-0011-pydantic-models",
        "to": "pkt-0010-action-exec"
      },
      {
        "from": "pkt-0005-ctrl-surface",
        "to": "gate-is_implemented"
      },
      {
        "from": "pkt-0006-evidence-ssot",
        "to": "gate-is_implemented"
      },
      {
        "from": "pkt-0007-root-preflight-enforce",
        "to": "gate-is_implemented"
      },
      {
        "from": "pkt-0009-decontaminate-repos",
        "to": "gate-is_implemented"
      },
      {
        "from": "pkt-0010-action-exec",
        "to": "gate-is_implemented"
      }
    ],
    "graph_version": "xtrl.packet_dag/v1",
    "nodes": [
      {
        "deliverables": [
          "docs/drr/DRR-0001-projectops-naming-paths.md"
        ],
        "exit_criteria": [
          "DRR committed on main",
          "DRR referenced from README or docs index (optional)"
        ],
        "id": "pkt-0001-projectops-drr",
        "stage": "P0",
        "status": "done",
        "title": "Lock ProjectOps decisions (DRR-0001)",
        "type": "packet"
      },
      {
        "deliverables": [
          "tools path resolution: codex_home vs codex_state",
          "repo-shipped wrappers + Justfile template",
          "docs: XDG layout",
          "smoke test asserting no state under CODEX_HOME"
        ],
        "exit_criteria": [
          "tests/smoke_xdg_paths.py passes",
          "state outputs default under CODEX_STATE/xtrl"
        ],
        "id": "pkt-0002-xdg-split",
        "stage": "P0",
        "status": "done",
        "title": "Enforce XDG split (CODEX_STATE owns runtime output)",
        "type": "packet"
      },
      {
        "deliverables": [
          "update skills-pack/** scripts to pass --codex-state and write state to CODEX_STATE",
          "update dot_config/codex/** snippets to reflect CODEX_STATE/CODEX_DATA",
          "mechanical grep/rg guard: deny executable refs to $CODEX_HOME/xtrl/(out|worktrees|packets)"
        ],
        "exit_criteria": [
          "rg finds no executable references to $CODEX_HOME/xtrl/(out|worktrees|packets)",
          "end-to-end smoke test uses --codex-state successfully"
        ],
        "id": "pkt-0003-consistency-sweep",
        "notes": [
          "Leave legacy mentions only in explicitly marked docs if unavoidable."
        ],
        "stage": "P0",
        "status": "planned",
        "title": "Sweep remaining CODEX_HOME-as-state refs (skills-pack/**, dot_config/**)",
        "type": "packet"
      },
      {
        "deliverables": [
          "install scripts produce stable PATH wrappers (recommended: ~/.local/bin)",
          "xtrl just render writes $CODEX_HOME/xtrl/Justfile deterministically",
          "mcp launcher watches $CODEX_HOME/xtrl and registers tools from generated Justfile"
        ],
        "exit_criteria": [
          "tools register under just-mcp from $CODEX_HOME/xtrl/Justfile",
          "commands run from any cwd with explicit repo_root targeting"
        ],
        "id": "pkt-0004-render-install-surface",
        "stage": "P0",
        "status": "planned",
        "title": "Verify install + render surfaces (MCP watch root stable)",
        "type": "packet"
      },
      {
        "deliverables": [
          "ctrl.help",
          "ctrl.list",
          "ctrl.doctor",
          "ctrl.paths",
          "ctrl.preflight",
          "ctrl.exec",
          "ctrl.check",
          "ctrl.evidence",
          "ctrl.promote (deny-by-default initially)"
        ],
        "exit_criteria": [
          "ctrl.* discoverable via MCP",
          "downstream callers (Yazi/MCP) can use ctrl.* only",
          "ctrl.preflight enforces strict gates (clean + forbidden roots)"
        ],
        "id": "pkt-0005-ctrl-surface",
        "stage": "P0",
        "status": "planned",
        "title": "Layer 1 public actuator surface: ctrl.*",
        "type": "packet"
      },
      {
        "deliverables": [
          "evidence.json schema/fields (ComplianceReport SSOT)",
          "OUT_DIR layout standard (XDG state rooted)",
          "required files: summary.md, commands.log",
          "ctrl.evidence generates and ctrl.check validates SSOT"
        ],
        "exit_criteria": [
          "ctrl.evidence always produces required files in OUT_DIR",
          "ctrl.check fails fast when required evidence missing or malformed"
        ],
        "id": "pkt-0006-evidence-ssot",
        "stage": "P1",
        "status": "planned",
        "title": "Evidence SSOT: ComplianceReport (evidence.json) + required outputs",
        "type": "packet"
      },
      {
        "deliverables": [
          "root-preflight scans tracked + untracked for .codex/.quint",
          "strict clean gate: git status --porcelain must be empty",
          "machine-checkable reasoncodes for denials"
        ],
        "exit_criteria": [
          "consistent denial reasoncodes emitted",
          "ctrl.preflight denies forbidden roots deterministically"
        ],
        "id": "pkt-0007-root-preflight-enforce",
        "stage": "P1",
        "status": "planned",
        "title": "Enforce root-preflight: deny repo-local roots + strict clean gate everywhere",
        "type": "packet"
      },
      {
        "deliverables": [
          "inventory tool/report per repo: packets/out/worktrees",
          "migrate .codex/packets -> $CODEX_STATE/xtrl/packets/<repo>/...",
          "migrate .codex/out -> $CODEX_STATE/xtrl/out/<repo>/...",
          "worktree salvage/discard plan + manifests (hashes, mappings)"
        ],
        "exit_criteria": [
          "migration manifest produced for each repo",
          "no data loss for selected salvage set",
          "migrated artifacts are addressable under CODEX_STATE"
        ],
        "id": "pkt-0008-legacy-codex-migration",
        "stage": "P0",
        "status": "planned",
        "title": "Migrate legacy repo-local .codex packets/out; triage worktrees",
        "type": "packet"
      },
      {
        "deliverables": [
          "delete repo-local .codex/ directories after migration",
          "update docs/scripts that refer to .codex defaults",
          "ensure CI/preflight blocks reintroduction"
        ],
        "exit_criteria": [
          "find <repo> -name .codex -o -name .quint returns nothing",
          "root-preflight passes on all target repos"
        ],
        "id": "pkt-0009-decontaminate-repos",
        "stage": "P0",
        "status": "planned",
        "title": "Remove repo-local .codex/ from target repos; update references",
        "type": "packet"
      },
      {
        "deliverables": [
          "pydantic models + validators",
          "typed parsing and error taxonomy",
          "unit tests covering invalid inputs"
        ],
        "exit_criteria": [
          "invalid contracts/packets rejected with stable reasoncodes",
          "tests pass in CI"
        ],
        "id": "pkt-0011-pydantic-models",
        "stage": "P1",
        "status": "planned",
        "title": "Pydantic authoritative models (Packet/Contract/ResolvedCtx/ComplianceReport)",
        "type": "packet"
      },
      {
        "deliverables": [
          "ACTION argv-only execution (no arbitrary shell)",
          "{VAR} allowlist substitution rules",
          "ctrl.exec gated on evidence.ok==true (when SSOT present)"
        ],
        "exit_criteria": [
          "unapproved ACTION denied with ACTION_NOT_AUTHORIZED reasoncode",
          "disallowed {VAR} denied deterministically",
          "exec blocked when evidence.ok != true"
        ],
        "id": "pkt-0010-action-exec",
        "stage": "P1",
        "status": "planned",
        "title": "ACTION-based exec + {VAR} allowlist substitution (deny-by-default)",
        "type": "packet"
      },
      {
        "deliverables": [
          "mechanical checks proving predicate fields true"
        ],
        "exit_criteria": [
          "all prerequisite packets complete",
          "predicate must_be_true satisfied",
          "target repos contain no repo-local roots"
        ],
        "id": "gate-is_implemented",
        "stage": "GATE",
        "status": "planned",
        "title": "GATE: spec is_implemented == true",
        "type": "gate"
      }
    ],
    "spec": {
      "is_implemented_predicate": {
        "must_be_true": [
          "xdg_split_enforced",
          "codex_home_config_only",
          "state_written_under_codex_state",
          "deny_repo_local_roots",
          "strict_clean_gate",
          "ctrl_surface_stable",
          "evidence_ssot_present",
          "action_exec_enforced",
          "vars_allowlist_enforced",
          "target_repos_decontaminated"
        ],
        "must_have_artifacts": [
          "DRR-0001 committed",
          "generated Justfile template in-repo",
          "install wrappers in-repo",
          "evidence schema + required outputs (summary.md, commands.log)",
          "root-preflight denial reasoncodes",
          "migration manifests for legacy .codex data"
        ]
      },
      "name": "xtrl-ops authoritative binding"
    },
    "topological_order": [
      "pkt-0001-projectops-drr",
      "pkt-0002-xdg-split",
      "pkt-0003-consistency-sweep",
      "pkt-0004-render-install-surface",
      "pkt-0005-ctrl-surface",
      "pkt-0006-evidence-ssot",
      "pkt-0007-root-preflight-enforce",
      "pkt-0008-legacy-codex-migration",
      "pkt-0009-decontaminate-repos",
      "pkt-0011-pydantic-models",
      "pkt-0010-action-exec",
      "gate-is_implemented"
    ]
  },
  "schema_version": "xtrl.consolidated/v1",
  "sources": [
    {
      "kind": "packet_dag_only",
      "path": "backlog.json",
      "sha256": "0ace8e7b9aea6b9acd58061fb1000f8e1c6b2a7977f89ed193340eaedfd1cd34"
    },
    {
      "kind": "consolidated_with_packet_dag",
      "path": "backlog1.json",
      "sha256": "2263538277ca2a7cedece8541518b1d1fc0036b10eb3d741573efc3d700d1465"
    }
  ],
  "ssot": {
    "canonical_blocks": [
      "packet_dag",
      "components",
      "derived_mappings"
    ],
    "document_id": "xtrl-ops-living-ssot",
    "last_updated": "2026-02-02"
  },
  "summary": {
    "counts": {
      "by_stage": {
        "GATE": 1,
        "P0": 7,
        "P1": 4
      },
      "by_stage_status": {
        "GATE": {
          "planned": 1
        },
        "P0": {
          "done": 2,
          "planned": 5
        },
        "P1": {
          "planned": 4
        }
      },
      "by_status": {
        "done": 2,
        "planned": 10
      },
      "packets_total": 12
    },
    "next_focus": {
      "definition_of_done": [
        "rg finds no executable references to $CODEX_HOME/xtrl/(out|worktrees|packets)",
        "end-to-end smoke test uses --codex-state successfully"
      ],
      "next_packet": "pkt-0003-consistency-sweep"
    }
  },
  "timezone": "America/Montreal",
  "validation": {
    "notes": [
      "backlog1.json fully subsumes backlog.json; packet_dag sections are byte-for-byte identical after JSON parsing (same nodes/edges/topological_order/backlog_fold_suggestion)."
    ],
    "packet_dag_identical_to_backlog_json": true
  }
}
```
