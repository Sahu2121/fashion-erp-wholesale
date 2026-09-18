import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
# Draft order amendment
app.ensure_sales_order_tables(c)
o=app.create_sales_order(c,'ABC Traders','2026-09-18',gid,remark='old')
i1=app.add_sales_order_item(c,o['id'],101,'L','Blue',10,0,100)
i2=app.add_sales_order_item(c,o['id'],102,'M','Red',0,20,50)
r=app.update_sales_order_header(c,o['id'],party='ABC Wholesale',remark='amended')
assert r['party']=='ABC Wholesale' and r['remark']=='amended'
i=app.update_sales_order_item(c,i1['id'],pcs=15,rate=110)
assert i['pcs']==15 and i['rate']==110
r=app.remove_sales_order_item(c,i2['id'])
assert r['item_count']==1
# Summary / pending
s=app.sales_order_summary_report(c)
assert s['count']==1 and s['status_counts']['DRAFT']==1 and s['total_pcs']==15 and s['total_value']==1650
p=app.pending_sales_order_report(c)
assert p['count']==1 and p['total_value']==1650
# Confirmed/reserved order becomes immutable through amendment APIs
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,101,'L','Blue',100,0)); c.commit()
app.confirm_sales_order(c,o['id'])
try: app.update_sales_order_header(c,o['id'],party='Blocked')
except ValueError: pass
else: raise AssertionError('Confirmed order must not be editable')
try: app.update_sales_order_item(c,i1['id'],pcs=20)
except ValueError: pass
else: raise AssertionError('Confirmed order item must not be editable')
print('PHASE 61 TESTS PASS')
