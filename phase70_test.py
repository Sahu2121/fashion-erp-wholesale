import sqlite3, importlib.util, tempfile, os
s=importlib.util.spec_from_file_location('app','app.py'); app=importlib.util.module_from_spec(s); s.loader.exec_module(app)
c=sqlite3.connect(':memory:'); c.row_factory=sqlite3.Row; app.set_role_permission(c,'ADMIN','SALES_EDIT',True); assert app.has_permission(c,'ADMIN','SALES_EDIT'); app.write_audit_log(c,'ADMIN','CREATE','SALES',1,'ok'); assert c.execute('select count(*) from audit_log').fetchone()[0]==1
f=tempfile.mktemp('.db'); app.backup_database(c,f); assert os.path.exists(f); os.unlink(f); print('PHASE 70 TESTS PASS')
