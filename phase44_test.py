import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (ensure_godown_tables, ensure_stock_reservation_table,
                 create_stock_reservation, fulfill_stock_reservation,
                 reservation_fulfillment_status, expire_stock_reservation,
                 expire_due_stock_reservations, stock_reservation_report,
                 stock_available_for_reservation)

def main():
    c=sqlite3.connect(':memory:')
    ensure_godown_tables(c); ensure_stock_reservation_table(c)
    c.execute("INSERT INTO godowns(name) VALUES('MAIN')")
    gid=c.execute("SELECT id FROM godowns WHERE name='MAIN'").fetchone()[0]
    c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,1,'M','BLUE',100,200)); c.commit()
    r=create_stock_reservation(c,gid,1,'M','BLUE',40,80,reference_no='SO1',expiry_date='2026-09-10')
    fulfill_stock_reservation(c,r['id'],10,20)
    a=stock_available_for_reservation(c,gid,1,'M','BLUE')
    assert a['reserved_pcs']==30 and a['reserved_meter']==60 and a['available_pcs']==60 and a['available_meter']==120
    e=expire_stock_reservation(c,r['id'],'2026-09-18','SYSTEM')
    assert e['status']=='EXPIRED'
    s=reservation_fulfillment_status(c,r['id'])
    assert s['remaining_pcs']==0 and s['released_pcs']==30 and s['released_meter']==60
    r2=create_stock_reservation(c,gid,1,'M','BLUE',20,40,expiry_date='2026-09-01')
    r3=create_stock_reservation(c,gid,1,'M','BLUE',10,20,expiry_date='2026-10-01')
    out=expire_due_stock_reservations(c,'2026-09-18')
    assert out['expired_count']==1 and out['expired'][0]['reservation_no']==r2['reservation_no']
    rep=stock_reservation_report(c,status='EXPIRED')
    assert rep['count']==2
    c.close(); print('PHASE 44 TESTS: OK')
if __name__=='__main__': main()
