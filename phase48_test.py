import os, sqlite3, importlib.util, tempfile
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)

def db():
    c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row; return c

c=db(); app.ensure_reservation_issue_table(c)
app.ensure_reservation_issue_sla_table(c)
r=c.execute("INSERT INTO stock_reservation_issues(reservation_id,code,severity,message) VALUES(?,?,?,?,?)".replace('?,?,?,?,?','?,?,?,?'),(1,'X','ERROR','test')).lastrowid
c.commit()
assert app.set_reservation_issue_sla(c,r,ack_due_minutes=30,resolve_due_minutes=60,priority='HIGH')['items'][0]['status']=='OPEN'
q=app.reservation_issue_sla_report(c,issue_id=r); assert q['count']==1 and q['items'][0]['priority']=='HIGH'
# force due timestamps in the past
c.execute("UPDATE stock_reservation_issues SET created_at='2000-01-01 00:00:00' WHERE id=?",(r,)); c.commit()
es=app.escalate_overdue_reservation_issues(c,as_of='2000-01-03 00:00:00'); assert es['escalated_count']==1
q=app.reservation_issue_sla_report(c,issue_id=r); assert q['items'][0]['escalated_at'] is not None
print('PHASE 48 TESTS PASS')
