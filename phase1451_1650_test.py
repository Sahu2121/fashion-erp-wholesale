import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
conn=sqlite3.connect(':memory:'); conn.row_factory=sqlite3.Row
# Minimal representative ERP tables so every mapped phase exercises its real logic.
for ddl in [
'CREATE TABLE sales_invoices(id INTEGER PRIMARY KEY, invoice_no TEXT, status TEXT, invoice_date TEXT, total REAL)',
'CREATE TABLE purchase_bills(id INTEGER PRIMARY KEY, bill_no TEXT, status TEXT, bill_date TEXT, total REAL)',
'CREATE TABLE godown_stock(id INTEGER PRIMARY KEY, qty REAL, updated_at TEXT)',
'CREATE TABLE journal_entries(id INTEGER PRIMARY KEY, entry_date TEXT, amount REAL)',
'CREATE TABLE gst_period_closures(id INTEGER PRIMARY KEY, status TEXT, closure_date TEXT)',
'CREATE TABLE accounts(id INTEGER PRIMARY KEY, name TEXT, balance REAL)',
'CREATE TABLE stock_transfers(id INTEGER PRIMARY KEY, status TEXT, transfer_date TEXT)',
'CREATE TABLE sales_orders(id INTEGER PRIMARY KEY, order_no TEXT, status TEXT, order_date TEXT)',
'CREATE TABLE role_permissions(id INTEGER PRIMARY KEY, role TEXT)',
'CREATE TABLE audit_log(id INTEGER PRIMARY KEY, created_at TEXT)',
'CREATE TABLE payment_register(id INTEGER PRIMARY KEY, amount REAL, payment_date TEXT)',
'CREATE TABLE audit_trail(id INTEGER PRIMARY KEY, created_at TEXT)',
'CREATE TABLE collection_followups(id INTEGER PRIMARY KEY, status TEXT, followup_date TEXT)',
'CREATE TABLE schema_version(id INTEGER PRIMARY KEY, version TEXT)',
'CREATE TABLE period_locks(id INTEGER PRIMARY KEY, status TEXT, lock_date TEXT)',
'CREATE TABLE stock_movements(id INTEGER PRIMARY KEY, qty REAL, movement_date TEXT)',
'CREATE TABLE hsn_master(id INTEGER PRIMARY KEY, hsn_code TEXT, description TEXT)']:
    conn.execute(ddl)
conn.commit()
res=app.phases_1451_1650_smoke(conn)
assert res['count']==200, res
assert res['ok'], [x for x in res['checks'] if not x['ok']][:5]
s=app.enterprise_release_snapshot_1650(conn)
assert s['status']=='READY', s
print('PHASE_1451_1650_TEST_PASS',res['count'],s['log_count'])
