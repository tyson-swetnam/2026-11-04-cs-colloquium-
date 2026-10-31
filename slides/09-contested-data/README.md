# Slide 09 · Contested data, Western defaults

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-09)

Added in the revised deck (2026-10-31). Claims are in [`claims.yaml`](claims.yaml). Checked 2026-10-31.

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Bartz: $1.5B, ~$3,100 per work, ~480,000 works | supported | Final approval order: $1.5B fund, 482,460 works; $1.5B / 482,460 = $3,109 gross. Court says ~$3,000 before fees; ~$2,855 after fees and costs. | Keep. Optionally "before fees". |
| c2 Training fair use in Bartz and Kadrey; piracy not | partially supported | Bartz (Dkt. 231) held pirated library copies not fair use. Kadrey (Dkt. 598) held Meta's downloading fair use on that record. | "In 2025, two judges held training fair use (Bartz; Kadrey v. Meta). Bartz held that pirated library copies were not." |
| c3 Still in court: NYT, Midjourney, music publishers ($3B+) | partially supported | NYT at summary judgment (Sept. 2026). Publishers' complaint (Jan. 2026), partial motion to dismiss (Aug. 2026). Midjourney: last status found is mediation due Aug. 19, 2026. $3B+ is the publishers' estimate of potential damages. | "Still in court: NYT v. OpenAI and Microsoft (summary judgment); Disney, Universal and Warner Bros. v. Midjourney; music publishers v. Anthropic, claiming up to $3B+." |
| c4 More than half of web content is English; models mostly European/North American text | contradicted (first half) | W3Techs: 49.5% of websites in English, under 50% since 2025. Common Crawl 2026-43: 42.6% of pages. Llama 2 data 89.7% English; 51.3% of C4 pages US-hosted. | "About half of websites are in English (49.5%), and open training sets are mostly English (Llama 2: 90%), so models carry a Western default." |
| c5 (notes) Final approval July 20, 2026; largest US copyright settlement | partially supported | Date in order. "Largest" is how counsel and press describe it, not the court. | "described as the largest US copyright recovery" |
| c6 (notes) 20M de-identified ChatGPT logs ordered | supported | Stein order, Jan. 5, 2026, affirming Wang (Nov. 2025). | Keep. |
| c7 (notes) Publishers allege torrenting of ~20,000 songs | contradicted | Complaint: 714 works allegedly torrented (Ex. A); 20,517 training/output works (Ex. B). | "...$3B+ over more than 20,000 songs used in training, 714 of them allegedly torrented." |
| c8 (notes) GEMA v. OpenAI, Munich, Nov. 2025 | supported | LTO report of LG München I, 11.11.2025, 42 O 14139/24 (first instance). | Keep. |
| c9 (notes) Getty v. Stability: weights not infringing copies | supported | [2025] EWHC 2863 (Ch). Training claim was dropped. | Keep. |
| c10 (notes) Little market incentive to fix bias | opinion | Not applicable. | — |

Re-check before the talk: the Midjourney docket and NYT summary-judgment status. The slide footer says "as of August 2026".

## Reproduce

```
uv run python slides/09-contested-data/src/01_fetch.py        # download sources, log in data/raw/sources/MANIFEST.yaml
uv run python slides/09-contested-data/src/00_write_facts.py  # write data/raw/research/facts.csv
uv run python slides/09-contested-data/src/02_check.py        # check quotes, compute numbers -> data/processed/
```

Blocked: CourtListener docket pages and search API (403/401) and the Wikipedia API (429), so they were not used. Court PDFs came from RECAP storage or copies linked from news pages.
