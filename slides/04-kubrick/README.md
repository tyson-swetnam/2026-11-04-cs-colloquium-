# Slide 04 · Kubrick’s 1964 political satire

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-04)

Added in the revised deck (2026-10-31). Claims are listed in [`claims.yaml`](claims.yaml); quotes are in [`data/raw/research/facts.csv`](data/raw/research/facts.csv).

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Title, Kubrick, Columbia Pictures, 1964 | supported | BBFC record: director Stanley Kubrick; 1964 certificate (9 Jan 1964), distributor Columbia Picture Corp. Ltd | none |
| c2 Poster, War Room still and trailer are public domain via Commons | partially supported | War Room still and trailer: `{{PD-US-no notice}}` on Commons (US only; uploader's tag, not checked further). The poster in the deck is not the Commons file (see c4). The trailer is only linked in the notes | “Poster: Tomi Ungerer, 1964 (copyrighted; used for commentary) · War Room still: Columbia Pictures, 1964, via Wikimedia Commons · Public domain in the US (per Commons: published without a copyright notice) · Trailer linked in notes” |
| c3 Plot: a general orders a first strike; the War Room tries to recall the bombers | supported | BBFC synopsis; Wikipedia plot summary | none |
| c4 The poster image shown is public domain | **contradicted** | Deck image is the non-free English Wikipedia file “Dr._Strangelove_poster.jpg” (same pixels; byte/SHA-1 check in `enwiki_poster_match.json`). No fetched source names the copyright holder; that page's fair-use rationale covers Wikipedia only | “Poster: Tomi Ungerer, 1964 (copyrighted; used for commentary)”, or replace with the Commons trailer frame (tagged public domain in the US) |
| c5 The poster is by Tomi Ungerer | supported (secondary) | ERIAC article; Wikipedia infobox caption | none |
| c6 In 1964 the worry was a nuclear war | supported (framing, secondary) | Wikipedia: the film “parodies the heightened fears during the Cold War of a nuclear war” | none |

Notes:
- “Public domain” here means public domain in the US only: the trailer was published without a copyright notice. The film itself is still under copyright.
- The trailer is linked in the speaker notes; it is not embedded in the deck.
- Do not write “© 1964 Columbia Pictures” or “fair use” on the slide: no fetched source names the poster's owner, and whether the talk's use is fair use is a legal judgement.
- The Commons API and upload.wikimedia.org returned HTTP 429 (rate limited). The file-page wikitext was read with `action=raw` instead. The image size of the Commons poster PNG comes from its file page, read with WebFetch.

## Reproduce

```
uv run python slides/04-kubrick/src/01_commons_licences.py   # Commons licence wikitext -> data/processed/commons_licences.json
uv run python slides/04-kubrick/src/02_deck_images.py        # deck embeds vs Commons -> data/processed/deck_images.json
uv run python slides/04-kubrick/src/03_enwiki_poster_sha1.py # deck poster vs en.wikipedia file (size, SHA-1) -> data/processed/enwiki_poster_match.json
```
