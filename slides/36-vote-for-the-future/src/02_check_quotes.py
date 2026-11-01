"""Slide 36: check every quote in data/raw/research/facts.csv against the saved source it cites (tools/quote_check.py).

Run src/01_fetch_sources.py first.

    uv run python slides/36-vote-for-the-future/src/02_check_quotes.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.quote_check import run  # noqa: E402

if __name__ == "__main__":
    sys.exit(run(HERE))
