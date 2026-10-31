"""Measure the images embedded in talk/deck.html for slide 04 and compare them with the Commons files.

Finds each <img> by its alt text, decodes the data: URI, and reports format, pixel size,
byte size and SHA-256. The War Room still is compared with the Commons original
downloaded to data/raw/sources/ (if present). Output: data/processed/deck_images.json.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
DECK = ROOT / "talk" / "deck.html"
ALTS = {
    "poster": "Theatrical release poster for Dr. Strangelove",
    "war_room": "The War Room in Dr. Strangelove",
}
COMMONS = {
    "war_room": HERE / "data" / "raw" / "sources" / "img_Dr._Strangelove_-_The_War_Room.png",
}

html = DECK.read_text(encoding="utf-8")
out = {}
for key, alt in ALTS.items():
    tags = [m.group(0) for m in re.finditer(r"<img\b[^>]*>", html) if alt in m.group(0)]
    if not tags:
        sys.exit(f"no <img> with alt containing {alt!r}")
    src = re.search(r'src="data:image/(\w+);base64,([^"]+)"', tags[0])
    data = base64.b64decode(src.group(2).replace("&#x2F;", "/"))
    im = Image.open(io.BytesIO(data))
    rec = {
        "alt": alt,
        "mime": f"image/{src.group(1)}",
        "pixels": list(im.size),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "img_tags_found": len(tags),
    }
    ref = COMMONS.get(key)
    if ref and ref.exists():
        rim = Image.open(ref)
        rec["commons_pixels"] = list(rim.size)
        rec["same_aspect_as_commons"] = abs(im.size[0] / im.size[1] - rim.size[0] / rim.size[1]) < 0.01
    out[key] = rec

out["video_tags_in_deck"] = len(re.findall(r"<video\b", html))
out["strangelove_trailer_webm_mentioned"] = "Trailer.webm" in html
(HERE / "data" / "processed").mkdir(parents=True, exist_ok=True)
(HERE / "data" / "processed" / "deck_images.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
