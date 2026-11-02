"""Split the 188,522 Biorepository records (c8) into carabid and bycatch collections,
and save collection metadata for collid 4, 11, 13 and 63 (what those records are)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from evidence.http import CachedGet  # noqa: E402
from evidence.fetch import record  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
get = CachedGet(ROOT / "data/cache", UA)
SRC = ROOT / "data/raw/sources"
checks = json.loads((ROOT / "data/processed/checks.json").read_text())
recs = {c["collid"]: c["records"] for c in checks["biorepo"]["collections"]}

meta = {}
for c in (4, 11, 13, 63):
    url = f"https://biorepo.neonscience.org/portal/api/v2/collection/{c}"
    st, b = get(url)
    p = SRC / f"biorepo_collection{c}.json"
    p.write_text(b, encoding="utf-8")
    record(p, url=url, source="NEON Biorepository portal API", note="collection metadata")
    j = json.loads(b)
    meta[c] = {k: j.get(k) for k in ("collectionName", "datasetname") if k in j}

CARABID = [11, 14, 39, 63, 95]         # carabid collections (incl. DNA extracts)
BYCATCH_NAMED = [12, 13, 15, 16, 17]   # collections named "...Bycatch..."
INVERT_VOUCHER = [4]                   # invertebrate vouchers sorted from bycatch
out = {
    "total": sum(recs.values()),
    "carabid": sum(recs[c] for c in CARABID),
    "carabid_excl_dna": sum(recs[c] for c in CARABID if c != 63),
    "dna_extracts_collid63": recs[63],
    "bycatch_named": sum(recs[c] for c in BYCATCH_NAMED),
    "bycatch_named_plus_collid4": sum(recs[c] for c in BYCATCH_NAMED + INVERT_VOUCHER),
    "collection_metadata": meta,
}
out["non_carabid"] = out["total"] - out["carabid"]
(ROOT / "data/processed/bycatch.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
