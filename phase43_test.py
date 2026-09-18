import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (ensure_godown_tables, ensure_stock_reservation_table,
                 create_stock_reservation, fulfill_stock_reservation,
                 reservation_fulfillment_status, release_stock_reservation_quantity,
                 stock_reservation_event_report)

def main():
    c = sqlite3.connect(':memory:')
    ensure_godown_tables(c); ensure_stock_reservation_table(c)
    c.execute("INSERT INTO godowns(name) VALUES('MAIN')")
    gid = c.execute("SELECT id FROM godowns WHERE name='MAIN'").fetchone()[0]
    c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",
              (gid, 101, 'M', 'BLUE', 100, 200)); c.commit()
    r = create_stock_reservation(c, gid, 101, 'M', 'BLUE', 40, 80, party='ABC', reference_no='SO100')
    s = fulfill_stock_reservation(c, r['id'], pcs=15, meter=30, fulfilled_by='USER')
    assert s['status'] == 'OPEN' and s['consumed_pcs'] == 15 and s['remaining_pcs'] == 25
    s = release_stock_reservation_quantity(c, r['id'], pcs=5, meter=10, released_by='USER')
    assert s['remaining_pcs'] == 20 and s['remaining_meter'] == 40
    s = fulfill_stock_reservation(c, r['id'], pcs=20, meter=40, fulfilled_by='USER')
    assert s['status'] == 'CONSUMED' and s['remaining_pcs'] == 0 and s['remaining_meter'] == 0
    stock = c.execute("SELECT pcs,meter FROM godown_stock WHERE godown_id=? AND product_id=?", (gid,101)).fetchone()
    assert stock == (65.0, 130.0)
    events = stock_reservation_event_report(c, r['id'])
    assert events['count'] == 3
    c.close(); print('PHASE 43 TESTS: OK')
if __name__ == '__main__': main()
