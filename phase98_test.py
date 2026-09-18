import sqlite3, sys, tempfile
sys.path.insert(0, '.')
import app
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
# bootstrap core tables used by the release hardening helpers
try: app.ensure_schema_version_table(c)
except Exception: pass
# PHASE 98 — BACKGROUND JOB QUEUE
jid=app.enqueue_job(c,'TEST','x'); assert app.claim_job(c)['id']==jid; app.complete_job(c,jid); assert c.execute('SELECT status FROM job_queue WHERE id=?',(jid,)).fetchone()[0]=='DONE'
print('PHASE 98 PASS')
