import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_reservation_issue_table(c); app.ensure_reservation_issue_sla_table(c)
r=c.execute("INSERT INTO stock_reservation_issues(reservation_id,code,severity,message,created_at) VALUES(?,?,?,?,?)",(1,'X','ERROR','test','2000-01-01 00:00:00')).lastrowid
app.set_reservation_issue_sla(c,r,ack_due_minutes=30,resolve_due_minutes=60,priority='HIGH')
q=app.queue_reservation_issue_notifications(c,channel='IN_APP',recipient='manager'); assert q['created_count']==2
cl=app.reservation_issue_notification_claim_with_lease(c,limit=1,lease_minutes=30,worker_id='w1'); assert cl['claimed_count']==1
nid=cl['notification_ids'][0]; tok=cl['claim_token']
cl2=app.reservation_issue_notification_claim_with_lease(c,limit=1,lease_minutes=30,worker_id='w2'); assert cl2['claimed_count']==1
# The second claim gets the other notification, while the first remains leased.
assert nid != cl2['notification_ids'][0]
try:
    app.reservation_issue_notification_complete_claim(c,nid,'bad',True)
    raise AssertionError('bad token accepted')
except ValueError:
    pass
app.reservation_issue_notification_complete_claim(c,nid,tok,success=False,error='adapter down')
assert app.reservation_issue_notification_dispatch_report(c,status='FAILED')['count']==1
# Reclaim the other leased item using an explicit future timestamp.
future='2100-01-01 00:00:00'
rcl=app.reservation_issue_notification_reclaim_stale(c,now=future); assert rcl['reclaimed_count']==1
assert app.reservation_issue_notification_dispatch_report(c,status='PENDING')['count']==1
print('PHASE 51 TESTS PASS')
