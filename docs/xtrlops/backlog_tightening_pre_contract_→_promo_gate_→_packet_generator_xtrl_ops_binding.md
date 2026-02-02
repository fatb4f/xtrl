# Backlog Tightening: PreContract → PromoGate → PacketGenerator → Contract (xtrl-ops binding)

**Status:** Draft → Ready-to-implement

## Current on-disk shape (Backlog.md project)

```
.
├── archive/
├── completed/
├── decisions/
├── docs/
├── drafts/
├── milestones/
├── tasks/
└── config.yml
```

### Task file naming (current)
- `tasks/pkt-<component>-<nnnn>-<slug> - <slug>.md`
- Completed tasks move to `completed/`.

This is already a **tight** layout: the filename encodes a packet identity (component, sequence) and the directory encodes lifecycle.

---

## Objective

Introduce a strict chain:

**Task.md (human)** → **pre_contract.json (machine SSOT)** → **PromoGate (deny-fast)** → **packet_generator (materialize run-ready)** → **contract.json + exec-prompt.md (OUT_DIR)** → **ACTION-only execution**

This chain is constrained by **xtrl-ops_authoritative_binding**:
- runtime outputs live under `$CODEX_STATE/xtrl/...`
- `contract.json` must exist in OUT_DIR *before execution*
- ACTION-only (argv array) commands
- deny-fast for repo-local forbidden roots and other invariants

---

## Canonical objects

### 1) Task (Markdown)
- Your existing `tasks/*.md` and `completed/*.md`.
- Human-readable intent, rationale, acceptance criteria.

### 2) PreContract (JSON; SSOT for execution intent)
- Machine-checkable intent + constraints + actions.
- Lives **next to the task** in git.

### 3) GateDecision (JSON; deny-fast output)
- Result of PromoGate: `ALLOW` or `DENY` + reason codes.
- Written to OUT_DIR (not in repo) for audit.

### 4) Contract (JSON; run-ready)
- Materialized in OUT_DIR.
- Fully binding-compliant; contains only executable state.

### 5) Exec prompt (Markdown)
- Materialized in OUT_DIR.
- Human-facing summary and invocation instructions.

### 6) EvidenceCapsule (runtime outputs)
- Written under OUT_DIR in the binding-required layout.

---

## Default: where `pre_contract.json` lives

No reorg required.

For each task:
- `tasks/<task>.md`
- `tasks/<task>.pre_contract.json`

For completed tasks (recommended to keep for audit):
- `completed/<task>.md`
- `completed/<task>.pre_contract.json`

Optional later tightening:
- migrate to `tasks/<packet_id>/{task.md, pre_contract.json}` to avoid quoted filenames.

---

## PromoGate (deny-fast)

### Mandatory deny-fast checks
PromoGate **DENIES** if any are true:

**PreContract required fields**
- missing: `schema_version`, `packet_id`, `repo`, `base_ref`, `mode`, `budgets`, `constraints`, `actions`, `evidence.required_files`

**Mode + budgets**
- `mode` not in `{NORMAL, REPAIR, SAFE}`
- budgets missing or invalid: time/diff/iteration

**ACTION-only enforcement**
- `actions.*` not an argv-array (shell strings forbidden)

**Path control**
- `constraints.allowed_paths` empty
- `constraints.deny_repo_local_roots` not exactly `[".codex", ".quint"]`

**Diff budget**
- diff budget missing or malformed

**Base ref**
- base_ref missing (and later, exec-time mismatch should reasoncode)

### Gate outputs (always)
Write GateDecision to OUT_DIR:
- `$CODEX_STATE/xtrl/out/<repo>/<packet_id>/gate/decision.json`
- optional `$CODEX_STATE/xtrl/out/<repo>/<packet_id>/gate/explain.md`

---

## PacketGenerator (materialization)

### CLI shape (default)
- `xtrl packet generate <path/to/*.pre_contract.json>`

### Behavior
1. Load PreContract.
2. Run PromoGate.
   - If DENY: emit GateDecision, exit non-zero.
   - If ALLOW: emit GateDecision and materialize run-ready artifacts.

### Required materialization target (OUT_DIR)
Default:
- `OUT_DIR = $CODEX_STATE/xtrl/out/<repo>/<packet_id>`

On ALLOW, generator writes:
- `OUT_DIR/contract.json`
- `OUT_DIR/exec-prompt.md`
- `OUT_DIR/packet.json` (pointers: task path + precontract hash)

Optional pre-seed (consistent with binding):
- `OUT_DIR/evidence/plan.md`
- `OUT_DIR/evidence/decision.md`

---

## Example `pre_contract.json` (template)

```json
{
  "schema_version": "xtrl.pre_contract/v0.2",
  "packet_id": "pkt-exec-0001-enforce-action-only-execution",
  "repo": "xtrl",
  "component": "exec",
  "base_ref": "origin/main",

  "mode": "NORMAL",

  "budgets": {
    "time_minutes": 45,
    "diff_budget": { "max_files_changed": 20, "max_lines_changed": 600 },
    "iteration_budget": 2
  },

  "plan_card": {
    "who": "xtrl controller",
    "what": "enforce ACTION-only execution; deny arbitrary shell",
    "why": "prevent uncontrolled actuation; make runs auditable",
    "where": "xtrl repo (controller surface)",
    "when": "on ctrl.exec / xtrl exec",
    "how": "argv-only actions resolved from contract.json"
  },

  "constraints": {
    "clean_repo_required": true,
    "deny_repo_local_roots": [".codex", ".quint"],
    "allowed_paths": [
      "tools/**",
      "src/**",
      "docs/**",
      "tests/**",
      "pyproject.toml"
    ],
    "forbidden_paths": [
      ".git/**",
      "backlog/**"
    ],
    "forbidden_patterns": [
      "subprocess\\.run\\(.*shell\\s*=\\s*True",
      "os\\.system\\(",
      "eval\\(",
      "exec\\("
    ]
  },

  "actions": {
    "test": ["pytest", "-q"],
    "lint": ["ruff", "check", "."],
    "format": ["ruff", "format", "."]
  },

  "evidence": {
    "required_files": [
      "evidence/plan.md",
      "evidence/decision.md",
      "evidence/scope.json",
      "evidence/integrity.json",
      "evidence/tests.junit.xml",
      "evidence/regression.md",
      "commands.log",
      "summary.md",
      "packet.json",
      "contract.json",
      "exec-prompt.md"
    ]
  },

  "inputs": {
    "task_md_path": "tasks/pkt-exec-0001-enforce-action-only-execution - enforce-action-only-execution.md",
    "binding_ref": "docs/xtrl-ops_authoritative_binding.md"
  }
}
```

---

## Minimum `contract.json` shape (generator output)

```json
{
  "schema_version": "xtrl.contract/v0.2",
  "packet_id": "pkt-exec-0001-enforce-action-only-execution",
  "base_ref": "origin/main",
  "constraints": {
    "clean_repo_required": true,
    "deny_repo_local_roots": [".codex", ".quint"],
    "allowed_paths": ["tools/**", "src/**", "docs/**", "tests/**", "pyproject.toml"],
    "forbidden_paths": [".git/**", "backlog/**"],
    "diff_budget": { "max_files_changed": 20, "max_lines_changed": 600 },
    "forbidden_patterns": [
      "subprocess\\.run\\(.*shell\\s*=\\s*True",
      "os\\.system\\(",
      "eval\\(",
      "exec\\("
    ]
  },
  "actions": {
    "test": ["pytest", "-q"],
    "lint": ["ruff", "check", "."],
    "format": ["ruff", "format", "."]
  },
  "evidence": {
    "required_files": [
      "evidence/plan.md",
      "evidence/decision.md",
      "evidence/scope.json",
      "evidence/integrity.json",
      "evidence/tests.junit.xml",
      "evidence/regression.md",
      "commands.log",
      "summary.md",
      "packet.json",
      "contract.json",
      "exec-prompt.md"
    ]
  }
}
```

---

## Immediate tightening rules

1. **PreContract is the only promotable input** to Contract generation.
2. Any PreContract change requires re-running PromoGate and re-materializing Contract in OUT_DIR.
3. Execution runs only against `OUT_DIR/contract.json` (never directly from git).
4. Denials always emit GateDecision artifacts.

---

## Implementation checklist (minimal)

- [ ] Add `*.pre_contract.json` siblings for each `tasks/*.md` (starting with exec/evidence packets).
- [ ] Implement `xtrl packet generate`:
  - [ ] load pre_contract
  - [ ] promo_gate (deny-fast)
  - [ ] emit gate decision to OUT_DIR
  - [ ] on allow: emit `contract.json`, `exec-prompt.md`, `packet.json`
- [ ] Update actuator path: `xtrl exec` only consumes OUT_DIR/contract.json

---

## Optional next tightening (filesystem)

- Replace quoted filenames by directory-per-packet:
  - `tasks/<packet_id>/task.md`
  - `tasks/<packet_id>/pre_contract.json`
  - `completed/<packet_id>/...`

This reduces filesystem quoting risk and makes packet identity purely structural.

