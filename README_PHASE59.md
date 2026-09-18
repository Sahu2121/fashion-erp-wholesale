# FASHION ERP WHOLESALE — PHASE 59

## Inventory Returns / Stock Correction Workflow

Phase 58 remains intact. Phase 59 adds an additive inventory-return layer without deleting or overwriting existing records or workflows.

### Added
- Sales Return register and item-level return records linked to posted Sales Invoices.
- Sales Return stock-in to the invoice godown with immutable `SALES_RETURN` movement entries.
- Purchase Return register and item-level return records linked to Purchase Bills.
- Purchase Return stock-out from the Purchase Order godown with immutable `PURCHASE_RETURN` movement entries.
- Partial returns supported; cumulative return quantity cannot exceed source document quantity.
- Purchase returns are blocked when physical stock is insufficient.
- Sales/Purchase return reports with PCS, METER and value totals.
- Return document numbering (`SR000001...`, `PR000001...`).
- Inventory-side correction is separated from future financial credit/debit-note posting.

### Key APIs
- `ensure_inventory_return_tables(conn)`
- `create_sales_return(conn, invoice_id, items, ...)`
- `sales_return_report(conn, ...)`
- `create_purchase_return(conn, bill_id, items, ...)`
- `purchase_return_report(conn, ...)`

### Validation
- `phase59_test.py` => PASS
- Phase 58 regression => PASS
- All available Phase 36–59 regression tests => PASS

Existing features were preserved; this phase is additive.
