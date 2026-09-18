# FASHION ERP WHOLESALE — PHASE 48

## Reservation Issue SLA / Escalation Control

Phase 48 adds a non-destructive SLA and escalation layer over the Phase 47 reservation conflict-resolution queue.

Included:
- Safe migration of SLA metadata onto `stock_reservation_issues`.
- Severity-based default priority and acknowledgement/resolution SLA windows.
- Per-issue SLA override support.
- SLA due timestamps and overdue indicators.
- Escalation of overdue OPEN/ACKNOWLEDGED issues with escalation level, timestamp and remark.
- Idempotent escalation (an issue is not repeatedly escalated to the same/lower level).
- SLA report filters by issue, status and priority; overdue-only reporting.
- No mutation of stock, reservations, payments, bills or original reconciliation findings.
- Existing Phase 35–47 APIs/data preserved.
