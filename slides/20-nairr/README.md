# Slide 20 · Funded under NAIRR

> **Revised deck.** The revised deck (2026-10-31) fills this slide (was: three placeholders). The award record below still applies, and the new specifics are claims `c4`–`c10`.

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-20)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c4 NSF-led partnership; since 2024; 940+ projects, 50 states | supported | nairrpilot.org counter: 950 projects, 50 states + DC + PR. NSF's own pages say 800+ and 600+ (older) | "Piloted since January 2024: 950 projects in all 50 states, DC and Puerto Rico." |
| c5 Operations center at SDSC and TACC "now runs it" | partially supported | NSF, 1 Sep 2026: NAIRR-OC led by SDSC with TACC; award 2616251 started 1 Oct 2026; the pilot portal still runs on nairrpilot.org (SGX3) | "A new NSF operations center, led by SDSC with TACC, is taking over from the pilot." |
| c6 "FREE" GPU/HPC time through one portal | partially supported | Start-up call lists GPU-hours on Bridges-2, Anvil, Expanse, Vista; industry credits; no source says "free"; access is peer-reviewed, 12 months | "No-cost, peer-reviewed allocations: GPU and HPC time ..." |
| c7 Agentic AI on Jetstream2, NRP, FabAID | partially supported | Jetstream2 is a NAIRR provider (its docs). NRP is free and hosts LLMs, but no NAIRR listing found. FabAID (award 2609485) is a data fabric, funded from Data Cyberinfrastructure | "Run agents on Jetstream2 and the National Research Platform; move data with FabAID." |
| c8 Hosted open and commercial models, "National Inference Service" | partially supported | Jetstream2 inference service; TACC Sagebrush (award 2537075) for NAIRR; Anthropic/OpenAI/Azure access. "National Inference Service": 0 hits in the NSF Award API, NSF pages or the web (nearest name: National Deep Inference Fabric, which is for interpretability) | "Hosted open models (Jetstream2, NRP, TACC Sagebrush) and commercial model APIs from industry partners." |
| c9 Early adopters NEON, ESIIL, NCEMS, NSCORE, AIIRA, EHT | partially supported | The abstract names ESIIL, NCEMS, AIIRA and EHT. NEON and NSCORE are not on any public source I found | Mark NEON and NSCORE as joining, or cite letters |
| c10 Award #2632685, funded under NAIRR | supported | NSF API: fundProgramName "NAIRR-Nat AI Research Resource"; the MESA site credits IDSS | none |
| c11 Pilot launched January 2024 (notes) | supported | NSF release, 24 Jan 2024 | none |
| c12 25+ private partners; DOE and NIH lead NAIRR Secure (notes) | supported | NSF NAIRR-OC release; nairrpilot.org | none |
| c13 IDSS is "one of three programs that feed NAIRR" (notes) | partially supported | NSF: the NAIRR-OC "will coordinate with projects supported through three NSF programs", one of them IDSS | "... one of three NSF programs the NAIRR Operations Center coordinates with." |
| c14 105 NAIRR Classroom awards (notes) | supported | nairrpilot.org counter | none |

**Code.** `src/02_nairr_check.py` pulls the NSF award records, runs keyword searches and checks every quote in `data/raw/research/facts.csv` against the saved source. Outputs are in `data/processed/` (`nairr_awards.csv`, `keyword_search.csv`, `quote_check.csv`, `project_counts.csv`). Fetched pages are in `data/raw/sources/`, which is gitignored and logged in `MANIFEST.yaml`.

**Not reached.** The NAIRR resource catalog (submit-nairr.xras.org) failed TLS verification through the proxy, and the nairrpilot.org resource list loads by JavaScript. Whether NRP is a listed NAIRR resource is still open.

## What needs checking

- **`c1`** (placeholder, high): Agentic AI on public clouds: [which clouds, which models, who can request access]
- **`c2`** (placeholder, high): Data science on data lakehouses: [workflows supported today; partners]
- **`c3`** (placeholder, high): [NSF / NAIRR Award No. ____]

Status and the plan for each claim are in [`claims.yaml`](claims.yaml).

## Evidence

_Nothing yet. Code goes in `src/`, data in `data/`, outputs in `figures/`; see the top-level README._
