"""Check every quote in a slide's data/raw/research/facts.csv against the saved source it cites.

facts.csv columns: id, claim_id, quote, source_file, url, date, source_type, notes. Pages are reduced to plain text
(tags stripped, entities decoded, curly quotes and dashes folded, whitespace collapsed, case folded). A quote with
" … " passes only if every segment is found, in order. Bluesky getPosts responses contribute the post texts; X oEmbed
responses the post HTML; other JSON its serialized values; .md and .txt files are read as plain text. Where the notes start "Para N", the nearest numbered
paragraph before the quote must be N. Writes data/processed/quote_check.csv; run() returns 1 if anything is missing.
"""

from __future__ import annotations

import csv
import html
import json
import re
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup

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
    if path.suffix in (".md", ".txt"):
        return raw
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


def run(slide: Path) -> int:
    """Check slide/data/raw/research/facts.csv against slide/data/raw/sources; write data/processed/quote_check.csv."""
    SOURCES = slide / "data" / "raw" / "sources"
    FACTS = slide / "data" / "raw" / "research" / "facts.csv"
    OUT = slide / "data" / "processed" / "quote_check.csv"
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
