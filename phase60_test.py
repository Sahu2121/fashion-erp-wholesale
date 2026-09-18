import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); app.ensure_stock_movement_table(c)
c.execute("INSERT INTO godowns(name) VALUES('Main')"); g=c.execute("SELECT id FROM godowns WHERE name='Main'").fetchone()[0]
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(g,101,'M','Blue',100,0))
app._record_stock_movement(c,'PURCHASE',g,101,'M','Blue',100,0,100,'2026-01-01','GRN',1,'GRN1','Opening purchase','TEST'); c.commit()
r=app.stock_valuation_report(c,product_id=101); assert r['total_value']==10000.0, r
c.execute("UPDATE godown_stock SET pcs=90 WHERE godown_id=? AND product_id=?",(g,101)); app._record_stock_movement(c,'SALE',g,101,'M','Blue',10,0,120,'2026-03-01','SALE',1,'INV1','Sale','TEST'); c.commit()
r=app.stock_valuation_report(c,product_id=101); assert r['items'][0]['avg_rate']==100.0 and r['total_value']==9000.0, r
age=app.inventory_aging_report(c,product_id=101,as_of_date='2026-04-15',dead_stock_days=90); assert age['items'][0]['age_days']==104 and age['items'][0]['dead_stock']
# Return movements must now reconcile as in/out.
app._record_stock_movement(c,'SALES_RETURN',g,101,'M','Blue',5,0,100,'2026-04-01','SALES_RETURN',1,'SR1','return','TEST')
app._record_stock_movement(c,'PURCHASE_RETURN',g,101,'M','Blue',3,0,100,'2026-04-02','PURCHASE_RETURN',1,'PR1','return','TEST'); c.commit()
m=app.stock_movement_report(c,product_id=101); assert m['total_in_pcs']==105 and m['total_out_pcs']==13, m
print('PHASE 60 TESTS PASS')
