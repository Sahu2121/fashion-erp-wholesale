import sqlite3,importlib.util
s=importlib.util.spec_from_file_location("app","app.py");a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
c=sqlite3.connect(":memory:");c.row_factory=sqlite3.Row
c.execute("CREATE TABLE t(id INTEGER PRIMARY KEY,name TEXT)")
try:
 with a.atomic_operation(c,"test"):
  c.execute("INSERT INTO t(name) VALUES(?)",("ok",));raise RuntimeError()
except RuntimeError:pass
assert c.execute("SELECT COUNT(*) FROM t").fetchone()[0]==0
print("PHASE 82 TESTS PASS")