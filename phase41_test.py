import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (create_payment, allocate_payment, set_party_credit_limit,
                 get_party_credit_limit, set_party_credit_hold,
                 calculate_credit_exposure, credit_exposure_report)


def main():
    c = sqlite3.connect(':memory:')
    p = create_payment(c, 'RECEIPT', 'R0041', '2026-09-18', 'ABC', 200)
    allocate_payment(c, p, 'RECEIPT', 'R0041', 'ABC', 'SALE', 1, 'S0041', 200)
    bills = [
        {'bill_type':'SALE','bill_id':1,'bill_no':'S0041','party':'ABC','bill_date':'2026-08-01','due_date':'2026-08-18','bill_amount':1000},
        {'bill_type':'SALE','bill_id':2,'bill_no':'S0042','party':'ABC','bill_date':'2026-09-10','due_date':'2026-09-25','bill_amount':500},
        {'bill_type':'SALE','bill_id':3,'bill_no':'S0043','party':'XYZ','bill_date':'2026-09-01','due_date':'2026-09-20','bill_amount':300},
    ]
    cfg = set_party_credit_limit(c, 'ABC', 1000, warning_percent=80, credit_days=30, updated_by='ADMIN')
    assert cfg['credit_limit'] == 1000 and cfg['credit_days'] == 30
    r = calculate_credit_exposure(c, 'ABC', bills, '2026-09-18', proposed_amount=250)
    assert r['outstanding'] == 1300
    assert r['exposure'] == 1550
    assert r['status'] == 'EXCEEDED' and not r['can_post']
    set_party_credit_hold(c, 'XYZ', True, 'Old overdue balance', 'ADMIN')
    h = calculate_credit_exposure(c, 'XYZ', bills, '2026-09-18', 10)
    assert h['status'] == 'ON_HOLD' and not h['can_post']
    report = credit_exposure_report(c, ['ABC','XYZ'], bills, '2026-09-18')
    assert report['count'] == 2 and report['exceeded'] == 1 and report['on_hold'] == 1
    c.close()
    print('PHASE 41 TESTS: OK')

if __name__ == '__main__':
    main()
