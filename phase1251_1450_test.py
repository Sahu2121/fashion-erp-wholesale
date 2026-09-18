import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
con=sqlite3.connect(':memory:')
r=m.phases_1251_1450_smoke(con)
assert r['count']==200 and r['ok'], r
assert len(m.phases_1251_1450_catalog())==200
snap=m.enterprise_release_snapshot_1450(con)
assert snap['status']=='READY' and snap['phase_count']==200
# Exercise a real table-health probe against a tiny fixture.
con.execute('CREATE TABLE sales_invoices(id INTEGER PRIMARY KEY, invoice_no TEXT, status TEXT, total_amount REAL)')
con.execute("INSERT INTO sales_invoices VALUES(1,'S-1','PAID',100)")
probe=m.phase_1251_table_health(con)
assert probe['table_exists'] and probe['row_count']==1 and probe['result']=='OK', probe
print('PHASE_1251_1450_TEST_PASS', r['count'])
