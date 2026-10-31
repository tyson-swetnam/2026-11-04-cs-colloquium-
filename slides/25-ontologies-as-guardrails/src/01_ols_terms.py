"""Slide 25: check every CURIE, label and free-text variant on the slide against OLS4,
the class hierarchy (Carabidae under Coleoptera), OBO Foundry membership of the three
ontologies, and the NSF award number in the footer.

Outputs (data/processed/):
  terms.csv            CURIE, OLS label, synonyms, obsolete flag, defining ontology
  variants.csv         each free-text variant on the slide: is it a name of the term?
  hierarchy.csv        OLS hierarchical ancestors of NCBITaxon:41073
  obo_foundry.csv      registry entries for ncbitaxon, obi, uo
  nsf_award.csv        NSF Award API record for 2632685
Raw API responses are saved under data/raw/sources/ and logged in its MANIFEST.yaml.
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
from evidence.ontology import OLS, OLSClient, validate  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
CACHE = SLIDE / "data" / "cache"
SOURCES = SLIDE / "data" / "raw" / "sources"
PROCESSED = SLIDE / "data" / "processed"

# Field, CURIE on the slide, label on the slide, free-text variants on the slide, allowed prefix.
ROWS = [
    ("Taxon", "NCBITaxon:41073", "Carabidae", ["ground beetle", "carabid", "Carabidae"], ("NCBITaxon",)),
    ("Specimen", "OBI:0100051", "specimen", ["pinned beetle", "voucher", "sample"], ("OBI",)),
    ("Length", "UO:0000016", "millimetre", ["mm", "millimeters", "millim."], ("UO",)),
    ("Area", "UO:0000082", "square millimetre", ["mm²", "sq mm", "mm2"], ("UO",)),
]
EXTRA = ["NCBITaxon:7041"]  # Coleoptera, for the hierarchy claim


def save(name: str, url: str, body: str, note: str) -> None:
    SOURCES.mkdir(parents=True, exist_ok=True)
    p = SOURCES / name
    p.write_text(body, encoding="utf-8")
    record(p, url=url, source="API", note=note)


def main() -> None:
    get = CachedGet(CACHE, UA)
    client = OLSClient(CACHE / "ols", UA)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    terms, variants = [], []
    for fieldname, curie, slide_label, texts, prefixes in ROWS + [("-", c, "", [], ()) for c in EXTRA]:
        prefix = curie.split(":")[0].lower()
        url = f"{OLS}/ontologies/{prefix}/terms?obo_id={curie}"
        status, body = get(url)
        save(f"ols_{curie.replace(':', '_')}.json", url, body, f"OLS4 term record for {curie}")
        t = json.loads(body)["_embedded"]["terms"][0]
        ann = t.get("annotation") or {}
        terms.append({
            "field": fieldname, "curie": curie, "slide_label": slide_label, "ols_label": t["label"],
            "slide_label_is_a_name": slide_label.lower() in [s.lower() for s in [t["label"], *(t.get("synonyms") or [])]] if slide_label else "",
            "synonyms": "; ".join(t.get("synonyms") or []),
            "rank": "; ".join(ann.get("has_rank", [])),
            "is_obsolete": t["is_obsolete"], "defining_ontology": t["ontology_name"], "is_defining": t["is_defining_ontology"],
        })
        for text in texts:
            c = validate(client, text, curie, prefixes)
            variants.append({"field": fieldname, "text": text, "curie": curie, "is_a_name_of_term": c.ok, "reason": c.reason})

    pd.DataFrame(terms).to_csv(PROCESSED / "terms.csv", index=False)
    pd.DataFrame(variants).to_csv(PROCESSED / "variants.csv", index=False)

    # Hierarchy: save the raw ancestors response too.
    t = client.term("NCBITaxon:41073")
    from urllib.parse import quote
    iri = quote(quote(t.iri, safe=""), safe="")
    url = f"{OLS}/ontologies/ncbitaxon/terms/{iri}/hierarchicalAncestors?size=500"
    status, body = get(url)
    save("ols_NCBITaxon_41073_ancestors.json", url, body, "OLS4 hierarchical ancestors of Carabidae")
    anc = [(a.get("obo_id"), a.get("label")) for a in json.loads(body)["_embedded"]["terms"]]
    pd.DataFrame(anc, columns=["curie", "label"]).to_csv(PROCESSED / "hierarchy.csv", index=False)

    # OBO Foundry registry.
    url = "https://obofoundry.org/registry/ontologies.jsonld"
    status, body = get(url)
    save("obofoundry_ontologies.jsonld", url, body, "OBO Foundry registry")
    reg = {o["id"]: o for o in json.loads(body)["ontologies"]}
    pd.DataFrame([
        {"id": i, "title": reg[i].get("title"), "activity_status": reg[i].get("activity_status"), "in_registry": i in reg}
        for i in ("ncbitaxon", "obi", "uo")
    ]).to_csv(PROCESSED / "obo_foundry.csv", index=False)

    # NSF award in the footer.
    url = "https://api.nsf.gov/services/v1/awards/2632685.json?printFields=id,title,awardeeName,piFirstName,piLastName,startDate,expDate,fundProgramName"
    status, body = get(url)
    save("nsf_award_2632685.json", url, body, "NSF Award API record")
    aw = json.loads(body)["response"]["award"][0]
    keep = ["id", "title", "awardeeName", "pdPIName", "startDate", "expDate", "estimatedTotalAmt", "fundProgramName", "divAbbr"]
    aw = {k: aw.get(k) for k in keep}
    pd.DataFrame([aw]).to_csv(PROCESSED / "nsf_award.csv", index=False)

    print(pd.DataFrame(terms).to_string(index=False))
    print(pd.DataFrame(variants).to_string(index=False))
    print("Coleoptera in ancestors:", any(c == "NCBITaxon:7041" for c, _ in anc))
    print(pd.read_csv(PROCESSED / "obo_foundry.csv").to_string(index=False))
    print(aw)


if __name__ == "__main__":
    main()
