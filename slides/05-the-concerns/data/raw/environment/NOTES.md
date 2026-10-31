# s05 Environment: research notes (fact-check for slide "Environmental cost")

Researched 2026-10-30. Every number in facts.csv comes from a page or document fetched in this session. Local copies are in `raw/` (PDFs, xlsx) and `raw/html/` (saved news and press-release HTML).

## Headline takeaways
- **US electricity:** LBNL's 2025 Update (published June 2026) supersedes the Dec 2024 report. US data centers used **192 TWh in 2024, 4.7% of US electricity**. The reference case is **649 TWh in 2030 (11.8%)**, with a range of 521–843 TWh (9.5–15.3%). The 2024 report's figures, via DOE's release, were 176 TWh and 4.4% in 2023, and 325–580 TWh (6.7–12%) by 2028.
- **US water:** LBNL 2024 §5, as cited on a DOE national-lab slide (NLR, Sept 2026), gives **66 billion L direct (~17.4 billion gal) in 2023** and **nearly 800 billion L indirect (~12× direct)**. The 2025 Update has no water estimate.
- **Project Jupiter (Santa Teresa, Doña Ana Co.):**
  - Developers are BorderPlex Digital Assets and Stack Infrastructure. Tenants are Oracle and OpenAI, and it is one of the Stargate sites announced 2025-09-23.
  - The county approved a **$165B IRB** (4-1) on 2025-09-19.
  - The power source is the **YGI Microgrid**, Bloom solid-oxide fuel cells running on natural gas. Nameplate is **2,462 MW** (NMED notice). The revised application adds an enforceable operating cap of **1,600 MW** (news report).
  - NMED's draft Statement of Basis (7/29/26), written before the cap, lists **8,820,970 tpy GHG**.
  - The air permit has **not been issued**. The public hearing starts **Dec 7, 2026**.
  - The NM Supreme Court stayed the permit proceeding and the well (Aug 23), then lifted both stays (Sept 17).
  - On Oct 27, 2026 the county voted to notify the developers of a "potential breach" of the IRB over Oracle's proposed El Paso Electric backup-power deal.
- **NM baseline (EIA 2024):** 30.3 TWh retail sales, 11,887 MW net summer capacity, 39.7 TWh generation, 13.4 Mt CO2 from the power sector at 743 lb/MWh. PNM's all-time peak was 2,264 MW on 2026-08-03 (ABQ Journal, quoting PNM).

## Comparisons (our arithmetic, from facts in facts.csv)
| Comparison | Arithmetic | Result |
|---|---|---|
| YGI nameplate vs NM capacity | 2,462 / 11,887 MW | 20.7% |
| YGI nameplate vs PNM all-time peak | 2,462 / 2,264 MW | 109% (exceeds) |
| 1,600 MW cap vs PNM peak | 1,600 / 2,264 | 71% |
| 1,600 MW run all year | 1,600 MW × 8,760 h = 14.0 TWh; ÷ 30.3 TWh | 46% of NM 2024 retail sales |
| 2,462 MW run all year | 21.6 TWh ÷ 30.3 TWh | 71% of NM retail sales |
| NM average load, 2024 | 30,296,354 MWh ÷ 8,784 h (leap year) | ≈3,450 MW |
| Draft-permit GHG vs NM power-sector CO2 | 8,820,970 short t × 0.9072 = 8.0 Mt ÷ 13.4 Mt | ≈60% (pre-cap; CO2e vs CO2, so indicative only) |
| Implied GHG intensity | 8,820,970 t × 2,000 lb ÷ (2,462 MW × 8,760 h) | ≈818 lb/MWh vs NM grid 743 lb/MWh |
| US data centers vs all of NM | 192 TWh ÷ 30.3 TWh | 6.3× NM's 2024 retail sales |
| Meta Los Lunas water | 213.4 ac-ft × 325,851 gal | ≈69.5 million gal/yr |
| PNM data-center requests, 2025 | 0.47 × 5,321 MW | ≈2,500 MW |

Caveats:
- The 1,600 MW cap is reported by the ABQ Journal from YGI's revised application. The revised application itself was not read; it sits in the NMED Administrative Record supplements.
- The "1,600 MW × 8,760 h" figure is an upper bound on the energy the microgrid could generate. It is not a measured load, and the data center may also draw from El Paso Electric.
- The ABQ Journal says 2.4 GW is "roughly equivalent to the power provided by [PNM]'s entire grid". That holds against PNM's peak (2,264 MW) but not against PNM's quoted total grid capacity of ~4,900 MW.

## Conflicts and uncertainties to flag
1. **Jupiter capacity estimates have grown.** WRA (Oct 2025) estimated 700–900 MW and 3–4 Mt/yr GHG. NMED's 2026 figure is 2,462 MW nameplate; news reports round it to 2.4 or 2.45 GW.
2. **Jupiter water, conflicting claims:**
   - Oracle says operations will use about as much water as nine US households per year, averaged over 15 years, with no potable water for cooling.
   - OSE's general counsel, via the Santa Fe New Mexican and relayed by the ABQ Journal, said the earlier gas-plant design would need nearly 1 million gal/day. The ABQ Journal could not verify this.
   - CBD says the well supplied more than 197 million gallons for construction.
   - The IRB caps potable use at 60,000 gal/day, with an average of 20,000.
3. **NM statewide data-center water:** HARC's slide says 502 Mgal/yr now and about 16 Bgal/yr planned. A search snippet attributed a 23.6 Bgal/yr projection to coverage of the same hearing, but Source NM returned 403, so that figure is unverified.
4. **Meta Los Lunas site size:** OSE says about 537 acres; the Village of Los Lunas says a 1,200-acre campus. No primary source gave Meta's load in MW. Aggregators say 200–400 MW, which is not verified.
5. **US 2028 water projection:** search snippets cite 38–73 billion gal (LBNL), but no fetched document confirmed it. Not used.
6. **IEA vs LBNL:** LBNL says IEA's 2030 US figure is about 430 TWh, against LBNL's 649 TWh.
7. **Short tons vs metric tons:** NMED "tpy" is taken to mean short tons (assumed). EIA reports thousand metric tons.

## Blocked sources (not circumvented)
- **LBNL 2024 report PDF:** eta-publications.lbl.gov redirects to eScholarship, which returned an empty 202 bot challenge. The climate.mit.edu mirror returned 403 (Akamai), and LBNL news pages returned 403. Its figures were obtained from the DOE release and the NLR slide instead.
- **IEA "Energy and AI":** 403.
- **Source NM / newsfromthestates.com:** 403.
- **SEC EDGAR (TXNM 10-K, PNM peak table):** 403, because SEC requires a declared User-Agent. Not retried with a custom UA.
- **cloud.env.nm.gov** returned 403 to curl. The Statement of Basis PDF was retrieved through WebFetch and saved to raw/.

## Notes on quotes
- Quotes from slide decks (NLR, OSE, PRC, HARC, WRA) were reassembled from multi-column PDF text. In those quotes, " / " and "•" mark line or bullet breaks and "..." marks omitted text.
- EIA quotes are rows from the xlsx, with cells separated by "|".

## Files
- `raw/lbnl_2025_update.pdf`: LBNL 2025 Update (OSTI 3374245)
- `raw/osti_17273330.pdf`: NLR "Managing Water Resources around Data Centers"
- `raw/osti_3020313.pdf`: PNNL water-security brief (background only)
- `raw/shehabi_eli_slides.pdf`: Shehabi ELI slides (176 TWh / 325–580 TWh)
- `raw/drbc_thompson.pdf`: DRBC slides (figures are images; not used)
- `raw/eia_SEP_Tables_for_NM_2024.xlsx`: EIA NM State Electricity Profile 2024, full tables
- `raw/nmed_AQB26-57_amended_notice_2026-08-12.pdf`, `raw/nmed_AQB26-57_2nd_amended_sched_order_2026-10-16.pdf`, `raw/nmed_10883_draft_statement_of_basis_2026-07-29.pdf`: NMED filings
- `raw/nmlegis_*.pdf`: NM Legislature committee handouts (PRC, OSE, HARC, Meta, WRA, Los Lunas)
- `raw/pnm_irp2026_forecasts_demand_markets.pdf`: PNM 2026 IRP workshop forecast slide
- `raw/wra_2025_DataCenter_FactSheet_NM.pdf`: WRA NM fact sheet
- `raw/newera_7GW_LeaCounty_pr_2025-11-06.pdf`: New Era press release
- `raw/html/`: Oracle releases (2026-07-28, 2026-09-14, 2026-10-13), SoftBank/Stargate release, DOE release, ABQ Journal and KRWG/KOB articles, NMED docket pages
