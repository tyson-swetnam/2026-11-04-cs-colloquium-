# Slide 34 · AI’s future is a choice we make

Section: 04 · Stop worrying · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-34)

Added 2026-11-01, after slide 33. *Questions?* is now slide 35. The slide points to three sources: the White House Blueprint for an AI Bill of Rights, through Alondra Nelson, who led the team that wrote it; Pope Leo XIV's encyclical *Magnifica Humanitas*; and his @Pontifex posts. It ends with the take-away "We must vote for our leaders, and for the future." That line is the speaker's own. None of the sources says it, so it has no quotation marks.

`src/03_place_slide.py` builds the slide and places it in `talk/deck.html`. The take-away rises in on the first click. Claims are in [`claims.yaml`](claims.yaml), and quotes in [`data/raw/research/facts.csv`](data/raw/research/facts.csv).

## Findings (checked 2026-11-01)

All 23 quotes in `facts.csv` match their saved source word for word ([`data/processed/quote_check.csv`](data/processed/quote_check.csv)). Paragraph numbers in the encyclical are checked too.

| Claim | Verdict | Key evidence |
|---|---|---|
| c2 Nelson: "Red states and blue states are writing AI Bills of Rights." | supported | Bluesky post, 14 May 2026, read through the public API |
| c3 She led the team behind the Blueprint (2022) | supported | Her own description (Bluesky, 3 Oct 2026); OSTP release byline, 4 Oct 2022 |
| c5 "A more moral AI is not enough if that morality is determined by a few." | supported | *Magnifica Humanitas* ¶107 (signed 15 May, released 25 May 2026) |
| c6 @Pontifex: "The future of #ArtificialIntelligence is not pre-determined. ... its future depends on the choices we make." | supported | X oEmbed: Pope Leo XIV (@Pontifex), 30 Oct 2026 |
| c7 "We must vote for our leaders, and for the future." | speaker's own | The encyclical uses "vote" or "ballot" 0 times. The closest passages are ¶39 (elect and replace leaders) and ¶73 (make your voice heard). |
| c8 Election Day was Nov. 3 | supported | NM Secretary of State: "2026 General Election: Tuesday, November 3, 2026" |

The speaker notes cover the five principles, what happened to EO 14110, the *Science* essay and ¶106. Those claims are checked as c4 and c9 to c11.

## Corrections for the course page this slide draws on

The [Legal page](https://tyson-swetnam.github.io/intro-gpt/legal/) of *GPT 101* (checked 2026-11-01) says several things that the primary sources do not support:

- **"rescinded by ... Removing Barriers to American Leadership in Artificial Intelligence" (Jan 2025).** EO 14110 was revoked by EO 14148, *Initial Rescissions of Harmful Executive Orders and Actions* (20 Jan 2025, Sec. 2(ggg)). EO 14179 (23 Jan) refers to "the revoked Executive Order 14110".
- **"These principles were incorporated into" EO 14110.** EO 14110 adopted "practices derived from" the Blueprint and the NIST AI RMF for federal agencies' own AI use. Nelson herself writes "Parts of it were incorporated".
- **"Although rescinded at the federal level, the Blueprint ..."** No order names the Blueprint. It was a non-binding white paper; only EO 14110 was revoked.
- **Nelson "led the Blueprint's development as acting director".** The release lists her as Deputy Director for Science and Society. She had been performing the duties of director since Feb 2022, but "led the team" (her own words) is the safer phrasing.
- **Magnifica Humanitas as a "235-page document".** No source gives a page count. The English text has 245 numbered paragraphs.
- **"personally presented ... alongside Chris Olah" and "the first time a pontiff has presented an encyclical himself rather than delegating the task to cardinals".** The Vatican programme lists five speakers, cardinals among them, then the Pope's address. Only ANSA (a secondary source) calls his attending and speaking "a first".
- **Addressed to "every person of goodwill".** The English text says "to all men and women of goodwill" (¶16).
- **Quotes attributed to Nelson's *Science* essay.** Not checked: science.org is behind a bot check. Her Bluesky thread is quoted instead.

## Reproduce

```
uv run python slides/34-vote-for-the-future/src/01_fetch_sources.py   # primary sources -> data/raw/sources/ (+ MANIFEST.yaml)
uv run python slides/34-vote-for-the-future/src/02_check_quotes.py    # every quote in facts.csv, word for word -> data/processed/quote_check.csv
uv run python slides/34-vote-for-the-future/src/03_place_slide.py     # insert/refresh the slide in talk/deck.html (idempotent)
```

Sources are fetched with plain requests: X posts through X's public oEmbed endpoint and Bluesky posts through the public AppView API, with no logins and no bot-check workarounds.
