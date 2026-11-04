"""Slide 16: put System 1 in the middle column and System 2 on the right, and add the Thinking, Fast and Slow cover.

Columns: the table had System 2 (LLMs) in the middle and System 1 (Jev, Clef) on the right. Each row's two value
cells are swapped whole, so System 1 keeps its red text. The grid narrows to leave room for the cover.

Cover: the English Wikipedia file "Thinking, Fast and Slow.jpg" (259 x 385, 11 KB), the book's hardcover cover art.
Wikipedia marks it as copyrighted and uses it under a non-free fair-use rationale ("used for identification in the
context of critical commentary"; read 2026-11-04). It is shown at that low resolution, credited on the slide as fair
use via Wikipedia, and used here for the same purpose: identifying the book the slide comments on. The copy in
figures/ is the downloaded file, unchanged. Idempotent.

    uv run python slides/16-system-one-models/src/04_cover_and_columns.py
"""

from __future__ import annotations

import base64
import re
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from evidence.fetch import fetch  # noqa: E402

DECK = ROOT / "talk" / "deck.html"
URL = "https://upload.wikimedia.org/wikipedia/en/c/c1/Thinking%2C_Fast_and_Slow.jpg"
FILE_PAGE = "https://en.wikipedia.org/wiki/File:Thinking,_Fast_and_Slow.jpg"
COVER = HERE / "figures" / "thinking_fast_and_slow_cover.jpg"
MARK = "kahneman-cover"
SANS = "Montserrat, Arial, ui-sans-serif, system-ui, sans-serif"
CREDIT = "Cover: Daniel Kahneman, Thinking, Fast and Slow (2011). Image via Wikipedia, used under fair use."
ALT = "Cover of Thinking, Fast and Slow by Daniel Kahneman"
TABLE_W = 1312  # px; the cover column takes the rest (300 px plus a 52 px gap)


def swap_columns(slide: str) -> str:
    header = re.search(r'<div data-cell="0\.1" [^>]*>([^<]*)</div>', slide)
    if header and "SYSTEM 1" in header.group(1).upper():
        return slide  # already swapped
    rows = sorted({int(r) for r in re.findall(r'data-cell="(\d+)\.\d"', slide)})
    for r in rows:
        a = re.search(rf'<div data-cell="{r}\.1" [^>]*>.*?</div>', slide)
        b = re.search(rf'<div data-cell="{r}\.2" [^>]*>.*?</div>', slide)
        ca = a.group(0).replace(f'data-cell="{r}.1"', f'data-cell="{r}.2"')
        cb = b.group(0).replace(f'data-cell="{r}.2"', f'data-cell="{r}.1"')
        slide = slide[: a.start()] + cb + slide[a.end() : b.start()] + ca + slide[b.end() :]
    return slide


def cover_frame() -> str:
    data = base64.b64encode(COVER.read_bytes()).decode()
    return (f'<!--{MARK}--><div data-frame-id="{MARK}" style="position: absolute; right: 128px; top: 283px; width: 300px; '
            f'box-sizing: border-box;"><img alt="{escape(ALT)}" draggable="false" src="data:image/jpeg;base64,{data}" '
            f'style="display: block; width: 300px; height: auto; border: 1px solid rgb(220, 220, 220); '
            f'box-shadow: rgba(0, 0, 0, 0.15) 12px 12px 0px 0px;">'
            f'<div style="font-family: {SANS}; font-size: 17px; line-height: 1.35; color: rgb(99, 102, 106); margin-top: 22px; '
            f'white-space: pre-wrap; overflow-wrap: break-word;">{escape(CREDIT)}</div></div><!--/{MARK}-->')


def main() -> int:
    fetch(URL, COVER, source=f"English Wikipedia, {FILE_PAGE} (non-free, fair use)",
          user_agent="colloquium-evidence/0.1 (UNM CARC research)")
    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*data-label="System One models decide; they don’t write"', html).start()
    end = html.index("</section>", start)
    slide = re.sub(rf"<!--{MARK}-->.*?<!--/{MARK}-->", "", html[start:end], flags=re.S)
    slide = swap_columns(slide)
    slide = re.sub(r'(<div data-node-path="1" style="display: grid; grid-template-columns: 20fr 40fr 40fr; )width: [^;]*;',
                   rf"\1width: {TABLE_W}px;", slide, count=1)
    tail = "</div></div></div>"
    if not slide.endswith(tail):
        print("slide 16: unexpected structure", file=sys.stderr)
        return 1
    slide = slide[: -len(tail)] + cover_frame() + tail
    DECK.write_text(html[:start] + slide + html[end:], encoding="utf-8")
    print("slide 16: System 1 middle, System 2 right; cover added")
    return 0


if __name__ == "__main__":
    sys.exit(main())
