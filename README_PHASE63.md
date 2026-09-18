# FASHION ERP WHOLESALE — PHASE 63

## Sales Credit Note / Purchase Debit Note

Phase 63 is additive. Existing Sales, Purchase, Inventory, Return, Invoice, Payment and Reservation workflows remain intact.

### Added
- Sales Return -> Credit Note (`CN000001...`)
- Purchase Return -> Debit Note (`DN000001...`)
- One note per posted return; duplicate note creation is blocked.
- Note links preserve source return + source invoice/bill references.
- Taxable amount and GST split are derived from source line GST rate where available.
- Credit/Debit Note reporting and compact summary.
- Notes do not create another stock movement; stock remains controlled by the return workflow.
- Notes do not yet mutate receivable/payable balances; that accounting posting layer is reserved for the Accounting phase.

### Key APIs
- `ensure_return_note_tables(...)`
- `create_sales_credit_note(...)`
- `create_purchase_debit_note(...)`
- `sales_credit_note_report(...)`
- `purchase_debit_note_report(...)`
- `return_note_summary_report(...)`

### Validation
- `phase63_test.py` => PASS
