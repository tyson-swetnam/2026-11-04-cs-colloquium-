# s05 Training and misuse: research notes (2026-10-30)

Facts with exact quotes are in `facts.csv` (27 rows). Source documents are in `raw/`.

## How the quotes were checked
- **Checked against downloaded text in `raw/`:** A1, A2, A5–A9, A11, B1–B5, B6 (GTIG page saved later), C1–C7, D1 (Epoch page saved later), D2.
- **Taken from a WebFetch extraction, with no local copy:**
  - A3: settlement site homepage. curl got a 403; WebFetch worked.
  - A4: Pearl Cohen.
  - A10: Wikipedia.
  - A12: MediaLaws.
  - Treat these as quoted through an extraction model. Re-open the URL before putting any of them on a slide.
- **Text files in `raw/` and their sources:**
  - `b.txt`: Bartz order, layout text.
  - `k.txt`: Kadrey order.
  - `ross.txt`: 3d Cir. opinion.
  - `notice.txt`: settlement long-form notice.
  - `getty.txt`: text from the National Archives XML.
  - `suchak_plosbio.xml`: PLOS Biology article.

## Findings versus allegations
- **Bartz (N.D. Cal.):**
  - *Finding (summary judgment, 2025-06-23):* training was fair use ("exceedingly transformative"). Pirated central-library copies were not fair use.
  - For the pirated copies, the court "accepted the Authors' version of the facts", so the "over seven million" figure is the summary-judgment record, not a trial finding.
  - The case settled for $1.5B. Final approval came 2026-07-20.
  - The settlement notice states that "Anthropic denies all the allegations and denies that it did anything wrong."
  - It is not binding precedent and was never appealed.
- **Kadrey (N.D. Cal., 2025-06-25):** Meta won summary judgment against 13 authors. The judge said explicitly that the ruling does not mean Meta's training is lawful. The plaintiffs "made the wrong arguments".
- **Thomson Reuters v. ROSS (3d Cir., 2026-09-29):** the first appellate ruling on AI training and fair use. It found no fair use. The court stressed that ROSS was a non-generative system, so the ruling does not decide the LLM question. Footnote 7 confirms the DOJ Statement of Interest (Sept. 1, 2026) supporting OpenAI in the S.D.N.Y. MDL.
- **NYT v. OpenAI/Microsoft:**
  - Pending in the MDL before Judge Stein, at the summary-judgment stage (Sept. 2026). There is no fair-use merits ruling.
  - The status comes from secondary sources: Wikipedia, which cites 404 Media and Reuters. Axios returned a 403.
- **Getty v Stability (UK, 2025-11-04):**
  - Getty abandoned the training claim because there was no evidence of training in the UK.
  - The court held that the model weights are "not themselves an infringing copy", so secondary infringement failed. Getty won only limited trade-mark points.
  - Appeal status is unclear: secondary sources conflict.
- **GEMA v OpenAI (Munich, 2025-11-11):**
  - The court held that memorized lyrics in GPT models are reproductions, and that the TDM exception does not cover them.
  - This is a first-instance ruling, sourced to MediaLaws (secondary).
- **Misuse reports:** these are the developers' own characterizations and are not independently verified.
  - The GTG-1002 attribution ("high confidence" Chinese state-sponsored) is Anthropic's assessment.
  - Anthropic wrote "potentially affecting" for the 17 organizations.
  - In the same report, Anthropic notes that Claude "frequently overstated findings and occasionally fabricated data" during the attack.
  - OpenAI and GTIG both stress incremental gains and no breakthrough capabilities. GTIG does report the first zero-day exploit it believes was developed with AI (not Gemini).

## Peer review and research integrity: method caveats
- **Pangram's 21% figure (C1):** a detector estimate published by a detector vendor, not an ICLR finding. ICLR itself says detector "accuracy is far from perfect". ICLR used two detectors only to *flag* reviews to area chairs and published no fraction.
- **ICML's 795 reviews, about 1% (C4):** the strongest number here.
  - The method was a hidden-prompt watermark, not a generic detector.
  - Every flagged review was checked by a human, and the family-wise false-flag probability is 0.0001.
  - It covers only reviewers who had *pledged* not to use LLMs, so it is a lower bound.
- **GPTZero (C5):** a vendor analysis, with human verification. The page says both "51" and "53" papers.
- **Charlotin database (C6):** counts court decisions, not all incidents, and includes some decisions where AI use was alleged but not confirmed (the author's judgment call).
- **NHANES paper (C7):** peer-reviewed and shows correlation in time only. The authors did not establish LLM use or paper-mill origin for any specific paper.

## Blocked or not obtained (no workarounds attempted)
- **openai.com** (all /index and /global-affairs pages): 403. I used the October 2025 PDF on cdn.openai.com instead, so no 2026 cumulative count from OpenAI is verified. A February 2026 report exists, per secondary coverage.
- **PMC** (pmc.ncbi.nlm.nih.gov): reCAPTCHA. I fetched the article from journals.plos.org instead.
- **Other 403s:** BAILII, Axios, Jurist, Bird & Bird and Taylor Wessing. I used the National Archives Find Case Law copy, Pearl Cohen and MediaLaws instead.
- **Not covered:** Microsoft's threat reporting; the Bartz final-approval order PDF itself; RLHF labor reporting (optional item D).
