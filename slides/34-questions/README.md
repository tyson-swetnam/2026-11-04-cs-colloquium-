# Slide 34 · Questions?

Section: 04 · Stop worrying · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-34)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` MESA award OAC-2632685 · [NAIRR] | partially supported | NSF Award API: UNM, PI Swetnam, OAC, $4.62M, 07/2026–05/2029; funding program "NAIRR-Nat AI Research Resource". No other OAC/DBI award found. | "…under Award OAC-2632685 (NAIRR program)." Drop the placeholders. |
| `c2` idss-mesa.github.io · github.com/idss-mesa | partially supported | Site returns HTTP 200 and links to github.com/idss-mesa; the org page could not be fetched from this session. | Click both links on the day. |
| `c3` six early-adopter award numbers | supported | NSF Award API for 2217817 (NEON/Battelle), 2153040 (ESIIL), 2335029 (NCEMS), 2438843 (NSCORE), 2535855 (EHT, MIT); AIIRA page gives NIFA 2021-67021-35329. | Keep as is. |
| `c4` names and hosts in the notes | partially supported | ESIIL site and NSF title: "Innovation & **Impact** Lab", not "Inclusion". NSCORE full name ends "…to Environmental Change". | Fix the two names in the notes. |
| `c5` these six are MESA early adopters | partially supported | Award abstract and MESA site name ESIIL, NCEMS, AIIRA, EHT. NEON appears only as a data source; NSCORE is not mentioned anywhere public. | Confirm NEON and NSCORE before calling them early adopters. |
| `c6` name and email | supported | NSF PI fields: Tyson L Swetnam, tswetnam@unm.edu (PhD not checked). | — |

Other notes: an earlier award with the same title, 2608717 (University of Arizona, 06–08/2026, inactive), looks like the version before the move to UNM. You don't need to list it. The NIFA record for AIIRA (accession 1027030) couldn't be read as text, so the NIFA number comes from Iowa State's AIIRA page.

## Evidence

- `src/01_fetch.py`: NSF Award API records for all six NSF numbers, the AIIRA keyword search and link checks. Output: `data/processed/awards.json`.
- `src/02_nifa_and_names.py`: AIIRA, ISU, ESIIL and MESA pages. Output: `data/processed/fetch_status_02.json`.
- `src/00_write_facts.py`: writes `data/raw/research/facts.csv` (26 quotes).
- `src/03_check_quotes.py`: confirms each quote appears in its saved source. Output: `data/processed/quote_checks.json`, 26/26 found.
- Fetched documents are in `data/raw/sources/` (gitignored, logged in `MANIFEST.yaml`).
