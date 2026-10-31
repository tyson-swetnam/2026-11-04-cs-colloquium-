# Slide 08 · Power, water and public health

Section: 01 · Fear · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-08)

Added in the revised deck (2026-10-31). Claims are listed in [`claims.yaml`](claims.yaml).

## Findings (checked 2026-10-31)

The slide is broadly right. Main problems:
1. The Colossus 2 numbers (27 turbines, about 1,700 t NOx) date from the April 2026 complaint. The complaint says "approximately" 1,700 t, as a potential to emit; "more than 1,700" is SELC's and Earthjustice's wording. SELC's Oct. 2026 release gives higher emission figures (>5,000 t NOx) but no new turbine count; it called the 27-turbine fleet "dozens" in April too.
2. The recycling plant has a promised restart date (Q1 2027), and it treats Maxson wastewater rather than sitting at Maxson.
3. The "Unpaid Toll" figures are scenario projections in every version: v1 (2024) uses McKinsey's medium-growth case for 2030; v4 (2026) uses its high-growth case for 2028. Costs are "up to more than $20B".
4. "Data centers reach 945 TWh by 2030" is an IEA projection, not a fact.

Correction (2026-10-31, after review): earlier text here said the Colossus 2 fleet "has grown beyond 27" and that the suit alleges "more than 1,700 tons". Neither is supported by the sources; both are fixed below.

The emissions and turbine figures are allegations made by the NAACP and its counsel. The Oct. 30, 2026 order denied a motion to dismiss; it did not decide liability.

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c1 IEA: more than double, ~3%, Japan, 945 TWh | supported | IEA press release (verbatim reprint): "more than double by 2030 to around 945 TWh, slightly more than ... Japan today" (F01, F02); "just under 3%" (F03, F04); 945/415 = 2.28x. iea.org itself blocked us (403 challenge) | "…to just under 3% of the world total, about what Japan uses today (IEA, 2025)" |
| c2 35 turbines at Colossus 1; 27 at Colossus 2; 1,700+ t NOx | partially supported | 35 is from SELC (F06). The court order recites the complaint: ≥27 turbines, ≥495 MW (unit mix sums to 495), potential to emit "approximately 1,700 tons" NOx (F08, F33, F09). "More than 1,700" is counsel's wording (F35). SELC's Oct. figures are higher (>5,000 t, F11) but give no count; "dozens" was used for 27 in April too (F34) | "Colossus 2 is powered by unpermitted turbines in Mississippi: the April 2026 suit names 27 and alleges they could emit about 1,700 tons of NOx a year." |
| c3 Aquifer; 3.7 MGD requested; plant stalled April 2026 | supported | E&E News/Politico, citing MLGW (F17–F19). Restart promised by Q1 2027 (WWD, June 2026, F21) | Add "xAI now says it will restart in early 2027." |
| c4 (notes) 1,300 deaths, 600,000 asthma cases, $20B, by 2030 | partially supported | v1 (2024): 2030, McKinsey medium-growth case, "up to more than $20 billion" (F24, F37, F38). v4 (June 2026, retitled "Health-Informed Computing"): 2028, high-growth case, "1,300 premature deaths", "up to more than $20 billion" (F25, F26, F39, F40). Both are scenarios; cost is not "close to" $20B; cases are "asthma symptom cases" | "In a high-growth scenario … could cause about 1,300 premature deaths and 600,000 asthma symptom cases in 2028, with health costs of up to more than $20B (Han et al., preprint, rev. 2026)" |
| c5 Jevons, 1865 | supported | Ch. VII: "wholly a confusion of ideas … The very contrary is the truth"; Watt's inventions were "modes of economising heat" (F27–F30). The link to AI is the speaker's analogy, and 945 TWh is an IEA projection (F01) | "AI may be doing the same: the IEA projects data centers will use about 945 TWh by 2030." |
| c6 (notes, new) 27 turbines, 495 MW, ½ mile from homes, 1,700 t NOx, 180 t PM, 19 t formaldehyde | partially supported | Match the complaint as the court recites it ("approximately", potential to emit), plus Earthjustice for the distances (F08, F33, F09, F12). "More than 1,700" / "up to 180" are Earthjustice's words (F35). Should be framed as allegations dated April 2026 (F11) | "at least 27 (495 MW) when the NAACP sued in April 2026. The complaint alleges they could emit about 1,700 t NOx, 180 t fine particulates and 19 t formaldehyde a year." |
| c7 (notes, new) NAACP suit; MTD denied Oct. 30, 2026 | supported | Opinion and Order, N.D. Miss. No. 3:26-cv-74, Doc. 139, signed by Judge Brown (F13–F15). A DOJ motion was denied "shortly" before, per SELC; no date given (F36) | Keep; say this was a motion-to-dismiss ruling |
| c8 (notes, new) ALA F for ozone | partially supported | SELC only (F16). The ALA pages load grades by script, so we could not read them | Check lung.org in a browser |
| c9 (notes, new) Colossus 1 since June 2024; removed turbines, 15 permitted | supported (SELC account) | F06, F07 | Keep, credit SELC |
| c10 (notes, new) Maxson recycling plant, permit Jan. 2026, 13 MGD, paused April 2026 | partially supported | Memphis Flyer citing TDEC (F22, F23); pause from E&E News (F18). The plant treats Maxson effluent; it is not described as at Maxson | "A recycling plant to treat T.E. Maxson wastewater…" |

## Not checked

- The IEA executive summary on iea.org (Cloudflare challenge, 403). The figures come from a verbatim reprint of the IEA press release and from news reports.
- The current Colossus 2 turbine count (press reports range from 46 to 59; SELC gives none), the date of the DOJ motion ruling, the MDEQ permit itself, the Shelby County permit for Colossus 1, and the ALA county grades.
- Any MLGW document for the 3.7 MGD figure; it is known only through E&E News.

## Reproduce

```
uv run python slides/08-power-water-health/src/01_fetch.py   # fetch + log sources (MANIFEST.yaml)
uv run python slides/08-power-water-health/src/02_check.py   # verify facts.csv quotes; computed.csv
```

Sources are saved in `data/raw/sources/` (gitignored). The quote check normalises whitespace, curly quotes and dashes.
