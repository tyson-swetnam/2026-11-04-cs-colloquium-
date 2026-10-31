# Slide 21 · Data lakehouse

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-21)

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Low-cost storage, with governance and ACID transactions | partially supported | DuckLake docs: full ACID, snapshot isolation; local demo shows rollback and a rejected conflicting commit, but only in one DuckDB process with a DuckDB catalog (the docs' single-client setup; multi-user remote use needs PostgreSQL, not tested). Access control "is not per se a feature of DuckLake"; MESA governance is a planned objective, and no source says iRODS policy governs the lakehouse. | "Low-cost object storage with ACID transactions and time travel; access control via catalog and storage permissions" |
| c2 Figure: MESA proposal · NSF Award #2632685 | supported | NSF Award API: MESA, UNM, PI Swetnam, NAIRR program, 2026-07-15 to 2029-05-31; abstract names a "data lakehouse". Figure itself not checked (proposal not public). | none |
| c3 DuckLake + Parquet give database behaviour over plain files | supported | DuckLake home page and spec v1.1; demo reads a lake Parquet file directly. Small writes are inlined in the catalog by default. | none |
| c4 Time travel: rewind to the day the paper was submitted | supported | DuckLake time-travel docs; demo returns the old state by version and timestamp. Only if snapshots were not expired. | none |
| c5 Lakehouse = object-store economics + database guarantees | supported | Armbrust et al., CIDR 2021 definition. | none |
| c6 DuckLake, Iceberg, Delta Lake are table formats | supported | Project home pages. | none |
| c7 Structured, semi-structured and unstructured data underneath | supported (general lakehouse statement) | CIDR 2021 Figure 1. Caveat: DuckLake itself manages only tabular Parquet data; how MESA handles unstructured files is not in any fetched source. | none |
| c8 MESA's lakehouse is DuckLake | supported (project-reported) | MESA public site. Code not checked. | none |

## Evidence

- `src/01_fetch_sources.py` fetches the NSF award, DuckLake/Iceberg/Delta pages, the CIDR 2021 paper and the MESA page (to `data/raw/sources/`, gitignored, logged in MANIFEST.yaml).
- `src/02_ducklake_demo.py` builds a small DuckLake (DuckDB 2.0.0) and writes `data/processed/ducklake_demo.json`: Parquet files on disk, rollback, concurrent commits, time travel. Storage was a local folder, not S3; both connections ran in one DuckDB process with a DuckDB-file catalog (single-client setup), so multi-user or remote writers were not tested.
- `src/03_check_quotes.py` checks every quote in `data/raw/research/facts.csv` against the saved sources (`data/processed/quote_check.json`).
