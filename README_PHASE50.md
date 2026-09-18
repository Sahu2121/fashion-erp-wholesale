# FASHION ERP WHOLESALE — PHASE 50

## Notification Outbox Dispatch / Retry Control

Phase 50 adds a safe worker-facing dispatch/retry layer over the Phase 49 notification outbox.

Included:
- Additive attempt-count and worker claim metadata.
- Claim pending/failed notifications in bounded batches.
- Failed notification retry back to PENDING.
- Dispatch monitoring/report with status, channel and minimum-attempt filters.
- SENT/FAILED audit remains intact; notifications are never deleted.
- No external messages are sent by this layer; a future delivery adapter/worker can consume claimed records.
- Existing stock, reservations, payments, bills and issue/SLA data remain untouched.
- Existing Phase 35–49 APIs/data preserved.

Tests: `phase50_test.py` plus all Phase 35–49 regression tests PASS.
