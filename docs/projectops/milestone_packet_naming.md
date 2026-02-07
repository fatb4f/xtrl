# Milestone + Packet Naming Standard (AFT)

This standard defines a layerable naming system that maps to the plant, schema, and directory structure.

## Format

```
<AREA>.<FUNCTION>.<TARGET> — <packet_id>
```

- **AREA** = plant layer / subsystem
- **FUNCTION** = action/intent (verb or verb+noun)
- **TARGET** = behavior or artifact focus

### Examples

- `runtime.enforce.argv_only — pkt-loop-0003-argv-only-actions`
- `state.emit.evidencecapsule — pkt-compat-0003-evidencecapsule-v0-2-emitter-compat`
- `src.snapshot.ast — pkt-src-0002-snapshots-ast`

## AREA taxonomy (maps to repo structure)

- `runtime` — execution loop / runner / gates
- `state` — out/, worktrees/, ledger/latest
- `contract` — pre_contract / contract / exec-prompt
- `evidence` — EvidenceCapsule outputs + integrity
- `src` — src/ conventions, snapshots, validation
- `backlog` — backlog sync + queue
- `skills` — skills-pack + tool registry
- `schema` — SSOT schemas + registry
- `promote` — patch/promotion gate
- `observability` — telemetry, reports, fuzz

## FUNCTION taxonomy (short, consistent verbs)

- `seed`
- `emit`
- `validate`
- `enforce`
- `snapshot`
- `describe`
- `replay`
- `fuzz`
- `promote`
- `index`
- `sync`

## TARGET taxonomy (behavioral or structural)

- `argv_only`
- `evidencecapsule`
- `gate_decision`
- `ledger_latest`
- `src_conventions`
- `dep_graph`
- `api_surface`
- `module_manifest`
- `work_queue`
- `replay_report`
- `mutation_report`

## Conventional Commit alignment (optional)

```
feat(runtime): enforce argv_only (pkt-loop-0003)
fix(evidence): correct tests.junit.xml handling (pkt-compat-0003)
docs(schema): add src_snapshot_canonicalization spec
```

## Recommended usage

- **Milestones**: use the AFT triple in the title or description.
- **Packets**: map each packet to exactly one AFT triple.
- **Schemas**: keep TARGET names aligned with schema artifacts when possible.

## Non-goals

- Enforcing AFT in git branch names (not required).
- Overloading AFT with team or priority metadata (use labels instead).
