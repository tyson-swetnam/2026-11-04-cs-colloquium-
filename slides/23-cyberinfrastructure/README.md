# Slide 23 · AI sandboxes and secure enclaves

> **Revised deck.** The revised deck (2026-10-31) removes CAISP from the slide, but the speaker note still mentions it, and adds CARC-hosted models and co-scientists.

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-23)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` Petabytes of iRODS on CyVerse; public data read anonymously | partially supported | CyVerse docs: "over 6 PB" via iRODS; anonymous WebDAV access documented. Our scripted anonymous read got a 307 to an IP-unblock CAPTCHA (anti-crawler block); not bypassed. Three size figures: over 6 PB (CyVerse docs, undated), 5.2 PB (CARC job page, MESA hiring page), "five petabytes" (MESA home) | "Petabytes of iRODS collections on CyVerse. Public collections need no account." |
| `c2` Kubernetes sandboxes, allowed tools only, egress proxy, every call recorded | partially supported (developer-reported) | MESA mesa-sandbox page: per-agent pods, egress proxy for allow-listed hosts; "the Kubernetes profiles are untested on a cluster" (2026-09-06). Logging of every call not stated publicly; code not read | "Kubernetes AI sandboxes (in development): each agent in its own pod; egress only to allow-listed hosts through a proxy." |
| `c3` ACCESS allocations, CPU/GPU VMs from IaC templates | superseded (was correct) | Jetstream2 allocation and flavour docs; CyVerse CACAO IaC | none (replaced by c5) |
| `c4` CAISP | superseded | removed from slide | none |
| `c5` ACCESS-CI JS2, NRP, NIS for self-hosted inference, training, gateways | partially supported | JS2: ACCESS, GPU VMs, science-gateway backend, free vLLM inference service; its LLM guide says fine-tuning "is more achievable" but pre-training is likely too big for a typical allocation. NRP: ACCESS catalogue, hosted open-weight LLMs, run-your-own via vLLM, "AI and machine learning tasks" (training not named). "NIS" not identifiable | "ACCESS-CI Jetstream2 and NRP: self-hosted or hosted open-weight inference, small-scale fine-tuning, science gateways." |
| `c6` CARC: locally hosted, private, open-weight models | partially supported | CARC (2026-10-13): no hosted LLM "production service". MESA docs (draft, developer-reported): LiteLLM/vLLM gateway on CARC hosts, SSH tunnel only; not on CARC's page | "CARC: private open-weight models on campus GPUs (MESA gateway in testing, developer-reported; not a campus service yet)" |
| `c7` Co-scientists that hypothesise, test, analyse and report continuously | unverified | No public page shows such a loop; MESA lists agentic orchestration as a goal | "Co-scientists (goal): agents that propose hypotheses, write the tests, fetch and analyse data, and report." |
| `c8` Note still cites CAISP | supported | deck check: CAISP only in the note | Drop the CAISP sentence from the note |
| `c9` (new) Note: "all four are bookable now" | contradicted | Sandboxes untested on a cluster; co-scientists a goal. Data Store (free account or subscription, not "allocations") and Private inference (JS2/NRP via ACCESS) are bookable | "Two of these you can book now: CyVerse storage (free account or subscription), and Jetstream2 or NRP through ACCESS-CI." |
| `c10` (new) Footer NSF Award #2632685 | supported | NSF Award API: MESA, University of New Mexico, 2026-07-15 to 2029-05-31 | none |

Open question for the speaker: what does "NIS" stand for?

## Evidence

- `data/raw/research/facts.csv`: 29 exact quotes, each with source URL; all found in the fetched documents (`data/processed/quote_check.csv`).
- `data/raw/sources/MANIFEST.yaml`: URL, date and SHA-256 of every fetched document (documents themselves are gitignored).
- `src/01_record_sources.py`: logs the fetched documents.
- `src/02_anon_read.py` → `data/processed/anon_read.json`: anonymous WebDAV read attempt (blocked by CyVerse's IP challenge from this network).
- `src/03_check_quotes.py` → `data/processed/quote_check.csv`, `data/processed/deck_check.json`: quote check and the slide-23 deck text check.
- `src/04_nsf_award.py` → `data/processed/nsf_award_2632685.json`: NSF Award API record (contact fields removed).

Caveats: MESA claims rely on MESA's public site only (developer-reported); the mesa-sandbox and mesa-anyjev repositories were not read. The anonymous read should be re-run from a campus network before the talk.
