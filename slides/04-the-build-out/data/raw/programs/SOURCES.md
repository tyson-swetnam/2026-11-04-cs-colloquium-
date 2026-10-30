# Program spend series: sources and methods

All CSVs have the columns `year,nominal_usd_millions,note`. Some have extra columns after those, described below. Values are in **current (nominal) US dollars, millions**. No GDP or CPI denominators were fetched, except Gallman's constant-1860-dollar GNP, which comes with the railroad source itself.

Every number traces to a file in `sources/` that was downloaded and read in this session, or to a web page quoted below. Where the source did not give an annual series, the annual series here is **derived**, and the `note` column says so.

Reproduction: `src/programs/rebuild.sh` (from the slide folder). It runs `pdftotext -layout` on the Ulmer, Rhode and FA-203 PDFs in `sources/`, writes the results to `work/`, and then runs `parse_ulmer.py`, `parse_gallman.py` and `build.py`. It reproduces these CSVs byte for byte (checked 2026-10-30). The parsers apply internal consistency checks; see each section. Source documents are not committed. Their URLs and SHA-256 hashes are in `sources/MANIFEST.yaml`.

The "rough inflation" sanity notes use approximate CPI-U ratios to 2024 from memory: about ×18 for 1944, ×13 for 1949, ×9.7 for 1966, ×5.2 for 1977, and about ×25–38 for 1840–1900 dollars (MeasuringWorth-style CPI). They are only order-of-magnitude checks. Do not use them in the analysis.

---

## 1. Railroads (`railroads.csv`, 1830–1909): most important

**Bottom line.** 1830–1900 cumulative nominal: **$9.03 billion**. That is $0.99B for 1830–60, $1.05B for 1861–69 and $6.99B for 1870–1900 (Ulmer, excluding land; $7.16B including land). At about ×30 to 2024 dollars this is roughly **$270B**, about half of Moorhouse's $550B over 71 years. Moorhouse probably used a different method (for example miles × cost per mile at today's prices, or a wage or GDP-based deflator). Gallman's real-share numbers, below, are the cleaner basis for "share of GDP".

### 1a. Nominal series, `nominal_usd_millions`. It has three segments with different bases.

| Years | Value | Source | How obtained |
|---|---|---|---|
| 1870–1909 | Annual gross capital expenditures by steam railroads, **excluding land**, calendar year | Melville J. Ulmer (1960), *Capital in Transportation, Communications, and Public Utilities: Its Formation and Financing*, Princeton Univ. Press for NBER. Appendices, **Table C-10, col. 3** (pp. 271–272); identical to Table C-1 col. 3. https://www.nber.org/system/files/chapters/c1498/c1498.pdf → `sources/ulmer1960_appendices_c1498.pdf` | Text extracted from the OCR'd PDF. The parser checks col1 × (1 − col2) ≈ col3 for every year and that C-1 col 3 = C-10 col 3; all 81 years pass. The note gives the including-land figure (Table C-10 col. 1). |
| 1830–1860 | **DERIVED.** $990.7M distributed across 1830–1860 in proportion to miles of railroad built each year | Total: Fishlow's adjustment of the 1860 Census "cumulative cost of construction" ($1,151.6M), which excludes overvaluation (stock-paid construction), land and non-railroad assets and adds omitted roads. Reported in Gallman & Rhode (2020), *Capital in the Nineteenth Century*, NBER/Univ. of Chicago Press, ch. 10 "Transportation", §10.4.2 and **Table 10.6 panel A** (p. 245). https://www.nber.org/system/files/chapters/c14398/c14398.pdf → `sources/gallman_rhode2020_capital19c_ch10_transportation_c14398.pdf`. Miles built: NBER Macrohistory series **a02082a**, "Miles of railroad built, Census–Railway Age", 1830–1952 (1830–79 = HSUS 1960 series Q-43, from the 10th Census) → `sources/nber_macrohistory_a02082a.*` | Period total × (miles in year ÷ miles 1830–60). It is gross of depreciation and net of (negligible) retirements, on a cost basis. Small pre-1830 outlays (B&O, begun 1828) fall into 1830. Cost per mile varied over the period, so the annual shape is approximate. |
| 1861–1869 | **DERIVED.** $1,048.4M distributed by miles built 1861–1869 | $2,200M book value of construction accounts at the start of 1870 (Fishlow 1966, p. 592, citing *American Railroad Journal* 1870), minus the unadjusted 1860 Census cost of construction, $1,151.6M. Fishlow (1966), "Productivity and Technological Change in the Railroad Sector, 1840–1910", in *Output, Employment, and Productivity in the U.S. after 1800*, NBER Studies in Income and Wealth vol. 30. https://www.nber.org/system/files/chapters/c1578/c1578.pdf → `sources/fishlow1966_c1578.pdf` | Both ends are on an unadjusted book basis. Book values carry write-ups, which Fishlow's 1860 adjustment cut by about 14%, so this segment may be overstated by about 10–15%. It excludes retirements and replacements charged to operating expenses. |

Caveats:
- Fishlow (1966, pp. 589–594) argues that Ulmer's current-dollar series is **understated**, by about $1.6B over 1870–1910, because it excludes replacements under replacement accounting. He also says its annual timing is distorted, partly because inter-sample years were interpolated on track mileage.
- Fishlow did **not** publish an annual current-dollar series. His 1966 Table 7 gives decadal gross capital formation in **1909 dollars**: 1828–38 88.8; 1839–48 172.5; 1849–58 761.2 (Variant II) or 926.9 (Variant I). His antebellum annual estimates (*American Railroads and the Transformation of the Ante-Bellum Economy*, 1965, App. B) were not accessible: the archive.org copy is borrow-only, and I did not use it.

### 1b. Gallman constant-1860-dollar series (extra columns, added at the coordinator's request)

Source: Paul W. Rhode (2002), "Gallman's Annual Output Series for the United States, 1834–1909", **NBER Working Paper 8860**. https://www.nber.org/system/files/working_papers/w8860/w8860.pdf → `sources/rhode2002_nber_w8860.pdf`.
- **Table 1** (1834–1859, **census years**: "1839" = 1 Jun 1839–31 May 1840) gives Railroad gross new construction and GNP excluding inventory changes, in millions of 1860 dollars.
- **Table 2** (1869–1909, calendar years) gives the original Volume-30 Railroad construction, GNP excluding inventory changes, and **Gallman's 1994/96 revised railroad construction**, 1870–1909. The revision allocates his decadal real railroad investment by miles built; Rhode recommends it over the original series.
- Rhode's "As Corrected" rows fix a decimal error in 1875–77: the original RR becomes 28/29/34 and GNP becomes 6372.2/6795.0/7207.1. The corrected values are used.
- Rhode's required citation statement: **"These data were not constructed for analysis as annual series."**

Columns:
- `gallman_rr_construction_1860usd_millions`: the revised series for 1870–1909, and the only series available for 1834–59 (Table 1). It is blank for 1860–1869 (no annual data) and for 1869 (no revised value).
- `gallman_rr_construction_original_1860usd_millions`: the original Vol-30 series, which Rhode shows is poorly timed: its correlation with miles built is 0.07, and 1896–98 are zeros.
- `gallman_gnp_1860usd_millions`: GNP excluding inventory changes. For 1870–1909, Rhode notes the revised RR series changes GNP only slightly; GNP recomputed with the revised RR was not published.
- `gallman_rr_share_of_gnp_pct_1860prices`: **derived**, = 100 × RR ÷ GNP, both in 1860 prices. This is a **real** (constant-price) share, not a nominal share. No nominal railroad series is given in Rhode, and Table 3 (current prices) does not split out railroads, so no nominal Gallman values were derived.
- `miles_built`: from a02082a.

Check against Van Nieuwerburgh (2026): the mean revised share for 1870–1890 is **2.35%** here, against his 2.24%. The share is above 4% in **1871 (4.36%) and 1881 (4.08%)**; 1870 is 3.77%. With the *original* series, 1870 is 4.35%, so his "1870 and 1881" may mix vintages or use a different GNP column. Antebellum peak: 1853 at 2.49%.

---

## 2. Interstate Highway System (`interstate.csv`, 1956–1995)

- **Source:** FHWA, *Highway Statistics Summary to 1995*, **Table FA-203** "Expenditure of Federal Funds Administered by the FHWA, 1949–1995" (thousands of dollars), column "INTERSTATE". https://www.fhwa.dot.gov/ohim/Summary95/fa203.pdf → `sources/fhwa_summary95_fa203.pdf`. Downloaded text PDF, parsed.
- **Coverage:** the **federal share only**. The pre-1956 Interstate column (1953: $5.6M, 1954: $17.9M, 1955: $38.3M) is excluded. FY basis as in FHWA reporting. From 1992 (ISTEA), this column is Interstate construction only; Interstate Maintenance and Substitution are separate columns.
- **Extra column** `total_incl_state_match_est_usd_millions`: **derived** = federal × (128.9 ÷ 114.3). It uses the final 1991 Interstate Cost Estimate: "total cost $128.9 billion (Federal share: $114.3 billion)". Source: R. Weingroff, FHWA, "The Golden Fleece: Why was the $27 billion estimate so wrong?", https://www.fhwa.dot.gov/infrastructure/50estimate.cfm → `sources/fhwa_infrastructure_50estimate.html`.
- **Totals 1956–1992:** federal **$107.8B**; estimated federal + state **$121.6B**. The expenditure-weighted mean year is about 1977, so ×5.2 gives roughly $560–630B in 2024 dollars, consistent with Moorhouse's $620B over 37 years (1956–1992).
- Not used: the ICE estimate is a cost-to-complete estimate, not annual spending, so it serves only as the scaling ratio.

## 2b. All-government highway capital outlay (`highways_all.csv`, 1945–2014; coordinator request)

- **Source:** FHWA, *Highway Statistics 2014*, **Table DISB-C**, "Total disbursements for highways, by function, 1945–2014", chart-data sheet. https://www.fhwa.dot.gov/policyinformation/statistics/2014/xls/disbc.xls (and the PDF) → `sources/fhwa_hs2014_disbc.xls`, `.pdf`.
- `nominal_usd_millions` = Capital Outlay × 1000. The source is in billions, mostly to 3 decimals, with some later years at full precision. Extra columns hold maintenance, administration/enforcement/bond interest, and debt retirement. All units of government.

## 3. Apollo (`apollo.csv`, FY1960–FY1973)

- **Source:** Casey Dreier / The Planetary Society, "How much did the Apollo program cost?" dataset. Google Sheet `1QW8MaPWa2YXDik52h4M0LN4SVc_tINoFEwashbaOjgE`, exported as xlsx → `sources/tps_cost_of_apollo.xlsx`. Sheet **"Apollo Program (original $)"**, in thousands of dollars. Its underlying data are NASA budget-justification "actual" obligations for FY1961–74, plus NASA HQ Budget Operations cost summaries (see the "Sources" sheet). Peer-reviewed version: Dreier, *Space Policy*, "An Improved Cost Analysis of the Apollo Program".
- `nominal_usd_millions` = **Annual Direct Costs + Annual Indirect Costs** (construction of facilities, operations and overhead, tracking and data). This sums to the sheet's "Total Project Apollo", **$25.774B**. Extra columns: direct R&D only ($20.58B in total), and "Lunar Effort Total", which adds Gemini and robotic lunar missions ($27.97B).
- NASA **fiscal years**: through FY1976 these run 1 Jul–30 Jun (e.g. FY1966 = Jul 1965–Jun 1966). Obligations, not outlays.
- Sanity: $25.8B centered around 1966 × about 9.7 ≈ $250B, against Moorhouse's $257B over 14 years (1960–73). Consistent.

## 4. Manhattan Project (`manhattan.csv`, 1942–1946)

- **Source:** Richard G. Hewlett & Oscar E. Anderson Jr. (1962), *The New World, 1939–1946* (History of the U.S. Atomic Energy Commission, vol. I), **Appendix 2, "Monthly Expenditures in the Manhattan Engineer District, August 1942 through December 1946"** (in thousands), p. 724. https://www.energy.gov/sites/prod/files/2013/08/f2/HewlettandAndersonNewWorldNoBookmarks.pdf → `sources/hewlett_anderson_1962_new_world.pdf`.
- Values are the printed **calendar-year** totals. The monthly figures were re-summed and match every annual total and the grand total of **$2,191,458K**. 1942 covers Aug–Dec only and includes $15.0M "transferred to OSRD". Excluded: pre-August-1942 OSRD/NDRC S-1 spending, and the roughly $76M Army Air Forces SILVERPLATE spending noted by Brookings.
- The same appendix gives cumulative cost by site through 31 Dec 1945: $1,889.6M (plant $1,382.0M + operations $507.6M).
- Sanity: $2.19B × about 17–18 ≈ $37–39B, against Moorhouse's $36B over 5 years. Consistent.

## 5. Marshall Plan / ERP (`marshall.csv`, FY1949–FY1952)

- **Source (annual):** USAID, *U.S. Overseas Loans and Grants* ("Greenbook"), obligations by fiscal year. The official data.usaid.gov copy was taken down in Jan 2025; the file here is the mirror at https://foreignassistance.andrewheiss.com/data/us_foreignaid_greenbook.xlsx ("Prepared by USAID Data Services on August 9, 2022") → `sources/usaid_greenbook_us_foreignaid_greenbook_heiss_mirror.xlsx`.
- **Selection (derived):** funding accounts "INACTIVE - USAID Grants" + "INACTIVE - USAID Loans" (the ECA/MSA predecessor agencies), FY1949–52. Included: Western/Eastern Europe region rows for the 16 ERP participants plus "Western Europe (not specified)", and Indonesia FY1949–50 only (Dutch East Indies aid counted under the ERP before December 1949). Excluded: Yugoslavia ("Serbia and Montenegro, Former") and Spain, which were not ERP participants.
- **Validation:** total **$13,326.6M**, against $13,325.8M in CRS R45079 Table 2 (Tarnoff, "The Marshall Plan: Design, Accomplishments, and Significance", 2018; recipients Apr 3 1948–Jun 30 1952). Country totals match, e.g. UK 3,189.9 vs 3,189.8 and France 2,713.8 vs 2,713.6. CRS page saved: `sources/crs_R45079_marshall_plan_everycrsreport.html` (from everycrsreport.com).
- **Fiscal years:** **FY1949 covers 3 Apr 1948–30 Jun 1949 (15 months)**; FY1950–52 run July–June. A calendar-year split would need an assumption, which I did not make.
- Extra column `crs_funds_made_available_usd_millions`: CRS R45079 **Table 1** (from Brown & Opie 1953, p. 247), "Funds made available to ECA": 6,220.6 / 4,060.2 / 2,254.1 for FY49–51 (total $12,534.9M to June 1951). This measures authority, not obligations.
- Sanity: $13.3B × about 13 ≈ $170–175B, against Moorhouse's $170B over 4 years. Consistent.

## 6. F-35 (`f35.csv`): NO ANNUAL DATA (header only)

- The annual then-year funding tables are in DoD Selected Acquisition Reports (esd.whs.mil). Every SAR/MSAR URL tried returned HTTP 403 (Akamai), DTIC copies returned 403, and the Wayback Machine is blocked by this sandbox's egress policy. No annual profile was invented.
- **Source total** (CRS R48304, "F-35 Lightning II: Background and Issues for Congress", Dec 2024, citing the Dec 2023 SAR): airframe acquisition **$401.1B then-year** (RDT&E $71.3B + procurement $325.8B + MilCon $4.0B), plus the F135 engine at $84.1B, for a program total of $485.2B TY. Saved: `sources/crs_R48304_f35_everycrsreport.html`. This is a full-program estimate (2,470 aircraft through the 2040s), **not spending to date**. Moorhouse's "$400B to date" matches the $401.1B airframe TY total, so he may have used this figure.
- To fill this in, download a recent F-35 SAR/MSAR ("Annual Funding TY$" tables by appropriation) from a network that can reach esd.whs.mil.

## 7. ISS (`iss.csv`, FY2008–FY2026 only; partial)

- **Source:** The Planetary Society, "Historical NASA Budget Dataset" (Dreier). Google Sheet `1NMRYCCRWXwpn3pZU57-Bb0P1Zp3yg2lTTVUzvc5GkIs` → `sources/tps_historical_nasa_budget.xlsx`. Per-fiscal-year sheets, **"Actual"** column; the actuals come from later-year NASA budget justifications.
- **Definitions change:**
  - FY2008–2016: the "ISS" line, which included ISS crew and cargo transportation.
  - FY2017 onward: "ISS" + "Space Transportation", after the split. Space Transportation also includes Commercial Crew development, so FY2017–20 is biased up by roughly $1B/yr. Both components are given in extra columns.
  - FY2026 is the value recorded in the FY2026 sheet; treat it as preliminary.
- **Not obtained annually:** FY1985–FY2007. Period totals from CRS IB93017 (M. Smith, "Space Stations", 4 Jan 2006; `sources/crs_IB93017_space_stations_20060104.html`): "From FY1985–FY2005, Congress appropriated approximately $35 billion for the space station program", of which **$11.4B** was Freedom, FY1985–1993. FY2006–07 is missing. Shuttle flights to ISS and partner contributions are excluded throughout.
- FY2008–2025 total: $53.1B. Adding about $24B (FY1994–2005) and about $3–4B (FY2006–07, not obtained) gives roughly $80B nominal for NASA-only ISS since 1994, before Shuttle support. Moorhouse's $150B over 27 years likely includes Shuttle-to-ISS costs or partner costs, so it is not comparable without those.

---

## Extra comparators (coordinator request)

### Canals (`canals.csv`, 1815–1860)
- H. Jerome Cranmer (1960), "Canal Investment, 1815–1860", in *Trends in the American Economy in the Nineteenth Century*, NBER Studies in Income and Wealth vol. 24, pp. 547–570, **Table 3 col. 1** (US total, state + private, millions of current dollars). https://www.nber.org/system/files/chapters/c2489/c2489.pdf → `sources/cranmer1960_c2489.pdf`.
- The text layer's row alignment was scrambled for 1820–1839, so those years were **verified against a rendered image of p. 555**. 1815–16 are "a" (< $0.05M), left blank.
- The rows sum to $194.9M, against the printed total of $194.6M; the source notes that rounding makes rows differ from totals. The values match the text's checks: about $50M spent by 1831, about $70M in the 1836–44 cycle, and a 1840 peak of $14.3M.
- Gallman/Rhode's footnote 52 notes a later revision removing $6.4M of Pennsylvania Mainline *railroad* spending (1829–45) from the canal series. It is not applied here.

### Electric light and power (`electrification.csv`, 1881–1950)
- Ulmer (1960), Appendix D, **Table D-1 col. 3**: gross capital expenditures, current dollars, privately owned electric utilities, excluding land (same PDF as the railroads).
- The parser checks col3 = col5 + col7 (capital consumption + net) to ±0.1 for all years. 1950 fails only because the col-7 OCR is garbled; 833.6 + 1,051.5 = 1,885.1 holds. OCR fixes applied: "115,6" → 115.6 (1918), "1,823:5" → 1,823.5 (1948).

## Files not used in the series but kept for provenance
- `sources/hsus1949_chK.pdf` (HSUS 1789–1945 ch. K) holds railroad capitalization 1850–1890, but the OCR of the 1860s rows is unreliable.
- `sources/hsus1960_chQ.pdf` (HSUS 1957 ch. Q, transportation).
- `sources/nber_macrohistory_a02082.*` holds Poor's mileage increases, 1831–1911.
- `sources/fhwa_summary95_fa204.pdf`.
- The Statistical Abstract 1954 scans had no text layer, and no OCR tool was available, so they were not used.
