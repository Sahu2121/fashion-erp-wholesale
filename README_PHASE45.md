# FASHION ERP WHOLESALE — PHASE 45

## Stock Reservation Utilization / Commitment Dashboard

Phase 45 continues Phase 44 non-destructively and adds read-only management reporting over the existing reservation and immutable event trail.

Included:
- Reservation commitment totals from original reservation quantities.
- Consumed and released PCS/METER totals derived from reservation events.
- Current OPEN reserved quantities after partial fulfillment/release/expiry events.
- Consumption and release percentages.
- Optional filters: godown, product, size, color, party, status and reference number.
- Scoped unreserved physical stock (physical stock minus currently OPEN reserved stock) when godown/product context is supplied.
- No reservation or physical-stock mutation; existing Phase 42–44 APIs/data remain intact.
- Phase 35–45 regression tests pass.
