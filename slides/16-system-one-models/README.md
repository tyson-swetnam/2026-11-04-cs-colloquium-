# Slide 16 · System One models decide; they don’t write

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-16)

Added in the revised deck (2026-10-31). Claims are in [`claims.yaml`](claims.yaml); quotes in
[`data/raw/research/facts.csv`](data/raw/research/facts.csv) (each checked verbatim against the fetched page by `src/03_facts.py`).

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Jev Sept. 15, closed API; Clef Oct. 1, 27B and 9B, Apache 2.0 | supported | TypeSafe launch post; Cloudflare blog dated 2026-10-01; Hub: 27.36B and 9.41B params, apache-2.0 | “Clef (27B) and Clef-flash (9B)”: the 9B model has its own name. Clef-omni (35B) followed Oct. 9. |
| c2 One pass; choice, score or yes probability; calibrated | partially supported | One pass shown for Clef only (code, model card); TypeSafe says only “single query” with a “parallel sampler” for Jev. TypeSafe lists four primitives: choice, score, noul and an experimental Box (image bounding box). Calibration is vendor-reported only | Confidence: “A probability you can threshold (vendors say calibrated)”. Notes: “returns all the answers at once (for Clef, in one forward pass)”. Since Oct. 19 Cloudflare’s Clairic adds *extraction* models that return values, so the slide describes decision models. |
| c3 Fails by picking a wrong option from your list | partially supported | True for choice and yes/no: Clef picks the argmax of your options. But a score can land between your levels (TypeSafe example: 1.4 on 0/1/2), Box takes no options, and Clairic extracts names and dates | “Picks a wrong answer, but only inside the answer space you defined” |
| c4 Kahneman framing | n/a | both vendors cite *Thinking, Fast and Slow* | none |
| c5 LLMs “sound sure either way” (new) | partially supported | Xiong et al. 2023/ICLR 2024: verbalised confidence tends to be overconfident | “Often overconfident when it states its confidence” |
| c6 Notes: “up to 100x faster and cheaper” (new) | partially supported | TypeSafe: two orders of magnitude, 40x-200x faster per call; home-page 193.6x faster, 444.6x cheaper from its own evals, which it calls “the higher end”. “Up to 100x” is MindStudio’s summary | “TypeSafe says ~100x, 40x-200x faster per call; home-page headline 194x faster, 445x cheaper from its own evals” |
| c7 Notes: 200-comment test, Jev 86%, Clef 83% (new) | partially supported | Better Stack: numbers right, but the “truth” was Claude Opus 5.5, not human labels | “Jev agreed with an LLM referee 86% of the time, Clef 83%” |
| c8 Notes: Clef uses Jev’s request format (new) | supported | Clef model card: “fully compatible with Jev and SystemOne” | none |
| c9 Pair them: System One for routing, LLM for reasoning (new) | partially supported | Both vendors recommend it (TypeSafe docs, Cloudflare blog); Better Stack advice. No evidence it is “common”: the products are under seven weeks old | “Both vendors recommend pairing them” |

Not run: Clef’s weights (27B needs an H200-class GPU). The one-pass and answer-from-your-list claims were
checked by reading Cloudflare’s published `joint_schema_model.py` (static analysis, not executed).

## Reproduce

```sh
uv run python slides/16-system-one-models/src/01_fetch_sources.py   # fetch pages, cards, Hub API, arXiv
uv run python slides/16-system-one-models/src/02_check.py           # data/processed/*.csv
uv run python slides/16-system-one-models/src/03_facts.py           # facts.csv, verbatim-quote check
```
