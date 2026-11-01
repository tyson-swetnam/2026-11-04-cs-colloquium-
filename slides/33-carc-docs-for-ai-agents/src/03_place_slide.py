"""Slide 33: the new CARC website and its documentation, published for people and for AI agents.

Shows the CARC home page and the docs' "For AI agents" page (screenshots supplied by the speaker, 2026-11-01). Next to
them are the endpoints an agent can use, and an example prompt anyone can paste into a chat. The endpoints and quoted
wording are checked against the live sites by src/01_fetch_sources.py and src/02_check_facts.py.

tools/deck_insert.py places the slide after "Access for everyone, and training to use it responsibly" (slide 32).
It is idempotent.

    uv run python slides/33-carc-docs-for-ai-agents/src/03_place_slide.py
"""

from __future__ import annotations

import base64
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.deck_insert import place  # noqa: E402

AFTER_LABEL = "Access for everyone, and training to use it responsibly"
LABEL = "Paste our URL into any chat"
FID = "carc33"
EYEBROW = "CARC docs, for people and for AI agents"
SHOTS = [  # (file, alt)
    ("carc_website.webp", "The new CARC website, carc.unm.edu: Advanced computing for every researcher in New Mexico"),
    ("carc_docs_for_ai_agents.webp", "CARC Documentation, For AI agents page: a table of entry points (llms.txt, llms-full.txt, page index.md, sitemap)"),
]
ROWS = [  # (endpoint, what it gives)
    ("/llms.txt", "An outline of all ~80 pages, with a one-line description of each"),
    ("<page>/index.md", "Any page as Markdown, with OKF frontmatter: type, sources, status"),
    ("/llms-full.txt", "The whole corpus in one file (~180K tokens)"),
]
PROMPT = "Read carc.unm.edu/docs/llms.txt, then tell me how to get access to the H100 GPUs on Easley. Cite the pages."
FOOTER = "carc.unm.edu · carc.unm.edu/docs · Open Knowledge Format (OKF) v0.2"
NOTES = (
    "[~1 min] The new CARC website and documentation are published for people and for AI agents. The docs are an "
    "Open Knowledge Format (OKF) v0.2 bundle: every page carries frontmatter saying what it is, where it came from and "
    "when it goes stale. The site exposes that directly: /llms.txt is an outline of every page, /llms-full.txt is "
    "the whole corpus, and adding index.md to any page URL returns its Markdown. So anyone can paste our URL into "
    "Claude, ChatGPT, Gemini or a local model and get answers grounded in CARC's own documentation, not in whatever "
    "the model remembers. Try the prompt on the slide: the FAQ says the h100 and l40s partitions are group-gated, through a ColdFront allocation your PI requests. When the docs do not cover something, the page tells agents to send people to a human (support.alliance.unm.edu or help@carc.unm.edu) rather than guess. "
    "Sources: https://carc.unm.edu/ https://carc.unm.edu/docs/about/ai-agents/ https://carc.unm.edu/docs/llms.txt "
    "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md https://llmstxt.org/"
)

SANS = "Montserrat, Arial, ui-sans-serif, system-ui, sans-serif"
SLAB = "&quot;Zilla Slab&quot;, Arial, ui-sans-serif, system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
TEXT = "margin: 0px; white-space: pre-wrap; overflow-wrap: break-word; text-wrap-style: pretty; min-width: 0px; min-height: 0px; overflow-y: visible;"
RED, TEAL = "rgb(186, 12, 47)", "rgb(0, 122, 134)"


def img(name: str, alt: str, style: str) -> str:
    data = base64.b64encode((HERE / "figures" / name).read_bytes()).decode()
    return f'<img alt="{escape(alt)}" draggable="false" src="data:image/webp;base64,{data}" style="{style}">'


def frame(i: int, style: str, inner: str) -> str:
    return f'<div data-frame-id="e{i}-{FID}" style="position: absolute; box-sizing: border-box; {style}">{inner}</div>'


def section(number: int, total: int) -> str:
    shot = "display: block; width: 100%; height: auto; border: 3px solid rgb(0, 0, 0); box-shadow: rgba(0, 0, 0, 0.18) 16px 16px 0px 0px; box-sizing: border-box;"
    rows = "".join(
        f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 18px 0; border-top: 2px solid rgb(220, 220, 220);">'
        f'<div style="font-family: {MONO}; font-size: 30px; font-weight: 700; color: {TEAL}; {TEXT}">{escape(ep)}</div>'
        f'<div style="font-family: {SANS}; font-size: 26px; font-weight: 400; line-height: 1.35; color: rgb(0, 0, 0); {TEXT}">{escape(what)}</div></div>'
        for ep, what in ROWS
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
        + frame(2, "left: 128px; width: 740px; top: 290px;", img(*SHOTS[0], shot))
        + frame(3, "left: 300px; width: 740px; top: 530px;", img(*SHOTS[1], shot))
        + frame(4, "left: 1140px; width: 652px; top: 300px;", rows)
        + frame(5, "left: 1140px; width: 652px; top: 720px;",
                f'<div style="background: rgb(0, 0, 0); padding: 26px 30px; box-shadow: rgba(0, 0, 0, 0.18) 16px 16px 0px 0px;">'
                f'<div style="font-family: {SANS}; font-size: 20px; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; color: rgb(255, 255, 255); opacity: 0.75; {TEXT}">Try it in any chat</div>'
                f'<div style="font-family: {MONO}; font-size: 25px; line-height: 1.4; color: rgb(255, 255, 255); {TEXT} margin-top: 10px;">{escape(PROMPT)}</div></div>')
        + frame(6, "left: 128px; width: 1664px; bottom: 56px;",
                f'<div style="font-family: {SANS}; font-size: 22px; font-weight: 600; line-height: 1.4; color: rgb(99, 102, 106); {TEXT} letter-spacing: 2px; text-transform: uppercase;">{escape(FOOTER)}</div>')
        + "</div></div></div></section>"
    )


MOTION_ENTRY = {
    "transition": "fade", "bg": "#ffffff",
    "steps": [
        {"hidden": [f"e5-{FID}"], "events": [], "auto": False},
        {"hidden": [], "events": [{"id": f"e5-{FID}", "dir": "in", "effect": "rise"}], "auto": False},
    ],
    "embeds": [],
}


def main() -> int:
    number = place(LABEL, AFTER_LABEL, section, MOTION_ENTRY)
    print(f"slide {number} placed: {LABEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
