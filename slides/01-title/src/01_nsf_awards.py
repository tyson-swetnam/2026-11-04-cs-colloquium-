"""Find NSF awards naming Tyson Swetnam as PI or co-PI and tally them by NSF division.

Also computes the day of week for the talk date and years since 2013 (start of CyVerse work).
Outputs: data/processed/nsf_awards.csv, data/processed/summary.txt
"""
import csv
import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from evidence.http import CachedGet  # noqa: E402

get = CachedGet(ROOT / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
FIELDS = ("id,title,piFirstName,piLastName,coPDPI,pdPIName,awardeeName,startDate,expDate,"
          "fundProgramName,primaryProgram,dirAbbr,divAbbr,orgLongName,orgLongName2,estimatedTotalAmt,fundsObligatedAmt")
BASE = "https://api.nsf.gov/services/v1/awards.json?"


def query(**params):
    out, offset = [], 0
    while True:
        status, body = get(BASE + urlencode(dict(params, printFields=FIELDS, offset=offset, rpp=25)))
        if status != 200:
            raise SystemExit(f"NSF API {status}: {body[:200]}")
        awards = json.loads(body).get("response", {}).get("award", [])
        out += awards
        if len(awards) < 25:
            return out
        offset += 25


awards = {}
for a in query(pdPIName="Swetnam"):
    awards.setdefault(a["id"], dict(a, role="PI"))
for a in query(coPDPI="Swetnam"):
    awards.setdefault(a["id"], dict(a, role="co-PI"))
# keep only Tyson Swetnam
rows = []
for a in awards.values():
    names = (a.get("pdPIName", "") + " " + " ".join(a.get("coPDPI", []) if isinstance(a.get("coPDPI"), list) else [str(a.get("coPDPI", ""))]))
    if "Tyson" not in names:
        continue
    if a["role"] == "PI" and a.get("piFirstName") != "Tyson":
        a["role"] = "co-PI"
    rows.append({k: (json.dumps(v) if isinstance(v, list) else v) for k, v in a.items()})
rows.sort(key=lambda r: r.get("startDate", "")[-4:] + r.get("startDate", ""))
out = ROOT / "data/processed"
out.mkdir(parents=True, exist_ok=True)
keys = ["id", "role", "title", "pdPIName", "coPDPI", "awardeeName", "startDate", "expDate",
        "dirAbbr", "divAbbr", "orgLongName", "orgLongName2", "primaryProgram", "fundProgramName",
        "estimatedTotalAmt", "fundsObligatedAmt"]
with (out / "nsf_awards.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, keys, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)

today = dt.date(2026, 10, 31)
lines = [f"Nov 4 2026 weekday: {dt.date(2026, 11, 4).strftime('%A')}",
         f"Years 2013 -> 2026: {2026 - 2013}",
         f"Tyson Swetnam awards (PI or co-PI): {len(rows)}"]
for r in rows:
    exp = dt.datetime.strptime(r["expDate"], "%m/%d/%Y").date() if r.get("expDate") else None
    active = exp and exp >= today
    lines.append(f"  {r['id']} {r['role']:5} {r.get('dirAbbr','')}/{r.get('divAbbr','')} "
                 f"{r.get('orgLongName2') or r.get('orgLongName','')} | {r.get('startDate')}-{r.get('expDate')} "
                 f"{'ACTIVE' if active else 'expired'} | {r.get('awardeeName')} | {r['title']}")
(out / "summary.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
