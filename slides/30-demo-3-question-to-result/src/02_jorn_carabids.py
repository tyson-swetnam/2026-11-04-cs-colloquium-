"""Slide 30: reproduce the demo's answer from NEON's own API, independent of the agent and the lakehouse.

The recorded demo asks "what is the most common ground beetle at the Jornada Experimental Range (JORN)?" and the agent,
reading the neon-beetle-seg DuckLake, answers: Tetragonoderus pallidus, 616 of 1,056 carabid individuals (58.3%), in
417 of 732 records, 2015-05-28 to 2025-09-10. This script downloads the same NEON data product (DP1.10022.001, ground
beetles from pitfall traps; table bet_sorting, basic package) for JORN from data.neonscience.org, keeps carabid
samples collected by 2025-09-10, and ranks taxa by individuals.

Status 2026-11-02: NEON's product listing loads, but its data endpoints return HTTP 403 {"detail":"Access Denied"}
without an API token, so this check has not run yet. With a free NEON token (https://data.neonscience.org/data-api/):

    NEON_TOKEN=... uv run python slides/30-demo-3-question-to-result/src/02_jorn_carabids.py

Writes data/processed/jorn_carabid_ranking.csv and data/processed/jorn_check.json. Downloads are cached in
data/raw/sources/neon/ (MANIFEST.yaml; the CSVs are not committed). The DuckLake on the Data Store was not read
directly: data.cyverse.org/dav-anon redirects this session to a bot check, which was not bypassed.

    uv run python slides/30-demo-3-question-to-result/src/02_jorn_carabids.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from evidence.fetch import record  # noqa: E402

API = "https://data.neonscience.org/api/v0"
PRODUCT, SITE, CUTOFF = "DP1.10022.001", "JORN", "2025-09-10"
UA = {"User-Agent": "colloquium-evidence/0.1 (UNM CARC research)"}
if os.environ.get("NEON_TOKEN"):  # NEON's data endpoints answered 403 "Access Denied" without one (2026-11-02)
    UA["X-API-Token"] = os.environ["NEON_TOKEN"]
RAW = HERE / "data" / "raw" / "sources" / "neon"
OUT = HERE / "data" / "processed"
DEMO = {"taxon": "Tetragonoderus pallidus", "individuals": 616, "total_individuals": 1056, "share_pct": 58.3,
        "records": 417, "total_records": 732, "first": "2015-05-28", "last": "2025-09-10"}


def get(url: str) -> requests.Response:
    for attempt in range(4):
        r = requests.get(url, headers=UA, timeout=120)
        if r.status_code not in (429, 503):
            r.raise_for_status()
            time.sleep(0.4)
            return r
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()
    return r


def sorting_files() -> list[Path]:
    product = get(f"{API}/products/{PRODUCT}").json()["data"]
    months = next(s for s in product["siteCodes"] if s["siteCode"] == SITE)["availableMonths"]
    RAW.mkdir(parents=True, exist_ok=True)
    paths = []
    for month in months:
        if month > CUTOFF[:7]:
            continue
        files = get(f"{API}/data/{PRODUCT}/{SITE}/{month}?package=basic").json()["data"]["files"]
        for f in files:
            if "bet_sorting" in f["name"] and f["name"].endswith(".csv"):
                dest = RAW / f["name"]
                if not dest.exists():
                    dest.write_bytes(get(f["url"]).content)
                    record(dest, url=f"{API}/data/{PRODUCT}/{SITE}/{month}?package=basic",
                           source="NEON Data API, DP1.10022.001 bet_sorting (basic)")
                paths.append(dest)
    return paths


def main() -> int:
    paths = sorting_files()
    df = pd.concat([pd.read_csv(p, low_memory=False) for p in paths], ignore_index=True)
    df = df.drop_duplicates(subset=[c for c in ("uid",) if c in df.columns] or None)
    df["collectDate"] = pd.to_datetime(df["collectDate"], utc=True, format="mixed")
    car = df[(df["sampleType"] == "carabid") & (df["collectDate"] <= pd.Timestamp(CUTOFF + "T23:59:59Z"))].copy()
    car["individualCount"] = pd.to_numeric(car["individualCount"], errors="coerce").fillna(0)
    rank = (car.groupby(["scientificName", "taxonRank"], dropna=False)
               .agg(individuals=("individualCount", "sum"), records=("individualCount", "size"))
               .sort_values("individuals", ascending=False).reset_index())
    total_ind, total_rec = int(car["individualCount"].sum()), int(len(car))
    rank["share_pct"] = (100 * rank["individuals"] / total_ind).round(1)
    OUT.mkdir(parents=True, exist_ok=True)
    rank.to_csv(OUT / "jorn_carabid_ranking.csv", index=False)
    top = rank.iloc[0]
    result = {
        "source": f"{API}/data/{PRODUCT}/{SITE} (bet_sorting, basic), {len(paths)} monthly files",
        "neon": {"top_taxon": top["scientificName"], "individuals": int(top["individuals"]), "records": int(top["records"]),
                 "total_individuals": total_ind, "total_records": total_rec, "share_pct": float(top["share_pct"]),
                 "first": str(car["collectDate"].min().date()), "last": str(car["collectDate"].max().date())},
        "demo": DEMO,
    }
    result["top_taxon_matches"] = DEMO["taxon"] in result["neon"]["top_taxon"]
    (OUT / "jorn_check.json").write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result["neon"], indent=1))
    print(rank.head(8).to_string(index=False))
    return 0 if result["top_taxon_matches"] else 1


if __name__ == "__main__":
    sys.exit(main())
