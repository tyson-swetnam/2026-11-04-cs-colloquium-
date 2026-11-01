"""Fetch a slide's primary sources into data/raw/sources/ and log each in that folder's MANIFEST.yaml.

Plain requests with an honest user agent; no logins, no bot-check workarounds. A page that fails is reported and
skipped, so the quote check marks its quotes "source not fetched" rather than passing them.
"""

from __future__ import annotations

import time
from pathlib import Path

import requests

from evidence.fetch import record

UA = "colloquium-evidence/0.1 (UNM CARC research)"


def fetch_pages(slide: Path, pages: dict[str, tuple[str, str]], refresh: bool = False) -> int:
    """pages: {file name: (url, source description)}. Returns the number of failures."""
    out = slide / "data" / "raw" / "sources"
    out.mkdir(parents=True, exist_ok=True)
    failed = 0
    for name, (url, source) in pages.items():
        dest = out / name
        if dest.exists() and not refresh:
            continue
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=120)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"skip {name}: {e}")
            failed += 1
            continue
        dest.write_bytes(r.content)
        record(dest, url=url, source=source)
        print(f"saved {name} ({len(r.content):,} bytes)")
        time.sleep(0.5)
    return failed
