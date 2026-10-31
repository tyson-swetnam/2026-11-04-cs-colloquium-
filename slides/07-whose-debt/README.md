# Slide 07 · Whose debt is it?

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-07)

Added in the revised deck (2026-10-31). Claims are listed in [`claims.yaml`](claims.yaml).

## Findings (checked 2026-10-31)

The slide rests on one report: Scherer and Jenkins, *Brace for Impact: Protecting People and the Economy When
the AI Bubble Bursts*, by the Open Markets Institute and the Americans for Financial Reform Education Fund, published
Oct. 16, 2026. Both groups are advocates, so the slide should present its points as their warning.
Independent economists (Van Nieuwerburgh, Brookings, 2026; Hepp, Chicago Booth Review, 2026) say the 2008 comparison
goes too far.

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 Think tanks see echoes of subprime | partially supported | Report says "eerily reminiscent of the subprime bubble" (F04). But it is one report, the publisher is not called "OpenMarkets", and "a 2008 repeat" goes further than the report does | "An advocacy think tank sees echoes of the 2008 subprime crisis in how the AI build-out is financed." Change the kicker to "echoes of 2008" |
| c2 Debt repackaged and sold to pensions and endowments | partially supported | The report's words (F04). In its main text, the buyers are "insurers and pension funds" (F06). Endowments are exposed through private-credit funds (Hepp, F07). Securitized AI debt is about $60B (F08) | "Some data-center loans are bundled into bonds sold to insurers and pension funds; endowments are exposed through private-credit funds." The slide repeats itself, so drop either "repackaged and resold" or "bundled and sold to" |
| c3 Trillions on a revenue gap | partially supported | Spending is over $1T a year and sales cover at most 20% of it (report, F09). The build-out needs $3.7T a year in revenue by 2032 (Van Nieuwerburgh, F12). Lab losses come from press reports (F10). SEC actuals put capex at 95.5% of operating cash flow, which is not yet negative (`data/processed/capex_vs_ocf.csv`) | "Over $1 trillion a year on AI infrastructure; sales cover a fifth at most (report estimate). The leading labs reportedly lost billions in 2025." |
| c4 Contagion risk | supported (as the report's view) | "Deeply interconnected… would likely spread" (F13, F14). For balance, Van Nieuwerburgh calls the systemic-risk comparison "premature" (F15) | Keep as is |
| c5 (notes) Odds of a crash are rising; the bubble is unique in size and scope | supported | F17, F18 | Keep as is |
| c6 (notes) Regulators are rolling back safeguards; the report's recommendations | supported (as the report's view) | F19, F20 | Say "the report says" |
| c7 Source line | partially supported | The report came out Oct. 16, 2026 from OMI and the AFR Education Fund (F01–F03). The Futurism byline and date are correct (F21) | "Source: Open Markets Institute & Americans for Financial Reform, “Brace for Impact” (Oct. 2026); via J. Wilkins, Futurism, Oct. 26, 2026" |

## Not checked

- The SEC no-action letter on data-center securitizations (July 29, 2026) returned 403 to our User-Agent, so it is
  not used.
- The D.C. location of the think tank comes only from Futurism.

## Reproduce

```
uv run python slides/07-whose-debt/src/00_write_facts.py   # facts.csv (exact quotes)
uv run python slides/07-whose-debt/src/01_check.py         # fetch + log sources, verify quotes, compute ratios
```

The source documents are saved in `data/raw/sources/`, which is gitignored and logged in its `MANIFEST.yaml`.
The capex/OCF series is read from slide 06's SEC XBRL output.
