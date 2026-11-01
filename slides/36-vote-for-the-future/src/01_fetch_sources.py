"""Slide 36: fetch the primary sources quoted on the slide and in its notes.

Each page is saved under data/raw/sources/ (not committed; the MANIFEST.yaml there is) with its URL, date and
SHA-256. X posts are read through X's public oEmbed endpoint (publish.twitter.com), which needs no login; Bluesky
posts through the public AppView API. Pages behind a bot check (science.org) are not fetched: only the DOI
metadata for Nelson's Science essay is used. Re-run with --refresh to download again.

    uv run python slides/36-vote-for-the-future/src/01_fetch_sources.py [--refresh]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from evidence.fetch import record  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
OUT = HERE / "data" / "raw" / "sources"
BSKY = "https://public.api.bsky.app/xrpc"
NELSON = "alondra.bsky.social"
NELSON_POSTS = ["3mltfqoc7ok2y", "3mltg2efhms2a", "3mltg4ldq2s2a", "3mltg6wjt6k2a", "3mltgdi6no22a", "3mltgmmxldc2c", "3mwxxzq3zkk2u"]
PONTIFEX = ["2116146977230459383", "2090763999075868746", "2058888313029685400", "2059235600230711574"]

# file name -> (url, Accept header or None, source description)
PAGES = {
    "blueprint.html": ("https://bidenwhitehouse.archives.gov/ostp/ai-bill-of-rights/", None,
                       "White House OSTP, Blueprint for an AI Bill of Rights (archived)"),
    "blueprint_about.html": ("https://bidenwhitehouse.archives.gov/ostp/ai-bill-of-rights/about-this-document/", None,
                             "White House OSTP, Blueprint: About this document (archived)"),
    "blueprint_release.html": ("https://bidenwhitehouse.archives.gov/ostp/news-updates/2022/10/04/blueprint-for-an-ai-bill-of-rightsa-vision-for-protecting-our-civil-rights-in-the-algorithmic-age/",
                               None, "OSTP release post, 4 Oct 2022 (archived)"),
    "eo14110.htm": ("https://www.govinfo.gov/content/pkg/FR-2023-11-01/html/2023-24283.htm", None,
                    "Federal Register: EO 14110 (30 Oct 2023)"),
    "eo14148.htm": ("https://www.govinfo.gov/content/pkg/FR-2025-01-28/html/2025-01901.htm", None,
                    "Federal Register: EO 14148 (20 Jan 2025)"),
    "nelson_science_csl.json": ("https://doi.org/10.1126/science.aeh7153", "application/vnd.citationstyles.csl+json",
                                "doi.org CSL-JSON for Nelson, A civic grammar for AI rights, Science (2026)"),
    "magnifica_humanitas.html": ("https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html",
                                 None, "Holy See: Magnifica Humanitas (Leo XIV, 15 May 2026)"),
    "vaticannews_announcement.html": ("https://www.vaticannews.va/en/pope/news/2026-05/pope-leo-xiv-first-encyclical-magnifica-humanitas.html",
                                      None, "Vatican News announcement of Magnifica Humanitas"),
    "leo_20261030_address.html": ("https://www.vatican.va/content/leo-xiv/en/speeches/2026/october/documents/20261030-incontro-pav.html",
                                  None, "Holy See: Leo XIV address, The Future of AI dialogue, 30 Oct 2026"),
    "nm_sos_voting.html": ("https://www.sos.nm.gov/voting-and-elections/", None,
                           "New Mexico Secretary of State: Voting & Elections"),
}


def get(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": UA, **({"Accept": accept} if accept else {})}
    r = requests.get(url, headers=headers, timeout=120)
    r.raise_for_status()
    time.sleep(0.5)
    return r.content


def save(name: str, url: str, accept: str | None, source: str, refresh: bool) -> None:
    dest = OUT / name
    if dest.exists() and not refresh:
        return
    try:
        dest.write_bytes(get(url, accept))
    except requests.HTTPError as e:
        print(f"skip {name}: {e}", file=sys.stderr)
        return
    record(dest, url=url, source=source)
    print(f"saved {name}")


def main() -> int:
    refresh = "--refresh" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (url, accept, source) in PAGES.items():
        save(name, url, accept, source, refresh)
    did = json.loads(get(f"{BSKY}/com.atproto.identity.resolveHandle?handle={NELSON}"))["did"]
    uris = "&".join(f"uris={quote(f'at://{did}/app.bsky.feed.post/{p}')}" for p in NELSON_POSTS)
    save("nelson_bluesky_posts.json", f"{BSKY}/app.bsky.feed.getPosts?{uris}", None,
         f"Bluesky public API: posts by @{NELSON} ({did})", refresh)
    for sid in PONTIFEX:
        post = f"https://x.com/Pontifex/status/{sid}"
        save(f"pontifex_{sid}.json", f"https://publish.twitter.com/oembed?omit_script=1&url={quote(post, safe='')}", None,
             f"X oEmbed for {post}", refresh)
    return 0


if __name__ == "__main__":
    sys.exit(main())
