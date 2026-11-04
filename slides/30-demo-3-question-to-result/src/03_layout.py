"""Slide 30: the Demo 3 intro slide, in its original layout (dashed frame left, text right, on black).

The video moved to its own slide, 31, at the same size as slide 25 (slides/31-demo-3-video). This restores
the exported frame (dashed border, icon), with its label changed from "Recorded clip goes here" to "Recording on
the next slide". It keeps the corrected caption: the export's placeholder "[A researcher asks a question; the agent
queries the lakehouse on NAIRR compute and returns a figure.]" does not match the recording (see claims.yaml c1).
The length line reads "Played at 1.5x · 2:10", and the notes become a short set-up for the demo. The recording
files (data/media/, figures/poster.webp) stay in this folder; slide 31 reads them from here. Idempotent.

    uv run python slides/30-demo-3-question-to-result/src/03_layout.py
"""

from __future__ import annotations

import re
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DECK = HERE.parents[1] / "talk" / "deck.html"
LABEL = "Recording on the next slide"
OLD_CAPTION = "[A researcher asks a question; the agent queries the lakehouse on NAIRR compute and returns a figure.]"
CAPTION = ("A researcher asks which ground beetle is most common at NEON\u2019s Jornada site. The agent queries the "
           "neon-beetle-seg lakehouse, read-only, and answers with a ranked table: Tetragonoderus pallidus, 58%.")
LENGTHS = ("Target length ~2:00", "Recorded \u00b7 played at 1.5\u00d7 \u00b7 2:10")
LENGTH = "Played at 1.5\u00d7 \u00b7 2:10"
NOTES = (
    "[~30 s] Set up Demo 3: a researcher\u2019s question, answered from the data where it lives. The question: what "
    "is the most common ground beetle at NEON\u2019s Jornada Experimental Range (JORN)? The data: the neon-beetle-seg "
    "DuckLake on the CyVerse Data Store, read-only over WebDAV, from the Claude app on the speaker\u2019s computer "
    "(not NAIRR compute). Watch for the agent\u2019s plan, its data checks, and the ranked answer. The recording "
    "plays on the next slide."
)
FRAME = '<div data-node-path="0" style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 24px; min-width: 1120px; min-height: 630px; max-width: 1120px; max-height: 630px; height: 630px; border-width: 3px; border-style: dashed; border-color: rgb(167, 168, 170); box-sizing: border-box;"><svg data-icon-path="0.0" data-node-path="0.0" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" style="width: 96px; height: 96px; min-width: 0px; min-height: 0px; display: block;"><text x="50" y="54" text-anchor="middle" dominant-baseline="central" font-family="mc-anthropicons" font-size="90" text-rendering="geometricPrecision" fill="#a7a8aa">\uf13c</text></svg><div data-text-path="0.1" data-node-path="0.1" style="font-family: Montserrat, Arial, ui-sans-serif, system-ui, sans-serif; font-size: 28px; font-weight: 600; line-height: 1.4; color: rgb(167, 168, 170); margin: 0px; white-space: pre-wrap; overflow-wrap: break-word; text-wrap-style: pretty; min-width: 0px; min-height: 0px; letter-spacing: 2px; text-transform: uppercase; overflow-y: visible;">{label}</div></div>'
ANY_FRAME = re.compile(r'<div data-node-path="0" style="display: flex; flex-direction: column; align-items: center; '
                       r'justify-content: center; gap: 24px; min-width: 1120px;.*?</div></div>', re.S)
VIDEO_FRAME = re.compile(r'<div data-node-path="0" data-evidence-frame="1"[^>]*><video [^>]*></video></div>')


def main() -> int:
    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*data-label="From question to result"', html).start()
    end = html.index("</section>", start)
    slide = html[start:end]
    m = VIDEO_FRAME.search(slide) or ANY_FRAME.search(slide)
    if not m:
        print("slide 30: frame not found", file=sys.stderr)
        return 1
    slide = slide[: m.start()] + FRAME.format(label=escape(LABEL)) + slide[m.end() :]
    slide = slide.replace(escape(OLD_CAPTION, quote=False), escape(CAPTION, quote=False))
    for old in LENGTHS:
        slide = slide.replace(old, LENGTH)
    slide = re.sub(r'data-speaker-notes="[^"]*"', f'data-speaker-notes="{escape(NOTES)}"', slide, count=1)
    DECK.write_text(html[:start] + slide + html[end:], encoding="utf-8")
    print("slide 30: original layout restored (frame: \"%s\")" % LABEL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
