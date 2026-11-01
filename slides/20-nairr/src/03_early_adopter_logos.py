"""Slide 20: replace the early-adopter name chips with each community's logo.

Downloads the logo files the speaker chose (2026-11-01) into data/raw/sources/logos/, each recorded in that folder's
MANIFEST.yaml. The downloads are not committed. The script trims the empty margins, scales each logo to a common
height, writes figures/logos/<key>.webp, and swaps each white name chip on slide 20 for a white tile holding the
logo. A community whose logo file is missing keeps its text chip.

NSCORE's file (linked by the speaker) is a lockup of the NSF logo, a divider and the NSCORE emblem, with no name. NSF
funds all six communities and is already in the slide footer, so the script keeps only the emblem (right of the
divider) and sets "NSCORE" beside it in the wordmark's blue, rgb(50, 88, 136), sampled from NSCORE's wordmark.
Idempotent.

    uv run python slides/20-nairr/src/03_early_adopter_logos.py
"""

from __future__ import annotations

import base64
import re
import sys
from html import escape
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from evidence.fetch import fetch  # noqa: E402

DECK = ROOT / "talk" / "deck.html"
RAW = HERE / "data" / "raw" / "sources" / "logos"
OUT = HERE / "figures" / "logos"
UA = "colloquium-evidence/0.1 (UNM CARC research)"
HEIGHT_PX = 160  # stored height; shown at TILE_PX
TILE_PX = 80

# Order and chip text as on the slide: (key, chip text, logo URL or None, alt text)
LOGOS = [
    ("neon", "NEON (Battelle)",
     "https://images.squarespace-cdn.com/content/v1/5c4f6792ec4eb7c7c4186cc0/1553045886628-D1LXYEX5JPWY97YAL4IJ/NEON_288.png",
     "NEON, the National Ecological Observatory Network, operated by Battelle"),
    ("esiil", "ESIIL", "https://esiil.org/sites/default/files/Final_ESIIL%20Wordmark%20Color_0.png",
     "ESIIL, the Environmental Data Science Innovation & Impact Lab"),
    ("ncems", "NCEMS",
     "https://cyverse.org/sites/default/files/styles/az_large/public/2024-10/Screenshot-2024-10-07-at-1.32.35-PM.png.webp?itok=CMtmuf6P",
     "NCEMS, the National Synthesis Center for Emergence in the Molecular and Cellular Sciences"),
    ("nscore", "NSCORE",
     "https://nscore.columbia.edu/sites/nscore.columbia.edu/files/styles/cu_crop/public/content/NSF_NSCORE_lockup_360_200.png.webp",
     "NSCORE, the National Synthesis Center for Organismal Resilience"),
    ("aiira", "AIIRA", "https://aiira.iastate.edu/resources/aiira-logo/download.php?file=aiira-logo-with-text-light-bg.png",
     "AIIRA, the AI Institute for Resilient Agriculture"),
    ("eht", "EHT",
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTv9TUQMHaFhZ1TKUXWRqce_ZYRehEnCQYI3XmMe3IlX_K_1ZIpGfmkJAc&s=10",
     "Event Horizon Telescope"),
]
CROP = {"nscore": (205, 0)}  # keep pixels right of x=205 (the lockup's divider is at x=199-200)
LABEL = {"nscore": ("NSCORE", "rgb(50, 88, 136)")}  # (text, colour) set beside a name-less emblem
TILE = ("display: flex; align-items: center; justify-content: center; min-width: 0px; min-height: 0px; "
        "background-color: rgb(255, 255, 255); padding: 12px 22px; box-sizing: border-box;")


def raw_file(key: str) -> Path | None:
    hits = sorted(RAW.glob(f"{key}.*"))
    return hits[0] if hits else None


def download() -> None:
    for key, _, url, _ in LOGOS:
        if url and raw_file(key) is None:
            fetch(url, RAW / f"{key}.img", source=f"{key} logo (link chosen by the speaker)", user_agent=UA)


def processed(key: str) -> bytes | None:
    src = raw_file(key)
    if src is None:
        return None
    im = Image.open(src).convert("RGBA")
    if key in CROP:
        im = im.crop((CROP[key][0], CROP[key][1], im.width, im.height))
    # Trim margins: transparent pixels, or near-white pixels on an opaque background.
    flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
    flat.alpha_composite(im)
    diff = ImageChops.difference(flat.convert("RGB"), Image.new("RGB", im.size, (255, 255, 255)))
    box = diff.convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
    if box:
        im = im.crop(box)
    w = round(im.width * HEIGHT_PX / im.height)
    im = im.resize((w, HEIGHT_PX), Image.LANCZOS)
    buf = BytesIO()
    im.save(buf, "WEBP", quality=90, method=6)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{key}.webp").write_bytes(buf.getvalue())
    return buf.getvalue()


def tile(i: int, key: str, alt: str, data: bytes) -> str:
    return (f'<div data-node-path="3.1.{i}" data-evidence="logo-{key}" style="{TILE}">'
            f'<img alt="{escape(alt)}" draggable="false" src="data:image/webp;base64,{base64.b64encode(data).decode()}" '
            f'style="display: block; height: {TILE_PX}px; width: auto; max-width: 260px; object-fit: contain;">'
            + (f'<span style="font-family: Georgia, &quot;Times New Roman&quot;, serif; font-size: 34px; font-weight: 400; '
               f'letter-spacing: 1px; color: {LABEL[key][1]}; margin-left: 14px; white-space: nowrap;">{LABEL[key][0]}</span>'
               if key in LABEL else "")
            + "</div>")


def main() -> int:
    download()
    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*data-label="What NAIRR gives researchers"', html).start()
    end = html.index("</section>", start)
    slide = html[start:end]
    placed = []
    for i, (key, chip, _, alt) in enumerate(LOGOS):
        data = processed(key)
        if data is None:
            continue
        chip_re = re.compile(rf'<div data-text-path="3\.1\.{i}" [^>]*>{re.escape(escape(chip, quote=False))}</div>')
        tile_re = re.compile(rf'<div data-node-path="3\.1\.{i}" data-evidence="logo-{key}" [^>]*><img [^>]*>(?:<span [^>]*>[^<]*</span>)?</div>')
        m = chip_re.search(slide) or tile_re.search(slide)
        if not m:
            print(f"{key}: chip not found on slide 20", file=sys.stderr)
            return 1
        slide = slide[: m.start()] + tile(i, key, alt, data) + slide[m.end() :]
        placed.append(key)
    # Centre the logos and any remaining text chip vertically in the row.
    slide = slide.replace(
        '<div data-node-path="3.1" style="display: flex; flex-flow: wrap; align-items: stretch;',
        '<div data-node-path="3.1" style="display: flex; flex-flow: wrap; align-items: center;')
    DECK.write_text(html[:start] + slide + html[end:], encoding="utf-8")
    missing = [k for k, *_ in LOGOS if k not in placed]
    print(f"logos on slide 20: {', '.join(placed)}" + (f"; text chip kept for: {', '.join(missing)}" if missing else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
