# s05 — "Researchers' work in closed systems" (fact-check notes, 2026-10-30)

All numbers in `facts.csv` come from documents fetched in this session. Raw files are in `raw/`. The scripts are kept separately in
`/tmp/claude-0/-home-user-2026-11-04-cs-colloquium-/f08c2bb6-0d45-5d8b-ab04-36cbd8ea6e56/scratchpad/s05_scripts/`, and nothing in `raw/` was executed.

## Computed numbers (reproducible)

1. **The Pile's scholarly share** (`pile_shares.py raw/pile_src/extracted/the-pile.tex`). The script parses the LaTeX source of Table 1 from the arXiv e-print. It checks that the totals reproduce 825.18 GiB raw and 1254.20 GiB effective, and that the weights sum to 100.00%.
   - PMC 14.40% + ArXiv 8.96% + PhilPapers 0.38% = **23.74%**. These are the full-text papers.
   - Adding PubMed Abstracts 3.07% and NIH ExPorter 0.30% gives **27.11%** of The Pile's effective bytes (340.05 / 1254.20 GiB).
   - On a raw-size basis (no upsampling), the share is 20.60% (170.01 / 825.18 GiB).
   - PMC is the 2nd-largest of the 22 components and ArXiv is the 5th.
2. **Scholarly text inside a closed model, BloombergGPT** (Table 2 of arXiv:2303.17564). The scholarly Pile parts are PMC 2.96 + ArXiv 2.35 + PubMed Abstracts 0.50 + PhilPapers 0.08 + NIH ExPorter 0.04, which is **5.92% of training tokens**: 420e8, about **42B tokens** out of 7,089e8. The model was not released.
3. **Cross-corpus shares** (`corpus_card_shares.py raw`):
   - Dolma v1.7, peS2o + arXiv: 85.2B / 2,308.5B = **3.69%**
   - Dolma v1.6, peS2o: 2.29%
   - OLMo-2 mix: 79.4B / 3.90T = **2.04%**
   - RedPajama-1T, arXiv: 28B / 1.2T = **2.33%**
   - LLaMA-1, ArXiv: 2.5% (stated in the paper, not computed)
   - The scholarly share is far larger in The Pile than in later web-heavy mixes.
4. **PMC licence breakdown** (`pmc_counts.sh`, NCBI E-utilities, queried 2026-10-30). The filter syntax comes from NLM's PMC AWS README.
   - Total PMC: **12,755,502** articles
   - Commercial-reuse CC licences (CC0/BY/BY-SA/BY-ND) in the OA or author-manuscript sets: **5,527,851 (43.34%)**
   - NC-only CC licences: 2,423,801 (19.00%)
   - Bulk-minable (OA subset or author manuscript): 9,382,251 (73.55%)
   - Not in either set: 3,373,251 (26.45%)
   - These counts change daily. The raw JSON responses and the query log are in `raw/pmc/eutils/`.
5. **Wiley cross-check**: FY24 + FY25 + FY26 = 23 + 40 + 49 = $112M. This is consistent with the press release's "lifetime AI revenue surpassed $110 million".

## Caveats / things NOT verified
- **Blocked sources:**
  - informa.com PDFs returned 403, so I used the identical RNS filings on the FCA National Storage Mechanism.
  - SEC EDGAR refused requests with an undeclared User-Agent. I did not want to put the user's email in a header, so the Wiley 10-K detail ("$49.1M, of which $19.4M content licensed from other publishers") is **unverified**.
  - The Wiley FY26 release blocked curl but loaded via WebFetch. The quotes are fragments joined with "...".
  - Nature news (d41586-024-02599-9) redirected to a login, so it was skipped.
  - The Bookseller T&F piece is paywalled, so only the standfirst is quoted.
- **Wording:** Wiley's FY26 figure is called "AI revenue", while FY25 used "AI licensing revenue". Informa's 2024 figure was a forecast in July 2024 ("expected to be over $75m"). It was confirmed as "$75m+ of data access revenue which is non-recurring" in March 2025. Informa did not disclose the 2025 amount, saying only that it was "lower than the exceptional levels achieved in 2024".
- **Authors asked or paid?**
  - T&F: authors claimed no notice, no opt-out and no extra pay (Bookseller standfirst, 2024-07-19). Informa says the deals bring "additional royalties for authors" (RNS, 2024-07-24).
  - Wiley: compensation "in accordance with existing contractual agreements". No opt-in was mentioned.
  - CUP: opt-in. It consulted more than 40,000 authors and says a "majority" opted in, without giving a percentage.
  - Sage: royalties per existing contracts.
  - OUP: "actively working with" LLM developers. No figures were found.
  - De Gruyter Brill: **nothing found** in primary sources, so it was not included.
- **Survey figures:** For the OUP survey, OUP says ">2,000" researchers and THE says ">2,300". The 8% figure matches in both.
- **DE-COP:** arXivTection is only 50 papers. Treat it as proof-of-concept evidence that arXiv papers appear in Claude, LLaMA-2 and Mixtral training data, not as a census.
- **NSF dates:** Supplement 2 (NSF 26-202, effective 2026-01-22) was verified on nsf.gov. Supplement 1 (NSF 26-200, 2025-12-08) appears only in university summaries.
- **NIH APC cap:** NOT-OD-25-138 was an RFI. Search results suggest no final cap had been issued as of March 2026, but I did not verify this against the primary source and did not include it.
- **Not computed:** the arXiv licence distribution. The metadata dump is too large for this pass. The arXiv default licence "limits re-use of any type from other entities", yet open corpora ingest all arXiv sources.

## Raw files
- `raw/pile_src/`: arXiv e-print of 2101.00027 (tar.gz plus extracted .tex/figures)
- `raw/pile_table1_parsed.csv`: parsed Table 1
- `raw/hf_cards/`: README dataset cards for dolma, peS2o, RedPajama-1T, olmo-mix-1124, dolmino-mix-1124
- `raw/publishers/`: Informa RNS HTML and text (2024 HY, 2024 FY, 2025 HY, 2025 FY)
- `raw/policy/`: OSTP memo PDF and text; NIH NOT-OD-25-047, -049 and -101
- `raw/pmc/`: PMC FTP readme, AWS README, E-utilities JSON
- `raw/papers/`: arXiv sources for DE-COP, LLaMA, GPT-4 report and BloombergGPT, plus abstracts for Copyright Traps and DE-COP
- `raw/open_models/`: AlphaFold DB download page, AlphaFold GitHub README
- `raw/web_snapshots/`: OUP survey page, CUP AR2025 page, NSF supplement, CC page, arXiv licence page, Arc Evo 2, Bookseller articles, THE article
- `raw/computed_outputs.txt`: output of both scripts
