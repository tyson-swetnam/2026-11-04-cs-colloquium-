"""Slide 33: fetch the CARC website, the docs' agent endpoints and the two conventions they follow (OKF, llms.txt).

    uv run python slides/33-carc-docs-for-ai-agents/src/01_fetch_sources.py [--refresh]
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.source_fetch import fetch_pages  # noqa: E402

PAGES = {
    "carc_home.html": ("https://carc.unm.edu/", "CARC home page"),
    "docs_ai_agents.html": ("https://carc.unm.edu/docs/about/ai-agents/", "CARC docs: For AI agents"),
    "docs_llms.txt": ("https://carc.unm.edu/docs/llms.txt", "CARC docs llms.txt (outline of every page)"),
    "docs_llms_full.txt": ("https://carc.unm.edu/docs/llms-full.txt", "CARC docs llms-full.txt (whole corpus)"),
    "docs_faq_general.md": ("https://carc.unm.edu/docs/faq/general/index.md", "CARC docs: General FAQ, Markdown twin"),
    "okf_spec.md": ("https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md",
                    "Open Knowledge Format specification (GoogleCloudPlatform/knowledge-catalog)"),
    "llmstxt.md": ("https://llmstxt.org/index.md", "The /llms.txt file proposal (llmstxt.org)"),
}

if __name__ == "__main__":
    sys.exit(1 if fetch_pages(HERE, PAGES, refresh="--refresh" in sys.argv) else 0)
