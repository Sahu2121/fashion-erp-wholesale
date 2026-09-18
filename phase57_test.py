import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')")
gid=c.execute('SELECT id FROM godowns').fetchone()[0]
po=app.create_purchase_order(c,'SUP-1','2026-09-18',gid); app.add_purchase_order_item(c,po['id'],101,'M','Blue',25,0,100); app.confirm_purchase_order(c,po['id']); app.receive_purchase_order(c,po['id'])
b=app.create_purchase_bill_from_grn(c,po['id'],'2026-09-18','2026-10-18'); assert b['items'][0]['status']=='UNPAID'
app.create_payment(c,'PAYMENT','P001','2026-09-20','SUP-1',1500)
pid=c.execute("SELECT id FROM payment_register ORDER BY id DESC LIMIT 1").fetchone()[0]
app.allocate_payment(c,pid,'PAYMENT','P001','SUP-1','PURCHASE',b['items'][0]['id'],b['items'][0]['bill_no'],500)
r=app.supplier_payable_report(c,'SUP-1'); assert r['outstanding']==2000 and r['items'][0]['settlement_status']=='PARTIAL'
print('PHASE 57 TESTS PASS')
