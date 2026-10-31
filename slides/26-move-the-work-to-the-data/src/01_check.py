"""Check slide 26 numbers against NEON, GBIF, OLS4 and the NSF Award API."""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from evidence.http import CachedGet  # noqa: E402
from evidence.ontology import OLSClient  # noqa: E402
from evidence.fetch import record  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
get = CachedGet(ROOT / "data/cache", UA)
SRC = ROOT / "data/raw/sources"
SRC.mkdir(parents=True, exist_ok=True)
out = {}


def save(name, url, body, source):
    p = SRC / name
    p.write_text(body, encoding="utf-8")
    record(p, url=url, source=source)


# c7 / c13: NEON product record
url = "https://data.neonscience.org/api/v0/products/DP1.10022.001"
st, body = get(url)
save("neon_DP1.10022.001.json", url, body, "NEON Data API")
d = json.loads(body)["data"]
sites = sorted(s["siteCode"] for s in d["siteCodes"])
months = Counter(m for s in d["siteCodes"] for m in s["availableMonths"])
url = "https://data.neonscience.org/api/v0/sites"
st, body = get(url)
save("neon_sites.json", url, body, "NEON Data API")
dom = {s["siteCode"]: s["domainCode"] for s in json.loads(body)["data"]}
out["neon"] = {
    "productName": d["productName"],
    "productStatus": d.get("productStatus"),
    "n_sites": len(sites),
    "n_domains": len({dom[s] for s in sites}),
    "first_month": min(months),
    "last_month": max(months),
    "sites_per_month_last6": dict(sorted(months.items())[-6:]),
    "releases": sorted({r["release"] for r in d.get("releases", [])}),
}

# c8: GBIF datasets of the NEON Biorepository ground-beetle collections
st, body = get("https://api.gbif.org/v1/dataset/search?q=NEON%20Biorepository%20carabid&limit=50")
ds = json.loads(body)["results"]
rows = []
for r in ds:
    u = f"https://api.gbif.org/v1/occurrence/search?datasetKey={r['key']}&limit=0"
    st, b = get(u)
    save(f"gbif_{r['key']}.json", u, b, "GBIF occurrence API")
    rows.append({"key": r["key"], "title": r["title"], "gbif_occurrences": json.loads(b)["count"]})
st, b = get("https://api.gbif.org/v1/occurrence/search?datasetKey=" + "&datasetKey=".join(r["key"] for r in ds) + "&limit=0&mediaType=StillImage")
out["gbif"] = {"datasets": rows, "total": sum(r["gbif_occurrences"] for r in rows),
               "total_with_images": json.loads(b)["count"]}

# c8: NEON Biorepository portal (Symbiota API v2) record counts for the
# 11 collections fed by ground-beetle pitfall sampling (same 11 as the GBIF datasets above)
COLLS = [4, 11, 12, 13, 14, 15, 16, 17, 39, 63, 95]
bio = []
for c in COLLS:
    st, b = get(f"https://biorepo.neonscience.org/portal/api/v2/collection/{c}")
    name = json.loads(b).get("collectionName") if st == 200 else None
    url = f"https://biorepo.neonscience.org/portal/api/v2/occurrence/search?collid={c}&limit=1"
    st, b = get(url)
    save(f"biorepo_collid{c}.json", url, b, "NEON Biorepository portal API")
    bio.append({"collid": c, "name": name, "records": json.loads(b)["count"]})
out["biorepo"] = {"collections": bio, "total": sum(r["records"] for r in bio)}
out["biorepo"]["share_on_gbif"] = round(out["gbif"]["total"] / out["biorepo"]["total"], 3)

# c9: ontology terms
ols = OLSClient(ROOT / "data/cache", UA)
out["ontology"] = {}
for c in ("NCBITaxon:41073", "UO:0000016"):
    t = ols.term(c)
    u = f"https://www.ebi.ac.uk/ols4/api/ontologies/{c.split(':')[0].lower()}/terms?obo_id={c}"
    st, b = get(u)
    save(f"ols_{c.replace(':', '_')}.json", u, b, "EBI OLS4")
    out["ontology"][c] = None if t is None else {"label": t.label, "obsolete": t.obsolete, "iri": t.iri}

# c12: NSF award
url = "https://api.nsf.gov/services/v1/awards/2632685.json?printFields=id,title,agency,startDate,expDate,awardeeName,piFirstName,piLastName,estimatedTotalAmt"
st, body = get(url)
save("nsf_2632685.json", url, body, "NSF Award API")
out["nsf"] = json.loads(body)["response"].get("award")

(ROOT / "data/processed").mkdir(parents=True, exist_ok=True)
(ROOT / "data/processed/checks.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
