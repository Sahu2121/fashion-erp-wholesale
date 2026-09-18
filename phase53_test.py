import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c)
c.execute("INSERT INTO godowns(name) VALUES('Main')")
gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,101,'L','Blue',100,200))
c.commit()
app.ensure_sales_order_tables(c)
o=app.create_sales_order(c,'ABC Traders','2026-09-18',gid,created_by='u1')
assert o['status']=='DRAFT' and o['order_no']=='SO000001'
i=app.add_sales_order_item(c,o['id'],101,'L','Blue',30,50,100)
assert i['line_no']==1
r=app.confirm_sales_order(c,o['id'],confirmed_by='u1')
assert r['status']=='RESERVED' and len(r['reservations'])==1
rid=r['reservations'][0]['reservation_id']
av=app.stock_available_for_reservation(c,gid,101,'L','Blue')
assert av['reserved_pcs']==30 and av['available_pcs']==70
canc=app.cancel_sales_order(c,o['id'],cancelled_by='u1',reason='Customer cancelled')
assert canc['status']=='CANCELLED'
av=app.stock_available_for_reservation(c,gid,101,'L','Blue')
assert av['reserved_pcs']==0 and av['available_pcs']==100
assert c.execute("SELECT status FROM stock_reservations WHERE id=?",(rid,)).fetchone()[0]=='RELEASED'
# Atomic validation: second order has two lines, one cannot reserve; neither line may remain reserved.
o2=app.create_sales_order(c,'XYZ','2026-09-18',gid)
app.add_sales_order_item(c,o2['id'],101,'L','Blue',20,0)
app.add_sales_order_item(c,o2['id'],101,'L','Blue',1000,0)
try: app.confirm_sales_order(c,o2['id'])
except ValueError: pass
else: raise AssertionError('Expected insufficient stock')
assert c.execute("SELECT COUNT(*) FROM sales_order_reservations WHERE sales_order_id=?",(o2['id'],)).fetchone()[0]==0
assert c.execute("SELECT COUNT(*) FROM stock_reservations WHERE reference_no=?",(o2['order_no'],)).fetchone()[0]==0
print('PHASE 53 TESTS PASS')
