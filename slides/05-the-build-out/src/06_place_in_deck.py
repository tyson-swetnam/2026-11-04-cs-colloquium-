"""Place the two build-out charts on slide 5 of talk/deck.html (idempotent).

Inserts (or replaces) one frame, data-frame-id="evidence-charts", between the title and the footer,
holding figures/deck_dollars.png and figures/deck_gdp.png as embedded PNGs, and sets the footer to
the charts' measures and sources. Re-run after updating the figures or re-exporting the deck.
"""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

SLIDE = Path(__file__).resolve().parents[1]
DECK = SLIDE.parents[1] / "talk" / "deck.html"
FOOTERS = (
    "Cumulative cost in 2025 dollars · FHWA, Epoch AI, NASA, Gartner · After Fin Moorhouse",
    "Dashed: 2026 estimate · SEC EDGAR, BEA, MeasuringWorth, FHWA, NASA, Ulmer · After Fin Moorhouse",
)
OLD_FOOTER_V1 = (
    "Left: cumulative cost, 2025 dollars (CPI) · Right: cumulative share of US GDP · Dashed: 2026 estimate · "
    "SEC EDGAR, BEA, MeasuringWorth, FHWA, NASA, Ulmer (1960) · After Fin Moorhouse"
)
OLD_FOOTER_V2 = "Dashed: 2026 estimate · SEC EDGAR, BEA, MeasuringWorth, FHWA, NASA, Ulmer (1960) · After Fin Moorhouse"
CHARTS = [  # (file, heading shown above it, alt text)
    ("deck_dollars.png", "In today's dollars (2025, CPI)", "Cumulative cost in 2025 dollars by years from program start: six years of data-center capex exceed 37 years of Interstates and 71 years of railroads."),
    ("deck_gdp.png", "As a share of the US economy (% of one year's GDP)", "The same comparison as a share of US GDP: railroads reach 108% of one year's GDP, Interstates 8%, data centers 3% (5% with the 2026 estimate)."),
]


HEADING = 'font-family: Montserrat, Arial, sans-serif; font-size: 28px; font-weight: 700; color: rgb(0, 0, 0); margin: 0 0 8px 0;'


def frame() -> str:
    cols = "".join(
        f'<figure style="margin: 0; width: 808px; display: flex; flex-direction: column; align-items: flex-start;">'
        f'<figcaption style="{HEADING}">{heading}</figcaption>'
        f'<img alt="{alt}" src="data:image/png;base64,{base64.b64encode((SLIDE / "figures" / name).read_bytes()).decode()}" '
        f'style="height: 520px; width: auto; max-width: 808px; object-fit: contain;"></figure>'
        for name, heading, alt in CHARTS
    )
    return (
        '<div data-frame-id="evidence-charts" style="position: absolute; left: 128px; width: 1664px; top: 365px; height: 580px; '
        'box-sizing: border-box; display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 48px;">'
        f"{cols}</div>"
    )


def main() -> int:
    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*\bid="5"', html).start()
    end = html.index("</section>", start)
    slide = html[start:end]
    slide = re.sub(r'<div data-frame-id="evidence-charts".*?</figure></div>', "", slide, flags=re.S)  # remove an earlier copy
    slide = re.sub(r'<div data-frame-id="evidence-charts"[^>]*>(?:<img [^>]*>)+</div>', "", slide)  # first version
    footer = slide.find('<div data-frame-id="e2-')
    if footer < 0:
        print("slide 5 footer frame not found; deck layout changed", file=sys.stderr)
        return 1
    slide = slide[:footer] + frame() + slide[footer:]
    for old in (FOOTERS[0], OLD_FOOTER_V1, OLD_FOOTER_V2):
        slide = slide.replace(old, FOOTERS[1])
    DECK.write_text(html[:start] + slide + html[end:], encoding="utf-8")
    print(f"placed {len(CHARTS)} charts on slide 5 of {DECK.relative_to(SLIDE.parents[1])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
