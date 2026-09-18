# FASHION ERP WHOLESALE — PHASE 62

## Sales Dispatch / Delivery Workflow

Phase 61 remains intact. Phase 62 is additive and does not delete or overwrite existing Sales Order, Reservation, Invoice, Receivable, Return, Purchase or Inventory workflows.

### Added
- Sales Dispatch / Delivery Challan master linked to Sales Order.
- Dispatch number sequence `DC000001...`.
- Dispatch states: DRAFT → DISPATCHED → DELIVERED, with CANCELLED for open dispatches.
- Vehicle, transporter, LR number and delivery-address fields.
- Partial dispatch support in PCS and METER.
- Cumulative dispatch validation prevents dispatching more than the ordered quantity.
- Only confirmed/reserved/closed sales orders can be dispatched; draft/cancelled orders are blocked.
- DRAFT dispatches can be prepared before posting and require at least one item to post.
- Delivery completion is controlled: only DISPATCHED records can become DELIVERED.
- Dispatch reporting by Sales Order, Party and Status.
- Dispatch deliberately creates **no new stock movement**; invoice posting remains the stock-consumption source so stock is not deducted twice.

### Key APIs
- `ensure_sales_dispatch_tables(...)`
- `create_sales_dispatch(...)`
- `add_sales_dispatch_item(...)`
- `dispatch_summary(...)`
- `post_sales_dispatch(...)`
- `mark_sales_dispatch_delivered(...)`
- `cancel_sales_dispatch(...)`
- `sales_dispatch_report(...)`

### Validation
- `phase62_test.py` => PASS
- Phase 36–62 regression suite => PASS
