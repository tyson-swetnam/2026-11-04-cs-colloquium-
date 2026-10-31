"""Slide 15 notes: are MESA's MCP servers public? Checked from MESA's public docs only (not its code).

Fetches the Markdown twins of idss-mesa.github.io pages, saves them under data/raw/sources/,
logs them in MANIFEST.yaml, and pulls out the sentences that bear on public availability.
Output: data/processed/mesa_public.csv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.fetch import record  # noqa: E402
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
BASE = "https://idss-mesa.github.io/"
# (finding, page, exact text to find)
CHECKS = [
    ("Public one-line installer fetched from GitHub", "docs/index.md", "curl -fsSL https://raw.githubusercontent.com/idss-mesa/docs/main/install.sh | bash"),
    ("Anonymous public data access, no credentials", "docs/index.md", "anonymous public CyVerse access by default — no credentials required to get started"),
    ("Source repos in the idss-mesa GitHub org", "docs/index.md", "Source repositories live in the [**idss-mesa**](https://github.com/idss-mesa) GitHub"),
    ("Installer clones repos from the idss-mesa org", "docs/install/index.md", "| `MESA_GIT_ORG` | `idss-mesa` | GitHub org to clone from |"),
    ("Installer clones repos it lacks", "docs/install/index.md", "- Repos are `git pull --ff-only`'d if already present, cloned otherwise."),
    ("mesa-mcp repo link", "docs/servers/mesa-mcp/index.md", "**Repo:** [idss-mesa/mesa-mcp](https://github.com/idss-mesa/mesa-mcp)"),
    ("irods-mcp-server built from source", "docs/servers/irods-mcp-server/index.md", "The installer builds it from source and registers the stdio binary against the repo's"),
    ("irods-mcp-server Docker image published", "docs/servers/irods-mcp-server/index.md", "A published Docker image, `cyverse/irods-mcp-server`, is also available"),
    ("Formation is CyVerse's own hosted server", "docs/servers/formation-mcp/index.md", "Formation is the CyVerse Discovery Environment's own MCP server"),
    ("CyVerse public read-only hosted endpoint", "docs/llms-full.txt", "hosts a public, read-only Data Store server at <https://mcp-public.cyverse.ai/mcp>, which"),
    ("Installer's documented clients (four)", "docs/index.md", "[Antigravity](https://idss-mesa.github.io/docs/antigravity/), or [OpenCode](https://idss-mesa.github.io/docs/opencode/) — with a single command, so"),
    ("MESA CLI app ships five agent CLIs incl. Goose", "docs/index.md", "A terminal in the browser, with Claude Code, Codex, OpenCode, Goose, and Antigravity"),
]
LICENCE = re.compile(r"\b(licen[cs]e[sd]?|MIT|Apache[- ]2|BSD|GPL)\b", re.I)


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache", UA)
    raw = SLIDE / "data" / "raw" / "sources"
    raw.mkdir(parents=True, exist_ok=True)
    pages: dict[str, str] = {}
    for page in sorted({p for _, p, _ in CHECKS}):
        status, body = get(BASE + page)
        if status != 200:
            raise SystemExit(f"{page}: HTTP {status}")
        dest = raw / page.replace("/", "_")
        dest.write_text(body, encoding="utf-8")
        record(dest, url=BASE + page, source="MESA documentation (idss-mesa.github.io)", note="Markdown twin; public docs only")
        pages[page] = body
    rows = [{"finding": f, "url": BASE + p, "found": q in pages[p], "quote": q} for f, p, q in CHECKS]
    lic_pages = ("docs/servers/mesa-mcp/index.md", "docs/servers/irods-mcp-server/index.md", "docs/install/index.md")
    lic = sorted({m.group(0) for p in lic_pages for m in LICENCE.finditer(pages[p])})
    rows.append({"finding": "Licence named on server/install pages", "url": BASE + "docs/servers/", "found": bool(lic), "quote": "; ".join(lic)})
    df = pd.DataFrame(rows)
    out = SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "mesa_public.csv", index=False)
    print(df[["finding", "found"]].to_string(index=False))


if __name__ == "__main__":
    main()
