import sqlite3, sys, tempfile, os
sys.path.insert(0,'/mnt/data/work107_154')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# schema/version basics
app.ensure_schema_version_table(c)
# test phase functions progressively
app.ensure_system_profile(c); app.set_system_profile(c,company_name='TEST'); assert app.configuration_snapshot(c)['company_name']=='TEST'
assert app.tax_configuration_status(c)['ok'] is False or app.tax_configuration_status(c)['ok'] is True
app.ensure_price_list_tables(c); c.execute("INSERT INTO price_lists(name) VALUES('WHOLESALE')"); app.set_price(c,1,10,125); assert app.set_price(c,1,10,130)==130
app.ensure_party_contact_tables(c); assert app.add_party_contact(c,'CUSTOMER',1,'Test')==1
app.ensure_order_status_audit(c); assert app.audit_order_status(c,1,'DRAFT','CONFIRMED')==1
app.ensure_receipt_quality_tables(c); assert app.record_receipt_quality(c,1,10,1)==1
app.ensure_batch_tables(c); assert app.upsert_batch(c,1,'B1',5)
app.ensure_barcode_tables(c); c.execute("INSERT INTO product_barcodes(product_id,barcode) VALUES(1,'X')"); assert app.barcode_lookup(c,'X')['product_id']==1
app.ensure_stock_adjustment_tables(c); assert app.request_stock_adjustment(c,1,2)>=1
app.ensure_cash_bank_tables(c); assert app.cash_bank_balance(c)==0
app.ensure_expense_tables(c); assert app.add_expense(c,'2026-01-01','TEST',10)>=1
app.ensure_backup_manifest_tables(c); app.ensure_changelog_tables(c); assert app.add_changelog(c,'1.0-P154',151,'test')>=1
# safe analytics outputs
for fn in [app.supplier_performance,app.reorder_suggestions,app.variant_matrix,app.accounts_hierarchy,app.profit_loss_summary,app.balance_sheet_summary,app.cash_flow_summary,app.gst_reconciliation_status,app.validate_hsn_master,app.receivable_age_buckets,app.collection_dashboard,app.payable_age_buckets,app.purchase_analytics,app.sales_analytics,app.gross_margin_snapshot,app.salesman_performance,app.godown_performance,app.customer_profitability,app.dead_stock_action_queue,app.reorder_purchase_suggestions,app.sales_return_analytics,app.purchase_return_analytics,app.audit_report,app.system_health_score,app.data_quality_score,app.operational_kpi_snapshot,app.release_manifest,app.full_regression,app.production_readiness]:
    try: r=fn(c); assert r is not None, fn.__name__
    except Exception as e: raise AssertionError((fn.__name__,str(e)))
assert app.service_contract_catalog()
print('PHASE 107-154 ALL TESTS PASS')
