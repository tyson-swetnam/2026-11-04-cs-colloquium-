# Slide 28 · Five layers, all open source

> **Revised deck.** The revised deck (2026-10-31) removes the status placeholder.

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-28)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` Five layers, all open source | contradicted | The figure has five layers. But it lists VAST (commercial EULA that forbids deriving source code) and AWS S3 (a commercial service whose API belongs to Amazon). Kubernetes/CSI (Apache-2.0), DuckLake (MIT), iRODS (BSD-3) and Lustre are open source. Compute and OSN are facilities, so the label does not apply to them. [`licences.csv`](data/processed/licences.csv) | "Five layers, built on open-source software where it exists" |
| `c2` Running today on CyVerse, TACC, ACCESS-CI and NAIRR | partially-supported | CyVerse hosts the Formation server and public Data Store connector MESA uses (developer-reported); the MESA servers themselves install on the user's machine, so this is not a full CyVerse deployment. mesa.cyverse.org is up. The MESA site and docs do not mention TACC, Jetstream/ACCESS-CI or NAIRR. The NSF abstract says MESA "will operate" on TACC, OSN, CyVerse and Jetstream-2 through ACCESS-CI, with no dates. NAIRR is only the award's funding program, not a site. | "Running today on CyVerse services; planned on TACC, Jetstream2 and OSN through ACCESS-CI (NSF award 2632685)." |
| `c3` Status placeholder | superseded | Removed from the slide. | (none) |
| `c4` Notes: layer order | supported | The figure, top to bottom: User Interface, Agentic AI, Data Management, Compute, Object Storage. | "user interface … object storage" |
| `c5` Notes: every layer swappable and open | partially-supported | "Swappable" is design intent: the figure lists alternatives in most layers, and MESA reports (developer-reported) support for four agent clients. No source shows swapping compute or storage. "Open" fails for the same reasons as `c1`; compute is facilities, so it has no open-source choice. | "each layer is designed to be swappable, with open-source software at the core where it exists" |
| `c6` Figure credit, NSF Award #2632685 | supported | Confirmed by the NSF Award API. Proposals are not public, so the figure's source is the speaker's own statement. | (none) |

Not checked: the licence of MESA's own servers. The public docs mention a LICENSE file but do not name the licence, and the code was out of scope. The Antigravity licence was not checked either.

## Evidence

- `src/01_fetch_sources.py`: fetches sources into `data/raw/sources/` (gitignored, logged in `MANIFEST.yaml`). It also pulls the slide figure, its alt text and the speaker notes out of `talk/deck.html`, saving them to `data/processed/deck_slide28.json`.
- `src/02_licences_and_checks.py` writes four files:
  - `licences.csv`: each figure component's licence, from the deps.dev API.
  - `site_mentions.csv`: how often MESA's pages mention each compute site.
  - `endpoints.csv`: a live check of the MESA endpoints.
  - `quote_check.csv`: confirms every facts.csv quote is verbatim.
- `data/raw/research/facts.csv`: the exact quotes, f01 to f16.
