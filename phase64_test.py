import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT)"); c.execute("INSERT INTO products VALUES(101,'Shirt')"); c.execute("INSERT INTO products VALUES(102,'Trouser')"); c.commit()
po=app.create_purchase_order(c,'Supplier A','2026-09-18',gid)
a=app.add_purchase_order_item(c,po['id'],101,'L','Blue',10,0,100); a= c.execute('SELECT * FROM purchase_order_items WHERE purchase_order_id=? AND product_id=101',(po['id'],)).fetchone()
b=app.add_purchase_order_item(c,po['id'],102,'M','Black',5,0,200); b=c.execute('SELECT * FROM purchase_order_items WHERE purchase_order_id=? AND product_id=102',(po['id'],)).fetchone()
app.update_purchase_order_header(c,po['id'],remark='Urgent')
app.update_purchase_order_item(c,a['id'],pcs=12)
app.remove_purchase_order_item(c,b['id'])
# re-add second line for receipt test
b=app.add_purchase_order_item(c,po['id'],102,'M','Black',5,0,200); b=c.execute('SELECT * FROM purchase_order_items WHERE purchase_order_id=? AND product_id=102',(po['id'],)).fetchone()
app.confirm_purchase_order(c,po['id'])
r1=app.receive_purchase_order_partial(c,po['id'],[{'purchase_order_item_id':a['id'],'pcs':5,'meter':0}],'2026-09-18','T')
assert r1['status']=='PARTIALLY_RECEIVED'
r2=app.receive_purchase_order_partial(c,po['id'],[{'purchase_order_item_id':a['id'],'pcs':7,'meter':0},{'purchase_order_item_id':b['id'],'pcs':5,'meter':0}],'2026-09-18','T')
assert r2['status']=='RECEIVED'
try: app.receive_purchase_order_partial(c,po['id'],[{'purchase_order_item_id':a['id'],'pcs':1,'meter':0}])
except ValueError: pass
else: raise AssertionError('Over receipt must be rejected')
rep=app.purchase_receipt_detail_report(c,purchase_order_id=po['id'])
assert rep['count']==2
stock=c.execute("SELECT pcs FROM godown_stock WHERE godown_id=? AND product_id=?",(gid,101)).fetchone()[0]
assert stock==12
print('PHASE 64 TESTS PASS')
