import sqlite3,importlib.util
s=importlib.util.spec_from_file_location("app","app.py");a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
c=sqlite3.connect(":memory:");c.row_factory=sqlite3.Row
r=a.final_release_check(c);assert r["version"]=="1.0-P90" and r["regression_ok"]
print("PHASE 90 TESTS PASS")