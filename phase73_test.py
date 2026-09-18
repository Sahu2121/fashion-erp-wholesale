import sqlite3, importlib.util, tempfile, os
s=importlib.util.spec_from_file_location("app","app.py"); a=importlib.util.module_from_spec(s); s.loader.exec_module(a)
c=sqlite3.connect(":memory:"); c.row_factory=sqlite3.Row
a.log_master_change(c,"PRODUCT",1,"CREATE"); assert c.execute("select count(*) from master_change_log").fetchone()[0]==1
print("PHASE 73 TESTS PASS")
