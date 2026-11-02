"""Slide 25: check the Formation page the demo shows (de.cyverse.org/formation) for the facts in the notes.

The notes say the server is added to Claude Code with one command and that sign-in is OAuth through CyVerse. This
saves the live page (data/raw/sources/, MANIFEST.yaml) and checks the quotes in data/raw/research/facts.csv word for
word (tools/quote_check.py).

    uv run python slides/25-demo-1-video/src/03_check_formation_docs.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.quote_check import run  # noqa: E402
from tools.source_fetch import fetch_pages  # noqa: E402

PAGES = {"formation.html": ("https://de.cyverse.org/formation", "CyVerse Formation MCP server page")}

if __name__ == "__main__":
    failed = fetch_pages(HERE, PAGES, refresh="--refresh" in sys.argv)
    sys.exit(failed or run(HERE))
