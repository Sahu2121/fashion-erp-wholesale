import sqlite3, importlib.util
s=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(s); s.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row; app.ensure_sales_invoice_tables(c); app.ensure_purchase_bill_tables(c)
c.execute("INSERT INTO sales_invoices(invoice_no,invoice_date,sales_order_id,party,taxable_amount,cgst,sgst,igst,net_amount,status) VALUES(?,?,?,?,?,?,?,?,?,?)",('SI1','2026-09-18',1,'A',100,9,9,0,118,'POSTED'))
c.execute("INSERT INTO purchase_bills(bill_no,supplier,amount,bill_date) VALUES(?,?,?,?)",('PB1','S',50,'2026-09-18')); c.commit()
r=app.gst_return_summary(c,'2026-01-01','2026-12-31'); assert r['output_cgst']==9 and r['output_sgst']==9 and r['purchase_value']==50
print('PHASE 68 TESTS PASS')
