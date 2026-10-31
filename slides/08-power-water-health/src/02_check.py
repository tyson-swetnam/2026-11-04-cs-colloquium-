"""Check every facts.csv quote against the saved source text, and compute the slide's derived numbers.

Run from the repo root:  uv run python slides/08-power-water-health/src/02_check.py
Writes data/processed/quote_check.csv and data/processed/computed.csv.
Text matching normalises whitespace, curly quotes, dashes and spaces left before punctuation by tag stripping.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from textutil import to_text  # noqa: E402

SLIDE = HERE.parent
SRC = SLIDE / "data" / "raw" / "sources"
PROC = SLIDE / "data" / "processed"

# url -> saved file
FILES = {
    "https://www.hydrocarbonengineering.com/the-environment/10042025/iea-ai-set-to-drive-surging-electricity-demand/": "hydrocarbonengineering_iea_press_release.html",
    "https://brusselstimes.com/1528980/data-centres-will-double-global-electricity-demand-by-2030-iea": "brusselstimes_iea.html",
    "https://sustainabilityonline.net/news/data-centres-to-account-for-3-of-global-electricity-consumption-by-2030/": "sustainabilityonline_iea_3pct.html",
    "https://iifiir.org/en/news/ai-set-to-drive-doubling-of-electricity-demand-from-data-centres": "iifiir_iea_summary.html",
    "https://www.selc.org/news/xai-built-an-illegal-power-plant-to-power-its-data-center/": "selc_colossus1.html",
    "https://earthjustice.org/wp-content/uploads/2026/10/10313375508_6407.pdf": "court_order_mtd_denied_2026-10-30.pdf",
    "https://www.selc.org/press-release/court-tosses-request-to-block-clean-air-act-lawsuit-against-musks-xai/": "selc_mtd_denied.html",
    "https://earthjustice.org/case/xai-illegal-gas-power-plant-data-center-colossus": "earthjustice_case.html",
    "https://www.eenews.net/articles/xai-sidelines-major-water-reuse-project-as-ipo-looms/": "eenews_water_reuse_stalled.html",
    "https://www.thecooldown.com/green-tech/musk-ai-water-recycling-project-memphis/": "cooldown_water_recycling.html",
    "https://www.wwdmag.com/wastewater-treatment/news/55386236/xai-commits-to-restarting-memphis-wastewater-recycling-project-in-2027": "wwdmag_restart_2027.html",
    "https://www.memphisflyer.com/state-issues-operating-permit-for-colossus-water-plant/": "memphisflyer_water_permit.html",
    "https://arxiv.org/pdf/2412.06288v1": "arxiv_2412.06288v1.pdf",
    "https://arxiv.org/pdf/2412.06288": "arxiv_2412.06288.pdf",
    "https://arxiv.org/abs/2412.06288": "arxiv_2412.06288_abs.html",
    "https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html?chapter_num=9": "econlib_jevons_coal_question_ch7.html",
    "https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html": "econlib_jevons_coal_question_front.html",
    "https://www.selc.org/press-release/groups-threaten-lawsuit-over-xais-unpermitted-gas-turbines-in-mississippi/": "selc_2026-02-13_threaten_suit.html",
    "https://www.selc.org/press-releases/mississippi-regulators-rubber-stamp-air-permit-for-xai-power-plant-ignoring-overwhelming-public-pushback/": "selc_2026-03-10_permit.html",
}


def norm(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,.;:)\]])", r"\1", s)
    s = re.sub(r"([(\[])\s+", r"\1", s)
    s = re.sub(r"\s*-\s*", "-", s)  # em dashes rendered with or without spaces
    return s.strip()


def check_quotes() -> int:
    texts: dict[str, str] = {}
    rows, bad = [], 0
    with open(SLIDE / "data/raw/research/facts.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fn = FILES.get(r["url"])
            if fn is None:
                ok, where = False, "no saved file"
            else:
                if fn not in texts:
                    texts[fn] = norm(to_text(SRC / fn))
                ok, where = norm(r["quote"]) in texts[fn], fn
            bad += not ok
            rows.append({"id": r["id"], "claim_id": r["claim_id"], "found": ok, "file": where})
    PROC.mkdir(parents=True, exist_ok=True)
    with open(PROC / "quote_check.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        if not r["found"]:
            print("NOT FOUND", r)
    return bad


def compute() -> None:
    # IEA (via press-release reprint and news): 415 TWh in 2024 (1.5%), ~945 TWh in 2030 (just under 3%).
    ratio = 945 / 415
    implied_2024_total = 415 / 0.015
    implied_2030_share_if_3pct = 945 / 0.03
    # Court order footnote 4: unit mix and per-unit MW at the Southaven plant (complaint, as of April 7, 2026).
    mix = {"SMT-130": (14, 13), "M35": (1, 25), "TM2500 Gen 6": (4, 22), "TM2500 Gen 7": (5, 25), "TM2500 Gen 8": (3, 25)}
    units = sum(n for n, _ in mix.values())
    mw = sum(n * c for n, c in mix.values())
    # Unpaid Toll v1 vs v4 target year
    rows = [
        ("c1", "IEA 2030 / 2024 data-centre electricity (945/415)", round(ratio, 3), "x", "more than double: True" if ratio > 2 else "False"),
        ("c1", "Implied global electricity 2024 (415 TWh / 1.5%)", round(implied_2024_total), "TWh", "sanity check only"),
        ("c1", "Global electricity implied if 945 TWh were exactly 3%", round(implied_2030_share_if_3pct), "TWh", "IEA says 'just under 3%', so 2030 total > this"),
        ("c2;c6", "Southaven turbines in complaint (sum of unit mix)", units, "units", "matches 'twenty-seven'" if units == 27 else "mismatch"),
        ("c2;c6", "Southaven capacity from unit mix", mw, "MW", "matches 'at least 495 MW'" if mw == 495 else "mismatch"),
        ("c3", "Requested water vs recycling plant capacity (3.7 / 13 MGD)", round(3.7 / 13, 3), "ratio", "recycling plant would offset more than the requested draw"),
    ]
    with open(PROC / "computed.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["claim_id", "quantity", "value", "unit", "note"])
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    n = check_quotes()
    compute()
    print(f"{n} quote(s) not found")
    sys.exit(1 if n else 0)
