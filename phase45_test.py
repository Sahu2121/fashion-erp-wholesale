import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (ensure_godown_tables, ensure_stock_reservation_table,
                 create_stock_reservation, fulfill_stock_reservation,
                 release_stock_reservation_quantity, reservation_utilization_report)

def main():
    c=sqlite3.connect(':memory:')
    ensure_godown_tables(c); ensure_stock_reservation_table(c)
    c.execute("INSERT INTO godowns(name) VALUES('MAIN')")
    gid=c.execute("SELECT id FROM godowns WHERE name='MAIN'").fetchone()[0]
    c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,1,'M','BLUE',100,200))
    c.commit()
    r1=create_stock_reservation(c,gid,1,'M','BLUE',40,80,party='ABC',reference_no='SO1')
    r2=create_stock_reservation(c,gid,1,'M','BLUE',20,40,party='XYZ',reference_no='SO2')
    fulfill_stock_reservation(c,r1['id'],10,20)
    release_stock_reservation_quantity(c,r2['id'],5,10)
    rep=reservation_utilization_report(c)
    assert rep['reservation_count']==2
    assert rep['original_pcs']==60 and rep['original_meter']==120
    assert rep['consumed_pcs']==10 and rep['consumed_meter']==20
    assert rep['released_pcs']==5 and rep['released_meter']==10
    assert rep['open_reserved_pcs']==45 and rep['open_reserved_meter']==90
    assert rep['open_available_pcs'] is None and rep['open_available_meter'] is None
    scoped=reservation_utilization_report(c,godown_id=gid,product_id=1,size='M',color='BLUE')
    assert scoped['open_available_pcs']==45 and scoped['open_available_meter']==90
    party=reservation_utilization_report(c, party='ABC')
    assert party['reservation_count']==1 and party['open_reserved_pcs']==30
    status=reservation_utilization_report(c, status='OPEN')
    assert status['reservation_count']==2
    c.close(); print('PHASE 45 TESTS: OK')
if __name__=='__main__': main()
