import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT)"); c.execute("INSERT INTO products VALUES(1,'Shirt')"); c.commit()
po=app.create_purchase_order(c,'Supplier A','2026-09-18',gid)
it=app.add_purchase_order_item(c,po['id'],1,'L','Blue',10,0,100)
app.confirm_purchase_order(c,po['id'])
app.receive_purchase_order(c,po['id'],'2026-09-18','TEST')
b=app.create_purchase_bill_from_grn(c,po['id'],'2026-09-18','2026-10-18')
bid=b['items'][0]['id']
assert app.purchase_bill_settlement(c,bid)['status']=='UNPAID'
app.update_purchase_bill(c,bid,due_date='2026-10-20',amount=1000)
res=app.make_supplier_payment(c,bid,400,'2026-09-18','SP000001')
assert res['bill']['status']=='PARTIAL' and res['bill']['outstanding']==600
res=app.make_supplier_payment(c,bid,600,'2026-09-19','SP000002')
assert res['bill']['status']=='PAID' and res['bill']['outstanding']==0
try: app.make_supplier_payment(c,bid,1,'2026-09-20','SP000003')
except ValueError: pass
else: raise AssertionError('Overpayment must be rejected')
pay=app.create_payment(c,'PAYMENT','SP000004','2026-09-20','Supplier A',500)
# create another bill for allocation test
po2=app.create_purchase_order(c,'Supplier A','2026-09-18',gid); app.add_purchase_order_item(c,po2['id'],1,'M','Red',5,0,100); app.confirm_purchase_order(c,po2['id']); app.receive_purchase_order(c,po2['id'],'2026-09-18','TEST'); b2=app.create_purchase_bill_from_grn(c,po2['id'],'2026-09-18','2026-10-18'); bid2=b2['items'][0]['id']
app.allocate_existing_payment_to_purchase_bill(c,pay,bid2,500)
assert app.purchase_bill_settlement(c,bid2)['status']=='PAID'
s=app.supplier_payable_summary(c,'Supplier A','2026-09-20')
assert s['total_outstanding']==0
print('PHASE 65 TESTS PASS')
