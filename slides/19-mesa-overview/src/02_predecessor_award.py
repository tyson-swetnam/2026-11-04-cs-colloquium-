"""Fetch NSF award 2608717 (MESA at the University of Arizona, predecessor of 2632685)
and a keyword search listing both MESA awards."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evidence.http import CachedGet
from evidence.fetch import record

HERE = Path(__file__).resolve().parents[1]
get = CachedGet(HERE / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
FIELDS = ("id,title,awardeeName,pdPIName,coPDPI,startDate,expDate,fundProgramName,orgLongName2,"
          "estimatedTotalAmt,fundsObligatedAmt,fundsObligated,progEleCode,progRefCode,program,transType,date")
url = f"https://api.nsf.gov/services/v1/awards/2608717.json?printFields={FIELDS}"
status, body = get(url)
assert status == 200, status
out = HERE / "data/raw/sources/nsf_award_2608717.json"
out.write_text(body)
record(out, url=url, source="NSF Award API", note="award 2608717 (MESA, University of Arizona)")
aw = json.loads(body)["response"]["award"][0]
# keep co-PI names (public on the award page) but drop contact fields
aw = {k: v for k, v in aw.items() if k not in ("pi", "piEmail", "poEmail", "poPhone", "awardeePhone")}
aw["coPDPI"] = [" ".join(w for w in x.split() if "@" not in w) for x in aw.get("coPDPI", [])]
(HERE / "data/processed/award_2608717.json").write_text(json.dumps(aw, indent=2))
print(json.dumps({k: v for k, v in aw.items() if k != "abstractText"}, indent=2))

url2 = ("https://api.nsf.gov/services/v1/awards.json?keyword=CyVerse&printFields=id,title,awardeeName,startDate,expDate")
status, body = get(url2)
assert status == 200, status
out2 = HERE / "data/raw/sources/nsf_search_mesa.json"
out2.write_text(body)
record(out2, url=url2, source="NSF Award API", note="keyword search for MESA awards")
hits = [a for a in json.loads(body)["response"].get("award", []) if "MESA" in a["title"]]
(HERE / "data/processed/mesa_awards_search.json").write_text(json.dumps(hits, indent=2))
print(json.dumps(hits, indent=2))
