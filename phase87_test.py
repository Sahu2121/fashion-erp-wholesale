import sqlite3,importlib.util
s=importlib.util.spec_from_file_location("app","app.py");a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
c=sqlite3.connect(":memory:");c.row_factory=sqlite3.Row
a.log_error(c,"TEST","RUN",ValueError("x"));assert a.diagnostics_summary(c)["open_errors"]==1
print("PHASE 87 TESTS PASS")