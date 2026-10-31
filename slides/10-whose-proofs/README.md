# Slide 10 · Whose proofs are they?

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-10)

Added in the revised deck (2026-10-31). Claims are in [`claims.yaml`](claims.yaml). Checked 2026-10-31.

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 722 manuscripts, 372 problems, openai/math, Oct 2026, 3 retracted within a day | supported | Retraction Watch (722 on 372, 3 withdrawn Oct 7, under 24 h); OpenAI history.md (Oct 6 release, 3 withdrawn). Repo now shows 721 / 373 after later edits | keep |
| c2 About half in Lean; OpenAI had not read all; 28 Fields Medalists | partially supported | OpenAI log: 300/719 = 42% formalized; "about half" was OpenAI's release-day claim. "Not read all" is Scientific American's statement. Declaration: 25 signers at launch (Zenodo, single version; Tao, 12 Sep), 28 now (mathandai.org); no date for the 3 later signers | "About 42% had Lean proofs, and OpenAI researchers had not read them all. A declaration by 25 Fields Medalists (now 28) had warned …" |
| c3 Buckmaster allegation | partially supported | Buckmaster's statement: tips that "information about our progress" reached OpenAI; asked whether Codex sessions trained the model; "I am not accusing anyone". OpenAI denies seeing any of their work before it was public (Sep 8 post via TechCrunch). Alpöge works at Anthropic (Sci Am) | "… says word of his and Alpöge's (Anthropic) unpublished Euler work reached OpenAI … OpenAI says it saw none of their work until it was public." Avoid "leaked" in notes |
| c4 OpenAI's shifting answer; dispute unresolved | partially supported | Sep 8 post: saw none of their work; "cannot rule out … de-identified data" helped its models in general (TechCrunch). Spokesperson: "categorically … impossible" for his last two months of prompts (ABC, Verge). Different scopes, not a reversal: "shifting" is the slide's reading. Sci Am (Oct 13): resemblance "merely skin-deep" | "OpenAI says it saw none of their work … could not rule out that de-identified usage data helped its models in general; called influence from his last two months of prompts 'impossible.' Experts now say the proofs differ; the data question has not been independently checked, as far as public reporting shows." |
| c5 (notes) unreleased model; 14 revised | supported | OpenAI README says "unnamed internal OpenAI model"; history.md: 14 revised | say "unnamed internal model" |
| c6 (notes) AHM statement; Tao reshared it | supported | AHM quote confirmed. Tao reposted the full statement as a guest post on his blog, 7 Oct 2026. Futurism's "effectively endorsed" is its own reading; Tao hosted many guest posts that month | keep "reshared" (or "reposted on his blog"); avoid "endorsed" |
| c7 (notes) OpenAI says proofs differ; Alpöge disputes | partially supported | OpenAI quote via TechCrunch; Alpöge via Wikipedia only; Sci Am experts side with "different" | add that experts now say the methods differ |
| c8 Futurism source line | supported | byline F. Landymore, dated 2026-10-09 | keep |

## Limits

- openai.com returned HTTP 403, so OpenAI's Navier–Stokes post is quoted through TechCrunch, ABC and The Verge.
- The review of 2026-10-31 corrected c6 (the earlier check missed Tao's blog) and tightened c2-c5.
- OpenAI repository files were read as public raw files, not through GitHub tools.

## Files

- `src/01_check.py`: counts signatories (Zenodo vs mathandai.org), manuscripts and Lean share (OpenAI README/history), and searches Tao's Mastodon for the AHM reshare (none there; the reshare is on his blog, see `03`). Writes `data/processed/checks.json`.
- `src/03_review_checks.py`: review follow-up. Zenodo versions API (one version, 25 signers) and Tao's blog posts 1-15 Oct via the WordPress.com API (AHM repost, guest-post count). Writes `data/processed/review_checks.json`.
- `src/02_facts.py`: builds `data/raw/research/facts.csv` and checks each quote is verbatim in the saved source.
- Downloads are in `data/raw/sources/` (gitignored, logged in `MANIFEST.yaml`).
