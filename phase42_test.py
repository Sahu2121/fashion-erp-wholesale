import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (ensure_godown_tables, ensure_stock_reservation_table,
                 create_stock_reservation, stock_available_for_reservation,
                 reserved_stock_total, release_stock_reservation,
                 consume_stock_reservation, stock_reservation_report)

def main():
    c = sqlite3.connect(':memory:')
    ensure_godown_tables(c); ensure_stock_reservation_table(c)
    c.execute("INSERT INTO godowns(name) VALUES('MAIN')")
    gid = c.execute("SELECT id FROM godowns WHERE name='MAIN'").fetchone()[0]
    c.execute("INSERT INTO godown_stock(godown_id,product_id,size,color,pcs,meter) VALUES(?,?,?,?,?,?)",
              (gid, 101, 'M', 'BLUE', 100, 200))
    c.commit()
    r1 = create_stock_reservation(c, gid, 101, 'M', 'BLUE', pcs=30, meter=50,
                                  party='ABC', reference_no='SO001')
    assert r1['reservation_no'] == 'RSV000001'
    a = stock_available_for_reservation(c, gid, 101, 'M', 'BLUE')
    assert a['reserved_pcs'] == 30 and a['available_pcs'] == 70
    r2 = create_stock_reservation(c, gid, 101, 'M', 'BLUE', pcs=70, meter=100,
                                  party='ABC', reference_no='SO002')
    try:
        create_stock_reservation(c, gid, 101, 'M', 'BLUE', pcs=1, meter=1)
        raise AssertionError('Expected insufficient unreserved stock')
    except ValueError:
        pass
    release_stock_reservation(c, r1['id'], 'Customer cancelled')
    a = stock_available_for_reservation(c, gid, 101, 'M', 'BLUE')
    assert a['available_pcs'] == 30
    consume_stock_reservation(c, r2['id'])
    stock = c.execute("SELECT pcs,meter FROM godown_stock WHERE godown_id=? AND product_id=?", (gid,101)).fetchone()
    assert stock == (30.0, 100.0)
    rep = stock_reservation_report(c, status=None)
    assert rep['count'] == 2 and rep['pcs'] == 100
    c.close()
    print('PHASE 42 TESTS: OK')

if __name__ == '__main__':
    main()
