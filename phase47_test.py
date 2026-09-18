import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (ensure_godown_tables, ensure_stock_reservation_table,
                 ensure_stock_reservation_event_table, create_stock_reservation,
                 sync_reservation_reconciliation_issues, reservation_issue_report,
                 acknowledge_reservation_issue, close_reservation_issue)

def main():
    c=sqlite3.connect(':memory:')
    ensure_godown_tables(c); ensure_stock_reservation_table(c); ensure_stock_reservation_event_table(c)
    c.execute("INSERT INTO godowns(name) VALUES('MAIN')")
    gid=c.execute("SELECT id FROM godowns WHERE name='MAIN'").fetchone()[0]
    c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",(gid,1,'M','BLUE',10,20))
    c.commit()
    r1=create_stock_reservation(c,gid,1,'M','BLUE',5,10,party='ABC',reference_no='SO1')
    r2=create_stock_reservation(c,gid,1,'M','BLUE',3,6,party='ABC',reference_no='SO2')
    c.execute("UPDATE stock_reservations SET reference_no='SO1' WHERE id=?",(r2['id'],)); c.commit()
    s=sync_reservation_reconciliation_issues(c, party='ABC')
    assert s['created_count'] > 0
    assert sync_reservation_reconciliation_issues(c, party='ABC')['created_count'] == 0
    open_items=reservation_issue_report(c, status='OPEN')['items']
    assert open_items
    iid=open_items[0]['id']
    acknowledge_reservation_issue(c,iid,'manager','Reviewing conflict')
    assert reservation_issue_report(c,status='ACKNOWLEDGED')['count'] == 1
    close_reservation_issue(c,iid,'Resolved after stock review','manager')
    assert reservation_issue_report(c,status='CLOSED')['count'] == 1
    c.close(); print('PHASE 47 TESTS: OK')
if __name__=='__main__': main()
