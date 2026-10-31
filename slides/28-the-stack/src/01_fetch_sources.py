"""Fetch the documents behind slide 28 and log them in data/raw/sources/MANIFEST.yaml.

Also extracts the slide-28 figure (and its alt text) from talk/deck.html so the layer list
can be checked against the figure itself.

Run from the repo root:  uv run python slides/28-the-stack/src/01_fetch_sources.py
"""
from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))

from evidence.fetch import record  # noqa: E402
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
SRC = HERE / "data/raw/sources"
OUT = HERE / "data/processed"

# (local file, url, publisher/source label)
DOCS = [
    ("nsf_award_2632685.json", "https://api.nsf.gov/services/v1/awards/2632685.json"
     "?printFields=id,title,abstractText,fundProgramName,startDate,expDate,awardeeName,piFirstName,piLastName",
     "NSF Award API"),
    ("mesa_docs_llms-full.txt", "https://idss-mesa.github.io/docs/llms-full.txt", "MESA public docs (developer-published)"),
    ("mesa_stack.html", "https://idss-mesa.github.io/stack.html", "MESA public site (developer-published)"),
    ("ducklake_select.html", "https://ducklake.select/", "DuckDB Foundation / DuckLake"),
    ("irods_license.html", "https://irods.org/license/", "iRODS Consortium"),
    ("lustre_org.html", "https://www.lustre.org/", "OpenSFS / lustre.org"),
    ("vast_eula.html", "https://www.vastdata.com/legal/end-user-services-and-license-agreement", "VAST Data"),
    ("aws_s3_api_welcome.html", "https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html", "Amazon Web Services"),
    ("osn_home.html", "https://www.openstoragenetwork.org/", "Open Storage Network"),
    ("claude_code_legal.html", "https://code.claude.com/docs/en/legal-and-compliance", "Anthropic"),
]


def main() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    get = CachedGet(HERE / "data/cache", UA)
    status = {}
    for fn, url, source in DOCS:
        code, body = get(url)
        status[url] = code
        if code == 200:
            (SRC / fn).write_text(body, encoding="utf-8")
            record(SRC / fn, url=url, source=source, note="fetched by src/01_fetch_sources.py")
        print(code, url)

    # NSF award: keep a compact processed copy.
    award = json.loads((SRC / "nsf_award_2632685.json").read_text())["response"]["award"][0]
    for k in ("pi", "piEmail", "poEmail", "poPhone", "awardeePhone"):  # contact details not needed
        award.pop(k, None)
    (OUT / "nsf_award_2632685.json").write_text(json.dumps(award, indent=2))

    # Slide 28 figure and alt text, straight from the deck.
    deck = (REPO / "talk/deck.html").read_text(encoding="utf-8")
    start = deck.find('<section class="deck-slide" id="28"')
    end = deck.find("</section>", start)
    sec = deck[start:end]
    alt = re.search(r'alt="([^"]+)"', sec).group(1)
    png = re.search(r'src="data:image/png;base64,([^"]+)"', sec).group(1)
    (SRC / "slide28_figure.png").write_bytes(base64.b64decode(png))
    record(SRC / "slide28_figure.png", url="talk/deck.html#28", source="Speaker's deck (MESA proposal figure)",
           note="extracted from the embedded data URI")
    notes = re.search(r'data-speaker-notes="([^"]+)"', sec).group(1)
    (OUT / "deck_slide28.json").write_text(json.dumps({"alt": alt, "speaker_notes": notes,
                                                       "fetch_status": status}, indent=2))


if __name__ == "__main__":
    main()
