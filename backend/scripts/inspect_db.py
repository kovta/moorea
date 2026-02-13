import sqlite3, pathlib, sys
p = pathlib.Path("backend/dev.db")
if not p.exists():
    print("dev.db not found")
    sys.exit(0)
conn = sqlite3.connect(p)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:")
for t in tables:
    print(" -", t)
for t in ("users","moodboards","waitlist_users"):
    try:
        cnt = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t} count: {cnt}")
    except Exception:
        pass
conn.close()
