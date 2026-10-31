"""Fetch (once) and log the source documents, verify every facts.csv quote, compute two ratios.

Outputs:
  data/processed/quote_check.csv   one row per fact: was the quote found verbatim (whitespace-normalised)?
  data/processed/capex_vs_ocf.csv  five-hyperscaler capex vs operating cash flow, trailing 12 months
                                   (re-read from slide 06's SEC XBRL series)
  data/processed/capex_vs_ocf_quarterly.csv  same, single calendar quarters, four firms (report's set) and five
                                   (adds Oracle, whose fiscal quarters end Feb/May/Aug/Nov)
  data/processed/ratios.csv        report's off-balance-sheet debt vs 2007 subprime peak
"""
import csv
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import yaml  # noqa: E402
from evidence.fetch import fetch, record  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "data/raw/sources"
OUT = HERE / "data/processed"
UA = "colloquium-evidence/0.1 (UNM CARC research)"

DOCS = {
    "https://www.openmarketsinstitute.org/publications/report-brace-for-impact-protecting-people-and-the-economy-when-the-ai-bubble-burst": "omi_report.html",
    "https://www.openmarketsinstitute.org/s/Brace-for-Impact-Scherer-Jenkins-OMI-October2026-WEB-1.pdf": "Brace-for-Impact-Scherer-Jenkins-OMI-October2026-WEB-1.pdf",
    "https://www.openmarketsinstitute.org/s/Executive-Summary-Brace-for-Impact-Scherer-Jenkins-WEB.pdf": "Executive-Summary-Brace-for-Impact-Scherer-Jenkins-WEB.pdf",
    "https://finance.yahoo.com/technology/ai/articles/analysis-finds-signs-ai-bubble-195103377.html": "yahoo_futurism.html",
    "https://www.chicagobooth.edu/review/how-worried-should-we-be-about-ai-debt": "booth_hepp_ai_debt.html",
    "https://www.brookings.edu/wp-content/uploads/2026/09/4c_Van-Nieuwerburgh.pdf": "vn2026.pdf",
}
NOTES = {
    "omi_report.html": "OMI publication page (datePublished 2026-10-16)",
    "yahoo_futurism.html": "Futurism article by Joe Wilkins, syndicated on Yahoo Finance, 2026-10-26",
    "booth_hepp_ai_debt.html": "Stefan Hepp, Chicago Booth Review, 2026-08-07 (cited by OMI note 264)",
    "vn2026.pdf": "Van Nieuwerburgh, Financing the AI Buildout, BPEA draft 2026-09-04",
}


def norm(s: str) -> str:
    s = s.replace("­", "").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def text_of(path: Path) -> str:
    if path.suffix == ".pdf":
        raw = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
    else:
        t = path.read_text(encoding="utf-8", errors="replace")
        body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        raw = html.unescape(re.sub(r"<[^>]+>", " ", body)) + " " + html.unescape(t)  # visible text + metadata
    return norm(raw)


def main() -> None:
    texts = {}
    for url, name in DOCS.items():
        source = NOTES.get(name, "Open Markets Institute / AFR Education Fund, Brace for Impact (Oct. 2026)")
        p = fetch(url, SRC / name, source=source, user_agent=UA)
        manifest = SRC / "MANIFEST.yaml"
        logged = yaml.safe_load(manifest.read_text()) if manifest.exists() else {}
        if name not in (logged or {}):  # placed by hand (curl) before this script existed
            record(p, url=url, source=source, note="fetched 2026-10-31 with the colloquium User-Agent")
        texts[url] = text_of(p)

    OUT.mkdir(parents=True, exist_ok=True)
    facts = list(csv.DictReader((HERE / "data/raw/research/facts.csv").open()))
    bad = 0
    with (OUT / "quote_check.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "claim_id", "url", "found"])
        for r in facts:
            found = norm(r["quote"]) in texts[r["url"]]
            bad += not found
            w.writerow([r["id"], r["claim_id"], r["url"], found])
    print(f"quotes found: {len(facts) - bad}/{len(facts)}")

    # Capex vs operating cash flow, five hyperscalers, from slide 06 (SEC XBRL actuals).
    ttm = list(csv.DictReader((ROOT / "slides/06-the-concerns/data/processed/hyperscaler_ttm.csv").open()))
    with (OUT / "capex_vs_ocf.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["calendar_quarter", "capex_bn", "ocf_bn", "capex_to_ocf", "ocf_minus_capex_bn"])
        for r in ttm[-8:]:
            c, o = float(r["capex"]) / 1e9, float(r["ocf"]) / 1e9
            w.writerow([r["calendar_quarter"], round(c, 1), round(o, 1), round(c / o, 3), round(o - c, 1)])
    last = ttm[-1]
    print(f"{last['calendar_quarter']} TTM capex/OCF = {float(last['capex']) / float(last['ocf']):.3f}")

    # Single quarters: the TTM view smooths away the 2026 turn.
    q = list(csv.DictReader((ROOT / "slides/06-the-concerns/data/processed/hyperscaler_quarterly.csv").open()))
    four = {"Alphabet", "Amazon", "Meta", "Microsoft"}
    with (OUT / "capex_vs_ocf_quarterly.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["calendar_quarter", "firms", "capex_bn", "ocf_bn", "ocf_minus_capex_bn", "firms_with_capex_above_ocf"])
        for cq in ("2025Q4", "2026Q1", "2026Q2", "2026Q3"):
            rows = [r for r in q if r["calendar_quarter"] == cq]
            for label, sel in (("4 (GOOGL, AMZN, META, MSFT)", [r for r in rows if r["company"] in four]), ("5 (+ORCL)", rows)):
                c = sum(float(r["capex"]) for r in sel) / 1e9
                o = sum(float(r["ocf"]) for r in sel) / 1e9
                neg = ";".join(f"{r['company']} {(float(r['ocf']) - float(r['capex'])) / 1e9:+.1f}" for r in sel if float(r["capex"]) > float(r["ocf"]))
                w.writerow([cq, label, round(c, 1), round(o, 1), round(o - c, 1), neg])
                if cq == "2026Q3":
                    print(f"2026Q3 {label}: capex {c:.1f}B vs OCF {o:.1f}B -> {o - c:+.1f}B")

    with (OUT / "ratios.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["measure", "value", "basis"])
        w.writerow(["off_balance_sheet_vs_subprime_2007_real", round(3.1 / 2.3, 2), "OMI report: $3.1T off-balance-sheet (WSJ, 9 firms) / $2.3T subprime peak in 2026 dollars. Caveat: unlike kinds - the $3.1T is purchase commitments and signed leases (F28), the $2.3T is outstanding mortgage debt"])
        w.writerow(["total_debt_vs_subprime_2007_real", round(3.7 / 2.3, 2), "OMI report: $3.7T on- and off-balance-sheet / $2.3T (same caveat: mixes debt with commitments and leases)"])
        w.writerow(["genai_revenue_share_of_spend_upper", 0.20, "OMI report: genAI revenue from outside the genAI ecosystem is at most 20% (possibly <10%) of >$1T spent in 2026"])


if __name__ == "__main__":
    main()
