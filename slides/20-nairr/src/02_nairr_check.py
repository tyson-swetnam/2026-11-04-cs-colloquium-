"""Slide 20: NAIRR facts from NSF award records and saved NAIRR/NSF pages.

1. Pulls NSF Award API records for the NAIRR Operations Center (2616251), FabAID (2609485),
   Sagebrush (2537075) and MESA (2632685), and runs two keyword searches ("National Inference
   Service", "NAIRR Operations Center"). Contact fields are dropped.
2. Checks that every quote in data/raw/research/facts.csv occurs, word for word (whitespace
   normalised), in the saved copy of its source: a page under data/raw/sources/ (as text, tags
   stripped) or the raw API response.
3. Computes the project counts each source reports, for claim c4.

Outputs: data/raw/nsf_award_<id>.json, data/processed/nairr_awards.csv,
data/processed/keyword_search.csv, data/processed/quote_check.csv, data/processed/project_counts.csv
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
API = "https://api.nsf.gov/services/v1/awards"
AWARDS = ["2616251", "2609485", "2537075", "2632685"]
FIELDS = "id,title,awardeeName,startDate,expDate,date,estimatedTotalAmt,fundProgramName,program,pdPIName,transType,abstractText"
DROP = {"piEmail", "pi", "poEmail", "poPhone", "awardeePhone", "coPDPI"}
SOURCES = SLIDE / "data" / "raw" / "sources"

# URL in facts.csv -> saved page
PAGES = {
    "https://nairrpilot.org/": "nairrpilot.html",
    "https://nairrpilot.org/help/faq": "nairr_faq.html",
    "https://nairrpilot.org/opportunities/startup-project": "nairr_startup.html",
    "https://nairrpilot.org/opportunities/allocations": "nairr_allocations.html",
    "https://www.nsf.gov/cise/updates/nsf-establishes-operations-center-national-artificial": "nsf_ops_center.html",
    "https://www.nsf.gov/focus-areas/ai/nairr": "nsf_nairr.html",
    "https://www.nsf.gov/news/democratizing-future-ai-rd-nsf-launch-national-ai": "nsf_pilot_launch_2024.html",
    "https://www.nsf.gov/news/nsf-announces-83m-investment-integrated-data-systems": "nsf_idss_83m.html",
    "https://www.nsf.gov/cise/updates/nairr-2-years-advancing-american-artificial-intelligence": "nsf_nairr_2yrs.html",
    "https://docs.jetstream-cloud.org/alloc/overview/": "js2_alloc_overview.html",
    "https://docs.jetstream-cloud.org/inference-service/overview/": "js2_inference.html",
    "https://nrp.ai/": "nrp_home.html",
    "https://idss-mesa.github.io/": "mesa_site.html",
}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def page_text(path: Path) -> str:
    t = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?s)<(script|style).*?</\1>", "", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return norm(html.unescape(t))


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache", UA)
    raw, out = SLIDE / "data" / "raw", SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    api_bodies: dict[str, str] = {}

    rows = []
    for award in AWARDS:
        url = f"{API}/{award}.json?printFields={FIELDS}"
        status, body = get(url)
        api_bodies[f"{API}/{award}.json"] = body
        rec = {k: v for k, v in json.loads(body)["response"]["award"][0].items() if k not in DROP}
        (raw / f"nsf_award_{award}.json").write_text(json.dumps(rec, indent=2))
        rows.append({k: rec.get(k) for k in ("id", "title", "awardeeName", "fundProgramName", "startDate", "expDate", "estimatedTotalAmt", "transType")})
    awards = pd.DataFrame(rows)
    awards.to_csv(out / "nairr_awards.csv", index=False)
    print(awards.to_string(index=False, max_colwidth=50))

    hits = []
    for kw in ['"National Inference Service"', '"NAIRR Operations Center"', '"Deep Inference Fabric"']:
        url = f"{API}.json?keyword={kw.replace(' ', '%20').replace(chr(34), '%22')}&printFields=id,title,awardeeName,startDate"
        status, body = get(url)
        d = json.loads(body)["response"]
        hits.append({"keyword": kw, "status": status, "total": len(d.get("award", [])),
                     "ids_titles": "; ".join(f"{a['id']} {a['title'][:70]}" for a in d.get("award", []))})
    kws = pd.DataFrame(hits)
    kws.to_csv(out / "keyword_search.csv", index=False)
    print(kws.to_string(index=False, max_colwidth=90))

    facts = pd.read_csv(SLIDE / "data" / "raw" / "research" / "facts.csv", dtype=str).fillna("")
    texts: dict[str, str] = {}
    checks = []
    for f in facts.itertuples():
        if f.url in PAGES:
            name = PAGES[f.url]
            texts.setdefault(name, page_text(SOURCES / name))
            hay = texts[name]
        else:
            base = f.url.split("?")[0]
            hay = norm(api_bodies.get(base, ""))
        checks.append({"id": f.id, "claim_id": f.claim_id, "found": norm(f.quote) in hay, "url": f.url})
    chk = pd.DataFrame(checks)
    chk.to_csv(out / "quote_check.csv", index=False)
    print(chk.to_string(index=False))
    if not chk.found.all():
        raise SystemExit(f"quotes not found: {list(chk[~chk.found].id)}")

    pats = {
        "nairrpilot.org home": ("nairrpilot.html", r"(\d[\d,]*) Research projects supported"),
        "NSF NAIRR-OC announcement (2026-09-01)": ("nsf_ops_center.html", r"supported over (\d[\d,]*) research projects"),
        "NSF NAIRR focus-area page": ("nsf_nairr.html", r"supporting more than (\d[\d,]*) research projects"),
    }
    counts = []
    for label, (name, pat) in pats.items():
        m = re.search(pat, page_text(SOURCES / name))
        n = int(m.group(1).replace(",", "")) if m else None
        counts.append({"source": label, "projects": n, "meets_940_plus": bool(n and n >= 940)})
    cdf = pd.DataFrame(counts)
    cdf.to_csv(out / "project_counts.csv", index=False)
    print(cdf.to_string(index=False))


if __name__ == "__main__":
    main()
