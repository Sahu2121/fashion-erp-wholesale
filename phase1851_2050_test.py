import sqlite3
from app import phases_1851_2050_catalog, phases_1851_2050_smoke, reconciliation_snapshot_1851_2050

def main():
    conn=sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE sales_invoices(id INTEGER PRIMARY KEY, invoice_no TEXT, total_amount REAL, status TEXT, created_at TEXT)')
    conn.execute('CREATE TABLE sales_invoice_items(id INTEGER PRIMARY KEY, invoice_id INTEGER, amount REAL, FOREIGN KEY(invoice_id) REFERENCES sales_invoices(id))')
    conn.execute('CREATE TABLE purchase_bills(id INTEGER PRIMARY KEY, bill_no TEXT, total_amount REAL, status TEXT, created_at TEXT)')
    conn.execute('CREATE TABLE purchase_bill_items(id INTEGER PRIMARY KEY, bill_id INTEGER, amount REAL, FOREIGN KEY(bill_id) REFERENCES purchase_bills(id))')
    conn.execute('CREATE TABLE journal_entries(id INTEGER PRIMARY KEY)')
    conn.execute('CREATE TABLE journal_lines(id INTEGER PRIMARY KEY, journal_entry_id INTEGER, debit REAL, credit REAL, FOREIGN KEY(journal_entry_id) REFERENCES journal_entries(id))')
    conn.execute('INSERT INTO sales_invoices VALUES(1,"SI-1",100,"POSTED","2026-01-01")')
    conn.execute('INSERT INTO sales_invoice_items VALUES(1,1,100)')
    conn.commit()
    c=phases_1851_2050_catalog(); assert len(c)==200 and min(c)==1851 and max(c)==2050
    s=phases_1851_2050_smoke(conn); assert s['ok'] and s['count']==200
    snap=reconciliation_snapshot_1851_2050(conn); assert snap['smoke_ok'] and snap['phase_count']==200 and snap['log_count']==200
    print('PHASE_1851_2050_TEST_PASS', len(c), snap['log_count'])
if __name__=='__main__': main()
