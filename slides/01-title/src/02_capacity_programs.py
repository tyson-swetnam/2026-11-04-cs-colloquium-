"""Check how the NSF Award API files BIO 'Capacity' program awards (historically DBI) by division.

Also checks role flags ("(Former)") in the co-PI list for still-open awards, and
flags same-title award pairs (institutional transfers).
Outputs: data/processed/capacity_divisions.csv, data/processed/capacity_summary.txt
"""
import collections
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from evidence.http import CachedGet  # noqa: E402

get = CachedGet(ROOT / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
BASE = "https://api.nsf.gov/services/v1/awards.json?"
FIELDS = "id,title,fundProgramName,dirAbbr,divAbbr,orgLongName2,startDate,expDate,activeAwd"


def query(**params):
    out, offset = [], 1
    while True:
        status, body = get(BASE + urlencode(dict(params, printFields=FIELDS, offset=offset, rpp=25)))
        if status != 200:
            raise SystemExit(f"NSF API {status}: {body[:200]}")
        awards = json.loads(body).get("response", {}).get("award", [])
        out += awards
        if len(awards) < 25 or offset > 500:
            return out
        offset += 25


rows = []
for prog in ["Capacity: Cyberinfrastructure", "Capacity: Bio Collections", "Capacity: Field Stations"]:
    for a in query(fundProgramName=prog.replace(":", ""), dateStart="01/01/2021"):  # API returns 0 hits with the colon
        if prog in [x.strip() for x in a.get("fundProgramName", "").split(",")]:
            rows.append(dict(a, query_program=prog))
out = ROOT / "data/processed"
with (out / "capacity_divisions.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, ["query_program", "id", "dirAbbr", "divAbbr", "orgLongName2", "startDate",
                           "expDate", "activeAwd", "fundProgramName", "title"], extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
rows = list({(r["query_program"], r["id"]): r for r in rows}.values())
tally = collections.Counter((r["query_program"], r.get("dirAbbr"), r.get("divAbbr"), r.get("activeAwd")) for r in rows)
lines = ["Capacity-program awards (started 2021+) by program / directorate / division / activeAwd:"]
lines += [f"  {p} | {d}/{v} | active={a}: {n}" for (p, d, v, a), n in sorted(tally.items())]

# Swetnam awards: same-title pairs and "(Former)" flags
aw = list(csv.DictReader((out / "nsf_awards.csv").open()))
by_title = collections.defaultdict(list)
for r in aw:
    by_title[(r["title"].strip(), r["estimatedTotalAmt"])].append(r["id"])
lines.append(f"Swetnam API records: {len(aw)}; distinct (title, est. total) projects: {len(by_title)}")
for k, ids in by_title.items():
    if len(ids) > 1:
        lines.append(f"  same project, multiple awards: {ids} {k[0]} ${k[1]}")
for r in aw:
    if "Tyson L Swetnam (Former)" in r["coPDPI"]:
        lines.append(f"  {r['id']}: listed as 'Tyson L Swetnam (Former)' co-PI; expDate {r['expDate']}")
(out / "capacity_summary.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
