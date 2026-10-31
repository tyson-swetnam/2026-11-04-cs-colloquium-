"""Build a small DuckLake catalog from this talk's own evidence, for the MCP demo to query.

Tables (each with a description the find_data tool searches):
    talk_claims        every claim in slides/*/claims.yaml with its status
    buildout_ranking   slide 04: each build-out under every measure
    alphafold_open     slide 09: AlphaFold DB predictions fetched anonymously

Output: data/processed/lake/ (DuckLake catalog + Parquet; rebuilt each run, not committed)
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import duckdb
import pandas as pd
import yaml

SLIDE = Path(__file__).resolve().parents[1]
ROOT = SLIDE.parents[1]
LAKE = SLIDE / "data" / "processed" / "lake"

DESCRIPTIONS = {
    "talk_claims": "Every claim made on a slide of this talk, with kind, priority and verification status",
    "buildout_ranking": "Infrastructure build-outs (railroads, highways, telecom, data centers) as cumulative cost and share of GDP",
    "alphafold_open": "AlphaFold protein structure predictions fetched anonymously, with licence and confidence",
}


def claims() -> pd.DataFrame:
    rows = []
    for path in sorted((ROOT / "slides").glob("*/claims.yaml")):
        doc = yaml.safe_load(path.read_text())
        for c in doc.get("claims") or []:
            rows.append({"slide": doc["slide"], "slide_title": doc["title"], "claim_id": c["id"], "text": c["text"], "kind": c["kind"], "status": c["status"]})
    return pd.DataFrame(rows)


def main() -> None:
    shutil.rmtree(LAKE, ignore_errors=True)
    LAKE.mkdir(parents=True)
    tables = {
        "talk_claims": claims(),
        "buildout_ranking": pd.read_csv(ROOT / "slides/04-the-build-out/data/processed/ranking.csv"),
        "alphafold_open": pd.read_csv(ROOT / "slides/09-ai-molecular-science/data/processed/alphafold_open.csv"),
    }
    con = duckdb.connect()
    con.sql("INSTALL ducklake; LOAD ducklake;")
    con.sql(f"ATTACH 'ducklake:{LAKE / 'catalog.ducklake'}' AS lake (DATA_PATH '{LAKE / 'data'}')")
    for name, df in tables.items():
        con.register("df", df)
        con.sql(f"CREATE TABLE lake.{name} AS SELECT * FROM df")
        con.unregister("df")
    (LAKE / "descriptions.json").write_text(json.dumps(DESCRIPTIONS, indent=2))
    for name, df in tables.items():
        print(f"lake.{name}: {len(df)} rows")


if __name__ == "__main__":
    main()
