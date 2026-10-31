"""Matplotlib defaults that match the deck (UNM cherry on white, slab-serif titles)."""

from __future__ import annotations

import logging
import os

import matplotlib as mpl

CHERRY = "#ba0c2f"
INK = "#1a1a1a"
MUTED = "#6b6b6b"


def use() -> None:
    # Montserrat is the deck font; fall back quietly where it is not installed.
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    # Reproducible SVGs: fixed timestamp and element ids, so diffs show only real changes.
    os.environ.setdefault("SOURCE_DATE_EPOCH", "0")
    mpl.rcParams.update(
        {
            "figure.figsize": (16, 9),
            "figure.dpi": 120,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "font.family": ["Montserrat", "DejaVu Sans"],
            "font.size": 16,
            "axes.titlesize": 24,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.grid": True,
            "grid.color": "#e6e6e6",
            "legend.frameon": False,
            # Labels are full of dollar amounts; never treat "$...$" as math.
            "text.parse_math": False,
            "svg.hashsalt": "colloquium-evidence",
        }
    )
