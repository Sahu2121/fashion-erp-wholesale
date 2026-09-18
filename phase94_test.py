import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 94 — DOCUMENT SEQUENCE AUDIT / SAFE PREVIEW
app.configure_sequence(c,'INV','INV-',9,4); assert app.preview_document_number(c,'INV')=='INV-0009'; assert app.next_document_number(c,'INV')=='INV-0009'
print('PHASE 94 PASS')
