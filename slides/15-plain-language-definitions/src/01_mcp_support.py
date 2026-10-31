"""Slide 15: the USB-C analogy and MCP support in the five clients the notes name, from each one's own docs.

Re-run before the talk; documentation moves (Goose's moved to goose-docs.ai in 2026).
Output: data/processed/mcp_support.csv
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.fetch import record  # noqa: E402
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
PAGES = [
    # what, publisher, url, sentence to find (regex)
    ("USB-C analogy", "Model Context Protocol", "https://modelcontextprotocol.io/docs/getting-started/intro", r"Think of MCP like a USB-C port for AI applications\.|[^.]*USB-C port for AI applications\."),
    ("Claude Code", "Anthropic", "https://code.claude.com/docs/en/mcp", r"Claude Code can connect to [^.]*Model Context Protocol \(MCP\)[^.]*\."),
    ("Codex", "OpenAI", "https://developers.openai.com/codex/mcp", r"Model Context Protocol \(MCP\) lets ChatGPT and Codex use tools and information from other systems\."),
    ("Antigravity", "Google", "https://antigravity.google/docs/mcp", r"Antigravity supports the Model Context Protocol \(MCP\)[^.\"]*"),
    ("OpenCode", "SST / OpenCode", "https://opencode.ai/docs/mcp-servers/", r"You can add external tools to OpenCode using the Model Context Protocol , or MCP\."),
    ("Goose", "Block / Agentic AI Foundation", "https://goose-docs.ai/", r"MCP is the open standard for connecting AI agents to tools and data sources\."),
]


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache", UA)
    rows = []
    for what, publisher, url, pattern in PAGES:
        status, body = get(url)
        # requests falls back to ISO-8859-1 when a page sends no charset; undo that so quotes are exact.
        try:
            body = body.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        raw = SLIDE / "data" / "raw" / "sources" / f"client_{re.sub(r'[^a-z0-9]+', '_', what.lower()).strip('_')}.html"
        raw.write_text(body, encoding="utf-8")
        record(raw, url=url, source=publisher, note=f"MCP support page for {what}; body as served (cached GET)")
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
        m = re.search(pattern, text)
        rows.append({"claim": what, "publisher": publisher, "url": url, "http_status": status, "supported": bool(m), "quote": m.group(0).strip() if m else ""})
    df = pd.DataFrame(rows)
    out = SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "mcp_support.csv", index=False)
    print(df[["claim", "supported", "quote"]].to_string(index=False, max_colwidth=120))


if __name__ == "__main__":
    main()
