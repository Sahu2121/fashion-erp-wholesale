# FASHION ERP WHOLESALE — PHASE 53

## Sales Order / Reservation Orchestration

Phase 53 adds a non-destructive Sales Order layer around the existing Phase 42+ stock-reservation engine.

Included:
- Persistent sales order and sales order item tables.
- Automatic sales order numbering (`SO000001`, ...).
- Draft order creation and line-item management.
- Order confirmation validates every line before creating reservations.
- Confirmation creates one existing `stock_reservations` record per order line and does not reduce physical stock.
- Reservation linkage by sales order and line.
- Cancellation releases only OPEN reservations linked to that order.
- Close workflow for reserved orders.
- Party/status/order reporting with linked reservation details.
- Atomic confirmation semantics: insufficient stock prevents partial order reservation.
- Existing Phase 35–52 APIs/data preserved.

Tests: Phase 53 plus prior regression suite PASS.
