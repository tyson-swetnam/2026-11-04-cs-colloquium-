"""Slide 20: add resource logos to the "Research cloud" and "AI inference" cards, and name NDIF correctly.

Research cloud gets logos for Jetstream2, the National Research Platform (NRP) and FabAID, which replace the names in
its text ("Agentic AI on:"). AI inference used to say
"including the National Inference Service", a name with no source (see claims.yaml c8). It now names the NSF
National Deep Inference Fabric (NDIF), worded as ndif.us describes it, with its emblem.

How each logo is handled:
- Jetstream2: docs.jetstream-cloud.org/images/JS2-Logo-Transparent.png. jetstream-cloud.org itself failed TLS
  verification behind the session proxy, and that check was not bypassed.
- NRP: the horizontal logo the speaker linked. Its lettering is #CCCCCC, made for dark backgrounds, so it sits on a
  dark tile.
- FabAID: the site's mark (FabricMark.svg, embedded as SVG) plus the name as text, as in the site header.
- NDIF: the NSF + NDIF lockup from ndif.us, cropped to the NDIF emblem, which carries the name. NSF is already in
  the slide footer.

Downloads go to data/raw/sources/logos/ (MANIFEST.yaml; not committed); processed files go to figures/logos/.
Idempotent.

    uv run python slides/20-nairr/src/04_resource_logos.py
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
H = 32  # logo height on the slide, px

SOURCES = {  # key: (url, raw file name)
    "jetstream2": ("https://docs.jetstream-cloud.org/images/JS2-Logo-Transparent.png", "jetstream2.png"),
    "nrp": ("https://nrp.ai/_astro/NRP_Horizontal_Logo.png.DQL8-3kz.webp", "nrp.webp"),
    "fabaid": ("https://fabaid.io/images/logos/FabricMark.svg", "fabaid_mark.svg"),
    "ndif": ("https://ndif.us/_next/static/media/NSF_NDIF_Lockup.e0ccdffb.png", "ndif_lockup.png"),
}
CROP_LEFT = {"ndif": 116}  # NSF | NDIF lockup: the divider is at x=112
OLD_INFERENCE = "Hosted open and commercial models, including the National Inference Service."
NEW_INFERENCE = "Hosted open and commercial models, plus NDIF for research on model internals."
OLD_CLOUD = "Agentic AI on Jetstream2, the National Research Platform and FabAID."
NEW_CLOUD = "Agentic AI on:"
OLD_NOTE = "and AI inference (hosted models, including the National Inference Service)."
NEW_NOTE = ("and AI inference (hosted open and commercial models, plus the NSF National Deep Inference Fabric, NDIF, "
            "which gives free remote access to large open models and their internals; https://ndif.us/).")


def raster(key: str) -> bytes:
    url, name = SOURCES[key]
    src = fetch(url, RAW / name, source=f"{key} logo", user_agent=UA)
    im = Image.open(src).convert("RGBA")
    if key in CROP_LEFT:
        im = im.crop((CROP_LEFT[key], 0, im.width, im.height))
    box = im.split()[3].point(lambda v: 255 if v > 24 else 0).getbbox()
    flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
    flat.alpha_composite(im)
    if box is None or box == (0, 0, im.width, im.height):  # opaque image: trim near-white margins instead
        box = ImageChops.difference(flat.convert("RGB"), Image.new("RGB", im.size, "white")).convert("L").point(
            lambda v: 255 if v > 24 else 0).getbbox()
    im = im.crop(box)
    im = im.resize((round(im.width * H * 3 / im.height), H * 3), Image.LANCZOS)
    buf = BytesIO()
    im.save(buf, "WEBP", quality=90, method=6)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{key}.webp").write_bytes(buf.getvalue())
    return buf.getvalue()


def img(data: bytes, mime: str, alt: str, height: int = H) -> str:
    return (f'<img alt="{escape(alt)}" draggable="false" src="data:{mime};base64,{base64.b64encode(data).decode()}" '
            f'style="display: block; height: {height}px; width: auto;">')


def tile(inner: str, bg: str = "rgb(255, 255, 255)", border: str = "1px solid rgb(220, 220, 220)") -> str:
    return (f'<div style="display: flex; align-items: center; gap: 10px; background: {bg}; border: {border}; '
            f'padding: 8px 12px; box-sizing: border-box;">{inner}</div>')


def row(name: str, tiles: str, place: str = "margin-top: auto; padding-top: 8px;") -> str:
    return (f'<!--{name}--><div data-evidence="{name}" style="display: flex; flex-flow: wrap; align-items: center; '
            f'gap: 10px; {place}">{tiles}</div><!--/{name}-->')


def check_ndif() -> dict:
    """Save ndif.us and confirm the wording the slide relies on, and its NAIRR link (data/processed/ndif_check.json)."""
    import json

    from bs4 import BeautifulSoup

    page = fetch("https://ndif.us/", HERE / "data" / "raw" / "sources" / "ndif_us.html", source="NDIF home page", user_agent=UA)
    raw = page.read_text(encoding="utf-8")
    text = re.sub(r"\s+", " ", BeautifulSoup(raw, "html.parser").get_text(" "))
    result = {
        "url": "https://ndif.us/",
        "describes_free_remote_access_to_model_internals": "provides free remote access to large-scale AI models, democratizing access to model internals" in text,
        "names_itself_nsf_national_deep_inference_fabric": "The NSF National Deep Inference Fabric (NDIF)" in text,
        "links_nairr_pilot_as_supporter": "nairrpilot.org" in raw and "nairr-pilot-logo" in raw,
        "nsf_award": "2408455" if "NSF Award #2408455" in text else None,
    }
    out = HERE / "data" / "processed" / "ndif_check.json"
    out.write_text(json.dumps(result, indent=1) + "\n")
    return result


def main() -> int:
    ndif = check_ndif()
    if not all(v for k, v in ndif.items() if k != "url"):
        print(f"ndif.us no longer supports the slide wording: {ndif}", file=sys.stderr)
        return 1
    mark = fetch(SOURCES["fabaid"][0], RAW / SOURCES["fabaid"][1], source="fabaid logo mark", user_agent=UA).read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "fabaid_mark.svg").write_bytes(mark)
    cloud = row("logos-research-cloud",
                tile(img(raster("jetstream2"), "image/webp", "Jetstream2"))
                + tile(img(raster("nrp"), "image/webp", "NRP, the National Research Platform"),
                       bg="rgb(23, 20, 15)", border="1px solid rgb(23, 20, 15)")
                + tile(img(mark, "image/svg+xml", "", height=26)
                       + '<span style="font-family: Montserrat, Arial, sans-serif; font-size: 22px; font-weight: 700; '
                         'color: rgb(23, 20, 15); letter-spacing: 0.5px;" aria-label="FabAID">Fab<span style="color: rgb(182, 31, 36);">AID</span></span>'))
    inference = row("logos-ai-inference",
                    tile(img(raster("ndif"), "image/webp", "NDIF, the NSF National Deep Inference Fabric", height=60),
                         border="1px solid rgb(255, 255, 255)"),
                    place="position: absolute; top: 24px; right: 24px;")  # beside the heading; the card has no spare height

    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*data-label="What NAIRR gives researchers"', html).start()
    end = html.index("</section>", start)
    slide = html[start:end]
    head = html[start : html.index(">", start) + 1]
    slide = re.sub(r"<!--(logos-[a-z-]+)-->.*?<!--/\1-->", "", slide, flags=re.S)
    slide = slide.replace(OLD_INFERENCE, NEW_INFERENCE).replace(OLD_CLOUD, NEW_CLOUD)
    card = re.search(r'<div data-node-path="2\.2" style="', slide)  # anchor for the absolutely placed NDIF emblem
    if "position: relative" not in slide[card.end() : card.end() + 40]:
        slide = slide[: card.end()] + "position: relative; " + slide[card.end() :]
    for k, block in (("2.1", cloud), ("2.2", inference)):
        m = re.search(rf'(<div data-text-path="{k}\.1" [^>]*>[^<]*</div>)(</div>)', slide)  # card text, last child
        if not m:
            print(f"card {k}: text not found on slide 20", file=sys.stderr)
            return 1
        slide = slide[: m.end(1)] + block + slide[m.end(1) :]
    new_head = head.replace(escape(OLD_NOTE, quote=True), escape(NEW_NOTE, quote=True))
    slide = new_head + slide[len(head) :]
    DECK.write_text(html[:start] + slide + html[end:], encoding="utf-8")
    print("slide 20: logos on Research cloud (Jetstream2, NRP, FabAID) and AI inference (NDIF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
