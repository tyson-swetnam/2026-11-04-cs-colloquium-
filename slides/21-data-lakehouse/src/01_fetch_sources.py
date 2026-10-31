"""Fetch the primary sources for slide 21 (NSF award, DuckLake docs, Iceberg, Delta Lake, Lakehouse paper, MESA site)."""
import json, sys
from pathlib import Path
import requests
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evidence.http import CachedGet
from evidence.fetch import record

HERE = Path(__file__).resolve().parents[1]
UA = "colloquium-evidence/0.1 (UNM CARC research)"
get = CachedGet(HERE / "data/cache", UA)
SRC = HERE / "data/raw/sources"
SRC.mkdir(parents=True, exist_ok=True)

PAGES = {
    "nsf_award_2632685.json": ("https://api.nsf.gov/services/v1/awards/2632685.json?printFields=id,title,awardeeName,pdPIName,startDate,expDate,fundProgramName,orgLongName2,estimatedTotalAmt,abstractText,transType", "NSF Award API"),
    "ducklake_home.html": ("https://ducklake.select/", "DuckLake project site"),
    "ducklake_manifesto.html": ("https://ducklake.select/manifesto/", "DuckLake manifesto"),
    "ducklake_docs_index.html": ("https://ducklake.select/docs/stable/", "DuckLake docs"),
    "ducklake_duckdb_intro.html": ("https://ducklake.select/docs/stable/duckdb/introduction", "DuckLake docs"),
    "ducklake_time_travel.html": ("https://ducklake.select/docs/stable/duckdb/usage/time_travel", "DuckLake docs"),
    "ducklake_snapshots.html": ("https://ducklake.select/docs/stable/duckdb/usage/snapshots", "DuckLake docs"),
    "ducklake_conflicts.html": ("https://ducklake.select/docs/stable/duckdb/advanced_features/conflict_resolution", "DuckLake docs"),
    "ducklake_spec_intro.html": ("https://ducklake.select/docs/stable/specification/introduction", "DuckLake specification"),
    "iceberg_home.html": ("https://iceberg.apache.org/", "Apache Iceberg site"),
    "delta_home.html": ("https://delta.io/", "Delta Lake site"),
    "mesa_home.md": ("https://idss-mesa.github.io/okf/concepts/home.md", "MESA public site"),
}
for name, (url, source) in PAGES.items():
    status, body = get(url)
    print(status, name, len(body))
    if status == 200:
        (SRC / name).write_text(body, encoding="utf-8")
        record(SRC / name, url=url, source=source)

# Lakehouse paper (binary PDF): fetched directly, once.
pdf = SRC / "cidr2021_paper17_lakehouse.pdf"
url = "https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf"
if not pdf.exists():
    r = requests.get(url, headers={"User-Agent": UA}, timeout=120)
    r.raise_for_status()
    pdf.write_bytes(r.content)
    record(pdf, url=url, source="CIDR 2021", note="Armbrust, Ghodsi, Xin, Zaharia: Lakehouse")

# Added: governance (access control), transactions, encryption pages.
MORE = {
    "ducklake_access_control.html": "https://ducklake.select/docs/stable/duckdb/guides/access_control",
    "ducklake_transactions.html": "https://ducklake.select/docs/stable/duckdb/advanced_features/transactions",
    "ducklake_storage.html": "https://ducklake.select/docs/stable/duckdb/usage/choosing_storage",
}
for name, url in MORE.items():
    status, body = get(url)
    print(status, name, len(body))
    if status == 200:
        (SRC / name).write_text(body, encoding="utf-8")
        record(SRC / name, url=url, source="DuckLake docs")

# Processed copy of the award record (no contact fields).
aw = json.loads((SRC / "nsf_award_2632685.json").read_text())["response"]["award"][0]
keep = {k: aw[k] for k in ("id", "title", "awardeeName", "pdPIName", "startDate", "expDate", "fundProgramName",
                           "orgLongName2", "estimatedTotalAmt", "transType", "abstractText") if k in aw}
(HERE / "data/processed").mkdir(parents=True, exist_ok=True)
(HERE / "data/processed/nsf_award_2632685.json").write_text(json.dumps(keep, indent=2))
print({k: v for k, v in keep.items() if k != "abstractText"})
