"""Slide 34: check every quote in data/raw/research/facts.csv against the saved source it cites.

Pages are reduced to plain text (tags stripped, entities decoded, curly quotes and dashes folded, whitespace
collapsed, case folded). A quote with " … " passes only if every segment is found, in order. Bluesky responses
contribute the post texts; X oEmbed responses contribute the post HTML. Writes data/processed/quote_check.csv
and exits non-zero if any quote is missing. Where the notes say "Para N", the nearest paragraph number before the
quote in the encyclical must be N. Run src/01_fetch_sources.py first.

    uv run python slides/34-vote-for-the-future/src/02_check_quotes.py
"""

from __future__ import annotations

import csv
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parents[1]
SOURCES = HERE / "data" / "raw" / "sources"
FACTS = HERE / "data" / "raw" / "research" / "facts.csv"
OUT = HERE / "data" / "processed" / "quote_check.csv"
FOLD = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", html.unescape(text)).translate(FOLD)
    return re.sub(r"\s+", " ", text).strip().casefold()


def page_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".json":
        data = json.loads(raw)
        if "posts" in data:  # Bluesky getPosts
            return "\n".join(p["record"]["text"] for p in data["posts"])
        if "html" in data:  # X oEmbed
            return BeautifulSoup(data["html"], "html.parser").get_text(" ")
        return json.dumps(data, ensure_ascii=False)
    # Join inline elements without spaces so "Pius XII<a>…</a>’s" stays one run of text.
    return BeautifulSoup(raw, "html.parser").get_text("")


def found(quote: str, text: str) -> bool:
    pos = 0
    for seg in (norm(s) for s in quote.split("…")):
        if not seg:
            continue
        i = text.find(seg, pos)
        if i < 0:
            return False
        pos = i + len(seg)
    return True


def para_before(quote: str, text: str) -> int | None:
    """Number of the numbered paragraph ("107. ...") that the quote falls in."""
    i = text.find(norm(quote.split("…")[0]))
    nums = re.findall(r"(?:^|\s)(\d{1,3})\. ", text[max(0, i - 8000) : i]) if i >= 0 else []
    return int(nums[-1]) if nums else None


def main() -> int:
    texts: dict[str, str] = {}
    results, missing = [], 0
    for row in csv.DictReader(FACTS.open(encoding="utf-8")):
        src = SOURCES / row["source_file"]
        if not src.exists():
            status = "source not fetched"
        else:
            if src.name not in texts:
                texts[src.name] = norm(page_text(src))
            status = "found" if found(row["quote"], texts[src.name]) else "NOT FOUND"
            para = re.match(r"Para (\d+)", row["notes"])
            if status == "found" and para and para_before(row["quote"], texts[src.name]) != int(para.group(1)):
                status = f"found, not in para {para.group(1)}"
        missing += status != "found"
        results.append({"id": row["id"], "claim_id": row["claim_id"], "source_file": row["source_file"], "status": status})
        print(f"{row['id']} {row['claim_id']:>3} {status:18} {row['source_file']}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "claim_id", "source_file", "status"])
        w.writeheader()
        w.writerows(results)
    print(f"{len(results) - missing}/{len(results)} quotes found verbatim")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
