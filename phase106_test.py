import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 106 — RELEASE CANDIDATE HARDENING
assert app.release_candidate(c)['status']=='READY'
print('PHASE 106 PASS')
