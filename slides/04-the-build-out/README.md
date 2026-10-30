# Slide 04 · The build-out

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-04)

> **The largest single investment in human history**
> US data-center build: $560B through 2026 · $800B on the 2027 run rate
> *Notes:* Six years of data-center capex has already outrun 71 years of railroads and 37 years of the Interstates.

The slide follows Fin Moorhouse's chart ["The hyperscalers have already outspent the most famous US megaprojects"](https://x.com/finmoorhouse/status/2044933442236776794) (17 April 2026). That chart plots cumulative cost in 2024 dollars against years since each program started. In those units data centers reach ≈$930B in six years, against $620B in 37 years for the Interstates and $550B in 71 years for the railroads.

## The question this folder answers

CPI-adjusted dollars answer one question: what would the same basket of goods cost today? They do not answer how big a commitment each program was for the economy that paid for it. The US economy of 1870 was a small fraction of today's, in population and in output per worker. A railroad dollar in 1870 therefore used up a much larger share of what the country could produce. This folder rebuilds Moorhouse's comparison and then tests it under measures that account for that growth. It also adds the private capital booms that are a better match for hyperscaler capex than government programs: railroads, oil and gas, telecom and post-war reconstruction.

## Measures

Each is a function in [`evidence/econ.py`](../../evidence/econ.py). The names follow MeasuringWorth's *Measures of Worth*.

| Measure | Formula (per year *t*, then summed) | What it answers |
|---|---|---|
| CPI-real dollars (Moorhouse) | spendₜ × CPI_ref / CPIₜ | What the same goods would cost today |
| GDP-deflator dollars | spendₜ × P_ref / Pₜ | Same idea, with the whole economy's prices instead of a consumer basket |
| Share of GDP, cumulated | Σ spendₜ / GDPₜ | How many years of the whole economy's output it absorbed ("GDP-years") |
| Economic share | Σ (spendₜ / GDPₜ) × GDP_ref | The same share, priced at the size of today's economy |
| Per-capita-income value | Σ spendₜ / (GDP/pop)ₜ × (GDP/pop)_ref | Adjusts for productivity growth per person, but not for population growth |

The "cumulative productivity gains" correction is the gap between the first row and the last two. In the economic-share and per-capita-income rows, a dollar is weighted by how productive the economy was when it was spent.

## Outputs planned

1. **Baseline:** Moorhouse's chart rebuilt from primary sources in CPI-real dollars. If it does not match his to within a few percent, find out why before going further.
2. **Cumulative share of GDP against years since start:** the main corrected chart.
3. **Annual intensity:** spend as a percentage of GDP in each program year. This shows how hard each boom pushed at its peak, not only how long it ran.
4. **Ranking table:** each comparator's rank under every measure. This table decides claim `c1`.
5. **Private-capex panel:** data centers against railroads, shale, telecom and post-war investment, in share of GDP. Optionally add a net-capital-stock view, because GPUs depreciate in about five years and rail and highways over decades.

## Layout

```
04-the-build-out/
├── README.md          this file
├── claims.yaml        the five claims on the slide and in the notes, with status
├── comparators.yaml   every program, its years, financing, and candidate data series
├── src/               numbered scripts: 01_fetch → 02_build → 03_normalize → 04_figures
├── data/raw/          downloads as fetched, with MANIFEST.yaml (URL, date, SHA-256)
├── data/processed/    tidy CSVs: program, year, nominal_usd, source; then one column per measure
└── figures/           PNG and SVG for the deck, plus the ranking table as CSV
```

Run with `make slide-04` from the repo root once the scripts exist.

## Open decisions (to settle together)

- **What "productivity-corrected" means for the talk.** Economic share (GDP share, so population and productivity both count), per-capita income (productivity per person only), or output per hour worked (labor productivity proper; needs a historical hours series).
- **Data-center scope.** "US data-center build" (US-located; the slide's $560B) or global spend by US hyperscalers (Moorhouse's $930B). The answer also fixes the denominator: US GDP or world GDP.
- **Post-war reconstruction.** The US private investment boom of 1946–1960, or European and Japanese rebuilding. The second needs non-US GDP.
- **Oil and gas episode.** The shale boom (2008–2015), the 1973–1982 oil boom, or both.

## Evidence

_Nothing yet._
