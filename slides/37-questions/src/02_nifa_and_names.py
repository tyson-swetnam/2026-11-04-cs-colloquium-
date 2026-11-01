"""Slide 37: fetch (NIFA crisprojectpages returns 404 and the enterprise-search page is JavaScript-only; aiinstitutes.org returns 403 and is not pursued) the USDA NIFA project record for AIIRA and center home pages (names used in notes)."""
import re, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT))
from evidence.http import CachedGet
from evidence.fetch import record
HERE = Path(__file__).resolve().parents[1]
RAW = HERE / "data/raw/sources"
get = CachedGet(HERE / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
SRC = {
 "nifa_1027030.html": "https://portal.nifa.usda.gov/web/crisprojectpages/1027030-ai-institute-aiira-ai-institute-for-resilient-agriculture.html",
 "nifa_enterprise_1027030.html": "https://portal.nifa.usda.gov/enterprise-search/projects/1027030",
 "aiinstitutes_aiira.html": "https://aiinstitutes.org/institute-aiira/",
 "aiira_home.html": "https://aiira.iastate.edu/",
 "isu_research_aiira_news.html": "https://research.iastate.edu/?p=8706",
 "mesa_llms_full.txt": "https://idss-mesa.github.io/llms-full.txt",
 "esiil_home.html": "https://esiil.org/",
}
out = {}
for name, url in SRC.items():
    try:
        st, body = get(url)
    except Exception as e:
        st, body = f"error {type(e).__name__}", ""
    out[name] = st
    if st == 200:
        (RAW / name).write_text(body); record(RAW / name, url=url, source=url.split("/")[2], note="slide 34")
        (RAW / (name + ".txt")).write_text(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", " ", body))))
(HERE / "data/processed/fetch_status_02.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
