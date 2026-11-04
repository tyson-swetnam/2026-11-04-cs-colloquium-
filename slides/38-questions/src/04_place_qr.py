"""Slide 38 (Questions?): add a QR code that opens the deck on GitHub Pages.

The code encodes https://tyson-swetnam.github.io/2026-11-04-cs-colloquium-/deck/ (error correction M). It is drawn
as SVG with segno, written to figures/qr_deck.svg and embedded as a data: URL. It sits on a white square in the
right of the red band, with a short label beside it. It was checked by decoding a 1920x1080 render of the slide
(and a half-size one) with OpenCV, which returned the URL.
Idempotent.

    uv run python slides/38-questions/src/04_place_qr.py
"""

from __future__ import annotations

import base64
import io
import re
import sys
from html import escape
from pathlib import Path

import segno

HERE = Path(__file__).resolve().parents[1]
DECK = HERE.parents[1] / "talk" / "deck.html"
URL = "https://tyson-swetnam.github.io/2026-11-04-cs-colloquium-/deck/"
SVG = HERE / "figures" / "qr_deck.svg"
MARK = "qr-deck"
SANS = "Montserrat, Arial, ui-sans-serif, system-ui, sans-serif"
TEXT = "margin: 0px; white-space: pre-wrap; overflow-wrap: anywhere; text-wrap-style: pretty;"


def qr_svg() -> bytes:
    buf = io.BytesIO()
    segno.make(URL, error="m", micro=False).save(buf, kind="svg", scale=10, border=0, dark="#000000", light="#ffffff",
                                                 xmldecl=False, svgns=True, title="QR code: " + URL)
    SVG.parent.mkdir(parents=True, exist_ok=True)
    SVG.write_bytes(buf.getvalue())
    return buf.getvalue()


def block(svg: bytes) -> str:
    src = "data:image/svg+xml;base64," + base64.b64encode(svg).decode()
    label = (f'<div style="font-family: {SANS}; font-size: 24px; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; '
             f'color: rgb(255, 255, 255); {TEXT}">Slides &amp; evidence</div>'
             f'<div style="font-family: {SANS}; font-size: 26px; line-height: 1.35; color: rgb(255, 255, 255); {TEXT} margin-top: 10px;">'
             f'tyson-swetnam.github.io/<br>2026-11-04-cs-colloquium-</div>')
    return (f'<!--{MARK}--><div data-frame-id="{MARK}-label" style="position: absolute; right: 460px; width: 420px; top: 780px; '
            f'text-align: right; box-sizing: border-box;">{label}</div>'
            f'<div data-frame-id="{MARK}" style="position: absolute; right: 128px; top: 720px; width: 300px; height: 300px; '
            f'background: rgb(255, 255, 255); padding: 28px; box-sizing: border-box;">'
            f'<img alt="{escape("QR code linking to the slides: " + URL)}" draggable="false" src="{src}" '
            f'style="display: block; width: 100%; height: 100%; image-rendering: pixelated;"></div><!--/{MARK}-->')


def main() -> int:
    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*data-label="Questions\?"', html).start()
    end = html.index("</section>", start)
    slide = re.sub(rf"<!--{MARK}-->.*?<!--/{MARK}-->", "", html[start:end], flags=re.S)
    # insert just before the slide canvas closes: </div></div></div> at the end of the section
    tail = "</div></div></div>"
    if not slide.endswith(tail):
        print("slide 38: unexpected structure", file=sys.stderr)
        return 1
    slide = slide[: -len(tail)] + block(qr_svg()) + tail
    DECK.write_text(html[:start] + slide + html[end:], encoding="utf-8")
    print(f"slide 38: QR code for {URL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
