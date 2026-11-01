# Slide 20 · Funded under NAIRR

> **Revised deck.** The revised deck (2026-10-31) fills this slide (was: three placeholders). The award record below still applies, and the new slide specifics are claims `c4`–`c10`; `c11`–`c14` check the speaker notes. `c1`–`c3` are superseded.

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-20)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c4 NSF-led partnership; since 2024; 940+ projects, 50 states | supported | nairrpilot.org counter: 950 projects, 50 states + DC + PR. NSF's own pages say 800+ and 600+ (older) | Keep "940+" (live counter can change); attribute to nairrpilot.org if asked |
| c5 Operations center at SDSC and TACC "now runs it" | partially supported | NSF, 1 Sep 2026: NAIRR-OC led by SDSC with TACC; award 2616251 started 1 Oct 2026; the pilot portal still runs on nairrpilot.org (SGX3) | "A new NSF operations center, led by SDSC with TACC, is taking over from the pilot." |
| c6 "FREE" GPU/HPC time through one portal | partially supported | Start-up call lists GPU-hours on Bridges-2, Anvil, Expanse, Vista; industry credits; no source says "free" or "no-cost" (the FAQ only says overhead does not apply); access is peer-reviewed, 12 months | "Peer-reviewed allocations: GPU and HPC time and cloud credits ..." |
| c7 Agentic AI on Jetstream2, NRP, FabAID | partially supported | Jetstream2 is a NAIRR provider (its docs). NSF (Oct 2024) lists the Prototype NRP as a NAIRR pilot classroom resource. FabAID (award 2609485) is a data fabric, funded from Data Cyberinfrastructure | "Run agents on Jetstream2 and the National Research Platform (both NAIRR pilot resources); move data with FabAID." |
| c8 Hosted open and commercial models, "National Inference Service" | partially supported | Jetstream2 inference service; TACC Sagebrush (award 2537075) funded for NAIRR but only started 15 Sep 2026, no sign it is in service; Anthropic/OpenAI/Azure access. "National Inference Service": 0 hits in the NSF Award API, NSF pages or the web (nearest name: National Deep Inference Fabric, which is for interpretability) | "Hosted open models (Jetstream2, NRP; TACC Sagebrush funded and coming) and commercial model APIs from industry partners." |
| c9 Early adopters NEON, ESIIL, NCEMS, NSCORE, AIIRA, EHT | partially supported | The abstract names ESIIL, NCEMS, AIIRA and EHT. NEON and NSCORE are not on any public source I found | Name only the four award partners on the slide; say NEON and NSCORE aloud as the speaker's own statement |
| c10 Award #2632685, funded under NAIRR | supported | NSF API: fundProgramName "NAIRR-Nat AI Research Resource"; the MESA site credits IDSS | none |
| c11 Pilot launched January 2024 (notes) | supported | NSF release, 24 Jan 2024 | none |
| c12 25+ private partners; DOE and NIH lead NAIRR Secure (notes) | supported | NSF NAIRR-OC release; nairrpilot.org | none |
| c13 IDSS is "one of three programs that feed NAIRR" (notes) | partially supported | NSF: the NAIRR-OC "will coordinate with projects supported through three NSF programs", one of them IDSS | "... one of three NSF programs the NAIRR Operations Center coordinates with." |
| c14 105 NAIRR Classroom awards (notes) | supported | nairrpilot.org counter | none |

**Code.** `src/02_nairr_check.py` pulls the NSF award records, runs keyword searches and checks every quote in `data/raw/research/facts.csv` against the saved source. Outputs are in `data/processed/` (`nairr_awards.csv`, `keyword_search.csv`, `quote_check.csv`, `project_counts.csv`). Fetched pages are in `data/raw/sources/`, which is gitignored and logged in `MANIFEST.yaml`.

**Not reached.** The NAIRR resource catalog (submit-nairr.xras.org) failed TLS verification through the proxy, and the nairrpilot.org resource list loads by JavaScript. NRP's NAIRR link comes from an NSF page (Oct 2024), not the live catalog.

## Early-adopter logos

Since 2026-11-01 the early-adopter chips show each community's logo (`src/03_early_adopter_logos.py`). The files are the ones the speaker linked, with the AIIRA file taken from its [logo page](https://aiira.iastate.edu/resources/aiira-logo/). Downloads go to `data/raw/sources/logos/` (logged in `MANIFEST.yaml`, not committed). They are trimmed and scaled into `figures/logos/` ([Jetstream2](figures/logos/jetstream2.webp), [NRP](figures/logos/nrp.webp), [NDIF](figures/logos/ndif.webp), [NEON](figures/logos/neon.webp), [ESIIL](figures/logos/esiil.webp), [NCEMS](figures/logos/ncems.webp), [NSCORE](figures/logos/nscore.webp), [AIIRA](figures/logos/aiira.webp), [EHT](figures/logos/eht.webp)), and the alt text keeps each full name, including "operated by Battelle" for NEON.

- **NSCORE**: the linked file (`NSF_NSCORE_lockup_360_200`) is a lockup of the NSF logo and the NSCORE emblem, with no name. NSF funds all six communities and is already in the footer, so the script keeps only the emblem and sets "NSCORE" beside it in the wordmark's blue, rgb(50, 88, 136). The image file downloads normally, although nscore.columbia.edu's pages return 403 to automated requests.
- The **EHT** file is a 662-px Google image thumbnail, which looks fine at this size. eventhorizontelescope.org also returned 403.


- `data/raw/research/facts.csv`: 37 quoted facts from primary sources, each checked word for word by `src/02_nairr_check.py` (`data/processed/quote_check.csv`).
- `data/processed/`: `nairr_awards.csv`, `keyword_search.csv`, `project_counts.csv`, `award_facts.csv`.
- `data/raw/nsf_award_*.json`: NSF Award API records.

Status and the plan for each claim are in [`claims.yaml`](claims.yaml).
