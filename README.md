# How I Learned to Stop Worrying and Love the AI

**Site:** https://tyson-swetnam.github.io/2026-11-04-cs-colloquium-/ has the full deck and an evidence page for every slide. It's built by `tools/build_site.py` and published by `.github/workflows/pages.yml` on each push to `main`.

UNM Computer Science Colloquium · Tyson L. Swetnam · Wednesday, Nov. 4, 2026, 2 p.m. · Larrañaga Engineering Auditorium (Centennial 1041)

This repository holds the talk and the evidence for it. Every number, attribution and technical statement on a slide has an entry in that slide's folder. Each entry is backed by code you can rerun and data you can trace to its source, or it is marked as not yet checked. The [claims register](CLAIMS.md) shows where each one stands.

## Layout

```
talk/
  deck.html          the exported deck (source of truth for wording and speaker notes)
  slides.md          text and notes per slide, generated from deck.html for readable diffs
slides/
  NN-slug/           one folder per slide, numbered as in the deck
    README.md        what needs checking and, once done, what the evidence shows
    claims.yaml      each claim: text, kind, priority, status, how to validate, sources, evidence
    src/             analysis code, numbered in run order (created when the slide needs it)
    data/raw/        downloads as fetched, with MANIFEST.yaml (URL, date, SHA-256)
    data/processed/  tidy outputs of src/
    figures/         charts and tables that go back into the deck
evidence/            shared Python: data fetching with provenance, economic normalizations, plot style
tools/
  deck.py            extract slide text and notes; scaffold folders for new slides
  claims.py          validate every claims.yaml; build CLAIMS.md
tests/               unit tests for evidence/ and the claims schema
CLAIMS.md            generated register of every claim and its status
```

## Claims

Each claim in `claims.yaml` has a **kind** and a **status**.

| Kind | Meaning | Checked by |
|---|---|---|
| `quantitative` | A number | Code and data that reproduce it |
| `factual` | A date, name, award number or identifier | A scripted lookup against the authority (Nobel API, NSF Award API, OLS) |
| `attribution` | A figure or quote credited to someone else | Reading the primary source and citing it exactly |
| `technical` | How a system behaves | Running it and keeping the log |
| `qualitative` | Framing or opinion | Not checked; the reasoning is recorded |
| `placeholder` | Bracketed text still to be written | Writing it, then reclassifying |

Status moves from `unverified` to `in-progress`, then to `supported`, `partially-supported` or `contradicted`. A claim whose slide wording must change is marked `revise-slide` until the deck is updated. The validator refuses a verdict (`supported`, `partially-supported`, `contradicted`) unless it lists at least one evidence path that exists in the slide folder.

## Workflow for one slide

1. Read the slide's `README.md` and `claims.yaml`.
2. Put the code in `src/` and the data in `data/`. Fetch with `evidence.fetch.fetch()` so each file gets a manifest entry.
3. Write the result in the slide README under **Evidence**. Update the claim's `status` and `evidence`.
4. If the evidence changes the wording, edit the deck, re-export it to `talk/deck.html`, and run `make slides`.
5. Run `make claims check` and commit.

## Setup

```bash
make setup
```

```bash
make check
```

`make slide-NN` runs one slide's analysis (for example `make slide-05` for the build-out); see the `Makefile` for which slides have one.

## Data and licensing

Code is GPL-3.0 (see `LICENSE`). Data keeps its original license; each `MANIFEST.yaml` records the source and its terms. Anything over about 5 MB is not committed and is re-fetched from the recorded URL.
