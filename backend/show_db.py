"""Show the CitrusGuardAI database contents. Run from backend/:  python show_db.py"""
import sqlite3

con = sqlite3.connect("data/citrusguard.db")
con.row_factory = sqlite3.Row

print("=" * 60)
print("CitrusGuardAI DATABASE  (data/citrusguard.db)")
print("=" * 60)

tables = [r[0] for r in con.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'alembic%' ORDER BY name")]
print("\n--- TABLES + ROW COUNTS ---")
for t in tables:
    n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t:22} {n} rows")

print("\n--- ORCHARD ---")
for r in con.execute("SELECT id, name, location, area, crop FROM orchards"):
    print(f"  #{r['id']} {r['name']} | {r['location']} | {r['area']} acres | {r['crop']}")

print("\n--- ZONES A-H (Zone B = demo anomaly) ---")
for r in con.execute("SELECT zone_name, area, health_status, risk_score FROM orchard_zones ORDER BY zone_name"):
    print(f"  Zone {r['zone_name']} | {r['area']} ac | {r['health_status']} | risk {r['risk_score']}/100")

print("\n--- LATEST ALERTS ---")
for r in con.execute("SELECT id, zone_id, alert_type, severity, risk_score, status FROM alerts ORDER BY id DESC LIMIT 5"):
    print(f"  #{r['id']} zone_id={r['zone_id']} | {r['alert_type']} | {r['severity']} | risk {r['risk_score']} | {r['status']}")

print("\n--- LATEST SCANS ---")
for r in con.execute("SELECT id, scan_type, coverage, status, timestamp FROM scans ORDER BY id DESC LIMIT 5"):
    print(f"  #{r['id']} {r['scan_type']} | coverage {r['coverage']}% | {r['status']} | {r['timestamp']}")

print("\n--- USERS ---")
for r in con.execute("SELECT username, role, full_name FROM users"):
    print(f"  {r['username']} ({r['role']}) - {r['full_name']}")

print("\nDone.")
