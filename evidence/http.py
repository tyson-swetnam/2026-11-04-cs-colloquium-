"""GET with an on-disk cache and per-host politeness, for public APIs used by the analyses."""

from __future__ import annotations

import hashlib
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

# Seconds to wait after a live request, by host (arXiv asks for 3 s between calls).
PAUSE = {"export.arxiv.org": 3.0}
DEFAULT_PAUSE = 0.5


class CachedGet:
    def __init__(self, cache_dir: Path, user_agent: str):
        self.cache = Path(cache_dir)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.headers = {"User-Agent": user_agent}

    def __call__(self, url: str, accept: str | None = None) -> tuple[int, str]:
        """(status, body). Cached forever: delete the cache directory to refresh."""
        key = hashlib.sha1(f"{url}|{accept}".encode()).hexdigest()
        path = self.cache / f"{key}.txt"
        if path.exists():
            status, _, body = path.read_text(encoding="utf-8").partition("\n")
            return int(status), body
        headers = dict(self.headers, **({"Accept": accept} if accept else {}))
        pause = PAUSE.get(urlparse(url).hostname or "", DEFAULT_PAUSE)
        for attempt in range(4):
            r = requests.get(url, headers=headers, timeout=60)
            if r.status_code not in (429, 503):
                break
            time.sleep(pause * (attempt + 2))
        time.sleep(pause)
        path.write_text(f"{r.status_code}\n{r.text}", encoding="utf-8")
        return r.status_code, r.text
