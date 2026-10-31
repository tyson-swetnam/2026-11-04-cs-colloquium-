"""Fetch NSF award 2632685 from the NSF Award API and save title, PI, program, dates, abstract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evidence.http import CachedGet
from evidence.fetch import record

HERE = Path(__file__).resolve().parents[1]
get = CachedGet(HERE / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
FIELDS = "id,title,awardeeName,pdPIName,coPDPI,startDate,expDate,fundProgramName,orgLongName,orgLongName2,estimatedTotalAmt,fundsObligatedAmt,abstractText,progEleCode,progRefCode"
url = f"https://api.nsf.gov/services/v1/awards/2632685.json?printFields={FIELDS}"
status, body = get(url)
assert status == 200, status
out = HERE / "data/raw/sources/nsf_award_2632685.json"
out.write_text(body)
record(out, url=url, source="NSF Award API", note="award 2632685 (MESA)")
DROP = ("pi", "piEmail", "poEmail", "poPhone", "awardeePhone", "coPDPI", "projectOutComesReport")
aw = {k: v for k, v in json.loads(body)["response"]["award"][0].items() if k not in DROP}
proc = HERE / "data/processed/award_2632685.json"
proc.write_text(json.dumps(aw, indent=2))
for k, v in aw.items():
    print(k, "=", v if k != "abstractText" else v[:3000])

# CyVerse (the host of mesa.cyverse.org) is itself NSF-funded cyberinfrastructure: record its award.
url2 = "https://api.nsf.gov/services/v1/awards/1743442.json?printFields=id,title,awardeeName,startDate,expDate,orgLongName2,fundProgramName,estimatedTotalAmt"
status, body = get(url2)
assert status == 200, status
out2 = HERE / "data/raw/sources/nsf_award_1743442.json"
out2.write_text(body)
record(out2, url=url2, source="NSF Award API", note="award 1743442 (CyVerse)")
aw2 = {k: v for k, v in json.loads(body)["response"]["award"][0].items() if k not in DROP}
(HERE / "data/processed/award_1743442.json").write_text(json.dumps(aw2, indent=2))
print({k: aw2[k] for k in ("id", "title", "startDate", "expDate", "orgLongName2")})
