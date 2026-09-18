# FASHION ERP WHOLESALE — PHASE 49

## Reservation Issue SLA Notification Outbox

Phase 49 adds a non-destructive notification/outbox layer over the Phase 48 SLA/escalation workflow.

Included:
- Persistent notification outbox for overdue reservation issues.
- Idempotent notifications per issue/channel/event type.
- ACK SLA overdue and resolution SLA overdue event types.
- Priority-aware notification records.
- IN_APP/default channel plus arbitrary adapter channels.
- PENDING / SENT / FAILED notification lifecycle.
- Delivery timestamp and failure error audit.
- No external messages are sent by this layer; adapters/workers can consume the outbox.
- Existing stock, reservations, payments, bills and issue findings remain untouched.
- Existing Phase 35–48 APIs/data preserved.
