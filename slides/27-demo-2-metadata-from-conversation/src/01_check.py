"""Slide 27: check the identifiers and numbers in the AVU table on the slide.

- NCBITaxon:41073 and UO:0000016 through OLS4 (label, synonyms, obsolete flag).
- NEON data product DP1.10022.001 through the NEON Data API: name, number of sites
  with data, first and last month with data.
- NSF award 2632685 (footer) through the NSF Award API.
- The AVU layout on the slide against the "AVU contract" in MESA's public mesa-mcp docs
  (CURIE in the unit slot).

Outputs (data/processed/): terms.csv, neon_product.csv, nsf_award.csv, avu_layout.csv.
Raw API responses go to data/raw/sources/ and are logged in its MANIFEST.yaml.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
ROOT = SLIDE.parents[1]
sys.path.insert(0, str(ROOT))

from evidence.fetch import record  # noqa: E402
from evidence.http import CachedGet  # noqa: E402
from evidence.ontology import OLS, OLSClient  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
CACHE = SLIDE / "data" / "cache"
SOURCES = SLIDE / "data" / "raw" / "sources"
PROCESSED = SLIDE / "data" / "processed"

# AVU rows as shown on the slide: attribute, value, unit.
SLIDE_AVUS = [
    ("taxon", "NCBITaxon:41073 (Carabidae)", "none"),
    ("neon_product", "DP1.10022.001 (pitfall-trap beetles)", "none"),
    ("specimens", "65,830 segmented, 47 sites", "count"),
    ("elytra_length", "UO:0000016 (millimetre)", "mm"),
]
CURIE_PREFIXES = ("NCBITaxon:", "UO:", "OBI:")


def save(name: str, url: str, body: str, note: str) -> None:
    SOURCES.mkdir(parents=True, exist_ok=True)
    p = SOURCES / name
    p.write_text(body, encoding="utf-8")
    record(p, url=url, source="API", note=note)


def main() -> None:
    get = CachedGet(CACHE, UA)
    ols = OLSClient(CACHE / "ols", UA)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    # 1. Ontology terms
    rows = []
    for curie, slide_label in [("NCBITaxon:41073", "Carabidae"), ("UO:0000016", "millimetre")]:
        prefix = curie.split(":")[0].lower()
        url = f"{OLS}/ontologies/{prefix}/terms?obo_id={curie}"
        status, body = get(url)
        save(f"ols_{curie.replace(':', '_')}.json", url, body, f"OLS4 term record for {curie}")
        t = ols.term(curie)
        rows.append({
            "curie": curie,
            "slide_label": slide_label,
            "ols_label": t.label if t else "",
            "names": " | ".join(t.names) if t else "",
            "slide_label_is_a_name": bool(t and slide_label.lower() in [n.lower() for n in t.names]),
            "obsolete": t.obsolete if t else None,
            "ontology": t.ontology if t else "",
            "http_status": status,
        })
    pd.DataFrame(rows).to_csv(PROCESSED / "terms.csv", index=False)

    # 2. NEON data product
    url = "https://data.neonscience.org/api/v0/products/DP1.10022.001"
    status, body = get(url)
    save("neon_DP1.10022.001.json", url, body, "NEON Data API product record")
    d = json.loads(body)["data"]
    sites = d.get("siteCodes") or []
    months = sorted(m for s in sites for m in s.get("availableMonths", []))
    pd.DataFrame([{
        "productCode": d["productCode"],
        "productName": d["productName"],
        "productStatus": d.get("productStatus"),
        "n_sites_with_data": len(sites),
        "first_month": months[0] if months else "",
        "last_month": months[-1] if months else "",
        "n_site_months": len(months),
    }]).to_csv(PROCESSED / "neon_product.csv", index=False)

    # 3. NSF award
    url = "https://api.nsf.gov/services/v1/awards/2632685.json?printFields=id,title,awardeeName,piFirstName,piLastName,startDate,expDate"
    status, body = get(url)
    save("nsf_award_2632685.json", url, body, "NSF Award API record")
    awards = json.loads(body).get("response", {}).get("award", [])
    keep = ["id", "title", "awardeeName", "pdPIName", "startDate", "expDate", "fundProgramName", "estimatedTotalAmt"]
    pd.DataFrame(awards)[keep].to_csv(PROCESSED / "nsf_award.csv", index=False)

    # 4. AVU layout on the slide vs the documented contract (CURIE in the unit slot)
    layout = []
    for attr, value, unit in SLIDE_AVUS:
        curie_in_value = any(p in value for p in CURIE_PREFIXES)
        curie_in_unit = any(unit.startswith(p) for p in CURIE_PREFIXES)
        layout.append({
            "attribute": attr, "value": value, "unit": unit,
            "curie_in_value": curie_in_value, "curie_in_unit": curie_in_unit,
            "matches_documented_contract": (not curie_in_value) or curie_in_unit,
        })
    pd.DataFrame(layout).to_csv(PROCESSED / "avu_layout.csv", index=False)

    for f in ["terms.csv", "neon_product.csv", "nsf_award.csv", "avu_layout.csv"]:
        print(f"== {f}\n{(PROCESSED / f).read_text()}")


if __name__ == "__main__":
    main()
