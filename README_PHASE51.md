# FASHION ERP WHOLESALE — PHASE 51

## Notification Dispatch Lease / Stale Claim Recovery

Phase 51 adds a safe worker lease layer over the Phase 50 notification outbox.

Included:
- Worker claim tokens and lease expiry metadata.
- Lease-aware bounded notification claiming; already leased notifications are not claimed again until their lease expires.
- Stale lease recovery back to `PENDING` without deleting notification history.
- Token-validated completion so a different worker cannot complete another worker's claim.
- Successful completion clears the lease and marks `SENT`.
- Failed completion clears the lease, records the error and timestamp, and marks `FAILED` for retry.
- Additive schema migration works with older Phase 49/50 databases.
- Existing stock, reservations, payments, bills, SLA issues and notification records remain intact.
- Existing Phase 35–50 APIs/data preserved.

Tests: `phase51_test.py` plus all Phase 35–50 regression tests PASS.
