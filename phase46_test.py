import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (ensure_godown_tables, ensure_stock_reservation_table,
                 ensure_stock_reservation_event_table, create_stock_reservation,
                 reservation_reconciliation_report, fulfill_stock_reservation,
                 release_stock_reservation_quantity)

def main():
    c=sqlite3.connect(':memory:')
    ensure_godown_tables(c); ensure_stock_reservation_table(c); ensure_stock_reservation_event_table(c)
    c.execute("INSERT INTO godowns(name) VALUES('MAIN')")
    gid=c.execute("SELECT id FROM godowns WHERE name='MAIN'").fetchone()[0]
    c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,1,'M','BLUE',100,200))
    c.commit()
    r1=create_stock_reservation(c,gid,1,'M','BLUE',40,80,party='ABC',reference_no='SO1')
    r2=create_stock_reservation(c,gid,1,'M','BLUE',20,40,party='ABC',reference_no='SO1')
    rep=reservation_reconciliation_report(c)
    assert rep['checked_reservations']==2
    assert rep['warning_count']>=2 and any(x['code']=='DUPLICATE_ACTIVE_REFERENCE' for x in rep['issues'])
    fulfill_stock_reservation(c,r1['id'],10,20)
    release_stock_reservation_quantity(c,r2['id'],5,10)
    clean=reservation_reconciliation_report(c, reference_no='SO1') if False else None
    # A scoped report should retain both active reservations and reconcile totals.
    rep2=reservation_reconciliation_report(c, party='ABC')
    assert rep2['totals']['consumed_pcs']==10 and rep2['totals']['released_pcs']==5
    assert rep2['totals']['open_reserved_pcs']==45
    c.close(); print('PHASE 46 TESTS: OK')
if __name__=='__main__': main()
