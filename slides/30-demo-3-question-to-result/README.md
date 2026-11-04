# Slide 30 · Demo 3: from question to result

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-30)

Status and the plan for each claim are in [`claims.yaml`](claims.yaml). Quotes are in
[`data/raw/research/facts.csv`](data/raw/research/facts.csv); `src/01_check.py` pulls the NSF award record
and counts terms in MESA's public docs (`data/processed/`).

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 · researcher asks which beetle is most common at JORN; agent queries the lakehouse and answers (T. pallidus, 58%) | partially supported (recording; NEON re-check pending) | Clip not recorded yet. Award abstract plans agents over a lakehouse (f4). MESA docs put agents on CyVerse VICE / A16 nodes and never mention NAIRR or Jetstream (f5, f6); the documented DuckLake is AVU metadata history (f7). Award is on the NAIRR fund line (f2). | "A researcher asks a question; the agent queries the data on [machine used in the recording] and returns a figure." Say "NAIRR compute" only if the run used a NAIRR Pilot allocation (e.g. Jetstream2), and "lakehouse" only if the recording queries one. Whether CyVerse is a NAIRR Pilot resource was not confirmed. |
| c2 · MESA · NSF Award #2632685 | supported | NSF Award API (f1) | none |

Also: slide says target length ~2:00, notes say ~2.5 min.

## The recording

The speaker's recording of Demo 3 (2026-11-02; sped up 1.5× and converted to WebM by the speaker, 2:10, no audio, 5.5 MB) plays on **slide 31** ([`slides/31-demo-3-video`](../31-demo-3-video/)), full-size like slide 25. The files stay in this folder ([`data/media/MANIFEST.yaml`](data/media/MANIFEST.yaml), `figures/poster.webp`). From 2026-11-02 to 11-04 it played inside this slide's frame. On 2026-11-04, at the speaker's request, it moved to its own slide, and this slide went back to its original layout (`src/03_layout.py`): a dashed frame now labeled "Recording on the next slide", the caption, and a short set-up in the notes.

The caption keeps c1's corrections: no "NAIRR compute" (the run is on the speaker's computer against the CyVerse Data Store), and "ranked table" instead of "figure".

**Still to check:** the answer itself (*Tetragonoderus pallidus*, 616 of 1,056 carabid individuals, 58.3%). `src/02_jorn_carabids.py` recomputes it from NEON's API (DP1.10022.001, bet_sorting, JORN, to 2025-09-10), independently of the agent. NEON's data endpoints answered 403 "Access Denied" without a token, so run it with a free NEON API token:

```
NEON_TOKEN=... uv run python slides/30-demo-3-question-to-result/src/02_jorn_carabids.py
```
