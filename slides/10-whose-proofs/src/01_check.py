"""Slide 10: recompute the countable parts of the claims from public sources.

- Fields Medalist signatories: Zenodo record (as published 2026-09-11) vs mathandai.org (live).
- openai/math README + history.md (public raw files): manuscript, family and Lean counts.
- Tao's public Mastodon timeline (statuses incl. reblogs): any reshare of the AHM statement.
Writes data/processed/checks.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from evidence.http import CachedGet  # noqa: E402

get = CachedGet(HERE / "data" / "cache", "colloquium-evidence/0.1 (UNM CARC research)")
out: dict = {}

# 1. Fields Medalists
st, body = get("https://zenodo.org/api/records/22737751")
rec = json.loads(body)
out["zenodo_record"] = {
    "id": rec["id"],
    "title": rec["metadata"]["title"],
    "publication_date": rec["metadata"]["publication_date"],
    "created": rec["created"],
    "n_creators": len(rec["metadata"]["creators"]),
}
st, page = get("https://mathandai.org/")
names = re.findall(r"\(Fields Medal (\d{4})\)", re.sub(r"<[^>]+>", " ", page))
out["mathandai_signatories"] = len(names)
z = {c["name"].split(",")[0].strip() for c in rec["metadata"]["creators"]}
text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page))
live = re.findall(r"([A-Z][\wÀ-ỹ'-]+(?: [A-Z][\wÀ-ỹ'-]+)*) \(Fields Medal \d{4}\)", text)
out["added_after_zenodo"] = sorted(n for n in live if not any(s in n for s in z))

# 2. openai/math counts
st, readme = get("https://raw.githubusercontent.com/openai/math/main/README.md")
st, hist = get("https://raw.githubusercontent.com/openai/math/main/history.md")
m = re.search(r"contains (\d+) manuscripts organized into (\d+) families", readme)
out["readme_now"] = {"manuscripts": int(m.group(1)), "families": int(m.group(2))}
f = re.search(r"(\d+) / (\d+) = ~(\d+)%", hist)
num, den = int(f.group(1)), int(f.group(2))
out["lean_top_line_oct7"] = {"formalized": num, "total": den, "pct": round(100 * num / den, 1)}
withdrawn = len(re.findall(r"^- (Algebraicity|The rational Hodge conjecture for products)", hist, re.M))
added_oct26 = 2
out["manuscript_arithmetic"] = {
    "released": 722, "withdrawn_oct7": withdrawn, "added_oct26": added_oct26,
    "expected_now": 722 - withdrawn + added_oct26, "readme_now": out["readme_now"]["manuscripts"],
}
out["revised_oct7"] = int(re.search(r"revised (\d+) other manuscripts", hist).group(1))

# 3. Tao Mastodon reshare of AHM statement (Oct 6-8 window)
st, acct = get("https://mathstodon.xyz/api/v1/accounts/lookup?acct=tao")
aid = json.loads(acct)["id"]
st, sts = get(f"https://mathstodon.xyz/api/v1/accounts/{aid}/statuses?limit=40")
sts = json.loads(sts)
hits = []
for s in sts:
    r = s.get("reblog")
    c = (r or s)["content"]
    if re.search(r"Human Mathematics|ahmath\.org|\bAHM\b", c):
        hits.append(s["url"])
out["tao_mastodon"] = {
    "statuses_checked": len(sts),
    "oldest": sts[-1]["created_at"], "newest": sts[0]["created_at"],
    "reblogs": sum(1 for s in sts if s.get("reblog")),
    "ahm_mentions": hits,
}

dest = HERE / "data" / "processed" / "checks.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(json.dumps(out, indent=2, ensure_ascii=False))
