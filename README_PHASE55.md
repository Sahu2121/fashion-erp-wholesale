# FASHION ERP WHOLESALE — PHASE 55

## Sales Invoice → Receivable / Payment Integration

Additive integration layer over Phase 54.

- Invoice settlement status: UNPAID / PARTIAL / PAID
- Receipt creation and direct allocation to posted sales invoices
- Existing payment allocation to invoices with party and balance validation
- Active (non-voided) allocations only for settlement calculations
- Receivable report with invoice total, paid total and outstanding total
- Existing payment, invoice, reservation and ledger APIs preserved
- No external payment gateway is called automatically

## Tests
`phase55_test.py` — PASS
Phase 54 regression test — PASS
