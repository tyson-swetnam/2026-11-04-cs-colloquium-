"""Slide 13 (and 14, 18, 22, 28): the MESA award as NSF records it.

Fetches NSF Award Search API records for #2632685 (UNM) and #2608717 (the University of Arizona
award with the same title, made a month earlier), drops contact details (emails, phone numbers),
and keeps the fields the slides cite.

Output: data/raw/nsf_award_<id>.json (trimmed), data/processed/award_facts.csv
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
AWARDS = ["2632685", "2608717"]
FIELDS = "id,title,agency,awardeeName,awardeeStateCode,startDate,expDate,estimatedTotalAmt,fundsObligatedAmt,fundProgramName,program,orgLongName,orgLongName2,pdPIName,transType,date,abstractText"
DROP = {"piEmail", "pi", "poEmail", "poPhone", "awardeePhone"}


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache", UA)
    raw = SLIDE / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    rows = []
    for award in AWARDS:
        status, body = get(f"https://api.nsf.gov/services/v1/awards/{award}.json?printFields={FIELDS}")
        rec = {k: v for k, v in json.loads(body)["response"]["award"][0].items() if k not in DROP}
        (raw / f"nsf_award_{award}.json").write_text(json.dumps(rec, indent=2))
        rows.append({k: rec.get(k) for k in ("id", "awardeeName", "fundProgramName", "orgLongName2", "transType", "startDate", "expDate", "fundsObligatedAmt", "title")})
    df = pd.DataFrame(rows)
    out = SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "award_facts.csv", index=False)
    print(df.to_string(index=False, max_colwidth=60))
    abstract = json.loads((raw / "nsf_award_2632685.json").read_text())["abstractText"]
    for needle in ("ACCESS-CI", "ESIIL", "two-year prototype"):
        i = abstract.find(needle)
        print(f"  [{needle}] ...{abstract[max(0, i - 120):i + 220]}...")


if __name__ == "__main__":
    main()
