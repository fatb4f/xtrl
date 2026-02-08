# Exec Prompt — pkt-exec-0001-precontract-schema-examples

## Phase
P0.4

## Title
PreContract schema + examples (xtrl.pre_contract/v0.2)

## Dependencies
pkt-binding-0001-binding-ssot-schemas

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m tools.validate_schema control/spec/pre_contract.schema.json`
- `python -m tools.validate_schema control/spec/examples/pre_contract.example.json`
