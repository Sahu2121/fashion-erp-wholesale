import sqlite3,importlib.util
s=importlib.util.spec_from_file_location("app","app.py");a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
c=sqlite3.connect(":memory:");c.row_factory=sqlite3.Row
a.app.configure_sequence(c,"TEST","TX",1,4)
assert a.app.next_document_number(c,"TEST")=="TX0001" and a.app.next_document_number(c,"TEST")=="TX0002"
print("PHASE 84 TESTS PASS")