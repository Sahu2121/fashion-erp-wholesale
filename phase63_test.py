import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT)"); c.execute("INSERT INTO products VALUES(101,'Shirt')")
# Minimal source tables required by the existing invoice/return workflow.
app.ensure_sales_order_tables(c); app.ensure_stock_reservation_table(c); app.ensure_sales_invoice_tables(c)
o=app.create_sales_order(c,'ABC Traders','2026-09-18',gid); oi=app.add_sales_order_item(c,o['id'],101,'L','Blue',5,0,100)
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,101,'L','Blue',10,0)); c.commit()
app.confirm_sales_order(c,o['id']); app.create_stock_reservation(c,gid,101,'L','Blue',pcs=5,meter=0,party='ABC Traders',reference_no=o['order_no'],created_by='T')
inv=app.post_sales_order_invoice(c,o['id'],'2026-09-18',gst_rate=5,intra_state=True)
sr=app.create_sales_return(c,inv['id'],[{'invoice_item_id':inv['items'][0]['id'],'pcs':2,'meter':0}],'2026-09-18','Defect')
cn=app.create_sales_credit_note(c,sr['id'],'2026-09-18','T')
assert cn['note_no']=='CN000001' and round(cn['total_amount'],2)==210.0
try: app.create_sales_credit_note(c,sr['id'])
except ValueError: pass
else: raise AssertionError('Duplicate credit note must be rejected')
assert app.sales_credit_note_report(c,invoice_id=inv['id'])['count']==1
print('PHASE 63 TESTS PASS')
