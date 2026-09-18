import sqlite3, app

conn=sqlite3.connect(":memory:")
# create the representative tables required by the probes
for t in set(app.PHASE_851_1050_TABLES.values()):
    conn.execute(f"CREATE TABLE {t} (id INTEGER)")
    conn.execute(f"INSERT INTO {t}(id) VALUES (1)")
conn.commit()
assert len(app.PHASE_851_1050)==200
r=app.phases_851_1050_smoke(conn)
assert r["ok"] and r["count"]==200
s=app.enterprise_release_snapshot_1050(conn)
assert s["smoke_ok"] and s["status"]=="READY"
print("PHASE_851_1050_TEST_PASS 200")
