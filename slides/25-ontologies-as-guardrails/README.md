# Slide 25 · Every term resolves before it is written

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-25)

Checked live against EBI's Ontology Lookup Service, with the same validator as slide 17's control 2 (`evidence/ontology.py`). The results are in [`ontology_writes.csv`](../17-hallucination-is-engineering/data/processed/ontology_writes.csv).

| Field | CURIE on the slide | OLS label | Free-text variants that resolve as names | Variants that need a mapping |
|---|---|---|---|---|
| Taxon | NCBITaxon:41073 | Carabidae | ground beetle, Carabidae | carabid |
| Specimen | OBI:0100051 | specimen | none | pinned beetle, voucher, sample |
| Length | UO:0000016 | millimeter | mm, millimeters | millim. |
| Area | UO:0000082 | square millimeter | mm2, mm² | sq mm |

- **All four CURIEs exist, are current, and carry the labels the slide shows.** UO spells it "millimeter"; the slide says "millimetre".
- **Half the left column is mappings, not names.** "Pinned beetle" is not a name for *specimen*. An agent proposes the mapping, and the write is refused until a curator accepts it. That is the guardrail working, and worth saying on stage.
- **The hierarchy claim checks out.** Coleoptera (NCBITaxon:7041) is an ancestor of Carabidae in OLS, so a query for beetles finds every carabid.

Claims and status: [`claims.yaml`](claims.yaml).
