# Slide 04 · Kubrick’s 1964 political satire

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-04)

Added in the revised deck (2026-10-31). Claims are listed in [`claims.yaml`](claims.yaml); quotes are in [`data/raw/research/facts.csv`](data/raw/research/facts.csv).

## Findings (checked 2026-10-31)

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Title, Kubrick, Columbia Pictures, 1964 | supported | BBFC record: director Stanley Kubrick; 1964 certificate, distributor Columbia Picture Corp. Ltd | none |
| c2 Poster, War Room still and trailer are public domain via Commons | partially supported | War Room still and trailer: `{{PD-US-no notice}}` on Commons (US only). The poster in the deck is not the Commons file (see c4) | “Poster: Tomi Ungerer, © 1964 Columbia Pictures (fair use) · War Room still and trailer: Columbia Pictures, 1964, via Wikimedia Commons · Public domain in the US” |
| c3 Plot: a general orders a first strike; the War Room tries to recall the bombers | supported | BBFC synopsis; Wikipedia plot summary | none |
| c4 The poster image shown is public domain | **contradicted** | Deck image is 250×388 px, 47,827 bytes, the same as the non-free English Wikipedia file “Dr._Strangelove_poster.jpg”. The Commons “poster” PNG is a 1196×720 trailer frame | Credit as fair use (above), or replace with the public-domain Commons trailer frame |
| c5 The poster is by Tomi Ungerer | supported (secondary) | ERIAC article; Wikipedia infobox caption | none |

Notes:
- “Public domain” here means public domain in the US only: the trailer was published without a copyright notice. The film itself is still under copyright.
- The trailer is linked in the speaker notes; it is not embedded in the deck.
- The Commons API and upload.wikimedia.org returned HTTP 429 (rate limited). The file-page wikitext was read with `action=raw` instead. The image size of the Commons poster PNG comes from its file page, read with WebFetch.

## Reproduce

```
uv run python slides/04-kubrick/src/01_commons_licences.py   # Commons licence wikitext -> data/processed/commons_licences.json
uv run python slides/04-kubrick/src/02_deck_images.py        # deck embeds vs Commons -> data/processed/deck_images.json
```
