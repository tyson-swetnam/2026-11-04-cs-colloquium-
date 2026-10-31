"""Control 2, "It makes up metadata": every term must resolve in an ontology before it is written.

The agent proposes (field, text, CURIE). The write path accepts it only if OLS4 says the term
exists, is current, comes from the ontology the field allows, and is named by the text.
The cases are slide 25's examples (NEON ground beetles) plus the errors a language model actually makes:
a CURIE for the wrong concept, an invented CURIE, a term from the wrong ontology, a retired term.

Output: data/processed/ontology_writes.csv, ontology_hierarchy.csv
"""

from __future__ import annotations

import pandas as pd

import config
from evidence.ontology import OLSClient, validate

FIELDS = {"taxon": ("NCBITaxon",), "specimen": ("OBI",), "length_unit": ("UO",), "area_unit": ("UO",)}
PROPOSALS = [
    # field, text written, CURIE proposed, what the case tests (slide 25 = "Every term resolves before it is written")
    ("taxon", "ground beetle", "NCBITaxon:41073", "slide 25"),
    ("taxon", "carabid", "NCBITaxon:41073", "slide 25"),
    ("taxon", "Carabidae", "NCBITaxon:41073", "slide 25"),
    ("specimen", "pinned beetle", "OBI:0100051", "slide 25"),
    ("specimen", "voucher", "OBI:0100051", "slide 25"),
    ("specimen", "sample", "OBI:0100051", "slide 25"),
    ("length_unit", "mm", "UO:0000016", "slide 25"),
    ("length_unit", "millimeters", "UO:0000016", "slide 25"),
    ("length_unit", "millim.", "UO:0000016", "slide 25"),
    ("area_unit", "mm²", "UO:0000082", "slide 25"),
    ("area_unit", "sq mm", "UO:0000082", "slide 25"),
    ("area_unit", "mm2", "UO:0000082", "slide 25"),
    # The errors a language model actually makes:
    ("taxon", "Carabidae", "NCBITaxon:7041", "real CURIE, wrong concept (Coleoptera, the order)"),
    ("taxon", "Carabidae", "NCBITaxon:9999999", "invented CURIE"),
    ("length_unit", "mm", "NCBITaxon:41073", "right-looking term, wrong field"),
    ("specimen", "sequencing platform", "OBI:0000050", "retired (obsolete) term"),
]


def main() -> None:
    client = OLSClient(config.CACHE / "ols", config.UA)
    rows = []
    for fieldname, text, curie, case in PROPOSALS:
        check = validate(client, text, curie, FIELDS[fieldname])
        rows.append({"field": fieldname, "text": text, "curie": curie, "case": case, "written": check.ok, "reason": check.reason, "ols_label": check.label})
    df = pd.DataFrame(rows)
    config.PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.PROCESSED / "ontology_writes.csv", index=False)
    print(df[["field", "text", "curie", "written", "reason"]].to_string(index=False))

    # The payoff on slide 25: the class hierarchy lets a question about beetles (Coleoptera) find every carabid.
    anc = client.ancestors("NCBITaxon:41073")
    pd.DataFrame(anc, columns=["curie", "label"]).to_csv(config.PROCESSED / "ontology_hierarchy.csv", index=False)
    print("Coleoptera (NCBITaxon:7041) is an ancestor of Carabidae:", any(c == "NCBITaxon:7041" for c, _ in anc))


if __name__ == "__main__":
    main()
