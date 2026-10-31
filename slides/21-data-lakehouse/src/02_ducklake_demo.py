"""Runnable DuckLake demo for slide 21.

Shows, on this machine with DuckDB + the ducklake extension:
  1. data lands as plain Parquet files under DATA_PATH (local folder here, standing in for object storage);
  2. a multi-statement transaction is all-or-nothing (ROLLBACK leaves no trace, no new snapshot);
  3. two connections, each in its own transaction, commit concurrently;
     the conflict on the same row is detected and one commit fails;
  4. time travel: query the table AT (VERSION => n) and AT (TIMESTAMP => t), i.e. "rewind to the day the
     paper was submitted".
Writes data/processed/ducklake_demo.json. The lake itself is built in a scratch dir under data/cache/.
"""
import json, shutil, time, datetime as dt
from pathlib import Path
import duckdb

HERE = Path(__file__).resolve().parents[1]
WORK = HERE / "data/cache/ducklake_demo"
shutil.rmtree(WORK, ignore_errors=True)
WORK.mkdir(parents=True)
CATALOG = WORK / "catalog.ducklake"
DATA = WORK / "lake_files"
out = {"duckdb_version": duckdb.__version__}


def connect():
    c = duckdb.connect()
    c.execute("LOAD ducklake;")
    c.execute(f"ATTACH 'ducklake:{CATALOG}' AS lake (DATA_PATH '{DATA}/', DATA_INLINING_ROW_LIMIT 0)")  # no inlining: every write goes to Parquet
    c.execute("USE lake")
    return c


a = connect()
out["ducklake_extension_version"] = a.execute(
    "select extension_version from duckdb_extensions() where extension_name='ducklake'").fetchone()[0]
a.execute("CREATE TABLE obs (site VARCHAR, year INT, value DOUBLE)")
a.execute("INSERT INTO obs VALUES ('SRER', 2024, 1.0), ('JORN', 2024, 2.0)")
v_submitted = a.execute("SELECT max(snapshot_id) FROM ducklake_snapshots('lake')").fetchone()[0]
t_submitted = a.execute("SELECT get_current_timestamp()").fetchone()[0]
time.sleep(1.2)

# 1. Parquet files on disk
parquet = sorted(str(p.relative_to(WORK)) for p in DATA.rglob("*.parquet"))
out["parquet_files_after_first_insert"] = parquet

# 2. Atomicity: a failed / rolled-back transaction leaves nothing behind
snaps_before = a.execute("SELECT count(*) FROM ducklake_snapshots('lake')").fetchone()[0]
a.execute("BEGIN TRANSACTION")
a.execute("INSERT INTO obs VALUES ('BAD', 1900, -999)")
a.execute("DELETE FROM obs WHERE site='SRER'")
a.execute("ROLLBACK")
out["rollback"] = {
    "rows_after_rollback": a.execute("SELECT count(*) FROM obs").fetchone()[0],
    "bad_rows": a.execute("SELECT count(*) FROM obs WHERE site='BAD'").fetchone()[0],
    "snapshots_before": snaps_before,
    "snapshots_after": a.execute("SELECT count(*) FROM ducklake_snapshots('lake')").fetchone()[0],
}

# 3. Concurrency: a second connection (same DuckDB process, own transaction), both update the same row.
# The catalog here is a DuckDB file shared by two connections of one instance: the single-client setup in the
# DuckLake docs. SQLite (multiple local clients) and PostgreSQL (multi-user, remote clients) were not tested.
b = a.cursor()
b.execute("USE lake")
a.execute("BEGIN TRANSACTION"); b.execute("BEGIN TRANSACTION")
a.execute("UPDATE obs SET value = 10 WHERE site='JORN'")
b.execute("UPDATE obs SET value = 20 WHERE site='JORN'")
a.execute("COMMIT")
try:
    b.execute("COMMIT"); b_result = "committed"
except Exception as e:  # expected: conflict detected
    b_result = f"{type(e).__name__}: {str(e).splitlines()[0][:300]}"
# Concurrent inserts into the same table by two instances: should both succeed (retry without rewriting files).
a.execute("BEGIN TRANSACTION"); b.execute("BEGIN TRANSACTION")
a.execute("INSERT INTO obs VALUES ('A_SITE', 2025, 3.0)")
b.execute("INSERT INTO obs VALUES ('B_SITE', 2025, 4.0)")
a.execute("COMMIT")
try:
    b.execute("COMMIT"); b_insert = "committed"
except Exception as e:
    b_insert = f"{type(e).__name__}: {str(e).splitlines()[0][:300]}"
out["concurrency"] = {
    "conflicting_update_second_commit": b_result,
    "jorn_value_now": a.execute("SELECT value FROM obs WHERE site='JORN'").fetchone()[0],
    "concurrent_insert_second_commit": b_insert,
    "rows_now": a.execute("SELECT count(*) FROM obs").fetchone()[0],
}

# 4. Time travel to the 'submitted' snapshot, by version and by timestamp
out["time_travel"] = {
    "submitted_snapshot_version": v_submitted,
    "submitted_timestamp": str(t_submitted),
    "rows_at_version": a.execute(f"SELECT * FROM obs AT (VERSION => {v_submitted}) ORDER BY site").fetchall(),
    "rows_at_timestamp": a.execute(f"SELECT * FROM obs AT (TIMESTAMP => '{t_submitted}'::TIMESTAMPTZ) ORDER BY site").fetchall(),
    "rows_now": a.execute("SELECT * FROM obs ORDER BY site").fetchall(),
}
out["snapshots"] = [list(map(str, r)) for r in a.execute(
    "SELECT snapshot_id, snapshot_time, changes FROM ducklake_snapshots('lake') ORDER BY snapshot_id").fetchall()]
out["parquet_files_final"] = sorted(str(p.relative_to(WORK)) for p in DATA.rglob("*.parquet"))
# Parquet files are plain Parquet: read one directly with no DuckLake involved.
first = DATA.rglob("*.parquet").__next__()
out["plain_parquet_read"] = duckdb.connect().execute(f"SELECT count(*) FROM read_parquet('{first}')").fetchone()[0]
out["run_at"] = dt.datetime.now(dt.timezone.utc).isoformat()

(HERE / "data/processed").mkdir(parents=True, exist_ok=True)
(HERE / "data/processed/ducklake_demo.json").write_text(json.dumps(out, indent=2, default=str))
print(json.dumps(out, indent=2, default=str))
