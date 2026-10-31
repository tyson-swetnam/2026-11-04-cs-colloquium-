"""Write data/raw/research/facts.csv and assert every quote occurs verbatim in the saved source."""

from __future__ import annotations

import csv
from pathlib import Path

SLIDE = Path(__file__).resolve().parents[1]
S = SLIDE / "data" / "raw" / "sources"
OLS = "https://www.ebi.ac.uk/ols4/api/ontologies/"
EBI = ("EMBL-EBI OLS4", "2026-10-31")
MESA = "MESA (idss-mesa.github.io)"

ROWS = [
    ("f1", "c6", "Carabidae", '"label" : "Carabidae"', "OLS4 term NCBITaxon:41073", *EBI, OLS + "ncbitaxon/terms?obo_id=NCBITaxon:41073", "primary", "", "ols_NCBITaxon_41073.json"),
    ("f2", "c6", "synonym ground beetles", '"synonyms" : [ "ground beetles" ]', "OLS4 term NCBITaxon:41073", *EBI, OLS + "ncbitaxon/terms?obo_id=NCBITaxon:41073", "primary", "only synonym; carabid is not a name of the term", "ols_NCBITaxon_41073.json"),
    ("f3", "c6", "rank family", '"has_rank" : [ "http://purl.obolibrary.org/obo/TAXRANK_0000004" ]', "OLS4 term NCBITaxon:41073", *EBI, OLS + "ncbitaxon/terms?obo_id=NCBITaxon:41073", "primary", "TAXRANK_0000004 = family", "ols_NCBITaxon_41073.json"),
    ("f4", "c7", "specimen", '"label" : "specimen"', "OLS4 term OBI:0100051", *EBI, OLS + "obi/terms?obo_id=OBI:0100051", "primary", "", "ols_OBI_0100051.json"),
    ("f5", "c7", "no synonyms", '"synonyms" : [ ]', "OLS4 term OBI:0100051", *EBI, OLS + "obi/terms?obo_id=OBI:0100051", "primary", "pinned beetle / voucher / sample are mappings, not names", "ols_OBI_0100051.json"),
    ("f6", "c8", "millimeter", '"label" : "millimeter"', "OLS4 term UO:0000016", *EBI, OLS + "uo/terms?obo_id=UO:0000016", "primary", "", "ols_UO_0000016.json"),
    ("f7", "c8", "synonyms millimetre, mm", '"synonyms" : [ "millimetre", "mm" ]', "OLS4 term UO:0000016", *EBI, OLS + "uo/terms?obo_id=UO:0000016", "primary", "slide spelling millimetre is a synonym", "ols_UO_0000016.json"),
    ("f8", "c8", "square millimeter", '"label" : "square millimeter"', "OLS4 term UO:0000082", *EBI, OLS + "uo/terms?obo_id=UO:0000082", "primary", "", "ols_UO_0000082.json"),
    ("f9", "c8", "synonyms mm^[2], square millimetre", '"synonyms" : [ "mm^[2]", "square millimetre" ]', "OLS4 term UO:0000082", *EBI, OLS + "uo/terms?obo_id=UO:0000082", "primary", "mm2 and mm² match mm^[2] only after normalisation", "ols_UO_0000082.json"),
    ("f10", "c9", "Coleoptera is an ancestor of Carabidae", '"obo_id" : "NCBITaxon:7041"', "OLS4 hierarchical ancestors of NCBITaxon:41073", *EBI, OLS + "ncbitaxon/terms/{Carabidae IRI}/hierarchicalAncestors?size=500", "primary", "", "ols_NCBITaxon_41073_ancestors.json"),
    ("f11", "c9", "Coleoptera rank order", '"has_rank" : [ "http://purl.obolibrary.org/obo/TAXRANK_0000003" ]', "OLS4 term NCBITaxon:7041", *EBI, OLS + "ncbitaxon/terms?obo_id=NCBITaxon:7041", "primary", "TAXRANK_0000003 = order; synonym beetles", "ols_NCBITaxon_7041.json"),
    ("f12", "c10", "NCBITaxon in OBO Foundry registry", '"title": "NCBI organismal classification"', "OBO Foundry registry", "OBO Foundry", "2026-10-31", "https://obofoundry.org/registry/ontologies.jsonld", "primary", "obi and uo also listed; all three active", "obofoundry_ontologies.jsonld"),
    ("f13", "c10", "UO in OBO Foundry registry", '"title": "Units of measurement ontology"', "OBO Foundry registry", "OBO Foundry", "2026-10-31", "https://obofoundry.org/registry/ontologies.jsonld", "primary", "", "obofoundry_ontologies.jsonld"),
    ("f14", "c10", "mesa-mcp uses OBO/OLS", "| `mesa_ols_*` | Browse OBO/OLS ontologies: search terms, fetch hierarchies, generate AVU templates |", "mesa-mcp docs", MESA, "2026-07-18", "https://idss-mesa.github.io/docs/servers/mesa-mcp/", "primary", "developer-written docs", "mesa_llms_full.txt"),
    ("f15", "c4", "CURIE stored in the unit slot", "ontology CURIE when the AVU came from OBO/OLS.", "mesa-mcp docs: The AVU contract", MESA, "2026-07-18", "https://idss-mesa.github.io/docs/servers/mesa-mcp/", "primary", "developer-written; does not say unresolvable terms are refused", "mesa_llms_full.txt"),
    ("f16", "c4", "candidate terms come from OLS search", "| S | candidates | code | OLS search, prefix filter, dedup, cap |", "mesa-anyjev docs: Decision graph", MESA, "2026-09-25", "https://idss-mesa.github.io/mesa-anyjev/", "primary", "developer-written, status draft", "anyjev_llms_full.txt"),
    ("f17", "c4", "curator pick is authoritative", "| H | human pick | MRTR | the curator's choice is authoritative and becomes a label |", "mesa-anyjev docs: Decision graph", MESA, "2026-09-25", "https://idss-mesa.github.io/mesa-anyjev/", "primary", "developer-written, status draft", "anyjev_llms_full.txt"),
    ("f18", "c4", "a decline leaves the group unwritten", "decline leaves the group unwritten.", "mesa-anyjev docs: MCP tools", MESA, "2026-09-25", "https://idss-mesa.github.io/mesa-anyjev/concepts/mcp-tools/", "primary", "developer-written, status draft", "anyjev_llms_full.txt"),
    ("f19", "c12", "award 2632685 title", "Research Infrastructure: Category II: MESA (Multidisciplinary Environment for Scientific Advancement)", "NSF Award API 2632685", "U.S. National Science Foundation", "2026-07-26", "https://api.nsf.gov/services/v1/awards/2632685.json", "primary", "UNM; PI Tyson L Swetnam; 2026-07-15 to 2029-05-31", "nsf_award_2632685.json"),
]


def main() -> None:
    out = SLIDE / "data" / "raw" / "research" / "facts.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow("id,claim_id,value,quote,source_title,publisher,date,url,source_type,notes".split(","))
        for r in ROWS:
            assert r[3] in (S / r[10]).read_text(encoding="utf-8"), f"{r[0]}: quote not in {r[10]}"
            w.writerow(r[:10])
    print(f"{len(ROWS)} facts, every quote found verbatim")


if __name__ == "__main__":
    main()
