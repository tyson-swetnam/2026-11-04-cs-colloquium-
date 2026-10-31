# Slide 09 · Contested data, Western defaults

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-09)

Added in the revised deck (2026-10-31). Claims are in [`claims.yaml`](claims.yaml). Checked 2026-10-31.

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Bartz: $1.5B, ~$3,100 per work, ~480,000 works | supported | Final approval order: $1.5B fund, 482,460 works; $3,109 gross per work. Court and notice: ~$3,000 per work plus interest, less fees. Net about $2,855 per listed work, or about $3,127 per claimed work if unclaimed shares are redistributed. | Keep. Optionally "about $3,000 per work after fees". |
| c2 Training fair use in Bartz and Kadrey; piracy not | partially supported | Bartz (Dkt. 231): training fair use; pirated library copies sent to trial, no final holding. Kadrey (Dkt. 598): won by Meta on a narrow record ("these plaintiffs made the wrong arguments"); downloading treated as part of the use. | "In 2025, Bartz held training fair use but sent pirated library copies to trial; Kadrey v. Meta ruled for Meta on a narrow record." |
| c3 Still in court: NYT, Midjourney, music publishers ($3B+) | partially supported | NYT: summary-judgment motions Sept. 2026, no ruling. Midjourney: mediation ordered (Nov. 2025) to end Aug. 19, 2026; latest report a May 2026 discovery dispute; outcome unknown. Publishers: Concord/UMG/ABKCO suit (Jan. 2026) claims more than $3B; separate Sony/Warner Chappell suit (Aug. 28, 2026) gives no total. | "...; UMG, Concord and ABKCO v. Anthropic, claiming potential damages of more than $3B (plus a newer Sony/Warner Chappell suit)." |
| c4 More than half of web content is English; models mostly European/North American text | partially supported (first half contradicted) | W3Techs: 49.5% of websites in English, under 50% since 2025. Common Crawl 2026-43: 42.6% of pages. Meta reports Llama 2 data 89.7% English (2023; corpus not released); 51.3% of C4 pages US-hosted. | "About half of websites are in English (49.5%, W3Techs), and Meta reports Llama 2's training data was 90% English, so models carry a Western default." |
| c5 (notes) Final approval July 20, 2026; largest US copyright settlement | supported | Order (Dkt. 680) quotes the court: "the largest copyright class action settlement in history"; the official notice and website say the same. | "final approval July 20, 2026; the court calls it the largest copyright class action settlement in history" |
| c6 (notes) 20M de-identified ChatGPT logs ordered | supported | Stein order, Jan. 5, 2026, affirming Wang (Nov. 2025). | Keep. |
| c7 (notes) Publishers allege torrenting of ~20,000 songs | partially supported | Concord complaint: torrented books with "hundreds or thousands" of works, including 714 (Ex. A); a separate 20,517 works (Ex. B) for training and output; $3B adds both. Sony/Warner suit alleges torrenting of "hundreds or more" works, no total. All allegations. | "...claim potential damages of more than $3B over about 21,000 songs: at least 714 allegedly in torrented songbooks, and 20,517 allegedly used in training and output. Sony and Warner Chappell filed a separate torrenting suit in Aug. 2026." |
| c8 (notes) GEMA v. OpenAI, Munich, Nov. 2025 | supported | LTO report of LG München I, 11.11.2025, 42 O 14139/24; first instance, not yet final. | Keep. |
| c9 (notes) Getty v. Stability: weights not infringing copies | supported | [2025] EWHC 2863 (Ch). Getty granted permission to appeal this point (Dec. 2025); no appeal decision found. Training claim was dropped. | "a UK High Court held (now on appeal)..." |
| c10 (notes) Little market incentive to fix bias | opinion | Not applicable. | — |

Re-check before the talk: the Midjourney docket, NYT summary-judgment status, the music-publisher suits and the Getty appeal. The slide footer says "as of August 2026".

## Reproduce

```
uv run python slides/09-contested-data/src/01_fetch.py        # download sources, log in data/raw/sources/MANIFEST.yaml
uv run python slides/09-contested-data/src/00_write_facts.py  # write data/raw/research/facts.csv
uv run python slides/09-contested-data/src/02_check.py        # check quotes, compute numbers -> data/processed/
```

Blocked: CourtListener docket pages and search API (403/401) and the Wikipedia API (429), so they were not used. Court PDFs came from RECAP storage or copies linked from news pages.
