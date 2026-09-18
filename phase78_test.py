import sqlite3, importlib.util, tempfile, os
s=importlib.util.spec_from_file_location("app","app.py"); a=importlib.util.module_from_spec(s); s.loader.exec_module(a)
c=sqlite3.connect(":memory:"); c.row_factory=sqlite3.Row
assert isinstance(a.reconciliation_center(c),dict)
print("PHASE 78 TESTS PASS")
