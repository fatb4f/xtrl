# Exec Prompt — pkt-binding-0001-binding-ssot-schemas

## Phase
P0.4

## Title
Binding SSOT schemas + seed instances

## Dependencies
(none)

## Contract
- Use `contract.json` as the sole execution contract.
- Execute argv arrays only (no shell strings).
- Emit required evidence files in OUT_DIR.

## Actions
- `python -m tools.validate_schema control/spec/binding/plant_spec.json`
- `python -m tools.validate_schema control/spec/binding/ruleset.json`
