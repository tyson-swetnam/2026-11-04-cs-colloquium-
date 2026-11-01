"""Slide 33: check every quote in data/raw/research/facts.csv (tools/quote_check.py) and count the pages in llms.txt.

The slide says "~80 pages": llms.txt lists each documentation page with a Markdown twin (page URL + index.md).
The count goes to data/processed/llms_txt_pages.json.

    uv run python slides/33-carc-docs-for-ai-agents/src/02_check_facts.py
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.quote_check import run  # noqa: E402


def count_pages() -> int:
    text = (HERE / "data" / "raw" / "sources" / "docs_llms.txt").read_text(encoding="utf-8")
    twins = set(re.findall(r"https://carc\.unm\.edu/docs/[^\s)<>]+/index\.md", text))
    twins.discard("https://carc.unm.edu/docs/<path>/index.md")
    out = HERE / "data" / "processed" / "llms_txt_pages.json"
    out.write_text(json.dumps({"pages_with_markdown_twin": len(twins), "pages": sorted(twins)}, indent=1) + "\n")
    print(f"llms.txt lists {len(twins)} pages with a Markdown twin")
    return len(twins)


if __name__ == "__main__":
    status = run(HERE)
    n = count_pages()
    sys.exit(status or (0 if 70 <= n <= 90 else 1))
