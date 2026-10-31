"""Confirm the footer award number (NSF #2632685) against the NSF Award API."""
import json
from pathlib import Path

from evidence.http import CachedGet

HERE = Path(__file__).resolve().parents[1]
get = CachedGet(HERE / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
URL = ("https://api.nsf.gov/services/v1/awards/2632685.json?printFields="
       "id,title,awardeeName,piFirstName,piLastName,startDate,expDate,fundProgramName,estimatedTotalAmt")

if __name__ == "__main__":
    status, body = get(URL)
    awards = json.loads(body).get("response", {}).get("award", []) if status == 200 else []
    award = awards[0] if awards else None
    if award:  # drop personal contact fields; keep the public award facts
        award = {k: v for k, v in award.items() if not any(x in k.lower() for x in ("email", "phone")) and k != "pi"}
    out = {"url": URL, "status": status, "award": award}
    (HERE / "data/processed").mkdir(parents=True, exist_ok=True)
    (HERE / "data/processed/nsf_award_2632685.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
