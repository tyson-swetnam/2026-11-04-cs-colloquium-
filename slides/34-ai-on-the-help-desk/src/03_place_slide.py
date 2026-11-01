"""Slide 34: CARC's self-hosted, open-weight AI helping staff answer help-desk tickets, on 2x NVIDIA DGX Spark.

The screenshot (supplied by the speaker) is a real ticket from 28 Oct 2026 with the help desk's AI Summary panel.
The speaker had already blurred the requester's name and email. figures/ticket_ai_summary_redacted.webp also covers
the requester's initials, their group's directory name and a staff email address, because the deck is public. The
unredacted original is not in the repository.

DGX Spark specifications come from NVIDIA (src/01_fetch_sources.py, checked by src/02_check_facts.py). CARC's
configuration (two units, an open-weight model, and use of past tickets) is the speaker's own account; see claims.yaml.

tools/deck_insert.py places the slide after "Paste our URL into any chat" (slide 33). It is idempotent.

    uv run python slides/34-ai-on-the-help-desk/src/03_place_slide.py
"""

from __future__ import annotations

import base64
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.deck_insert import place  # noqa: E402

AFTER_LABEL = "Paste our URL into any chat"
LABEL = "Self-hosted AI helps answer our tickets"
FID = "carc34"
EYEBROW = "CARC help desk"
SHOT = ("ticket_ai_summary_redacted.webp",
        "A CARC help-desk ticket about a project scratch folder, with an AI Summary panel listing the customer's intent "
        "and a summary of the conversation. The requester's details are redacted.")
CAPTION = "A real ticket, Oct. 28, 2026 · requester details redacted"
POINTS = [  # (heading, text)
    ("Open weights, our hardware", "An open-weight model, self-hosted on 2× NVIDIA DGX Spark: each up to 128 GB of unified memory and 1 petaFLOP (FP4)."),
    ("Tickets, summarized", "Staff see what the user needs and what has happened so far, at a glance."),
    ("Trained on our history", "We taught the agent to use what we have learned from every previous CARC ticket."),
]
NOTES = (
    "[~1 min] What we use ourselves. Tickets in the CARC help desk get an AI summary: what the user is asking "
    "for and what has happened so far. This one is a real ticket from last week about a project scratch folder; the "
    "requester's details are redacted. The model is open-weight and runs on two NVIDIA DGX Spark systems on our own "
    "hardware, so ticket text is not sent to an outside AI service. We have also trained the agent to use the "
    "knowledge in all of our previous tickets, so its answers reflect how CARC has actually solved these problems. "
    "DGX Spark: NVIDIA GB10 Grace Blackwell Superchip, up to 128 GB unified "
    "memory and up to 1 petaFLOP at FP4 per unit (NVIDIA). "
    "Sources: https://www.nvidia.com/en-us/products/workstations/dgx-spark/ "
    "https://docs.nvidia.com/dgx/dgx-spark/hardware.html"
)

SANS = "Montserrat, Arial, ui-sans-serif, system-ui, sans-serif"
SLAB = "&quot;Zilla Slab&quot;, Arial, ui-sans-serif, system-ui, sans-serif"
TEXT = "margin: 0px; white-space: pre-wrap; overflow-wrap: break-word; text-wrap-style: pretty; min-width: 0px; min-height: 0px; overflow-y: visible;"
RED, TEAL = "rgb(186, 12, 47)", "rgb(0, 122, 134)"


def frame(i: int, style: str, inner: str) -> str:
    return f'<div data-frame-id="e{i}-{FID}" style="position: absolute; box-sizing: border-box; {style}">{inner}</div>'


def section(number: int, total: int) -> str:
    data = base64.b64encode((HERE / "figures" / SHOT[0]).read_bytes()).decode()
    shot = (f'<img alt="{escape(SHOT[1])}" draggable="false" src="data:image/webp;base64,{data}" '
            'style="display: block; width: 100%; height: auto; border: 3px solid rgb(0, 0, 0); '
            'box-shadow: rgba(0, 0, 0, 0.18) 16px 16px 0px 0px; box-sizing: border-box;">'
            f'<div style="font-family: {SANS}; font-size: 20px; color: rgb(99, 102, 106); {TEXT} margin-top: 24px;">{escape(CAPTION)}</div>')
    points = "".join(
        f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 20px 0 22px; border-top: 4px solid {c};">'
        f'<div role="heading" aria-level="3" style="font-family: {SLAB}; font-size: 40px; font-weight: 700; line-height: 1.1; color: {c}; {TEXT}">{escape(h)}</div>'
        f'<div style="font-family: {SANS}; font-size: 26px; line-height: 1.35; color: rgb(0, 0, 0); {TEXT}">{escape(t)}</div></div>'
        for (h, t), c in zip(POINTS, (TEAL, RED, "rgb(0, 0, 0)"))
    )
    return (
        f'<section class="deck-slide" id="{number}" aria-roledescription="slide" aria-label="Slide {number} of {total}" '
        f'data-document-role="page" data-label="{escape(LABEL)}" data-speaker-notes="{escape(NOTES)}">'
        '<div class="deck-fit"><div class="deck-scaler"><div style="width: 1920px; height: 1080px; position: relative; '
        'background: rgb(255, 255, 255); overflow: clip; contain: paint;" class="slide" data-canvas-width="1920" data-canvas-height="1080">'
        + frame(0, "left: 0px; width: 1920px; top: 0px; height: 16px;", f'<div style="width: 100%; height: 100%; background-color: {RED};"></div>')
        + frame(1, "left: 128px; width: 1664px; top: 96px;",
                f'<div style="font-family: {SANS}; font-size: 24px; font-weight: 600; line-height: 1.4; color: {RED}; {TEXT} letter-spacing: 4px; text-transform: uppercase;">{escape(EYEBROW)}</div>'
                f'<div role="heading" aria-level="2" style="font-family: {SLAB}; font-size: 80px; font-weight: 700; line-height: 1.05; color: rgb(0, 0, 0); {TEXT} margin-top: 12px;">{escape(LABEL)}</div>')
        + frame(2, "left: 128px; width: 1000px; top: 300px;", shot)
        + frame(3, "left: 1184px; width: 608px; top: 296px;", points)
        + "</div></div></div></section>"
    )


MOTION_ENTRY = {"transition": "fade", "bg": "#ffffff", "steps": [{"hidden": [], "events": [], "auto": False}], "embeds": []}


def main() -> int:
    number = place(LABEL, AFTER_LABEL, section, MOTION_ENTRY)
    print(f"slide {number} placed: {LABEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
