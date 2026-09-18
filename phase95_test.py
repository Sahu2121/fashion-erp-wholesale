import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 95 — BUSINESS DATA VALIDATION RULES
assert app.validate_business_values(c,{'qty':2,'amount':10,'invoice_date':'2026-01-01'})['ok']; assert not app.validate_business_values(c,{'qty':-1})['ok']
print('PHASE 95 PASS')
