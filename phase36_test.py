import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import (create_payment, ensure_payment_allocation_table, allocate_payment,
                 payment_allocation_summary, bill_settlement_status,
                 allocate_payment_fifo)

def main():
    c = sqlite3.connect(':memory:')
    ensure_payment_allocation_table(c)
    pid = create_payment(c, 'RECEIPT', 'R0001', '2026-09-18', 'ABC', 1500)
    allocate_payment(c, pid, 'RECEIPT', 'R0001', 'ABC', 'SALE', 1, 'S001', 1000)
    assert payment_allocation_summary(c, pid)['allocated'] == 1000
    assert bill_settlement_status(c, 'SALE', 1, 'S001', 1200)['outstanding'] == 200
    r = allocate_payment_fifo(c, pid, 'RECEIPT', 'R0001', 'ABC', [
        {'bill_type':'SALE','bill_id':2,'bill_no':'S002','outstanding':300},
        {'bill_type':'SALE','bill_id':3,'bill_no':'S003','outstanding':500},
    ])
    assert [x['allocated_amount'] for x in r['allocations']] == [300.0, 200.0]
    assert r['unallocated'] == 0.0
    try:
        allocate_payment(c, pid, 'RECEIPT', 'R0001', 'ABC', 'SALE', 4, 'S004', 1)
        raise AssertionError('over-allocation should fail')
    except ValueError:
        pass
    c.close()
    print('PHASE 36 TESTS: OK')
if __name__ == '__main__': main()
