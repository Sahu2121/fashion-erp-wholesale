import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,101,'L','Blue',100,200)); c.commit()
app.ensure_sales_order_tables(c); app.ensure_stock_reservation_table(c); app.ensure_sales_invoice_tables(c)
o=app.create_sales_order(c,'ABC','2026-09-18',gid); app.add_sales_order_item(c,o['id'],101,'L','Blue',10,0,100); app.confirm_sales_order(c,o['id']); inv=app.post_sales_order_invoice(c,o['id'],invoice_date='2026-09-18',gst_rate=18,intra_state=True)
s=app.sales_invoice_settlement(c,inv['id']); assert s['status']=='UNPAID' and s['outstanding']==1180
r=app.receive_invoice_payment(c,inv['id'],500,payment_date='2026-09-20',payment_no='RCPT1'); assert r['invoice']['status']=='PARTIAL' and r['invoice']['outstanding']==680
r2=app.receive_invoice_payment(c,inv['id'],680,payment_date='2026-09-21',payment_no='RCPT2'); assert r2['invoice']['status']=='PAID' and r2['invoice']['outstanding']==0
# void first allocation and verify it reopens invoice
alloc=c.execute("SELECT id FROM payment_allocations WHERE bill_id=? ORDER BY id LIMIT 1",(inv['id'],)).fetchone()[0]; app.void_payment_allocation(c,alloc,'u','correction'); assert app.sales_invoice_settlement(c,inv['id'])['outstanding']==500
# existing payment allocation can fill the reopened balance
pid=c.execute("SELECT id FROM payment_register WHERE payment_no='RCPT2'").fetchone()[0]
try: app.allocate_existing_payment_to_invoice(c,pid,inv['id'],500)
except ValueError: pass
else: raise AssertionError('Already fully allocated payment must not be reused')
print('PHASE 55 TESTS PASS')
