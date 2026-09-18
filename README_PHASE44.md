# FASHION ERP WHOLESALE — PHASE 44

## Stock Reservation Expiry / Lifecycle Control

Phase 44 continues Phase 43 non-destructively and adds reservation expiry metadata and automatic release.

Included:
- Optional expiry date on new reservations.
- Safe migration adds `expiry_date` and `expired_at` columns without deleting existing records.
- Automatic expiry of OPEN reservations whose expiry date is due.
- Expiry releases only the remaining reserved PCS/METER via the existing immutable event trail.
- New `EXPIRED` lifecycle status; existing OPEN/RELEASED/CONSUMED records remain valid.
- Expiry report with due-date filtering.
- Corrected reserved-stock availability to subtract prior partial CONSUME/RELEASE events, preventing over-reservation after Phase 43 partial fulfillment.
- Existing Phase 35–43 APIs/data preserved.
- Phase 44 tests pass.
