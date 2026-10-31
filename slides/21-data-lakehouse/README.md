# Slide 21 · Data lakehouse

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-21)

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Low-cost storage, with governance and ACID transactions | partially supported | DuckLake docs: full ACID, snapshot isolation; local demo shows rollback and a rejected conflicting commit. DuckLake docs: access control "is not per se a feature of DuckLake". | "Low-cost object storage with ACID transactions and time travel; governance from the catalog and iRODS policy" |
| c2 Figure: MESA proposal · NSF Award #2632685 | supported | NSF Award API: MESA, UNM, PI Swetnam, NAIRR program, 2026-07-15 to 2029-05-31; abstract names a "data lakehouse". Figure itself not checked (proposal not public). | none |
| c3 DuckLake + Parquet give database behaviour over plain files | supported | DuckLake home page and spec v1.1; demo reads a lake Parquet file directly. Small writes are inlined in the catalog by default. | none |
| c4 Time travel: rewind to the day the paper was submitted | supported | DuckLake time-travel docs; demo returns the old state by version and timestamp. Only if snapshots were not expired. | none |
| c5 Lakehouse = object-store economics + database guarantees | supported | Armbrust et al., CIDR 2021 definition. | none |
| c6 DuckLake, Iceberg, Delta Lake are table formats | supported | Project home pages. | none |
| c7 Structured, semi-structured and unstructured data underneath | partially supported | CIDR 2021 Figure 1; DuckLake stores tables as Parquet only. | Notes: unstructured files sit alongside in object storage / iRODS, referenced from tables. |
| c8 MESA's lakehouse is DuckLake | supported (project-reported) | MESA public site. Code not checked. | none |

## Evidence

- `src/01_fetch_sources.py` fetches the NSF award, DuckLake/Iceberg/Delta pages, the CIDR 2021 paper and the MESA page (to `data/raw/sources/`, gitignored, logged in MANIFEST.yaml).
- `src/02_ducklake_demo.py` builds a small DuckLake (DuckDB 2.0.0) and writes `data/processed/ducklake_demo.json`: Parquet files on disk, rollback, concurrent commits, time travel. Storage was a local folder, not S3.
- `src/03_check_quotes.py` checks every quote in `data/raw/research/facts.csv` against the saved sources (`data/processed/quote_check.json`).
