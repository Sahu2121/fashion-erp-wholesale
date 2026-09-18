# FASHION ERP WHOLESALE — PHASE 65

## Purchase Bill / Supplier Payable Completion

Phase 65 is additive and preserves Phase 64 and earlier workflows.

### Added
- Purchase bill settlement/status helper.
- Supplier payment creation and atomic allocation against purchase bills.
- Existing payment allocation to purchase bills with party and balance validation.
- Purchase bill edit for fully unpaid bills only.
- Supplier payable summary with open/overdue counts and amounts.
- Payment over-allocation and bill overpayment protection.
- Supplier payment uses the existing payment register/allocation infrastructure.

### APIs
- `update_purchase_bill(...)`
- `purchase_bill_settlement(...)`
- `make_supplier_payment(...)`
- `allocate_existing_payment_to_purchase_bill(...)`
- `supplier_payable_summary(...)`

### Validation
- `phase65_test.py` => PASS
- Phase 36–64 regression => PASS
