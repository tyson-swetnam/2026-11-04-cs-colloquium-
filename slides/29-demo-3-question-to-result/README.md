# Slide 29 · Demo 3: from question to result

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-29)

Status and the plan for each claim are in [`claims.yaml`](claims.yaml). Quotes are in
[`data/raw/research/facts.csv`](data/raw/research/facts.csv); `src/01_check.py` pulls the NSF award record
and counts terms in MESA's public docs (`data/processed/`).

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 · researcher asks; agent queries the lakehouse on NAIRR compute; returns a figure | unverified | Clip not recorded yet. Award abstract plans agents over a lakehouse (f4). MESA docs put agents on CyVerse VICE / A16 nodes and never mention NAIRR or Jetstream (f5, f6); the documented DuckLake is AVU metadata history (f7). Award is on the NAIRR fund line (f2). | "A researcher asks a question; the agent queries the data on [machine used in the recording] and returns a figure." Say "NAIRR compute" only if the run used a NAIRR Pilot allocation (e.g. Jetstream2), and "lakehouse" only if the recording queries one. Whether CyVerse is a NAIRR Pilot resource was not confirmed. |
| c2 · MESA · NSF Award #2632685 | supported | NSF Award API (f1) | none |

Also: slide says target length ~2:00, notes say ~2.5 min.

## Before the talk

Keep the prompt, the agent transcript, the DuckLake snapshot ID, the machine it ran on and the output figure
in this folder, then re-check c1.
