import sqlite3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (
    create_payment, allocate_payment, ensure_payment_allocation_reversal_columns,
    payment_reconciliation, void_payment_allocation,
    active_bill_settlement_status,
)

def main():
    c = sqlite3.connect(':memory:')
    ensure_payment_allocation_reversal_columns(c)
    pid = create_payment(c, 'RECEIPT', 'R0037', '2026-09-18', 'ABC', 1500)
    allocate_payment(c, pid, 'RECEIPT', 'R0037', 'ABC', 'SALE', 7, 'S0007', 1000)
    assert payment_reconciliation(c, pid)['allocated'] == 1000
    assert payment_reconciliation(c, pid)['unallocated'] == 500
    assert active_bill_settlement_status(c, 'SALE', 7, 'S0007', 1200)['outstanding'] == 200

    result = void_payment_allocation(c, 1, 'MANAGER', 'Customer payment reallocation')
    assert result['allocated'] == 0
    assert result['unallocated'] == 1500
    assert result['voided_allocations'] == 1000
    assert active_bill_settlement_status(c, 'SALE', 7, 'S0007', 1200)['status'] == 'UNPAID'

    try:
        void_payment_allocation(c, 1, 'MANAGER', 'Again')
        raise AssertionError('double void should fail')
    except ValueError:
        pass

    try:
        allocate_payment(c, pid, 'RECEIPT', 'R0037', 'ABC', 'SALE', 8, 'S0008', 0)
        raise AssertionError('zero allocation should fail')
    except ValueError:
        pass
    c.close()
    print('PHASE 37 TESTS: OK')

if __name__ == '__main__':
    main()
