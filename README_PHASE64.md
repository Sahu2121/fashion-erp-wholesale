# FASHION ERP WHOLESALE — PHASE 64

## Purchase Module Completion

Phase 64 is additive and preserves the Phase 63 base.

### Added
- Draft Purchase Order header editing.
- Draft Purchase Order line editing/removal with duplicate-line protection.
- Purchase Order summary report.
- Pending Purchase Order report including PARTIALLY_RECEIVED orders.
- Partial Purchase Order receiving / multi-GRN workflow.
- Received quantity validation against ordered PCS/METER.
- GRN receipt detail report.
- Partial receipt updates physical stock and stock movement ledger exactly once per receipt.
- Purchase Order status: CONFIRMED -> PARTIALLY_RECEIVED -> RECEIVED.

### APIs
- `update_purchase_order_header(...)`
- `update_purchase_order_item(...)`
- `remove_purchase_order_item(...)`
- `purchase_order_summary_report(...)`
- `pending_purchase_order_report(...)`
- `receive_purchase_order_partial(...)`
- `purchase_receipt_detail_report(...)`

### Validation
- `phase64_test.py` => PASS
- Phase 35–64 regression => PASS
