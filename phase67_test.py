import sqlite3, importlib.util
s=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(s); s.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row; app.ensure_accounts_tables(c)
a=c.execute("INSERT INTO accounts(name,account_type) VALUES('Cash','ASSET')").lastrowid; b=c.execute("INSERT INTO accounts(name,account_type) VALUES('Sales','INCOME')").lastrowid
j=app.create_journal_entry(c,'2026-09-18','RECEIPT',[{'account_id':a,'debit':100},{'account_id':b,'credit':100}]); assert j['journal']['voucher_no'].startswith('JV'); assert abs(sum(x['debit'] for x in j['lines'])-sum(x['credit'] for x in j['lines']))<.01
print('PHASE 67 TESTS PASS')
