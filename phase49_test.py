import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_reservation_issue_table(c); app.ensure_reservation_issue_sla_table(c)
r=c.execute("INSERT INTO stock_reservation_issues(reservation_id,code,severity,message,created_at) VALUES(?,?,?,?,?)",(1,'X','ERROR','test','2000-01-01 00:00:00')).lastrowid
c.commit(); app.set_reservation_issue_sla(c,r,ack_due_minutes=30,resolve_due_minutes=60,priority='HIGH')
q=app.queue_reservation_issue_notifications(c,channel='IN_APP',recipient='manager')
assert q['created_count']==2, q
assert app.queue_reservation_issue_notifications(c,channel='IN_APP',recipient='manager')['created_count']==0
items=app.reservation_issue_notification_report(c,issue_id=r)['items']; assert len(items)==2
app.mark_reservation_issue_notification_sent(c,items[0]['id'],sent_at='2000-01-03 00:00:00')
assert app.reservation_issue_notification_report(c,issue_id=r,status='SENT')['count']==1
app.mark_reservation_issue_notification_failed(c,items[1]['id'],'adapter unavailable')
assert app.reservation_issue_notification_report(c,issue_id=r,status='FAILED')['count']==1
print('PHASE 49 TESTS PASS')
