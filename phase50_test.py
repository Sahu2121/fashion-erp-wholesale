import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_reservation_issue_table(c); app.ensure_reservation_issue_sla_table(c)
r=c.execute("INSERT INTO stock_reservation_issues(reservation_id,code,severity,message,created_at) VALUES(?,?,?,?,?)",(1,'X','ERROR','test','2000-01-01 00:00:00')).lastrowid
c.commit(); app.set_reservation_issue_sla(c,r,ack_due_minutes=30,resolve_due_minutes=60,priority='HIGH')
q=app.queue_reservation_issue_notifications(c,channel='IN_APP',recipient='manager')
assert q['created_count']==2, q
claim=app.reservation_issue_notification_claim(c,limit=1); assert claim['claimed_count']==1
nid=claim['notification_ids'][0]
app.mark_reservation_issue_notification_failed(c,nid,'adapter unavailable')
assert app.reservation_issue_notification_dispatch_report(c,status='FAILED')['count']==1
app.retry_reservation_issue_notification(c,nid)
assert app.reservation_issue_notification_dispatch_report(c,status='PENDING')['count']==2
claim2=app.reservation_issue_notification_claim(c,limit=1); assert claim2['notification_ids']==[nid]
assert app.reservation_issue_notification_dispatch_report(c,min_attempts=2)['count']==1
app.mark_reservation_issue_notification_sent(c,nid,sent_at='2000-01-03 00:00:00')
assert app.reservation_issue_notification_dispatch_report(c,status='SENT')['count']==1
print('PHASE 50 TESTS PASS')
