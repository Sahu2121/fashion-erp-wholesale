import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 96 — AUDIT INTEGRITY / HASH CHAIN
app.append_audit_integrity(c,'U','CREATE','TEST','1','x'); assert app.verify_audit_integrity(c)['ok']
print('PHASE 96 PASS')
