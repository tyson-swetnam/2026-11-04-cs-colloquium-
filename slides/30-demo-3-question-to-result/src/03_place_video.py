"""Slide 30: put the recorded Demo 3 into the slide's "Recorded clip goes here" frame and fill in its caption.

The video is the speaker's recording (2026-11-02), already sped up 1.5x and converted to VP9 WebM by the speaker
(1280x700, 2:10, no audio, 5.5 MB). It is used as supplied (re-encoding would only add generation loss) and
recorded in data/media/MANIFEST.yaml. It fills the 1120x630 frame. It starts from the beginning each time the slide
opens, plays once and holds on the answer, pauses when the slide is left, and pauses or resumes on click. All of
that comes from the deck's shared video script (slides/04-kubrick/src/04_place_trailer.py).

The caption replaces the placeholder "[A researcher asks a question; the agent queries the lakehouse on NAIRR
compute and returns a figure.]" with what the recording shows. It does not say "NAIRR compute": the run is in the
Claude app on the speaker's computer, reading the data over WebDAV. It does not say "figure" either: the agent
returns a ranked table and a written answer. See claims.yaml c1. Idempotent.

    uv run python slides/30-demo-3-question-to-result/src/03_place_video.py [path/to/recording.webm]
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
DECK = HERE.parents[1] / "talk" / "deck.html"
VIDEO = HERE / "data" / "media" / "neon_beetle_seg_demo_1.5x.webm"
POSTER = HERE / "figures" / "poster.webp"
POSTER_AT = 3  # seconds (video time): the question on screen
MARK = 'data-evidence="demo-3-question-to-result"'
OLD_CAPTION = "[A researcher asks a question; the agent queries the lakehouse on NAIRR compute and returns a figure.]"
CAPTION = ("A researcher asks which ground beetle is most common at NEON’s Jornada site. The agent queries the "
           "neon-beetle-seg lakehouse, read-only, and answers with a ranked table: Tetragonoderus pallidus, 58%.")
OLD_LENGTH = "Target length ~2:00"
LENGTH = "Played at 1.5× · 2:10"
ARIA = ("Recorded demo, 2 minutes 10 seconds at 1.5 times speed, no sound. In the Claude app, a researcher asks which "
        "ground beetle is most common at the Jornada Experimental Range. The agent reads the neon-beetle-seg DuckLake "
        "read-only over WebDAV while the MESA portal shows the collection, its lakehouse, a specimen page and its "
        "ontology metadata; the agent answers Tetragonoderus pallidus, 616 of 1,056 carabid individuals (58.3%).")
NOTES = (
    "[~2.5 min] Recorded at normal speed, played at 1.5× (2:10), no sound: talk over it, and click the "
    "video to pause. "
    "0:00 In the Claude app, in a workspace for the collection, the question: query the neon-beetle-seg DuckLake "
    "directly with the DuckDB CLI, read-only over WebDAV without downloading the lake, and answer: what is the most "
    "common ground beetle at the Jornada Experimental Range (JORN)? "
    "0:15 The agent plans five steps: check DuckDB and the lake layout, attach the lake read-only, inspect the "
    "neon_sorting schema, run the JORN carabid ranking, check family/genus and subspecies splits. "
    "Meanwhile (from 0:05) the MESA portal shows the collection, its DuckLake (a SQL browser on beetles.ducklake), the "
    "project's results on GitHub, and a specimen page with its measurements in millimetres. "
    "1:00 The collection's metadata in the Ontology Explorer: 39 ontology-namespaced AVUs, including the Coleoptera "
    "Anatomy Ontology (COLAO) terms, e.g. elytron, linked to the 2018 Zooniverse elytra annotations. "
    "2:00 The agent's data checks (provisional vs released records, repeated sample/taxon pairs, records not "
    "identified to species); 2:05 the answer: Tetragonoderus pallidus, 616 of 1,056 carabid individuals (58.3%) in "
    "417 of 732 records, 2015-05-28 to 2025-09-10, and the ranked table. "
    "The point: a researcher's question, answered from the data where it lives, with the checks shown. "
    "Runs on the speaker's computer against the CyVerse Data Store; not NAIRR compute. "
    "Recording: data/media/MANIFEST.yaml in slides/30-demo-3-question-to-result."
)
FRAME_RE = re.compile(r'<div data-node-path="0" style="display: flex; flex-direction: column; align-items: center; '
                      r'justify-content: center; gap: 24px; min-width: 1120px;.*?Recorded clip goes here</div></div>', re.S)
VIDEO_RE = re.compile(rf'<div data-node-path="0" data-evidence-frame="1"[^>]*><video [^>]*{re.escape(MARK)}[^>]*></video></div>')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(src: Path | None) -> None:
    """Copy the speaker's WebM in (if given), make the poster and write the manifest."""
    if src is not None:
        VIDEO.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, VIDEO)
    POSTER.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(POSTER_AT), "-i", str(VIDEO), "-frames:v", "1",
                    "-c:v", "libwebp", "-quality", "85", str(POSTER)], check=True)
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height",
                                      "-of", "json", str(VIDEO)], capture_output=True, text=True, check=True).stdout)
    entry = {
        "title": "Demo 3: from question to result (most common ground beetle at NEON JORN, neon-beetle-seg DuckLake)",
        "source": "Screen recording by the speaker (Tyson Swetnam), 2026-11-02; sped up 1.5x and converted to VP9 WebM by the speaker",
        "original_upload": src.name if src else "(unchanged)",
        "bytes": VIDEO.stat().st_size,
        "sha256": sha256(VIDEO),
        "duration_s": round(float(info["format"]["duration"]), 2),
        "streams": info["streams"],
        "processing": "none in this repository (used as supplied)",
        "poster": f"figures/{POSTER.name} (frame at {POSTER_AT} s)",
    }
    (VIDEO.parent / "MANIFEST.yaml").write_text(yaml.safe_dump({VIDEO.name: entry}, sort_keys=False, allow_unicode=True))


def video_frame() -> str:
    src = "data:video/webm;base64," + base64.b64encode(VIDEO.read_bytes()).decode()
    poster = "data:image/webp;base64," + base64.b64encode(POSTER.read_bytes()).decode()
    return (f'<div data-node-path="0" data-evidence-frame="1" style="width: 1120px; height: 630px; min-width: 1120px; '
            f'max-width: 1120px; box-sizing: border-box; background: rgb(0, 0, 0);">'
            f'<video {MARK} autoplay muted playsinline preload="auto" aria-label="{escape(ARIA)}" poster="{poster}" src="{src}" '
            f'style="display: block; width: 100%; height: 100%; object-fit: contain; cursor: pointer;"></video></div>')


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if src is None and not VIDEO.exists():
        print("pass the recording's path on the first run", file=sys.stderr)
        return 1
    if src is not None or not POSTER.exists():
        prepare(src)
    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*data-label="From question to result"', html).start()
    end = html.index("</section>", start)
    slide = html[start:end]
    m = FRAME_RE.search(slide) or VIDEO_RE.search(slide)
    if not m:
        print("slide 30: placeholder frame not found", file=sys.stderr)
        return 1
    slide = slide[: m.start()] + video_frame() + slide[m.end() :]
    slide = slide.replace(escape(OLD_CAPTION, quote=False), escape(CAPTION, quote=False))
    for old in (OLD_LENGTH, "Recorded · played at 1.5× · 2:10"):  # placeholder, then an earlier wording of this line
        slide = slide.replace(old, LENGTH)
    slide = re.sub(r'data-speaker-notes="[^"]*"', f'data-speaker-notes="{escape(NOTES)}"', slide, count=1)
    DECK.write_text(html[:start] + slide + html[end:], encoding="utf-8")
    print(f"slide 30: video placed ({VIDEO.stat().st_size / 1e6:.1f} MB), caption and notes updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
