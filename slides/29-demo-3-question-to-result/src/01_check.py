"""Check slide 29: the MESA award record and what MESA's public docs say about where agents run
and what the DuckLake holds.

Outputs: data/processed/nsf_award.csv, data/processed/mesa_docs_terms.csv
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from evidence.http import CachedGet  # noqa: E402

get = CachedGet(ROOT / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
out = ROOT / "data/processed"
out.mkdir(parents=True, exist_ok=True)

# 1. NSF award record
status, body = get("https://api.nsf.gov/services/v1/awards/2632685.json?printFields=id,title,awardeeName,"
                   "pdPIName,startDate,expDate,fundProgramName,estimatedTotalAmt,transType,abstractText")
assert status == 200, status
raw = json.loads(body)["response"]["award"][0]
abstract = raw["abstractText"]
keep = ["id", "title", "awardeeName", "pdPIName", "startDate", "expDate", "fundProgramName",
        "estimatedTotalAmt", "transType"]
a = {k: raw.get(k, "") for k in keep}
a["abstract_names_nairr"] = "NAIRR" in abstract
a["abstract_compute_sentence"] = next(s for s in re.split(r"(?<=\.)\s+", abstract) if "cyberinfrastructure" in s)
with (out / "nsf_award.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, list(a))
    w.writeheader()
    w.writerow(a)

# 2. MESA public docs: count mentions of compute platforms and lakehouse terms
status, docs = get("https://idss-mesa.github.io/docs/llms-full.txt")
assert status == 200, status
terms = ["NAIRR", "Jetstream", "ACCESS", "CyVerse VICE", "A16", "DuckLake", "lakehouse",
         "mesa_ducklake_", "metadata history", "AVU metadata-history"]
with (out / "mesa_docs_terms.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["term", "count_case_insensitive", "first_line"])
    lines = docs.splitlines()
    for t in terms:
        hits = [i + 1 for i, l in enumerate(lines) if t.lower() in l.lower()]
        w.writerow([t, len(hits), hits[0] if hits else ""])
print(open(out / "nsf_award.csv").read())
print(open(out / "mesa_docs_terms.csv").read())
