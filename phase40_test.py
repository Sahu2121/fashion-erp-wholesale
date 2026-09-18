import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import create_payment, allocate_payment, build_collection_followup_queue, create_collection_followup, collection_followup_report, mark_collection_followup_sent, close_collection_followup

def main():
    c=sqlite3.connect(':memory:')
    p=create_payment(c,'RECEIPT','R0040','2026-09-18','ABC',500)
    allocate_payment(c,p,'RECEIPT','R0040','ABC','SALE',1,'S0040',500)
    bills=[
      {'bill_type':'SALE','bill_id':1,'bill_no':'S0040','party':'ABC','bill_date':'2026-07-01','due_date':'2026-07-10','bill_amount':1500},
      {'bill_type':'SALE','bill_id':2,'bill_no':'S0041','party':'ABC','bill_date':'2026-09-01','due_date':'2026-09-20','bill_amount':800},
      {'bill_type':'SALE','bill_id':3,'bill_no':'S0042','party':'XYZ','bill_date':'2026-05-01','due_date':'2026-06-01','bill_amount':2000},
    ]
    q=build_collection_followup_queue(c,bills,'2026-09-18')
    assert q['count']==2
    assert q['items'][0]['priority']=='CRITICAL'
    item=next(x for x in q['items'] if x['party']=='ABC')
    f=create_collection_followup(c,item,'MANAGER','WHATSAPP')
    assert f['status']=='OPEN'
    assert collection_followup_report(c,'ABC')['count']==1
    mark_collection_followup_sent(c,f['id'])
    assert collection_followup_report(c,'ABC','SENT')['count']==1
    close_collection_followup(c,f['id'],'Customer committed payment on 2026-09-20','MANAGER')
    assert collection_followup_report(c,'ABC','CLOSED')['count']==1
    try: close_collection_followup(c,f['id'],'again') ; raise AssertionError('double close')
    except ValueError: pass
    c.close(); print('PHASE 40 TESTS: OK')
if __name__=='__main__': main()
