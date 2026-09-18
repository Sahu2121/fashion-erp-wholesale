import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_godown_tables(c); c.execute("INSERT INTO godowns(name) VALUES('Main')"); gid=c.execute('SELECT id FROM godowns').fetchone()[0]
po=app.create_purchase_order(c,'SUP-1','2026-09-18',gid)
app.add_purchase_order_item(c,po['id'],101,'M','Blue',25,50,100)
app.confirm_purchase_order(c,po['id'])
assert app.purchase_order_report(c,po['id'])['items'][0]['status']=='CONFIRMED'
grn=app.receive_purchase_order(c,po['id'],received_by='u')
assert grn['status']=='RECEIVED'
r=c.execute("SELECT pcs,meter FROM godown_stock WHERE godown_id=? AND product_id=? AND size='M' AND color='Blue'",(gid,101)).fetchone()
assert float(r[0])==25 and float(r[1])==50
try: app.receive_purchase_order(c,po['id'],received_by='u')
except ValueError: pass
else: raise AssertionError('duplicate receipt must fail')
print('PHASE 56 TESTS PASS')
