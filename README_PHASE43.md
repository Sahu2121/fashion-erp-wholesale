# FASHION ERP WHOLESALE — PHASE 43

## Stock Reservation Fulfillment / Partial Release & Audit

Phase 43 continues Phase 42 non-destructively and adds a fulfillment event layer.

Included:
- Partial fulfillment of OPEN stock reservations.
- Partial release of OPEN reservations without changing physical stock.
- Automatic transition to CONSUMED or RELEASED when the remaining reservation quantity reaches zero.
- Immutable fulfillment/release event trail in `stock_reservation_events`.
- Reservation fulfillment status with reserved, consumed, released and remaining PCS/METER quantities.
- Event report filtered by reservation and event type.
- Existing Phase 35–42 APIs and data preserved.
- Tests: Phase 35–43 all pass.
