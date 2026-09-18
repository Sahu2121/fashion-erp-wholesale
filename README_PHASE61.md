# FASHION ERP WHOLESALE — PHASE 61

## Sales Module Completion / Sales Order Control

Phase 60 remains intact. Phase 61 is additive and does not delete or overwrite existing Sales, Inventory, Returns, Purchase, Payment or Invoice workflows.

### Added
- Safe amendment of DRAFT sales-order header (party/date/godown/remark).
- Safe amendment of DRAFT sales-order line (product, size, color, PCS, METER, rate, remark).
- Safe removal of DRAFT sales-order lines.
- Confirmed/reserved/closed/cancelled orders are protected from draft edits.
- Compact Sales Order Summary report with status counts and PCS/METER/value totals.
- Pending Sales Order report for operational follow-up.
- Existing reservation, invoice posting, stock consumption, receivable and return flows are unchanged.

### Key APIs
- `update_sales_order_header(...)`
- `update_sales_order_item(...)`
- `remove_sales_order_item(...)`
- `sales_order_summary_report(...)`
- `pending_sales_order_report(...)`

### Validation
- `phase61_test.py` => PASS
- Phase 53/54/58/59/60 regression => PASS
- Existing phase 36–60 regression suite => PASS
