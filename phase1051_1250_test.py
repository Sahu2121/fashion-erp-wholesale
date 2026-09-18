import sqlite3, importlib.util
spec=importlib.util.spec_from_file_location('app','app.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
con=sqlite3.connect(':memory:')
r=m.phases_1051_1250_smoke(con)
assert r['count']==200 and r['ok'], r
snap=m.enterprise_release_snapshot_1250(con)
assert snap['status']=='READY' and snap['phase_count']==200
print('PHASE_1051_1250_TEST_PASS', r['count'])
