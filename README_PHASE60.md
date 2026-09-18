# FASHION ERP WHOLESALE — PHASE 60

## Inventory Valuation + Stock Aging / Dead Stock

Phase 59 remains intact. Phase 60 is additive and does not delete or overwrite existing ERP workflows or physical stock balances.

### Added
- Stock valuation report derived from the stock movement ledger.
- Weighted-average purchase/receipt rate per godown + product + size + color.
- Current stock value with PCS/METER-aware quantity handling.
- As-of-date valuation support.
- Inventory aging report based on the latest stock-in movement (purchase, opening, sales return, etc.).
- Configurable dead-stock threshold (default 90 days).
- Dead-stock count and dead-stock value summary.
- Aging buckets: 0–30, 31–60, 61–90, 91+ days.
- Corrected stock movement classification so SALES_RETURN counts as stock-in and PURCHASE_RETURN counts as stock-out in movement totals and reconciliation.

### Key APIs
- `stock_valuation_report(conn, ...)`
- `inventory_aging_report(conn, ...)`
- `stock_ageing_summary(conn, ...)`

### Safety
- Reporting/valuation layer does not mutate physical stock.
- Existing stock ledger, returns, sales, purchase, payment and invoice workflows are preserved.
- Returns are included correctly in inventory movement direction.

### Validation
- `phase60_test.py` => PASS
- Phase 58 regression => PASS
- Phase 59 regression => PASS
- Phase 36–59 regression suite => PASS
