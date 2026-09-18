import sqlite3, importlib.util, tempfile, os
s=importlib.util.spec_from_file_location("app","app.py"); a=importlib.util.module_from_spec(s); s.loader.exec_module(a)
c=sqlite3.connect(":memory:"); c.row_factory=sqlite3.Row
sid=a.start_session(c,"admin","ADMIN"); assert a.active_sessions(c); a.end_session(c,sid); assert not a.active_sessions(c)
print("PHASE 74 TESTS PASS")
