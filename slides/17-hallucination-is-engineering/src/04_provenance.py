"""Control 4, "I cannot audit it": record every step in DuckLake, then replay any run.

An agent session is logged to a DuckLake catalog: the request, each tool call (inputs,
outputs, a hash of the output) and the record it wrote. Later the record is overwritten.
The audit then (a) reads the catalog as of the original snapshot to see exactly what the
agent wrote, and (b) re-executes every logged tool call from its logged inputs and compares
output hashes, so a reviewer can tell a reproducible run from a changed world.

Output: data/processed/provenance_{snapshots,replay}.csv; the catalog itself in
data/processed/provenance/ (rebuilt each run, not committed).
"""

from __future__ import annotations

import hashlib
import json
import shutil

import duckdb
import pandas as pd

import config
from evidence.citations import Checker, parse
from evidence.ontology import OLSClient, validate

LAKE = config.PROCESSED / "provenance"


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]


def rows(con, sql: str, params=None) -> list[tuple]:
    """Run a query and fetch everything (DuckDB 2 refuses new work while a result is open)."""
    return con.execute(sql, params or []).fetchall()


def tools():
    ols = OLSClient(config.CACHE / "ols", config.UA)
    refs = Checker(config.CACHE / "citations", config.UA)
    return {
        "resolve_term": lambda a: vars(validate(ols, a["text"], a["curie"], tuple(a["allowed"]))),
        "check_citation": lambda a: vars(refs.check(parse(a["citation"]))),
    }


def main() -> None:
    shutil.rmtree(LAKE, ignore_errors=True)
    LAKE.mkdir(parents=True)
    con = duckdb.connect()
    con.sql("INSTALL ducklake; LOAD ducklake;")
    con.sql(f"ATTACH 'ducklake:{LAKE / 'catalog.ducklake'}' AS lake (DATA_PATH '{LAKE / 'data'}')")
    con.sql("CREATE TABLE lake.runs (run_id VARCHAR, request VARCHAR, model VARCHAR)")
    con.sql("CREATE TABLE lake.steps (run_id VARCHAR, step INTEGER, tool VARCHAR, input_json VARCHAR, output_json VARCHAR, output_sha VARCHAR)")
    con.sql("CREATE TABLE lake.records (run_id VARCHAR, record_json VARCHAR)")

    # --- the agent session ---------------------------------------------------------------
    run_id, call = "run-0001", tools()
    plan = [
        ("resolve_term", {"text": "mouse", "curie": "NCBITaxon:10090", "allowed": ["NCBITaxon"]}),
        ("resolve_term", {"text": "RNA-seq", "curie": "OBI:0001271", "allowed": ["OBI"]}),
        ("check_citation", {"citation": "Amil Merchant, Simon Batzner, Samuel S. Schoenholz. Scaling deep learning for materials discovery. Nature, 2023. doi: 10.1038/s41586-023-06735-9"}),
    ]
    con.execute("INSERT INTO lake.runs VALUES (?, ?, ?)", [run_id, "Register the mouse liver RNA-seq dataset", "any (logged per run)"])
    for i, (tool, args) in enumerate(plan, 1):
        out = call[tool](args)
        con.execute("INSERT INTO lake.steps VALUES (?, ?, ?, ?, ?, ?)", [run_id, i, tool, json.dumps(args), json.dumps(out), digest(out)])
    record = {"organism": "NCBITaxon:10090", "assay": "OBI:0001271", "doi": "10.1038/s41586-023-06735-9"}
    con.execute("INSERT INTO lake.records VALUES (?, ?)", [run_id, json.dumps(record)])
    written_at = rows(con, "SELECT max(snapshot_id) FROM lake.snapshots()")[0][0]

    # --- later, someone overwrites the record --------------------------------------------
    con.execute("UPDATE lake.records SET record_json = ? WHERE run_id = ?", [json.dumps(dict(record, organism="NCBITaxon:10116")), run_id])

    # --- the audit -----------------------------------------------------------------------
    now = json.loads(rows(con, "SELECT record_json FROM lake.records")[0][0])
    then = json.loads(rows(con, f"SELECT record_json FROM lake.records AT (VERSION => {written_at})")[0][0])
    replay = []
    for step, tool, inp, sha in rows(con, f"SELECT step, tool, input_json, output_sha FROM lake.steps AT (VERSION => {written_at}) ORDER BY step"):
        again = call[tool](json.loads(inp))
        replay.append({"step": step, "tool": tool, "logged_sha": sha, "replayed_sha": digest(again), "reproduced": digest(again) == sha})
    snaps = pd.DataFrame(rows(con, "SELECT snapshot_id, snapshot_time, changes FROM lake.snapshots() ORDER BY snapshot_id"), columns=["snapshot_id", "snapshot_time", "changes"])
    snaps["changes"] = snaps["changes"].astype(str)
    snaps.to_csv(config.PROCESSED / "provenance_snapshots.csv", index=False)
    pd.DataFrame(replay).to_csv(config.PROCESSED / "provenance_replay.csv", index=False)
    print(snaps[["snapshot_id", "changes"]].to_string(index=False))
    print(f"record now: organism={now['organism']}; as written at snapshot {written_at}: organism={then['organism']}")
    print(pd.DataFrame(replay).to_string(index=False))


if __name__ == "__main__":
    main()
