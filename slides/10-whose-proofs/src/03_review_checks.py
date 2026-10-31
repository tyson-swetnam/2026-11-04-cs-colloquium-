"""Slide 10 review follow-up: dated checks for c2 (signatory count at launch) and c6 (Tao's blog repost).

- Zenodo versions API for the Fields Medalists declaration: how many versions, dates, creator counts.
- WordPress.com public API for terrytao.wordpress.com, 1-15 Oct 2026: is the AHM statement reposted, and
  how many other guest posts appear (context for "endorsed" vs "reshared").
Writes data/processed/review_checks.json.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from evidence.http import CachedGet  # noqa: E402

get = CachedGet(HERE / "data" / "cache", "colloquium-evidence/0.1 (UNM CARC research)")
out: dict = {}

st, body = get("https://zenodo.org/api/records/22737751/versions")
hits = json.loads(body)["hits"]
out["zenodo_versions"] = {
    "status": st,
    "total": hits["total"],
    "versions": [
        {"id": h["id"], "publication_date": h["metadata"]["publication_date"], "n_creators": len(h["metadata"]["creators"])}
        for h in hits["hits"]
    ],
}

st, body = get(
    "https://public-api.wordpress.com/rest/v1.1/sites/terrytao.wordpress.com/posts/"
    "?after=2026-10-01T00:00:00&before=2026-10-15T00:00:00&number=30&fields=date,title,URL,excerpt"
)
posts = json.loads(body)["posts"]
rows = []
for p in posts:
    ex = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", p["excerpt"]))).strip()
    m = re.search(r"guest post by ([^,.\]]+?)(?:,| being| cross| reposted|\.)", ex)
    rows.append({"date": p["date"], "title": html.unescape(p["title"]), "url": p["URL"], "guest_author": m.group(1).strip() if m else None})
ahm = [r for r in rows if "AHM" in r["title"]]
out["tao_blog_oct1_15"] = {
    "status": st,
    "n_posts": len(rows),
    "n_guest_posts": sum(r["guest_author"] is not None for r in rows),
    "ahm_post": ahm,
    "posts": rows,
}

dest = HERE / "data" / "processed" / "review_checks.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: (v if k == "zenodo_versions" else {kk: vv for kk, vv in v.items() if kk != "posts"}) for k, v in out.items()}, indent=2, ensure_ascii=False))
