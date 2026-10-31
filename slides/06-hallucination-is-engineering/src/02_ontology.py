"""Control 2, "It makes up metadata": every term must resolve in an ontology before it is written.

The agent proposes (field, text, CURIE). The write path accepts it only if OLS4 says the term
exists, is current, comes from the ontology the field allows, and is named by the text.
The cases are the slide-19 examples plus the errors a language model actually makes:
a CURIE for the wrong concept, an invented CURIE, a term from the wrong ontology, a retired term.

Output: data/processed/ontology_writes.csv, ontology_hierarchy.csv
"""

from __future__ import annotations

import pandas as pd

import config
from evidence.ontology import OLSClient, validate

FIELDS = {"organism": ("NCBITaxon",), "assay": ("OBI",), "cell_line": ("CLO",)}
PROPOSALS = [
    # field, text written, CURIE proposed, what the case tests
    ("organism", "mouse", "NCBITaxon:10090", "slide 19"),
    ("organism", "Mouse", "NCBITaxon:10090", "slide 19"),
    ("organism", "M. musculus", "NCBITaxon:10090", "slide 19"),
    ("assay", "RNAseq", "OBI:0001271", "slide 19"),
    ("assay", "rna-seq", "OBI:0001271", "slide 19"),
    ("assay", "transcriptome", "OBI:0001271", "slide 19: a curator's mapping, not a name"),
    ("cell_line", "HeLa cells", "CLO:0003684", "slide 19"),
    ("organism", "mouse", "NCBITaxon:10116", "real CURIE, wrong concept (rat)"),
    ("assay", "RNA-seq", "OBI:0009999", "invented CURIE"),
    ("organism", "HeLa", "CLO:0003684", "right term, wrong field"),
    ("assay", "sequencing platform", "OBI:0000050", "retired (obsolete) term"),
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

    # The payoff on slide 19: the class hierarchy lets a question about mammals find the mouse.
    anc = client.ancestors("NCBITaxon:10090")
    pd.DataFrame(anc, columns=["curie", "label"]).to_csv(config.PROCESSED / "ontology_hierarchy.csv", index=False)
    print("Mammalia (NCBITaxon:40674) is an ancestor of Mus musculus:", any(c == "NCBITaxon:40674" for c, _ in anc))


if __name__ == "__main__":
    main()
