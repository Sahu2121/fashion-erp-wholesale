import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT)"); c.execute("INSERT INTO products VALUES(101,'Shirt')"); c.commit()
o=app.create_sales_order(c,'ABC Traders','2026-09-18',gid)
i=app.add_sales_order_item(c,o['id'],101,'L','Blue',10,2,100)
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,101,'L','Blue',20,5)); c.commit()
app.confirm_sales_order(c,o['id'])
d=app.create_sales_dispatch(c,o['id'],'2026-09-18',vehicle_no='UP32AB1234',transporter='Fast Transport')
app.add_sales_dispatch_item(c,d['id'],i['id'],pcs=6,meter=1)
app.post_sales_dispatch(c,d['id'],'RAJESH')
# Second dispatch can consume remaining, but cannot exceed ordered.
d2=app.create_sales_dispatch(c,o['id'],'2026-09-18'); app.add_sales_dispatch_item(c,d2['id'],i['id'],pcs=4,meter=1); app.post_sales_dispatch(c,d2['id'])
try:
    d3=app.create_sales_dispatch(c,o['id'],'2026-09-18'); app.add_sales_dispatch_item(c,d3['id'],i['id'],pcs=1,meter=0)
except ValueError: pass
else: raise AssertionError('Over-dispatch must be rejected')
app.mark_sales_dispatch_delivered(c,d['id'])
r=app.sales_dispatch_report(c,sales_order_id=o['id'])
assert r['count']==3 and sum(x['total_pcs'] for x in r['items'])==10
assert c.execute('SELECT COUNT(*) FROM stock_movement').fetchone()[0] == 1 if c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stock_movement'").fetchone() else True
print('PHASE 62 TESTS PASS')
