"""Slide 31: the recorded Demo 3, played on its own slide after the intro slide 30 ("From question to result").

Same layout and video size as slide 25 (1446 x 791 px under the heading). The recording is the speaker's
(2026-11-02; sped up 1.5x and converted to VP9 WebM by the speaker, 2:10, no audio, 5.5 MB). It stays in slide 30's
folder (slides/*-demo-3-question-to-result/data/media/, with its MANIFEST.yaml and poster); this script finds it there
by folder name, so later renumbering does not break it. Muted, it starts from the beginning each time the slide opens,
plays once and holds on the answer, pauses when the slide is left, and pauses or resumes on click. All of that comes
from the deck's shared video script (slides/04-kubrick/src/04_place_trailer.py).

tools/deck_insert.py places the slide after "From question to result" and renumbers the rest. Idempotent.

    uv run python slides/31-demo-3-video/src/01_place_slide.py
"""

from __future__ import annotations

import base64
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.deck_insert import place  # noqa: E402

AFTER_LABEL = "From question to result"
LABEL = "Which ground beetle is most common at Jornada?"
FID = "demo31"
EYEBROW = "Demo 3 of 3 · Claude + the neon-beetle-seg lakehouse"
DEMO3 = next(HERE.parent.glob("*-demo-3-question-to-result"))
VIDEO = DEMO3 / "data" / "media" / "neon_beetle_seg_demo_1.5x.webm"
POSTER = DEMO3 / "figures" / "poster.webp"
ARIA = ("Recorded demo, 2 minutes 10 seconds at 1.5 times speed, no sound. In the Claude app, a researcher asks which "
        "ground beetle is most common at the Jornada Experimental Range. The agent reads the neon-beetle-seg DuckLake "
        "read-only over WebDAV while the MESA portal shows the collection, its lakehouse, a specimen page and its "
        "ontology metadata; the agent answers Tetragonoderus pallidus, 616 of 1,056 carabid individuals (58.3%).")
NOTES = (
    "[~2.5 min] Recorded at normal speed, played at 1.5× (2:10), no sound: talk over it, and click the "
    "video to pause. "
    "0:00 In the Claude app, in a workspace for the collection, the question: query the neon-beetle-seg DuckLake "
    "directly with the DuckDB CLI, read-only over WebDAV without downloading the lake, and answer: what is the most "
    "common ground beetle at the Jornada Experimental Range (JORN)? "
    "0:15 The agent plans five steps: check DuckDB and the lake layout, attach the lake read-only, inspect the "
    "neon_sorting schema, run the JORN carabid ranking, check family/genus and subspecies splits. "
    "Meanwhile (from 0:05) the MESA portal shows the collection, its DuckLake (a SQL browser on beetles.ducklake), the "
    "project's results on GitHub, and a specimen page with its measurements in millimetres. "
    "1:00 The collection's metadata in the Ontology Explorer: 39 ontology-namespaced AVUs, including the Coleoptera "
    "Anatomy Ontology (COLAO) terms, e.g. elytron, linked to the 2018 Zooniverse elytra annotations. "
    "2:00 The agent's data checks (provisional vs released records, repeated sample/taxon pairs, records not "
    "identified to species); 2:05 the answer: Tetragonoderus pallidus, 616 of 1,056 carabid individuals (58.3%) in "
    "417 of 732 records, 2015-05-28 to 2025-09-10, and the ranked table. "
    "The point: a researcher's question, answered from the data where it lives, with the checks shown. "
    "Runs on the speaker's computer against the CyVerse Data Store; not NAIRR compute. "
    "Recording: data/media/MANIFEST.yaml in slides/30-demo-3-question-to-result (the intro slide before this one)."
)

SANS = "Montserrat, Arial, ui-sans-serif, system-ui, sans-serif"
SLAB = "&quot;Zilla Slab&quot;, Arial, ui-sans-serif, system-ui, sans-serif"
TEXT = "margin: 0px; white-space: pre-wrap; overflow-wrap: break-word; text-wrap-style: pretty; min-width: 0px; min-height: 0px; overflow-y: visible;"
RED = "rgb(186, 12, 47)"
VIDEO_W, VIDEO_H = 1446, 791  # 1280x700 source, scaled to fill the space under the heading


def section(number: int, total: int) -> str:
    src = "data:video/webm;base64," + base64.b64encode(VIDEO.read_bytes()).decode()
    poster = "data:image/webp;base64," + base64.b64encode(POSTER.read_bytes()).decode()
    left = (1920 - VIDEO_W) // 2
    return (
        f'<section class="deck-slide" id="{number}" aria-roledescription="slide" aria-label="Slide {number} of {total}" '
        f'data-document-role="page" data-label="{escape(LABEL)}" data-speaker-notes="{escape(NOTES)}">'
        '<div class="deck-fit"><div class="deck-scaler"><div style="width: 1920px; height: 1080px; position: relative; '
        'background: rgb(255, 255, 255); overflow: clip; contain: paint;" class="slide" data-canvas-width="1920" data-canvas-height="1080">'
        f'<div data-frame-id="e0-{FID}" style="position: absolute; left: 0px; width: 1920px; top: 0px; height: 16px; box-sizing: border-box;">'
        f'<div style="width: 100%; height: 100%; background-color: {RED};"></div></div>'
        f'<div data-frame-id="e1-{FID}" style="position: absolute; left: {left}px; width: {VIDEO_W}px; top: 56px; box-sizing: border-box;">'
        f'<div style="font-family: {SANS}; font-size: 22px; font-weight: 600; line-height: 1.4; color: {RED}; {TEXT} letter-spacing: 3px; text-transform: uppercase;">{escape(EYEBROW)}</div>'
        f'<div role="heading" aria-level="2" style="font-family: {SLAB}; font-size: 64px; font-weight: 700; line-height: 1.05; color: rgb(0, 0, 0); {TEXT} margin-top: 6px;">{escape(LABEL)}</div></div>'
        f'<div data-frame-id="e2-{FID}" style="position: absolute; left: {left}px; width: {VIDEO_W}px; top: 232px; height: {VIDEO_H}px; box-sizing: border-box;">'
        f'<video data-evidence="demo-3-question-to-result" autoplay muted playsinline preload="auto" aria-label="{escape(ARIA)}" '
        f'poster="{poster}" src="{src}" style="display: block; width: 100%; height: 100%; object-fit: contain; background: rgb(0, 0, 0); '
        f'border: 3px solid rgb(0, 0, 0); box-shadow: rgba(0, 0, 0, 0.18) 16px 16px 0px 0px; box-sizing: border-box; cursor: pointer;"></video></div>'
        "</div></div></div></section>"
    )


MOTION_ENTRY = {"transition": "fade", "bg": "#ffffff", "steps": [{"hidden": [], "events": [], "auto": False}], "embeds": []}


def main() -> int:
    if not VIDEO.exists():
        print(f"recording not found: {VIDEO}", file=sys.stderr)
        return 1
    number = place(LABEL, AFTER_LABEL, section, MOTION_ENTRY)
    print(f"slide {number} placed: {LABEL} ({VIDEO.stat().st_size / 1e6:.1f} MB video)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
