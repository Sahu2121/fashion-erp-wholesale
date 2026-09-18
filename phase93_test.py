import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 93 — FISCAL YEAR CONTROL
assert app.configure_fiscal_year(c,'FY26','2026-04-01','2027-03-31')['status']=='OPEN'; app.assert_fiscal_year_open(c,'2026-06-01')
print('PHASE 93 PASS')
