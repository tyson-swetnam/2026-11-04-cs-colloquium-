"""tools/deck_insert.place: insert after a labelled slide, renumber, keep the motion list aligned, idempotent."""

import json
import re

import pytest

from tools.deck_insert import place


def deck(labels):
    secs = "".join(
        f'<section class="deck-slide" id="{i}" aria-label="Slide {i} of {len(labels)}" data-label="{l}">x</section>'
        for i, l in enumerate(labels, 1)
    )
    motion = json.dumps({"slides": [{"bg": l} for l in labels]})
    return f'<main>{secs}</main><script type="application/json" id="deck-motion">{motion}</script>'


def build(n, total):
    return f'<section class="deck-slide" id="{n}" aria-label="Slide {n} of {total}" data-label="New">new</section>'


def state(path):
    html = path.read_text()
    labels = re.findall(r'data-label="([^"]*)"', html)
    ids = re.findall(r'<section class="deck-slide" id="(\d+)" aria-label="Slide (\d+) of (\d+)"', html)
    motion = [s["bg"] for s in json.loads(re.search(r'id="deck-motion">(.*?)</script>', html).group(1))["slides"]]
    return labels, ids, motion


def test_insert_renumber_and_idempotent(tmp_path):
    p = tmp_path / "deck.html"
    p.write_text(deck(["A", "B", "C"]))
    assert place("New", "B", build, {"bg": "New"}, deck=p) == 3
    first = p.read_text()
    labels, ids, motion = state(p)
    assert labels == ["A", "B", "New", "C"]
    assert ids == [(str(i), str(i), "4") for i in range(1, 5)]
    assert motion == ["A", "B", "New", "C"]
    assert place("New", "B", build, {"bg": "New"}, deck=p) == 3
    assert p.read_text() == first


def test_missing_anchor_leaves_deck_untouched(tmp_path):
    p = tmp_path / "deck.html"
    p.write_text(deck(["A"]))
    before = p.read_text()
    with pytest.raises(SystemExit):
        place("New", "Nope", build, {"bg": "New"}, deck=p)
    assert p.read_text() == before
