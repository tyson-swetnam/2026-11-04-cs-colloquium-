# Slide 30 · First pilot · NCEMS

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-30)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` MCP servers pointed at NCEMS data on CyVerse, this summer | unverified (speaker-reported) | Sources cover only the setting: MESA award names NCEMS as a planned test partner (future tense); NCEMS award 2335029 says CyVerse provides its cyberinfrastructure; MESA site says the stack is in use on the Data Store, with no NCEMS collection named. No public record of the pilot itself. | "MESA's MCP servers pointed at NCEMS collections on the CyVerse Data Store (summer 2026 pilot; collection link to be added)" |
| `c2` Metadata read, terms resolved via OLS/OBO, written back as AVUs | partially supported (capability only; pilot result speaker-reported) | mesa-mcp docs: `mesa_ols_*` ("OBO/OLS ontologies") and `mesa_avu_*` tools (CURIE in the unit slot). Docs do not name the EBI OLS endpoint. No public before/after AVU counts. | "Existing metadata read, terms matched to OBO ontologies via the Ontology Lookup Service (OLS), written back as iRODS AVUs" |
| `c3` Every write in DuckLake; session left as an OKF bundle | partially supported (DuckLake capability only); OKF half unverified, speaker-reported | mesa-ducklake docs: every AVU write mirrored, but history is off if no catalog DSN is set. Docs use OKF (Open Knowledge Format) only for the docs site; no session-to-OKF export is described. | "Every metadata write logged in DuckLake (history catalog enabled); session record exported as an Open Knowledge Format (OKF) bundle, link to be added" (or drop the OKF half) |
| `c4` (new, notes) Nothing copied, nothing new to operate | partially supported | DuckLake Parquet can live inside the iRODS project; but a catalog (DuckDB/Postgres) and the MCP servers still run somewhere. | "nothing copied, and no new service for NCEMS to run" |
| `c5` (new, notes) Everything is open source | partially supported | MESA site marks mesa-portal and mesa-forge repos private. | "The MCP servers and metadata tools are open source at github.com/idss-mesa" |
| `c6` (new) iRODS zone or S3 bucket joins the mesh without moving files | partially supported | iRODS federation is the stated design; S3/OSN buckets are only mounted (`osn-mount.sh`). | "a federated iRODS zone, or an S3 bucket mounted in place; no files move" |
| `c7` (new) MESA · NSF Award #2632685 | supported | NSF Award API. | — |
| `c8` (new) Title "Already running on real collections", "First pilot · NCEMS", "Done" | unverified (speaker-reported) | Title implies ongoing work on several collections; notes say one run this summer on NCEMS. MESA site names NCEMS only as an "anchor science community"; nothing public on a first pilot or current runs. | "First pilot · NCEMS / Tried on a real collection / Done (summer 2026)" |

What the speaker can add to close the gaps: the NCEMS collection path(s), before/after AVU counts, a DuckLake snapshot and the OKF bundle (or a link to them). All pilot results are currently speaker-reported; MESA docs are developer-written (several pages AI-generated) and the MESA code was not checked.

Blocked: `ncems.cyverse.org` reset the connection; the anonymous Data Store WebDAV path redirected to a CyVerse "Unblock Me" page, which was not pursued.

## Evidence

- `src/01_check.py` fetches the sources, checks every quote in `data/raw/research/facts.csv` against the saved text, and writes `data/processed/check_summary.json`.
- Fetched documents are in `data/raw/sources/` (gitignored) with `MANIFEST.yaml`.
