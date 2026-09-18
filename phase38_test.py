import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import create_payment, allocate_payment, void_payment_allocation, party_payment_reconciliation, allocation_audit_report

def main():
    c=sqlite3.connect(':memory:')
    p1=create_payment(c,'RECEIPT','R0038','2026-09-18','ABC',1500)
    p2=create_payment(c,'RECEIPT','R0039','2026-09-19','ABC',500)
    allocate_payment(c,p1,'RECEIPT','R0038','ABC','SALE',1,'S0001',1000)
    allocate_payment(c,p2,'RECEIPT','R0039','ABC','SALE',2,'S0002',500)
    void_payment_allocation(c,1,'MANAGER','Reallocation')
    r=party_payment_reconciliation(c,'ABC')
    assert r['payment_count']==2 and r['payment_total']==2000
    assert r['allocated']==500 and r['unallocated']==1500 and r['voided_allocations']==1000
    a=allocation_audit_report(c,'ABC')
    assert a['count']==2 and a['active_total']==500 and a['voided_total']==1000
    active=allocation_audit_report(c,'ABC',include_voided=False)
    assert active['count']==1 and active['active_total']==500
    c.close(); print('PHASE 38 TESTS: OK')
if __name__=='__main__': main()
