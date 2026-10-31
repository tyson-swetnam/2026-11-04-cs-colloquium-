# Slide 26 · Move the work to the data

> **Revised deck.** The revised deck (2026-10-31) rewrites this slide as the NEON ground-beetle worked example; the earlier repository claims are superseded.

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-26)

## Findings (2026-10-31)

Old repository claims c1–c6 are superseded by the rewrite. Run `uv run python slides/26-move-the-work-to-the-data/src/01_check.py` to rebuild `data/processed/checks.json`.

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c7 DP1.10022.001: 47 sites, 2013–2026 | supported | NEON Data API: "Ground beetles sampled from pitfall traps", ACTIVE, 47 sites, 2013-07 to 2026-10 | keep |
| c8 Biorepository 188,522 records, most on GBIF; 53,257 images | partially supported | Portal API: 11 pitfall-trap collections sum to 188,522 exactly; GBIF datasets sum to 145,263 (77%). 47,832 of the records are non-beetle bycatch. Image count not checked | "188,522 pitfall-trap specimen records in 11 collections, 77% also on GBIF" |
| c9 four verbs, GPU, CURIEs, DuckLake | partially supported | OLS4: NCBITaxon:41073 = Carabidae, UO:0000016 = millimeter, neither obsolete. GPU and DuckLake details not checked (project repo not read) | keep |
| c10 65,830 beetles; r = 0.98 | unverified | Project's own result; public report blocked from here (307 to unblockme.cyverse.org) | present as the project's result |
| c11 outputs on CyVerse Data Store | unverified | Same block; check the link from a normal network before the talk | keep |
| c12 MESA · NSF Award #2632685 (new) | supported | NSF Award API: MESA, UNM, PI Swetnam, start 2026-07-15 | keep |
| c13 notes: 20 domains, Jul 2013–Sep 2026 (new) | partially supported | 20 domains confirmed; API now lists Oct 2026 for 5 sites | "July 2013 to October 2026 (latest months provisional)" |
| c14 notes: 145,906 pinned, 826 taxa (new) | unverified | Needs full data download; not computed | say the source |
| c15 notes: 20,698 site-linked, 8% long, mostly unphotographed (new) | unverified | Project figures. Only 5,961 of 145,263 GBIF records have an image, which fits "mostly unphotographed" | keep, as project figures |

Status and the plan for each claim are in [`claims.yaml`](claims.yaml).

## Evidence

- `src/01_check.py`: NEON, Biorepository, GBIF, OLS4 and NSF API checks
- `data/processed/checks.json`: computed counts
- `data/raw/research/facts.csv`: exact quotes from the fetched API responses (saved in `data/raw/sources/`, gitignored)
