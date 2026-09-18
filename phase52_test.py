import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row
app.ensure_reservation_issue_table(c); app.ensure_reservation_issue_sla_table(c)
r=c.execute("INSERT INTO stock_reservation_issues(reservation_id,code,severity,message,created_at) VALUES(?,?,?,?,?)",(7,'STOCK','ERROR','Short stock','2000-01-01 00:00:00')).lastrowid
app.set_reservation_issue_sla(c,r,ack_due_minutes=30,resolve_due_minutes=60,priority='HIGH')
q=app.queue_reservation_issue_notifications(c,channel='IN_APP',recipient='manager'); assert q['created_count']==2
p=app.build_reservation_issue_notification_payload(c,q['notification_ids'][0]); assert p['channel']=='IN_APP'; assert p['recipient']=='manager'; assert p['event_type']=='ACK_SLA_OVERDUE'; assert p['message']
assert app.reservation_issue_notification_payload_report(c)['count']==2
cl=app.reservation_issue_notification_claim_with_lease(c,limit=1,lease_minutes=30,worker_id='w1')
nid=cl['notification_ids'][0]; tok=cl['claim_token']
def adapter(payload):
    assert payload['id']==nid
    return {'success':True,'provider_message_id':'demo-123'}
app.dispatch_reservation_issue_notification(c,nid,tok,adapter)
row=c.execute('SELECT status,provider_message_id,delivered_at FROM reservation_issue_notifications WHERE id=?',(nid,)).fetchone()
assert row['status']=='SENT' and row['provider_message_id']=='demo-123' and row['delivered_at']
print('PHASE 52 TESTS PASS')
