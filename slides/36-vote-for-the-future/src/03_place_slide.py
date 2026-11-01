"""Slide 36: insert the closing "AI's future is a choice we make" slide after "Sitting on the sidelines…" (slide 35) in talk/deck.html.

Three cards point to the White House Blueprint for an AI Bill of Rights (via Alondra Nelson), Pope Leo XIV's
encyclical Magnifica Humanitas, and a @Pontifex post. The take-away line ("We must vote for our leaders, and for the
future.") is the speaker's own conclusion. No source quoted here mentions voting, so it carries no quotation marks
or attribution. It rises in on the first click.

Every quote on the slide is in data/raw/research/facts.csv and checked word for word by src/02_check_quotes.py.

tools/deck_insert.py places it after the "Sitting on the sidelines" slide, renumbers the slides that follow, rewrites
every "Slide N of M" label and adds a matching entry to the deck's motion list. It is idempotent: re-running it
replaces the slide in place.

    uv run python slides/36-vote-for-the-future/src/03_place_slide.py
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from tools.deck_insert import place  # noqa: E402

AFTER_LABEL = "Sitting on the sidelines is the most dangerous choice a researcher can make."
LABEL = "AI’s future is a choice we make"
FID = "vote34"  # suffix for this slide's data-frame-id values

EYEBROW = "Who writes the rules for AI?"
CARDS = [  # (heading, background, quote, attribution)
    ("Rights", "rgb(0, 122, 134)",
     "“Red states and blue states are writing AI Bills of Rights.”",
     "Alondra Nelson, Bluesky, May 2026. She led the team behind the White House Blueprint for an AI Bill of Rights (2022)."),
    ("Dignity", "rgb(186, 12, 47)",
     "“A more moral AI is not enough if that morality is determined by a few.”",
     "Pope Leo XIV, Magnifica Humanitas ¶107, May 2026"),
    ("Choice", "rgb(0, 0, 0)",
     "“The future of #ArtificialIntelligence is not pre-determined. As a technology developed by human beings, "
     "its future depends on the choices we make.”",
     "@Pontifex on X, Oct. 30, 2026"),
]
TAKEAWAY = "We must vote for our leaders, and for the future."
FOOTER = "Election Day was Nov. 3 · Registration and upcoming elections: sos.nm.gov"
NOTES = (
    "[~1 min · by 45:00] Three voices, one point: the rules for AI are being written now, and who writes them is a "
    "political choice. Alondra Nelson led the White House OSTP team behind the Blueprint for an AI Bill of Rights "
    "(Oct. 4, 2022): five non-binding principles (safe and effective systems; algorithmic discrimination "
    "protections; data privacy; notice and explanation; human alternatives, consideration, and fallback). "
    "EO 14110 (2023) drew practices from it; EO 14148 revoked that order in January 2025. Since then, in Nelson’s "
    "words, red states and blue states are writing their own (Bluesky, May 14, 2026; essay: Science 392, "
    "doi:10.1126/science.aeh7153). Pope Leo XIV’s first encyclical, Magnifica Humanitas (signed May 15, released "
    "May 25, 2026), says aligning AI is not enough on its own (¶107) and asks for “a political system that does not "
    "abdicate its responsibility” (¶106). On Oct. 30 he posted that AI’s future “depends on the choices we make.” "
    "Neither of them tells anyone how to vote; that conclusion is mine. The people we elect, at every level, write "
    "these rules. Election Day was yesterday: whoever you supported, keep showing up. If you can’t vote, you can "
    "still make your voice heard. "
    "Sources: https://bidenwhitehouse.archives.gov/ostp/ai-bill-of-rights/ "
    "https://bsky.app/profile/alondra.bsky.social/post/3mltg2efhms2a "
    "https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html "
    "https://x.com/Pontifex/status/2116146977230459383 https://www.sos.nm.gov/voting-and-elections/"
)

SANS = "Montserrat, Arial, ui-sans-serif, system-ui, sans-serif"
SLAB = "&quot;Zilla Slab&quot;, Arial, ui-sans-serif, system-ui, sans-serif"
TEXT = "margin: 0px; white-space: pre-wrap; overflow-wrap: break-word; text-wrap-style: pretty; min-width: 0px; min-height: 0px; overflow-y: visible;"


def card(i: int, heading: str, bg: str, quote: str, who: str) -> str:
    return (
        f'<div data-node-path="1.{i}" style="display: flex; flex-direction: column; align-items: stretch; gap: 20px; '
        f'min-width: 0px; min-height: 0px; background-color: {bg}; padding: 40px; '
        f'box-shadow: rgba(0, 0, 0, 0.15) 16px 16px 0px 0px; box-sizing: border-box;">'
        f'<div data-text-path="1.{i}.0" data-node-path="1.{i}.0" role="heading" aria-level="3" style="font-family: {SLAB}; '
        f'font-size: 48px; font-weight: 700; line-height: 1.1; color: rgb(255, 255, 255); {TEXT}">{escape(heading)}</div>'
        f'<div data-text-path="1.{i}.1" data-node-path="1.{i}.1" style="font-family: {SANS}; font-size: 30px; '
        f'font-weight: 500; line-height: 1.4; color: rgb(255, 255, 255); {TEXT}">{escape(quote)}</div>'
        f'<div data-text-path="1.{i}.2" data-node-path="1.{i}.2" style="font-family: {SANS}; font-size: 22px; '
        f'font-weight: 400; line-height: 1.4; color: rgba(255, 255, 255, 0.85); {TEXT} margin-top: auto;">{escape(who)}</div>'
        "</div>"
    )


def section(number: int, total: int) -> str:
    cards = "".join(card(i, *c) for i, c in enumerate(CARDS))
    return (
        f'<section class="deck-slide" id="{number}" aria-roledescription="slide" aria-label="Slide {number} of {total}" '
        f'data-document-role="page" data-label="{escape(LABEL)}" data-speaker-notes="{escape(NOTES)}">'
        '<div class="deck-fit"><div class="deck-scaler"><div style="width: 1920px; height: 1080px; position: relative; '
        'background: rgb(255, 255, 255); overflow: clip; contain: paint;" class="slide" data-canvas-width="1920" data-canvas-height="1080">'
        f'<div data-frame-id="e0-{FID}" style="position: absolute; left: 0px; width: 1920px; top: 0px; height: 16px; box-sizing: border-box;">'
        '<div data-node-path="" style="display: flex; flex-direction: column; align-items: stretch; gap: 0px; width: 100%; height: 100%; background-color: rgb(186, 12, 47);"></div></div>'
        f'<div data-frame-id="e1-{FID}" style="position: absolute; inset: 0px; box-sizing: border-box;">'
        '<div data-node-path="" style="display: flex; flex-direction: column; align-items: stretch; gap: 48px; width: 100%; height: 100%; padding: 120px 128px 160px; box-sizing: border-box;">'
        '<div data-node-path="0" style="display: flex; flex-direction: column; align-items: stretch; gap: 16px; min-width: 0px; min-height: 0px;">'
        f'<div data-text-path="0.0" data-node-path="0.0" style="font-family: {SANS}; font-size: 24px; font-weight: 600; line-height: 1.4; '
        f'color: rgb(186, 12, 47); {TEXT} letter-spacing: 4px; text-transform: uppercase;">{escape(EYEBROW)}</div>'
        f'<div data-text-path="0.1" data-node-path="0.1" role="heading" aria-level="2" style="font-family: {SLAB}; font-size: 80px; '
        f'font-weight: 700; line-height: 1.05; color: rgb(0, 0, 0); {TEXT}">{escape(LABEL)}</div></div>'
        '<div data-node-path="1" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 40px; min-width: 0px; min-height: 0px;">'
        f"{cards}</div></div></div>"
        f'<div data-frame-id="e2-{FID}" style="position: absolute; left: 128px; width: 1664px; bottom: 132px; box-sizing: border-box;">'
        f'<div data-text-path="" data-node-path="" role="heading" aria-level="3" style="font-family: {SLAB}; font-size: 60px; font-weight: 700; '
        f'line-height: 1.1; color: rgb(186, 12, 47); {TEXT}">{escape(TAKEAWAY)}</div></div>'
        f'<div data-frame-id="e3-{FID}" style="position: absolute; left: 128px; width: 1664px; bottom: 64px; box-sizing: border-box;">'
        f'<div data-text-path="" data-node-path="" style="font-family: {SANS}; font-size: 22px; font-weight: 600; line-height: 1.4; '
        f'color: rgb(99, 102, 106); {TEXT} letter-spacing: 2px; text-transform: uppercase;">{escape(FOOTER)}</div></div>'
        "</div></div></div></section>"
    )


MOTION_ENTRY = {
    "transition": "fade", "bg": "#ffffff",
    "steps": [
        {"hidden": [f"e2-{FID}"], "events": [], "auto": False},
        {"hidden": [], "events": [{"id": f"e2-{FID}", "dir": "in", "effect": "rise"}], "auto": False},
    ],
    "embeds": [],
}


def main() -> int:
    number = place(LABEL, AFTER_LABEL, section, MOTION_ENTRY)
    print(f"slide {number} placed: {LABEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
