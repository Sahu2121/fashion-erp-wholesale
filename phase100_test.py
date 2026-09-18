import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 100 — MANAGEMENT KPI PACK
assert 'sales_total' in app.management_kpi_pack(c)
print('PHASE 100 PASS')
