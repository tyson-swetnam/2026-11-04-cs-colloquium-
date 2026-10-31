"""Fetch the public source documents for slide 08 and log them in data/raw/sources/MANIFEST.yaml.

Run from the repo root:  uv run python slides/08-power-water-health/src/01_fetch.py
Sources that refuse our User-Agent (e.g. iea.org behind a Cloudflare challenge) are reported and skipped.
"""
from __future__ import annotations

import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evidence.fetch import record  # noqa: E402

SLIDE = Path(__file__).resolve().parents[1]
OUT = SLIDE / "data" / "raw" / "sources"
UA = "colloquium-evidence/0.1 (UNM CARC research)"

SOURCES = {
    # name: (url, source label)
    "selc_colossus1.html": ("https://www.selc.org/news/xai-built-an-illegal-power-plant-to-power-its-data-center/", "SELC"),
    "selc_2026-02-13_threaten_suit.html": ("https://www.selc.org/press-release/groups-threaten-lawsuit-over-xais-unpermitted-gas-turbines-in-mississippi/", "SELC"),
    "selc_2026-03-10_permit.html": ("https://www.selc.org/press-releases/mississippi-regulators-rubber-stamp-air-permit-for-xai-power-plant-ignoring-overwhelming-public-pushback/", "SELC"),
    "selc_2026-04-09_appeal.html": ("https://www.selc.org/press-release/groups-appeal-air-permit-for-xais-personal-power-plant/", "SELC"),
    "selc_mtd_denied.html": ("https://www.selc.org/press-release/court-tosses-request-to-block-clean-air-act-lawsuit-against-musks-xai/", "SELC"),
    "earthjustice_case.html": ("https://earthjustice.org/case/xai-illegal-gas-power-plant-data-center-colossus", "Earthjustice"),
    "memphisflyer_water_permit.html": ("https://www.memphisflyer.com/state-issues-operating-permit-for-colossus-water-plant/", "Memphis Flyer"),
    "cooldown_water_recycling.html": ("https://www.thecooldown.com/green-tech/musk-ai-water-recycling-project-memphis/", "The Cool Down"),
    "wwdmag_restart_2027.html": ("https://www.wwdmag.com/wastewater-treatment/news/55386236/xai-commits-to-restarting-memphis-wastewater-recycling-project-in-2027", "Water & Wastes Digest"),
    "mstoday_2026-10-21_doj_mtd.html": ("https://mississippitoday.org/2026/10/21/judge-trump-administration-xai-naacp-lawsuit-southaven/", "Mississippi Today"),
    "arxiv_2412.06288_abs.html": ("https://arxiv.org/abs/2412.06288", "arXiv"),
    "arxiv_2412.06288.pdf": ("https://arxiv.org/pdf/2412.06288", "arXiv"),
    "arxiv_2412.06288v1.pdf": ("https://arxiv.org/pdf/2412.06288v1", "arXiv (v1, Dec 2024)"),
    "econlib_jevons_coal_question_ch7.html": ("https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html?chapter_num=9", "Econlib (Liberty Fund)"),
    "econlib_jevons_coal_question_front.html": ("https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html", "Econlib (Liberty Fund)"),
    "hydrocarbonengineering_iea_press_release.html": ("https://www.hydrocarbonengineering.com/the-environment/10042025/iea-ai-set-to-drive-surging-electricity-demand/", "Hydrocarbon Engineering (reprint of IEA press release)"),
    "iifiir_iea_summary.html": ("https://iifiir.org/en/news/ai-set-to-drive-doubling-of-electricity-demand-from-data-centres", "International Institute of Refrigeration"),
    "court_order_mtd_denied_2026-10-30.pdf": ("https://earthjustice.org/wp-content/uploads/2026/10/10313375508_6407.pdf", "U.S. District Court, N.D. Miss. (order, via Earthjustice)"),
    "eenews_water_reuse_stalled.html": ("https://www.eenews.net/articles/xai-sidelines-major-water-reuse-project-as-ipo-looms/", "E&E News by Politico"),
    "sustainabilityonline_iea_3pct.html": ("https://sustainabilityonline.net/news/data-centres-to-account-for-3-of-global-electricity-consumption-by-2030/", "Sustainability Online"),
    "brusselstimes_iea.html": ("https://brusselstimes.com/1528980/data-centres-will-double-global-electricity-demand-by-2030-iea", "Brussels Times (Belga)"),
    "ala_sota_shelby_tn.html": ("https://www.lung.org/research/sota/city-rankings/states/tennessee/shelby", "American Lung Association, State of the Air"),
    "ala_sota_desoto_ms.html": ("https://www.lung.org/research/sota/city-rankings/states/mississippi/desoto", "American Lung Association, State of the Air"),
    "iea_executive_summary.html":("https://www.iea.org/reports/energy-and-ai/executive-summary", "IEA"),
}


def main(only: list[str] | None = None) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (url, src) in SOURCES.items():
        if only and name not in only:
            continue
        dest = OUT / name
        if dest.exists():
            print("have", name)
            continue
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=90)
        except requests.RequestException as e:
            print("FAIL", name, e)
            continue
        if r.status_code != 200 or b"Just a moment..." in r.content[:3000]:
            print("BLOCKED", r.status_code, name, url)
            continue
        dest.write_bytes(r.content)
        record(dest, url=url, source=src, note="fetched by src/01_fetch.py")
        print("ok", r.status_code, len(r.content), name)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
