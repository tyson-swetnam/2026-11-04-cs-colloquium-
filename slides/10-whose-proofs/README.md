# Slide 10 · Whose proofs are they?

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-10)

Added in the revised deck (2026-10-31). Claims are in [`claims.yaml`](claims.yaml). Checked 2026-10-31.

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 722 manuscripts, 372 problems, openai/math, Oct 2026, 3 retracted within a day | supported | Retraction Watch (722 on 372, 3 withdrawn Oct 7, under 24 h); OpenAI history.md (Oct 6 release, 3 withdrawn). Repo now shows 721 / 373 after later edits | keep |
| c2 About half in Lean; OpenAI had not read all; 28 Fields Medalists | partially supported | OpenAI log: 300/719 = 42% formalized; "about half" was OpenAI's release-day claim. "Not read all" is Scientific American's statement. Declaration: 25 signers at launch (Zenodo), 28 now (mathandai.org) | "About 42% had Lean proofs, and OpenAI researchers had not read them all. 28 Fields Medalists had warned …" |
| c3 Buckmaster allegation | partially supported | Buckmaster's statement: tips that "information about our progress" reached OpenAI; asked whether Codex sessions trained the model; "I am not accusing anyone" | "… says word of his and Alpöge's unpublished Euler work reached OpenAI …". Avoid "leaked" in notes |
| c4 OpenAI's shifting answer; dispute unresolved | partially supported | "cannot rule out … de-identified data" (Sep 8 post, quoted by TechCrunch); "categorically … impossible" covers only his last two months of prompts (ABC, Verge). Sci Am (Oct 13): methods' resemblance "merely skin-deep" | "… then called influence from his last two months of Codex prompts 'impossible.' Experts now say the proofs differ; the data question was never independently checked." |
| c5 (notes) unreleased model; 14 revised | supported | OpenAI README and history.md | keep |
| c6 (notes) AHM statement; Tao reshared it | partially supported | AHM quote confirmed. Tao reshare only per Futurism (misspelled "Tau"); not on his Mastodon | drop the Tao reshare, or say "reported by Futurism" |
| c7 (notes) OpenAI says proofs differ; Alpöge disputes | partially supported | OpenAI quote via TechCrunch; Alpöge via Wikipedia only; Sci Am experts side with "different" | add that experts now say the methods differ |
| c8 Futurism source line | supported | byline F. Landymore, dated 2026-10-09 | keep |

## Limits

- openai.com returned HTTP 403, so OpenAI's Navier–Stokes post is quoted through TechCrunch, ABC and The Verge.
- OpenAI repository files were read as public raw files, not through GitHub tools.

## Files

- `src/01_check.py`: counts signatories (Zenodo vs mathandai.org), manuscripts and Lean share (OpenAI README/history), and searches Tao's Mastodon for the AHM reshare. Writes `data/processed/checks.json`.
- `src/02_facts.py`: builds `data/raw/research/facts.csv` and checks each quote is verbatim in the saved source.
- Downloads are in `data/raw/sources/` (gitignored, logged in `MANIFEST.yaml`).
