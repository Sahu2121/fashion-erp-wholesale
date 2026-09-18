import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 102 — BACKUP MANIFEST / VERIFICATION RECORD
p='/tmp/erp_backup_p102.db'; r=app.backup_with_manifest(c,p); assert r['ok']
print('PHASE 102 PASS')
