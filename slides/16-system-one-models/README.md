# Slide 16 · System One models decide; they don’t write

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-16)

Added in the revised deck (2026-10-31). Claims are in [`claims.yaml`](claims.yaml); quotes in
[`data/raw/research/facts.csv`](data/raw/research/facts.csv) (each checked verbatim against the fetched page by `src/03_facts.py`).

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Jev Sept. 15, closed API; Clef Oct. 1, 27B and 9B, Apache 2.0 | supported | TypeSafe launch post; Cloudflare blog dated 2026-10-01; Hub: 27.36B and 9.41B params, apache-2.0 | “Clef (27B) and Clef-flash (9B)”: the 9B model has its own name. Clef-omni (35B) followed Oct. 9. |
| c2 One pass; choice, score or yes probability; calibrated | partially supported | Clef code: one backbone call, no generation; three primitives. Calibration is vendor-reported only | “A probability you can threshold (vendors say calibrated)”. Since Oct. 19 Cloudflare’s Clairic adds *extraction* models that return values, so the slide describes decision models. |
| c3 Fails by picking a wrong option from your list | supported | Clef code: answer = argmax over caller’s options; TypeSafe: outputs defined in advance | none |
| c4 Kahneman framing | n/a | both vendors cite *Thinking, Fast and Slow* | none |
| c5 LLMs “sound sure either way” (new) | partially supported | Xiong et al. 2023/ICLR 2024: verbalised confidence tends to be overconfident | “Often overconfident when it states its confidence” |
| c6 Notes: “up to 100x faster and cheaper” (new) | partially supported | TypeSafe: two orders of magnitude; headline 193.6x faster, 444.6x cheaper (own evals) | “TypeSafe claims ~100x, up to 194x faster and 445x cheaper, in its own evals” |
| c7 Notes: 200-comment test, Jev 86%, Clef 83% (new) | partially supported | Better Stack: numbers right, but the “truth” was Claude Opus 5.5, not human labels | “Jev agreed with an LLM referee 86% of the time, Clef 83%” |
| c8 Notes: Clef uses Jev’s request format (new) | supported | Clef model card: “fully compatible with Jev and SystemOne” | none |
| c9 Pair them: System One for routing, LLM for reasoning (new) | supported (vendor guidance) | TypeSafe docs; Cloudflare blog; Better Stack | none |

Not run: Clef’s weights (27B needs an H200-class GPU). The one-pass and answer-from-your-list claims were
checked by reading Cloudflare’s published `joint_schema_model.py` (static analysis, not executed).

## Reproduce

```sh
uv run python slides/16-system-one-models/src/01_fetch_sources.py   # fetch pages, cards, Hub API, arXiv
uv run python slides/16-system-one-models/src/02_check.py           # data/processed/*.csv
uv run python slides/16-system-one-models/src/03_facts.py           # facts.csv, verbatim-quote check
```
