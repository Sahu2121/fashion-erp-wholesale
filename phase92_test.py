import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 92 — TRANSACTION POSTING GUARD
assert app.guarded_posting(c,'2026-01-01','noop',lambda conn: 7)==7
print('PHASE 92 PASS')
