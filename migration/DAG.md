# Migration DAG

```
ReasonCodes (SSOT)
  ├─ Gate decision bundle (SSOT)
  ├─ helper_created schema
  ├─ Ledger/latest schemas
  └─ Phase E snapshot schemas
        └─ xtrl alignment + schema pin (depends on all SSOT)
```

Notes:
- Gate decision bundle unlocks Phase B/C/D correctness.
- helper_created / ledger / snapshots can proceed once reason codes are fixed.
- xtrl alignment is last to avoid churn.
