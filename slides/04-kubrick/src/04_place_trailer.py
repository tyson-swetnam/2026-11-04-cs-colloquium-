"""Slide 4: play the Dr. Strangelove trailer (public domain in the US, via Wikimedia Commons), muted and looping.

The exported deck keeps the War Room still as the tinted background and leaves an empty black box beside
the poster where the trailer belongs. This script puts a <video autoplay muted loop playsinline> in that box,
keeping its size, border and shadow, with the War Room still (a frame of the trailer) as the poster image.
The trailer is embedded as a data: URL, so the deck plays offline and within its Content-Security-Policy
(media-src data: blob:). A small inline script restarts the trailer from the beginning whenever slide 4 comes
into view and pauses it when the slide is left. Idempotent: re-run after a re-export.

    uv run python slides/04-kubrick/src/04_place_trailer.py [path/to/trailer.webm]
"""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path

SLIDE = Path(__file__).resolve().parents[1]
DECK = SLIDE.parents[1] / "talk" / "deck.html"
TRAILER = SLIDE / "data" / "media" / "dr_strangelove_trailer.webm"
STILL_ALT = "The War Room in Dr. Strangelove"
MARK = 'data-evidence="strangelove-trailer"'
PLACEHOLDER = r'<div data-img-path="[^"]*" data-node-path="[^"]*" aria-hidden="true" style="[^"]*background-color: rgb\(0, 0, 0\);[^"]*"></div>'
RESTART = """<script data-evidence="video-restart">
(() => {
  // The deck keeps every slide in the DOM and marks the current one by removing aria-hidden/inert.
  // Restart each evidence video from the beginning when its slide becomes current; pause it when the slide is left.
  const sync = (section) => {
    const active = section.getAttribute('aria-hidden') !== 'true' && !section.inert;
    section.querySelectorAll('video[data-evidence]').forEach((v) => {
      if (active && !section.dataset.videoActive) { v.muted = true; v.currentTime = 0; v.play().catch(() => {}); }
      if (!active) v.pause();
    });
    if (active) section.dataset.videoActive = '1'; else delete section.dataset.videoActive;
  };
  const watch = () => document.querySelectorAll('video[data-evidence]').forEach((v) => {
    const section = v.closest('section.deck-slide');
    if (!section || section.dataset.videoWatched) return;
    section.dataset.videoWatched = '1';
    new MutationObserver(() => sync(section)).observe(section, { attributes: true, attributeFilter: ['aria-hidden', 'inert'] });
    sync(section);
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watch); else watch();
})();
</script>"""


def main() -> int:
    trailer = Path(sys.argv[1]) if len(sys.argv) > 1 else TRAILER
    html = DECK.read_text(encoding="utf-8")
    start = re.search(r'<section [^>]*\bid="4"', html).start()
    end = html.index("</section>", start)
    slide = html[start:end]
    src = "data:video/webm;base64," + base64.b64encode(trailer.read_bytes()).decode()

    existing = re.search(r"<video [^>]*" + re.escape(MARK) + r"[^>]*>\s*</video>", slide)
    if existing:  # already placed: refresh the video data only
        slide = slide.replace(existing.group(0), re.sub(r'src="data:video[^"]*"', f'src="{src}"', existing.group(0)))
    else:
        box = re.search(PLACEHOLDER, slide)
        still = re.search(r'<img [^>]*alt="(' + re.escape(STILL_ALT) + r'[^"]*)"[^>]*src="(data:image[^"]*)"', slide)
        if not box or not still:
            print("placeholder box or War Room still not found on slide 4; deck layout changed", file=sys.stderr)
            return 1
        style = re.search(r'style="([^"]*)"', box.group(0)).group(1) + " object-fit: cover;"
        video = (
            f'<video {MARK} autoplay muted loop playsinline preload="auto" '
            f'aria-label="Dr. Strangelove trailer (1964), muted, opening on {still.group(1)}" '
            f'poster="{still.group(2)}" src="{src}" style="{style}"></video>'
        )
        slide = slide.replace(box.group(0), video)
    html = html[:start] + slide + html[end:]
    html = re.sub(r'<script data-evidence="video-restart">.*?</script>\n?', "", html, flags=re.S)
    html = html.replace("</body>", RESTART + "\n</body>", 1)
    DECK.write_text(html, encoding="utf-8")
    print(f"trailer on slide 4: {trailer.stat().st_size / 1e6:.1f} MB embedded; deck is now {DECK.stat().st_size / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
