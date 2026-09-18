import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import create_payment, allocate_payment, void_payment_allocation, bill_outstanding_ageing, party_outstanding_ageing


def main():
    c = sqlite3.connect(':memory:')
    p = create_payment(c, 'RECEIPT', 'R0039', '2026-09-18', 'ABC', 1000)
    allocate_payment(c, p, 'RECEIPT', 'R0039', 'ABC', 'SALE', 1, 'S001', 500)
    bills = [
        {'bill_type':'SALE','bill_id':1,'bill_no':'S001','party':'ABC','bill_date':'2026-08-01','due_date':'2026-08-18','bill_amount':1000},
        {'bill_type':'SALE','bill_id':2,'bill_no':'S002','party':'ABC','bill_date':'2026-09-10','due_date':'2026-09-25','bill_amount':700},
        {'bill_type':'SALE','bill_id':3,'bill_no':'S003','party':'XYZ','bill_date':'2026-05-01','due_date':'2026-06-01','bill_amount':300},
    ]
    r = bill_outstanding_ageing(c, bills, '2026-09-18')
    assert r['count'] == 3
    assert r['bills'][0]['outstanding'] == 500
    assert any(x['bill_no']=='S002' and x['status']=='DUE' for x in r['bills'])
    a = party_outstanding_ageing(c, bills, '2026-09-18')
    assert a['totals']['total_outstanding'] == 1500
    abc = next(x for x in a['parties'] if x['party']=='ABC')
    assert abc['31_60'] == 500 and abc['current'] == 700
    xyz = next(x for x in a['parties'] if x['party']=='XYZ')
    assert xyz['91_plus'] == 300
    void_payment_allocation(c, 1, 'MANAGER', 'Reallocation')
    r2 = bill_outstanding_ageing(c, bills, '2026-09-18')
    assert next(x for x in r2['bills'] if x['bill_no']=='S001')['outstanding'] == 1000
    c.close()
    print('PHASE 39 TESTS: OK')

if __name__ == '__main__':
    main()
