"""Try an anonymous (no-credential) read of a public CyVerse Data Store collection over WebDAV.

Records the HTTP outcome. If CyVerse's anti-crawler IP block answers instead, we stop there:
the block page has a CAPTCHA (Cloudflare Turnstile) and we do not try to pass it.
"""
import json
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "data/processed/anon_read.json"
UA = "colloquium-evidence/0.1 (UNM CARC research)"
URLS = [
    "https://data.cyverse.org/dav-anon/iplant/home/shared/",
    "https://data.cyverse.org/dav-anon/iplant/commons/community_released/",
]

if __name__ == "__main__":
    rows = []
    for url in URLS:
        # No redirects followed, so we see the raw answer; no credentials sent.
        r = requests.get(url, headers={"User-Agent": UA}, timeout=60, allow_redirects=False)
        loc = r.headers.get("location", "")
        rows.append({
            "url": url,
            "status": r.status_code,
            "location": loc,
            "blocked_by_ip_challenge": "unblockme.cyverse.org" in loc,
            "bytes": len(r.content),
            "body_start": r.text[:300],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"retrieved": "2026-10-31", "user_agent": UA, "results": rows}, indent=2))
    print(json.dumps(rows, indent=2)[:1500])
