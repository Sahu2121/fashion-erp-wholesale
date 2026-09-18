# FASHION ERP WHOLESALE — PHASE 57

## Major workflow: Purchase Bill -> Supplier Payable -> Payment Allocation

Phase 56 remains intact. Phase 57 adds purchase billing and supplier payable integration without deleting or overwriting existing features.

### Added
- Purchase bill created from a received GRN/PO
- Automatic PB numbering
- Purchase bill line snapshot
- Supplier payable report with UNPAID/PARTIAL/PAID settlement status
- Existing payment allocation engine supports `bill_type='PURCHASE'`
- Active (non-voided) allocations reduce supplier outstanding
- Duplicate purchase bill prevention

### Test
`phase57_test.py` => PASS
All available Phase 35-57 regression tests => PASS
