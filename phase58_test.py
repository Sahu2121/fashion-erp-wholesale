import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c)
c.execute("INSERT INTO godowns(name) VALUES('Main')"); c.execute("INSERT INTO godowns(name) VALUES('Branch')")
g1=c.execute("SELECT id FROM godowns WHERE name='Main'").fetchone()[0]
g2=c.execute("SELECT id FROM godowns WHERE name='Branch'").fetchone()[0]
c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(g1,101,'M','Blue',25,50))
assert app.seed_stock_movement_opening(c,'2026-09-18')['created']==1
assert app.seed_stock_movement_opening(c,'2026-09-18')['created']==0
r=app.inventory_reconciliation_report(c,g1,101,'M','Blue'); assert r['items'][0]['status']=='OK'
app.set_stock_adjustment(c,g1,101,'M','Blue',pcs_delta=5,meter_delta=0,rate=100,adjustment_date='2026-09-18',reason='Count correction',created_by='u')
r=app.stock_balance_report(c,g1,101,'M','Blue'); assert r['items'][0]['pcs']==30
app.transfer_stock(c,g1,g2,101,'M','Blue',10,0)
r=app.stock_balance_report(c,g1,101,'M','Blue'); assert r['items'][0]['pcs']==20
r=app.stock_balance_report(c,g2,101,'M','Blue'); assert r['items'][0]['pcs']==10
m=app.stock_movement_report(c,product_id=101); assert m['count']==4
assert app.inventory_reconciliation_report(c,g1,101,'M','Blue')['items'][0]['status']=='OK'
try: app.set_stock_adjustment(c,g1,101,'M','Blue',pcs_delta=-999)
except ValueError: pass
else: raise AssertionError('negative stock adjustment must fail')
print('PHASE 58 TESTS PASS')
