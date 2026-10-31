# Slide 28 · Five layers, all open source

> **Revised deck.** The revised deck (2026-10-31) removes the status placeholder.

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-28)

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` Five layers, all open source | contradicted | The figure has five layers. But it lists VAST (commercial EULA that forbids deriving source code) and AWS S3 (a commercial service whose API belongs to Amazon). Kubernetes/CSI (Apache-2.0), DuckLake (MIT), iRODS (BSD-3) and Lustre are open source. Compute and OSN are facilities, so the label does not apply to them. [`licences.csv`](data/processed/licences.csv) | "Five layers, open standards: each layer has an open-source option" |
| `c2` Running today on CyVerse, TACC, ACCESS-CI and NAIRR | partially-supported | CyVerse is confirmed: Formation and the Data Store connector are hosted there (developer-reported), and mesa.cyverse.org is up. The MESA site and docs do not mention TACC, Jetstream/ACCESS-CI or NAIRR. The NSF abstract says MESA "will operate" there. | "Running today on CyVerse; TACC, ACCESS-CI and NAIRR resources next." |
| `c3` Status placeholder | superseded | Removed from the slide. | (none) |
| `c4` Notes: layer order | supported | The figure, top to bottom: User Interface, Agentic AI, Data Management, Compute, Object Storage. | "user interface … object storage" |
| `c5` Notes: every layer swappable and open | partially-supported | Each layer offers alternatives, so "swappable" holds. "Open" fails for the same reasons as `c1`. | "every layer is swappable, and each has an open-source choice" |
| `c6` Figure credit, NSF Award #2632685 | supported | Confirmed by the NSF Award API. Proposals are not public, so the figure's source is the speaker's own statement. | (none) |

Not checked: the licence of MESA's own servers. The public docs mention a LICENSE file but do not name the licence, and the code was out of scope. The Antigravity licence was not checked either.

## Evidence

- `src/01_fetch_sources.py`: fetches sources into `data/raw/sources/` (gitignored, logged in `MANIFEST.yaml`). It also pulls the slide figure, its alt text and the speaker notes out of `talk/deck.html`, saving them to `data/processed/deck_slide28.json`.
- `src/02_licences_and_checks.py` writes four files:
  - `licences.csv`: each figure component's licence, from the deps.dev API.
  - `site_mentions.csv`: how often MESA's pages mention each compute site.
  - `endpoints.csv`: a live check of the MESA endpoints.
  - `quote_check.csv`: confirms every facts.csv quote is verbatim.
- `data/raw/research/facts.csv`: the exact quotes, f01 to f15.
