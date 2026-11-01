"""Slide 37: fetch NSF Award API records for every NSF number on the slide, the NIFA award
record, and link-check the MESA site and GitHub org. Writes data/processed/awards.json."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evidence.http import CachedGet
from evidence.fetch import record

HERE = Path(__file__).resolve().parents[1]
RAW = HERE / "data/raw/sources"; RAW.mkdir(parents=True, exist_ok=True)
OUT = HERE / "data/processed"; OUT.mkdir(parents=True, exist_ok=True)
get = CachedGet(HERE / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")

F = ("id,title,awardeeName,awardeeCity,awardeeStateCode,pdPIName,coPDPI,startDate,expDate,"
     "fundProgramName,primaryProgram,agency,awardAgencyCode,fundAgencyCode,estimatedTotalAmt,"
     "fundsObligatedAmt,transType,orgLongName,orgLongName2,abstractText")
NSF = ["2632685", "2217817", "2153040", "2335029", "2438843", "2535855"]
summary = {}
for a in NSF:
    url = f"https://api.nsf.gov/services/v1/awards/{a}.json?printFields={F}"
    st, body = get(url)
    p = RAW / f"nsf_award_{a}.json"; p.write_text(body)
    record(p, url=url, source="api.nsf.gov", note="slide 34 acknowledgments")
    aw = (json.loads(body).get("response", {}).get("award") or [{}])[0] if st == 200 else {}
    summary[a] = {k: aw.get(k) for k in F.split(",") if k != "abstractText"} | {"http": st}

# Awards co-funded by NSF for AIIRA (NSF-NIFA AI institutes): search NSF for AIIRA
st, body = get(f"https://api.nsf.gov/services/v1/awards.json?keyword=AIIRA&printFields={F}")
(RAW / "nsf_search_AIIRA.json").write_text(body)
record(RAW / "nsf_search_AIIRA.json", url="https://api.nsf.gov/services/v1/awards.json?keyword=AIIRA", source="api.nsf.gov", note="slide 34")
summary["search_AIIRA"] = [{k: x.get(k) for k in ("id", "title", "awardeeName", "agency")}
                            for x in json.loads(body).get("response", {}).get("award", [])] if st == 200 else st

links = {}
for name, url in {"mesa_site.html": "https://idss-mesa.github.io/",
                  "github_org_api.json": "https://api.github.com/orgs/idss-mesa",
                  "github_org.html": "https://github.com/idss-mesa"}.items():
    try:
        st, body = get(url)
    except Exception as e:
        st, body = f"error {type(e).__name__}", ""
    links[url] = st
    if st == 200:
        (RAW / name).write_text(body); record(RAW / name, url=url, source=url.split("/")[2], note="slide 34 link check")
summary["links"] = links
(OUT / "awards.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
