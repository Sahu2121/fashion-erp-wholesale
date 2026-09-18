import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 103 — DATA RETENTION / ARCHIVE CONTROL
app.ensure_archive_tables(c); assert app.record_archive_run(c,'sales_invoices','2020-01-01',0)>0
print('PHASE 103 PASS')
