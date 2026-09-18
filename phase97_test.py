import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 97 — IDEMPOTENCY / DUPLICATE POST PROTECTION
assert app.claim_idempotency_key(c,'K1','TEST'); assert not app.claim_idempotency_key(c,'K1','TEST')
print('PHASE 97 PASS')
