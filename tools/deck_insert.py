"""Insert or refresh a slide in talk/deck.html, anchored on the label of the slide it follows.

Slide scripts that add a slide the export does not contain call `place()`. On the first run it inserts the section
after the slide whose data-label is `after_label`, adds the slide's entry to the deck's motion list (the list is
positional), and renumbers every section id and "Slide N of M" label. On later runs it replaces the section in place
and leaves the motion list alone. Anchoring on a label rather than a number keeps each script correct when other
slides are added earlier in the deck.
"""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "talk" / "deck.html"
SECTION = re.compile(r'<section class="deck-slide" id="(\d+)".*?</section>', re.S)
MOTION = re.compile(r'(<script type="application/json" id="deck-motion">)(.*?)(</script>)', re.S)
MARK = "\x00SLIDE\x00"


def label_of(section_html: str) -> str:
    m = re.search(r'data-label="([^"]*)"', section_html[:2000])
    return m.group(1) if m else ""


def place(label: str, after_label: str, build: Callable[[int, int], str], motion_entry: dict, deck: Path = DECK) -> int:
    """Insert/refresh the slide labelled `label` after the one labelled `after_label`; return its number.

    `build(number, total)` returns the full <section> HTML. Labels are compared HTML-escaped, as in the deck.
    """
    html = deck.read_text(encoding="utf-8")
    want, prev = escape(label), escape(after_label)
    sections = list(SECTION.finditer(html))
    existing = next((m for m in sections if label_of(m.group(0)) == want), None)
    if existing:
        html = html[: existing.start()] + MARK + html[existing.end() :]
    else:
        anchor_idx, anchor = next(((i, m) for i, m in enumerate(sections) if label_of(m.group(0)) == prev), (None, None))
        if anchor is None:
            raise SystemExit(f"no slide labelled {after_label!r} in {deck}")
        html = html[: anchor.end()] + MARK + html[anchor.end() :]
        motion = MOTION.search(html)
        cfg = json.loads(motion.group(2))
        cfg["slides"].insert(anchor_idx + 1, motion_entry)
        html = html[: motion.start(2)] + json.dumps(cfg, ensure_ascii=False, separators=(",", ":")) + html[motion.end(2) :]
    total = len(SECTION.findall(html)) + 1
    labels = [label_of(m.group(0)) for m in SECTION.finditer(html.replace(MARK, '<section class="deck-slide" id="0" data-label="' + want + '"></section>'))]
    number = labels.index(want) + 1
    html = html.replace(MARK, build(number, total))

    n = 0

    def renumber(m: re.Match) -> str:
        nonlocal n
        n += 1
        head = re.sub(r'^<section class="deck-slide" id="\d+"', f'<section class="deck-slide" id="{n}"', m.group(0), count=1)
        return re.sub(r'aria-label="Slide \d+ of \d+"', f'aria-label="Slide {n} of {total}"', head, count=1)

    html = SECTION.sub(renumber, html)
    count = len(json.loads(MOTION.search(html).group(2))["slides"])
    if count != total:
        raise SystemExit(f"motion list has {count} entries for {total} slides; deck not written")
    deck.write_text(html, encoding="utf-8")
    return number
