import sqlite3,importlib.util
s=importlib.util.spec_from_file_location("app","app.py");a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
c=sqlite3.connect(":memory:");c.row_factory=sqlite3.Row
a.set_period_status(c,"2026-04","2026-04-01","2026-04-30","LOCKED")
assert a.is_period_locked(c,"2026-04-15")
try:a.assert_period_open(c,"2026-04-15");raise AssertionError
except ValueError:pass
print("PHASE 83 TESTS PASS")