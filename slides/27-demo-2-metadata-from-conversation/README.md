# Slide 27 · Demo 2: metadata from a conversation

> **Revised deck.** Demo 2 in the revised deck (2026-10-31) is "Metadata from a conversation" (was: finding data across silos).

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-27)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c2 Claude Desktop + MESA MCP writes ontology-checked AVUs, shown in the Portal | partially supported | MESA docs: mesa-mcp writes AVUs with the CURIE in the unit slot; Portal shows the same AVUs. But MESA documents mesa-mcp for Claude Code, Codex, Antigravity and OpenCode, and Claude Desktop only through the Formation connector. Claude Desktop can run it if added by hand. | "In Claude (Code or Desktop) the researcher describes the collection; MESA's mesa-mcp server looks each term up in OLS and writes iRODS AVUs, which the MESA Portal shows." |
| c3 AVU table on the slide | partially supported | CURIEs are right (OLS4), DP1.10022.001 is NEON's pitfall-trap ground beetles with data at 47 sites (NEON API). The layout is wrong: MESA puts the CURIE in the **unit** column (its docs, and real MESA AVUs such as `ncbitaxon.carabidae · Carabidae · NCBITaxon:41073` and `uo.millimeter · bet_parataxonomistID.totalLength · UO:0000016`). | Move CURIEs to the unit column, e.g. `ncbitaxon.carabidae · Carabidae · NCBITaxon:41073`; `uo.millimeter · elytra_length · UO:0000016`; better, use the AVUs from the recorded run. |
| c4 (notes) server refuses any term that will not resolve | unverified | Not in public docs; it is in MESA code (out of scope). Same as slide 25 c4. | "looks each term up in OLS" rather than "refuses" unless the demo shows a refusal |
| c5 (notes) AVUs are iRODS's native triples, readable by any iRODS client | supported | iRODS imeta docs; MESA AVUs read here with CyVerse's own (non-MESA) Data Store server | - |
| c6 (notes) 65,830 beetles, ~53,000 images, 47 sites, r = 0.98 | unverified | Report URL hit a CyVerse bot check (not bypassed); GitHub repo out of scope. 47 = every site in the NEON product. | Present as the project's own results |
| c7 (notes) collection at /iplant/home/tswetnam/neon-beetle-seg/ with a public report | unverified | CyVerse's public Data Store server says "Path is not publicly accessible" (it only covers /iplant/home/shared, so not proof). | Open the report link in a private window before the talk |
| c8 MESA · NSF Award #2632685 | supported | NSF Award API | - |

c1 is superseded (old demo).

## Evidence

- `src/01_check.py`: OLS4 terms, NEON product (site count, months), NSF award, slide AVU layout -> `data/processed/terms.csv`, `neon_product.csv`, `nsf_award.csv`, `avu_layout.csv`.
- `src/02_datastore.py`: anonymous read-only calls to CyVerse's public Data Store MCP server (https://mcp-public.cyverse.ai/mcp); only list/get-metadata/search tools were used.
- `src/03_avu_compare.py`: AVUs MESA wrote on `/iplant/home/shared/mesa/lakehouse/neon/neon-ducklake/sites/KONZ/raw/DP1.10022.001` -> `data/processed/mesa_avus_observed.csv`.
- `src/04_facts.py`: writes `data/raw/research/facts.csv` and checks every quote against the saved source.
- Sources are under `data/raw/sources/` (gitignored), logged in `MANIFEST.yaml`.

Not reached: the public report at data.cyverse.org (redirected to unblockme.cyverse.org) and the neon-beetle-seg GitHub repository (out of scope).
