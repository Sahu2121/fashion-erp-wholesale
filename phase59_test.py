import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); app.ensure_sales_order_tables(c); app.ensure_sales_invoice_tables(c); app.ensure_purchase_order_tables(c); app.ensure_purchase_bill_tables(c); app.ensure_inventory_return_tables(c); app.ensure_stock_movement_table(c)
c.execute("INSERT INTO godowns(name) VALUES('Main')"); g=c.execute("SELECT id FROM godowns WHERE name='Main'").fetchone()[0]
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(g,101,'M','Blue',20,0))
# minimal sales invoice source
cur=c.execute("INSERT INTO sales_orders(order_no,party,order_date,godown_id,status) VALUES('SO1','Customer','2026-09-18',?,'CLOSED')",(g,)); so=cur.lastrowid
cur=c.execute("INSERT INTO sales_order_items(sales_order_id,line_no,product_id,size,color,pcs,meter,rate) VALUES(?,?,?,?,?,?,?,?)",(so,1,101,'M','Blue',10,0,100)); soi=cur.lastrowid
cur=c.execute("INSERT INTO sales_invoices(invoice_no,invoice_date,sales_order_id,party,godown_id,taxable_amount,net_amount,status) VALUES('INV1','2026-09-18',?,'Customer',?,1000,1000,'POSTED')",(so,g)); inv=cur.lastrowid
cur=c.execute("INSERT INTO sales_invoice_items(sales_invoice_id,sales_order_item_id,line_no,product_id,size,color,pcs,meter,rate,gross_amount,taxable_amount,amount) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(inv,soi,1,101,'M','Blue',10,0,100,1000,1000,1000)); sii=cur.lastrowid
r=app.create_sales_return(c,inv,[{'invoice_item_id':sii,'pcs':4}],return_date='2026-09-18',reason='Damaged return'); print('SR',r['return_no'])
assert c.execute('SELECT pcs FROM godown_stock WHERE godown_id=? AND product_id=101',(g,)).fetchone()[0]==24
try: app.create_sales_return(c,inv,[{'invoice_item_id':sii,'pcs':7}])
except ValueError: pass
else: raise AssertionError('over-return must fail')
# purchase bill source
cur=c.execute("INSERT INTO purchase_orders(order_no,party,order_date,godown_id,status) VALUES('PO1','Supplier','2026-09-18',?,'RECEIVED')",(g,)); po=cur.lastrowid
c.execute("INSERT INTO purchase_order_items(purchase_order_id,product_id,size,color,pcs,meter,rate,amount) VALUES(?,?,?,?,?,?,?,?)",(po,101,'M','Blue',8,0,90,720))
c.execute("INSERT INTO purchase_receipts(grn_no,purchase_order_id,receipt_date,status) VALUES('GRN1',?,'2026-09-18','RECEIVED')",(po,))
cur=c.execute("INSERT INTO purchase_bills(bill_no,supplier,purchase_order_id,grn_no,bill_date,amount,status) VALUES('PB1','Supplier',?,'GRN1','2026-09-18',720,'UNPAID')",(po,)); bill=cur.lastrowid
cur=c.execute("INSERT INTO purchase_bill_items(purchase_bill_id,product_id,size,color,pcs,meter,rate,amount) VALUES(?,?,?,?,?,?,?,?)",(bill,101,'M','Blue',8,0,90,720)); pbi=cur.lastrowid
r=app.create_purchase_return(c,bill,[{'bill_item_id':pbi,'pcs':3}],return_date='2026-09-18',reason='Supplier return'); print('PR',r['return_no'])
assert c.execute('SELECT pcs FROM godown_stock WHERE godown_id=? AND product_id=101',(g,)).fetchone()[0]==21
m=app.stock_movement_report(c,product_id=101); assert any(x['movement_type']=='SALES_RETURN' for x in m['items']); assert any(x['movement_type']=='PURCHASE_RETURN' for x in m['items'])
try: app.create_purchase_return(c,bill,[{'bill_item_id':pbi,'pcs':6}])
except ValueError: pass
else: raise AssertionError('purchase over-return must fail')
print('PHASE 59 TESTS PASS')
