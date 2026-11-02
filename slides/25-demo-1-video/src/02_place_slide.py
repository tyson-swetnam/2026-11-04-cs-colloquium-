"""Slide 25: the recorded Demo 1, played on its own slide right after the "Formation MCP" diagram (slide 24).

The video (data/media/formation_irods_mcp_demo.webm, from src/01_encode.py) is embedded as a data: URL. It is
muted (the recording has no audio), starts from the beginning each time the slide opens, plays once and holds on
its last frame, and pauses when the slide is left. Clicking it pauses or resumes, so the speaker can stop and
narrate. All of that comes from the deck's shared video script (slides/04-kubrick/src/04_place_trailer.py), which
handles every video[data-evidence].

tools/deck_insert.py places the slide after "Formation MCP" and renumbers the rest. Idempotent.

    uv run python slides/25-demo-1-video/src/02_place_slide.py
"""

from __future__ import annotations

import base64
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.deck_insert import place  # noqa: E402

AFTER_LABEL = "Formation MCP"
LABEL = "Connect once, then just ask"
FID = "demo25"
EYEBROW = "Demo 1 of 3 · Claude Code + MESA’s Formation and iRODS MCP servers"
VIDEO = HERE / "data" / "media" / "formation_irods_mcp_demo.webm"
POSTER = HERE / "figures" / "poster.webp"
ARIA = ("Recorded demo, 88 seconds, no sound: Claude Code adds the Formation MCP server with one command, signs in "
        "through CyVerse, lists the user's running analysis and its details, then asks the iRODS MCP server for the "
        "folders in a Data Store collection, with the MESA portal open alongside.")
NOTES = (
    "[~1.5 min] Recorded demo, 88 s, no sound: talk over it, and click the video to pause. "
    "0:00 One command adds the Formation MCP server to Claude Code: claude mcp add --transport http formation "
    "https://de.cyverse.org/formation/mcp. "
    "0:10 Sign-in is OAuth through CyVerse in the browser; Claude Code reports “Authentication successful. Connected "
    "to formation.” "
    "0:20 “Use the formation MCP to list my running apps”: one running analysis in the Discovery Environment. "
    "0:35 “Give me details, and list the name”: Claude looks the app up by ID; it is the MESA KASM Ubuntu Desktop "
    "(GPU), a private interactive VICE app. The MESA portal on the right shows the same analysis. "
    "1:10 “Use the iRODS MCP to list the folders in my neon-beetle-seg/ folder”: the agent calls the Data Store "
    "(iRODS) server, and the portal’s Data Browser shows that collection: archive, docs, ducklake, metadata, report. "
    "The point: no custom integration; the same servers work from any MCP client (previous slide). "
    "Recording: data/media/MANIFEST.yaml in slides/25-demo-1-video."
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
        f'<video data-evidence="demo-1-formation-irods" autoplay muted playsinline preload="auto" aria-label="{escape(ARIA)}" '
        f'poster="{poster}" src="{src}" style="display: block; width: 100%; height: 100%; object-fit: contain; background: rgb(0, 0, 0); '
        f'border: 3px solid rgb(0, 0, 0); box-shadow: rgba(0, 0, 0, 0.18) 16px 16px 0px 0px; box-sizing: border-box; cursor: pointer;"></video></div>'
        "</div></div></div></section>"
    )


MOTION_ENTRY = {"transition": "fade", "bg": "#ffffff", "steps": [{"hidden": [], "events": [], "auto": False}], "embeds": []}


def main() -> int:
    if not VIDEO.exists():
        print("run src/01_encode.py first", file=sys.stderr)
        return 1
    number = place(LABEL, AFTER_LABEL, section, MOTION_ENTRY)
    print(f"slide {number} placed: {LABEL} ({VIDEO.stat().st_size / 1e6:.1f} MB video)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
