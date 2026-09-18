import sqlite3, importlib.util, tempfile, os
s=importlib.util.spec_from_file_location("app","app.py"); a=importlib.util.module_from_spec(s); s.loader.exec_module(a)
c=sqlite3.connect(":memory:"); c.row_factory=sqlite3.Row
f=tempfile.mktemp(".csv"); a.ensure_gst_reporting_tables(c); a.export_table_csv(c,"hsn_master",f); assert os.path.exists(f); os.unlink(f)
print("PHASE 77 TESTS PASS")
