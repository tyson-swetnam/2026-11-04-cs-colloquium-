"""Compare the poster embedded in talk/deck.html with the English Wikipedia non-free file by SHA-1.

Queries the MediaWiki imageinfo API (size, sha1, dimensions) for File:Dr._Strangelove_poster.jpg,
saves the raw API JSON to data/raw/sources/, and writes data/processed/enwiki_poster_match.json.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from evidence.http import CachedGet  # noqa: E402
from evidence.fetch import record  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
URL = ("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=imageinfo"
       "&iiprop=size%7Csha1%7Cmime%7Ctimestamp%7Curl&titles=File:Dr._Strangelove_poster.jpg")

get = CachedGet(HERE / "data" / "cache", UA)
status, body = get(URL)
if status != 200:
    get.cache.joinpath(__import__("hashlib").sha1(f"{URL}|None".encode()).hexdigest() + ".txt").unlink(missing_ok=True)
    sys.exit(f"API returned HTTP {status}")
raw = HERE / "data" / "raw" / "sources" / "enwiki_api_imageinfo_Dr_Strangelove_poster_jpg.json"
raw.write_text(body, encoding="utf-8")
record(raw, url=URL, source="English Wikipedia (MediaWiki API)",
       note="imageinfo size/sha1 for the non-free poster file")
info = next(iter(json.loads(body)["query"]["pages"].values()))["imageinfo"][0]

html = (ROOT / "talk" / "deck.html").read_text(encoding="utf-8")
tag = next(m.group(0) for m in re.finditer(r"<img\b[^>]*>", html)
           if "Theatrical release poster for Dr. Strangelove" in m.group(0))
data = base64.b64decode(re.search(r'src="data:image/\w+;base64,([^"]+)"', tag).group(1).replace("&#x2F;", "/"))
out = {
    "enwiki": {k: info.get(k) for k in ("size", "width", "height", "sha1", "mime", "timestamp")},
    "deck": {"bytes": len(data), "sha1": hashlib.sha1(data).hexdigest()},
}
out["identical"] = out["enwiki"]["sha1"] == out["deck"]["sha1"] and out["enwiki"]["size"] == len(data)
(HERE / "data" / "processed" / "enwiki_poster_match.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
