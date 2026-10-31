"""Paths and shared settings for slide 17."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLIDE = HERE.parent
RAW = SLIDE / "data" / "raw"
PROCESSED = SLIDE / "data" / "processed"
FIGURES = SLIDE / "figures"
CACHE = SLIDE / "data" / "cache"  # API responses; gitignored, rebuilt on demand
ROOT = SLIDE.parents[1]
sys.path.insert(0, str(ROOT))

UA = "colloquium-evidence/0.1 (UNM CARC research)"
