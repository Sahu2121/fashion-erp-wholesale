import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 99 — REPORT SNAPSHOT CACHE
sid=app.save_report_snapshot(c,'R',{'x':1}); assert app.latest_report_snapshot(c,'R')['payload']['x']==1
print('PHASE 99 PASS')
