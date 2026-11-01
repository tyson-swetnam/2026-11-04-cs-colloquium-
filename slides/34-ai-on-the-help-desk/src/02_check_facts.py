"""Slide 34: check every quote in data/raw/research/facts.csv against the saved NVIDIA pages (tools/quote_check.py).

    uv run python slides/34-ai-on-the-help-desk/src/02_check_facts.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.quote_check import run  # noqa: E402

if __name__ == "__main__":
    sys.exit(run(HERE))
