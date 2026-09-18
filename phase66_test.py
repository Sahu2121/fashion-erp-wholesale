import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT)"); c.execute("INSERT INTO products VALUES(1,'Shirt')"); c.commit()
po=app.create_purchase_order(c,'Supplier A','2026-09-18',gid)
app.add_purchase_order_item(c,po['id'],1,'L','Blue',10,0,100)
app.confirm_purchase_order(c,po['id']); app.receive_purchase_order(c,po['id'],'2026-09-18','TEST')
b=app.create_purchase_bill_from_grn(c,po['id'],'2026-09-18','2026-10-18'); bid=b['items'][0]['id']
bill_item_id=b['items'][0]['items'][0]['id']
assert app.purchase_bill_settlement(c,bid)['outstanding']==1000
r=app.create_purchase_return(c,bid,[{'bill_item_id':bill_item_id,'pcs':2,'meter':0}],'2026-09-18','Damaged')
dn=app.create_purchase_debit_note(c,r['id'],'2026-09-18')
sett=app.purchase_bill_settlement(c,bid)
assert dn['total_amount']==200.0
assert sett['debit_notes']==200.0 and sett['outstanding']==800.0 and sett['status']=='PARTIAL'
app.make_supplier_payment(c,bid,700,'2026-09-18','SP66')
sett=app.purchase_bill_settlement(c,bid)
assert sett['outstanding']==100.0
try: app.make_supplier_payment(c,bid,101,'2026-09-18','OVER')
except ValueError: pass
else: raise AssertionError('Payment must respect debit-note-adjusted payable')
app.make_supplier_payment(c,bid,100,'2026-09-19','SP67')
sett=app.purchase_bill_settlement(c,bid)
assert sett['status']=='PAID' and sett['outstanding']==0 and sett['supplier_credit']==0
r2=app.create_purchase_return(c,bid,[{'bill_item_id':bill_item_id,'pcs':1,'meter':0}],'2026-09-19','Extra return')
dn2=app.create_purchase_debit_note(c,r2['id'],'2026-09-19')
sett=app.purchase_bill_settlement(c,bid)
assert sett['outstanding']==0 and sett['supplier_credit']==100.0
summary=app.purchase_return_payable_summary(c,supplier='Supplier A')
assert summary['debit_note_count']==2 and summary['debit_note_value']==300.0
print('PHASE 66 TESTS PASS')
