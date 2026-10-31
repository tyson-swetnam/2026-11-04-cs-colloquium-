"""Read licence metadata and wikitext for the three Commons files used on slide 04.

Uses the plain file-page wikitext (index.php?action=raw), one request per file
with the CachedGet pause; the API endpoint returned HTTP 429 from this network.
A non-200 response stops the script and is removed from the cache.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from evidence.http import CachedGet  # noqa: E402
from evidence.fetch import record  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
FILES = [
    "File:Dr._Strangelove_poster.png",
    "File:Dr._Strangelove_-_The_War_Room.png",
    "File:Dr._Strangelove_(1964)_-_Trailer.webm",
]
API = "https://commons.wikimedia.org/w/api.php"
CACHE = HERE / "data" / "cache"
get = CachedGet(CACHE, UA)
src = HERE / "data" / "raw" / "sources"
src.mkdir(parents=True, exist_ok=True)
out = []
for f in FILES:
    url = f"https://commons.wikimedia.org/w/index.php?title={quote(f)}&action=raw"
    status, text = get(url)
    if status != 200:
        key = hashlib.sha1(f"{url}|None".encode()).hexdigest()
        (CACHE / f"{key}.txt").unlink(missing_ok=True)
        sys.exit(f"{f}: HTTP {status}: {text[:200]}")
    stem = f.split(":", 1)[1].rsplit(".", 1)[0]
    stem = "".join(c if c.isalnum() else "_" for c in stem)
    path = src / f"commons_{stem}.wikitext"
    path.write_text(text)
    record(path, url=url, source="Wikimedia Commons", note="file description page wikitext (action=raw)")
    lic = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("{{") and ("PD" in ln or "icen" in ln.lower())]
    author = next((ln.split("=", 1)[1].strip() for ln in text.splitlines() if ln.strip().lstrip("|").startswith("author")), None)
    out.append({"file": f.replace("_", " "), "url": url, "licence_templates": lic, "author_field": author, "wikitext": text})
(HERE / "data" / "processed").mkdir(parents=True, exist_ok=True)
(HERE / "data" / "processed" / "commons_licences.json").write_text(json.dumps(out, indent=2))
for o in out:
    print("=====", o["file"], o["licence_templates"], "| author:", o["author_field"])
    print(o["wikitext"])
