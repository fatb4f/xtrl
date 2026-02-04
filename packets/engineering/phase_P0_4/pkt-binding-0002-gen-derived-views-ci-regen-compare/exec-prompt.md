# Exec Prompt — pkt-binding-0002-gen-derived-views-ci-regen-compare

## Phase
P0.4

## Title
Generate derived binding views + CI regen-and-compare

## Dependencies
pkt-binding-0001-binding-ssot-schemas

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python tools/gen_binding_views.py`
- `python tools/ci_regen_compare.py --paths control/plant/binding_dag.json control/plant/binding_dag.mmd`
