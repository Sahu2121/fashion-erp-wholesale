import sqlite3, importlib.util
s=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(s); s.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row; app.ensure_sales_invoice_tables(c); app.ensure_purchase_bill_tables(c)
c.execute("INSERT INTO sales_invoices(invoice_no,sales_order_id,party,net_amount,status) VALUES(?,?,?,?,?)",('SI1',1,'A',1000,'POSTED'))
c.execute("INSERT INTO purchase_bills(bill_no,supplier,amount) VALUES(?,?,?)",('PB1','S',500)); c.commit()
d=app.clean_dashboard_sections(c); assert len(d['kpis'])==4 and d['kpis'][0]['value']==1000
print('PHASE 69 TESTS PASS')
