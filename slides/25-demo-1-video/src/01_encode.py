"""Slide 25: convert the speaker's screen recording of Demo 1 for the deck.

Input: the QuickTime recording the speaker supplied (2026-11-02), 1280x700 H.264, 87.8 s, no audio track.
Output: data/media/formation_irods_mcp_demo.webm (VP9, CRF 30, no audio, about 1.5 MB), plus
figures/poster.webp (the frame at 35 s, shown before playback starts). VP9 WebM is what the deck already uses
for the slide 4 trailer, and it embeds as a data: URL within the deck's Content-Security-Policy. At CRF 30 the
terminal text is as legible as the source (checked frame by frame at 60 s). The recording itself is not committed;
data/media/MANIFEST.yaml records its size, SHA-256 and the exact ffmpeg command.

    uv run python slides/25-demo-1-video/src/01_encode.py path/to/formation_irods_mcp_demo_720p.mov
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "data" / "media" / "formation_irods_mcp_demo.webm"
POSTER = HERE / "figures" / "poster.webp"
POSTER_AT = 35  # seconds: the first Formation answer is on screen
CMD = ["ffmpeg", "-v", "error", "-y", "-i", "{src}", "-an", "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0",
       "-deadline", "good", "-cpu-used", "2", "-row-mt", "1", "-tile-columns", "2", "-pix_fmt", "yuv420p", "{out}"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    src = Path(sys.argv[1])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    POSTER.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([a.format(src=src, out=OUT) for a in CMD], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(POSTER_AT), "-i", str(src), "-frames:v", "1",
                    "-c:v", "libwebp", "-quality", "85", str(POSTER)], check=True)
    info_in, info_out = probe(src), probe(OUT)
    manifest = {
        OUT.name: {
            "title": "Demo 1: Claude Code with MESA's Formation and iRODS (Data Store) MCP servers",
            "source": "Screen recording supplied by the speaker (Tyson Swetnam), 2026-11-02",
            "original": {"file": src.name, "bytes": src.stat().st_size, "sha256": sha256(src),
                         "duration_s": round(float(info_in["format"]["duration"]), 2),
                         "streams": [{k: s.get(k) for k in ("codec_type", "codec_name", "width", "height")} for s in info_in["streams"]]},
            "processing": " ".join(CMD).replace("{src}", "<original>").replace("{out}", OUT.name),
            "bytes": OUT.stat().st_size,
            "sha256": sha256(OUT),
            "duration_s": round(float(info_out["format"]["duration"]), 2),
            "poster": f"figures/{POSTER.name} (frame at {POSTER_AT} s)",
        }
    }
    (OUT.parent / "MANIFEST.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True))
    print(f"wrote {OUT.relative_to(HERE)} ({OUT.stat().st_size / 1e6:.1f} MB) and {POSTER.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
