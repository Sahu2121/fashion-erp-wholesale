# FASHION ERP WHOLESALE — PHASE 58

## Complete Inventory Control / Stock Ledger

Phase 57 remains intact. Phase 58 adds an additive inventory-control layer without deleting or overwriting existing data or workflows.

### Added
- `stock_movements` immutable audit ledger for inventory movements.
- Movement numbering (`SM000001...`) and searchable movement report.
- Live stock balance report across godowns, product, size and color.
- Controlled stock adjustment API with negative-stock protection.
- Opening-balance seeding for legacy `godown_stock` rows; idempotent and non-destructive.
- Inventory reconciliation report comparing live physical stock with the Phase-58 movement ledger.
- Existing purchase receipt stock-in, sales invoice stock-consumption and godown transfer flows now write corresponding movement entries when the Phase-58 layer is loaded.
- Existing Phase 35-57 features/tests remain unchanged and pass regression testing.

### Key APIs
- `ensure_stock_movement_table(conn)`
- `stock_movement_report(...)`
- `stock_balance_report(...)`
- `set_stock_adjustment(...)`
- `seed_stock_movement_opening(...)`
- `inventory_reconciliation_report(...)`

### Validation
- `phase58_test.py` => PASS
- All available Phase 35-58 regression tests => PASS
