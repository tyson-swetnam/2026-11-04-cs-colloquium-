"""Write data/raw/research/facts.csv: exact quotes from documents fetched 2026-10-31.

Each quote is checked against the saved document text by src/01_check.py.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OMI = "https://www.openmarketsinstitute.org/publications/report-brace-for-impact-protecting-people-and-the-economy-when-the-ai-bubble-burst"
OMI_PDF = "https://www.openmarketsinstitute.org/s/Brace-for-Impact-Scherer-Jenkins-OMI-October2026-WEB-1.pdf"
OMI_ES = "https://www.openmarketsinstitute.org/s/Executive-Summary-Brace-for-Impact-Scherer-Jenkins-WEB.pdf"
OMI_T = "Brace for Impact: Protecting People and the Economy When the AI Bubble Bursts"
OMI_P = "Open Markets Institute and Americans for Financial Reform Education Fund"
YF = "https://finance.yahoo.com/technology/ai/articles/analysis-finds-signs-ai-bubble-195103377.html"
HEPP = "https://www.chicagobooth.edu/review/how-worried-should-we-be-about-ai-debt"
VN = "https://www.brookings.edu/wp-content/uploads/2026/09/4c_Van-Nieuwerburgh.pdf"

rows = [
    # id, claim, value, quote, title, publisher, date, url, type, notes
    ("F01", "c1", "2026-10-16", "Report - Brace for Impact: Protecting People and the Economy When the AI Bubble Bursts",
     OMI_T, "Open Markets Institute", "2026-10-16", OMI, "primary",
     "Publication page headline; datePublished 2026-10-16 in page metadata. Correct name is Open Markets Institute (OMI), not 'OpenMarkets'."),
    ("F02", "c1", "co-published with AFR", "Our report in partnership with Americans for Financial Reform outlines vulnerabilities in the financial system and wider economy that could intensify an AI crash into the next financial crisis",
     OMI_T, "Open Markets Institute", "2026-10-16", OMI, "primary", "Page description: a joint OMI and AFR Education Fund report."),
    ("F03", "c1", "authors", "Matthew U. Scherer, Fellow, Open Markets Institute",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "Second author: Maya Jenkins, Americans for Financial Reform Education Fund."),
    ("F04", "c1;c2", "subprime comparison", "Speculative data center debt is being repackaged and sold to pension and retirement funds, university endowments, and other institutional investors in a manner eerily reminiscent of the subprime bubble.",
     OMI_T + " (Executive Summary)", OMI_P, "2026-10", OMI_ES, "primary", "The report's own words; an advocacy assessment, not a measured finding."),
    ("F05", "c1", "$3.1T vs $2.3T", "the total size of the subprime mortgage market was $1.5 trillion, or $2.3 trillion in today’s dollars, at its 2007 peak",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "Compared in the report with $3.1T of off-balance-sheet commitments of nine hyperscalers and chipmakers (WSJ calculation)."),
    ("F06", "c2", "securitized; buyers insurers and pension funds", "these data center loans are often securitized — that is, sliced up and packaged into bonds that are sold to investors, often institutional investors such as insurers and pension funds.",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "Body text (Part II.B). Names insurers and pension funds; endowments appear in the executive summary."),
    ("F07", "c2;c4", "losses would rest with pension plans and endowments", "They would come to rest with the limited partners in those funds—principally pension plans and endowments—with private equity–owned insurance platforms, and, to a lesser extent, with private investors of business-development companies.",
     "How Worried Should We Be About AI Debt?", "Chicago Booth Review (Stefan Hepp)", "2026-08-07", HEPP, "secondary",
     "Independent analysis cited by the report (note 264). Refers to private-credit fund losses, not securitized bonds."),
    ("F08", "c2", "~$60B", "Infrastructure and asset-backed securities account for roughly $60 billion.",
     "How Worried Should We Be About AI Debt?", "Chicago Booth Review (Stefan Hepp)", "2026-08-07", HEPP, "secondary",
     "Securitized AI debt is a small slice of Hepp's estimate (vs ~$520B hyperscaler bonds, ~$250B project finance, ~$200B private credit)."),
    ("F09", "c3", ">$1T spend; revenue <=20%", "Revenues from generative AI products and services from outside the generative AI ecosystem thus appear to be at most 20%, and quite possibly less than 10%, of the more than $1 trillion companies are spending this year on the technology’s infrastructure",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "Report estimate."),
    ("F10", "c3", "OpenAI -$38B on $13B; Anthropic -$42B (2025)", "OpenAI reportedly lost more than $38 billion on just $13 billion in revenue in 2025. Anthropic reportedly lost a staggering $42 billion in 2025.",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "'Reportedly': the labs are private; figures come from press reports, not audited filings."),
    ("F11", "c3", "2026 revenue improved", "Anthropic has reported significantly improved revenues in 2026",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "The report itself flags that 2025 losses may not describe 2026."),
    ("F12", "c3", "$3.7T/yr by 2032", "the 2025–2032 buildout requires approximately $3.7 trillion in annual revenue by 2032 to earn a 10% unlevered return at a 50% operating cash-flow margin.",
     "Financing the AI Buildout (BPEA conference draft)", "Brookings Institution (S. Van Nieuwerburgh)", "2026-09-04", VN, "primary", "BPEA conference draft (Draft: September 4, 2026), not yet peer reviewed. Scope: a modelled 183 GW U.S. build-out (F32); holds under the stated assumptions (10% unlevered return, 50% operating cash-flow margin)."),
    ("F13", "c4", "interconnected; would likely spread", "the various players in the AI ecosystem are deeply interconnected, as the complex corporate arrangements for a massive data center in Abilene, Texas illustrate (see Figure ES-6). As a result, a crash affecting any one part of the industry would likely spread.",
     OMI_T + " (Executive Summary)", OMI_P, "2026-10", OMI_ES, "primary", ""),
    ("F14", "c4", "beyond tech", "If the AI industry can’t pay back its mounting debts, a financial crash could follow — and it could spread well beyond the tech sector.",
     OMI_T + " (Executive Summary)", OMI_P, "2026-10", OMI_ES, "primary", ""),
    ("F15", "c4", "counterpoint: premature", "It would be premature to conclude that AI infrastructure already poses systemic risk comparable to earlier credit booms.",
     "Financing the AI Buildout (BPEA conference draft)", "Brookings Institution (S. Van Nieuwerburgh)", "2026-09-04", VN, "primary", "Counterweight to the 2008 framing."),
    ("F16", "c4", "counterpoint: not 2008", "The result would be different from 2008: Aggregate credit losses would be smaller than the accompanying equity loss and far less concentrated in highly leveraged banks.",
     "How Worried Should We Be About AI Debt?", "Chicago Booth Review (Stefan Hepp)", "2026-08-07", HEPP, "secondary", "Counterweight to the 2008 framing."),
    ("F17", "c5", "crash odds rising", "the odds of a deep and severe AI crash are rapidly increasing.",
     OMI_T + " (Executive Summary)", OMI_P, "2026-10", OMI_ES, "primary", ""),
    ("F18", "c5", "unique in size and scope", "the AI bubble is unique in recent history in its size, scope, and risk.",
     OMI_T + " (Executive Summary)", OMI_P, "2026-10", OMI_ES, "primary", ""),
    ("F19", "c6", "regulators loosening", "the Trump administration and federal financial regulators are ripping up regulatory guardrails and exacerbating the harms a potential crisis would cause.",
     OMI_T + " (Executive Summary)", OMI_P, "2026-10", OMI_ES, "primary", "The report's characterisation (advocacy)."),
    ("F20", "c6", "recommendations", "murky finances, stop contributing to the inflation of the bubble with subsidies and regulatory giveaways, better protect working people’s retirement savings from outsized risk exposure, and strengthen the resilience of the financial system",
     OMI_T + " (Executive Summary)", OMI_P, "2026-10", OMI_ES, "primary", "Continues 'Regulators, Congress, and state policymakers should instead act swiftly to shine a light on the AI industry’s'."),
    ("F21", "c7", "Joe Wilkins, Oct 26 2026", "New Analysis Finds Signs the AI Bubble Is About to Blow Shutterstock / Futurism Joe Wilkins Mon, October 26, 2026",
     "New Analysis Finds Signs the AI Bubble Is About to Blow", "Futurism via Yahoo Finance", "2026-10-26", YF, "news", "Byline and date as rendered on the Yahoo page."),
    ("F22", "c7", "DC-based think tank 'OpenMarkets'", "As a new analysis by the DC-based think tank OpenMarkets concludes",
     "New Analysis Finds Signs the AI Bubble Is About to Blow", "Futurism via Yahoo Finance", "2026-10-26", YF, "news", "Futurism shortens the name; the publisher is the Open Markets Institute, with AFR Education Fund as co-author."),
    ("F23", "c3", "cash flows turning negative (report)", "With the hyperscalers’ cash flows turning negative as of the summer of 2026",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "Report's claim for four firms (Alphabet, Amazon, Meta, Microsoft), Bloomberg free cash flow, Q3 2026 onward marked as estimates (F26). Broadly consistent with SEC actuals for the July-September 2026 quarter: four-firm capex exceeded operating cash flow by about $26B, five-firm (with Oracle, fiscal quarter Jun-Aug) by about $32B (data/processed/capex_vs_ocf_quarterly.csv). On a trailing-12-month basis operating cash flow still exceeds capex (capex_vs_ocf.csv)."),
    ("F24", "c3", "VN: capex exceeds five-firm OCF in 2026", "On current estimates, capex will surpass the five firms’ combined operating cash flow for the first time in 2026.",
     "Financing the AI Buildout (BPEA conference draft)", "Brookings Institution (S. Van Nieuwerburgh)", "2026-09-04", VN, "primary", "Independent source; five firms are Oracle, Microsoft, Amazon, Meta, Alphabet. Estimate-based, calendar year 2026."),
    ("F25", "c3", "VN: capex outgrows internal cash flow", "As hyperscaler capital expenditures outgrow internal cash flow, financing is shifting toward leases, joint ventures, project debt, private credit, securitization, and special-purpose vehicles.",
     "Financing the AI Buildout (BPEA conference draft)", "Brookings Institution (S. Van Nieuwerburgh)", "2026-09-04", VN, "primary", "Abstract."),
    ("F26", "c3", "report figure: four firms, TTM, estimates", "Alphabet/Amazon/Meta/Microsoft Combined CapEx vs Free Cash Flow, 2020 - 2027 (Est) (trailing 12 months, in billion USD)",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "Figure 15 title. Its source line reads 'Source: Bloomberg. Figures from Q3 2026 onward are estimates.' Free cash flow, not operating cash flow."),
    ("F27", "c3", "broader revenue estimate $150-200B", "The Economist estimates $150 billion to $200 billion in “world revenues from AI services” in 2026, but that estimate appears to be based on sources such as Ramp that include all sales of AI services",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "The report's 20% ceiling excludes sales within the AI/tech ecosystem; broader counts are higher."),
    ("F28", "c1", "$3.1T is commitments and leases, not loans", "Whether or not the revenues ever arrive, purchase commitments and signed leases can’t be canceled, for the most part.",
     OMI_T, OMI_P, "2026-10", OMI_PDF, "primary", "Report footnote 50, quoting the WSJ (Rudegeair and Santilli, 16 Aug. 2026) on the $3.1T figure. Not the same kind of quantity as outstanding subprime mortgage debt."),
    ("F29", "c4", "counterpoint: may reduce contagion", "That structure may reduce the likelihood of contagion from AI financing to the broader system.",
     "How Worried Should We Be About AI Debt?", "Chicago Booth Review (Stefan Hepp)", "2026-08-07", HEPP, "secondary", "Counterweight to 'spread well beyond tech'."),
    ("F30", "c2", "scenario, not observed exposure", "Under the assumptions used in the analysis, first-loss and junior positions sit mainly outside the regulated banking system.",
     "How Worried Should We Be About AI Debt?", "Chicago Booth Review (Stefan Hepp)", "2026-08-07", HEPP, "secondary", "Context for F07: the endowment exposure is a modelled loss scenario."),
    ("F31", "c1", "Hepp: not a rerun of 2008", "The results of this test suggest that today’s situation is not a rerun of the 2008–09 financial crisis",
     "How Worried Should We Be About AI Debt?", "Chicago Booth Review (Stefan Hepp)", "2026-08-07", HEPP, "secondary", "Hepp's view on the 2008 comparison."),
    ("F32", "c3", "U.S. scope, 183 GW", "A 183 GW U.S. buildout completed by 2032",
     "Financing the AI Buildout (BPEA conference draft)", "Brookings Institution (S. Van Nieuwerburgh)", "2026-09-04", VN, "primary", "Scope of the $3.7T revenue requirement (F12)."),
]
out = HERE / "data/raw/research/facts.csv"
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "claim_id", "value", "quote", "source_title", "publisher", "date", "url", "source_type", "notes"])
    w.writerows(rows)
print(f"wrote {len(rows)} rows to {out}")
