import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,101,'L','Blue',100,200)); c.commit()
app.ensure_sales_order_tables(c); app.ensure_stock_reservation_table(c); app.ensure_sales_invoice_tables(c)
o=app.create_sales_order(c,'ABC Traders','2026-09-18',gid,created_by='u1'); app.add_sales_order_item(c,o['id'],101,'L','Blue',30,50,100)
app.confirm_sales_order(c,o['id'],confirmed_by='u1')
inv=app.post_sales_order_invoice(c,o['id'],invoice_date='2026-09-18',posted_by='u1',gst_rate=18,intra_state=True)
assert inv['invoice_no']=='INV000001' and inv['status']=='POSTED'
assert round(inv['taxable_amount'],2)==5000 and round(inv['cgst'],2)==450 and round(inv['sgst'],2)==450 and round(inv['net_amount'],2)==5900
assert c.execute("SELECT pcs,meter FROM godown_stock WHERE godown_id=? AND product_id=? AND size='L' AND color='Blue'",(gid,101)).fetchone()[0]==70
assert c.execute("SELECT status FROM sales_orders WHERE id=?",(o['id'],)).fetchone()[0]=='CLOSED'
assert c.execute("SELECT status FROM stock_reservations WHERE reference_no=?",(o['order_no'],)).fetchone()[0]=='CONSUMED'
try: app.post_sales_order_invoice(c,o['id'])
except ValueError: pass
else: raise AssertionError('Duplicate invoice posting must fail')
# Discount approval gate
app.set_party_credit_limit(c,'VIP',100000,credit_days=15)
o2=app.create_sales_order(c,'VIP','2026-09-18',gid); app.add_sales_order_item(c,o2['id'],101,'L','Blue',5,0,100); app.confirm_sales_order(c,o2['id'])
try: app.post_sales_order_invoice(c,o2['id'],discount_value=20,max_discount_pct=10)
except ValueError: pass
else: raise AssertionError('Approval should be required')
print('PHASE 54 TESTS PASS')
