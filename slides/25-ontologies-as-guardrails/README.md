# Slide 25 · Every term resolves before it is written

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-25)

Rechecked 2026-10-31 against EBI's Ontology Lookup Service (OLS4), the OBO Foundry registry, the NSF Award API and MESA's public docs. Run `uv run python slides/25-ontologies-as-guardrails/src/01_ols_terms.py` then `src/02_facts.py`. Outputs: [`terms.csv`](data/processed/terms.csv), [`variants.csv`](data/processed/variants.csv), [`hierarchy.csv`](data/processed/hierarchy.csv), [`obo_foundry.csv`](data/processed/obo_foundry.csv), [`nsf_award.csv`](data/processed/nsf_award.csv); quotes in [`facts.csv`](data/raw/research/facts.csv).

| Field | CURIE | OLS label (synonyms) | Variants that match a name of the term | Variants that need a mapping |
|---|---|---|---|---|
| Taxon | NCBITaxon:41073 | Carabidae (ground beetles), rank family | Carabidae (exact); ground beetle (up to plural) | carabid |
| Specimen | OBI:0100051 | specimen (none) | none | pinned beetle, voucher, sample |
| Length | UO:0000016 | millimeter (millimetre, mm) | mm (exact); millimeters (up to plural) | millim. |
| Area | UO:0000082 | square millimeter (mm^[2], square millimetre) | mm2, mm² (only after normalising) | sq mm |

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c4 A term that will not resolve fails the write | unverified | MESA docs (developer-written, draft): in mesa-anyjev, candidates come from an OLS search, a curator's pick is authoritative, a decline is not written; an `auto` policy also exists, and mesa-mcp's `mesa_avu_*` writes AVUs directly. No public statement that an unresolvable term is refused; that is in code. | "In MESA's annotation tool (draft), candidate terms come from an OLS search and, by default, a curator approves the pick." |
| c6 Taxon row | partially supported | OLS: Carabidae, synonym "ground beetles" (plural); "ground beetle" matches only up to plural. "carabid" is not a name. | Keep; say on stage that "carabid" needs a curator-approved mapping. |
| c7 Specimen row | partially supported | OLS: "specimen", no synonyms. None of the three variants is a name. | Keep; these are mappings, not resolutions. |
| c8 Unit rows | partially supported | UO labels use US spelling, but "millimetre" and "square millimetre" are synonyms, so the slide is fine. "millimeters" matches "millimeter" only up to plural. "millim." and "sq mm" do not resolve. | Keep. |
| c9 Coleoptera finds every carabid | partially supported | Coleoptera (NCBITaxon:7041) is an OLS ancestor of Carabidae. Whether MESA's queries expand to subclasses is not in public docs (c13). | "…a question about beetles (Coleoptera) *can* find every carabid." |
| c10 OLS and the OBO Foundry (new) | supported | All four CURIEs in OLS4; NCBITaxon, OBI, UO active in the OBO Foundry registry; MESA docs name OBO/OLS. | Keep. |
| c11 Notes: terms neon-beetle-seg uses (new) | unverified | Source is a separate GitHub repo, out of scope here. | Speaker to confirm. |
| c12 NSF Award #2632685 (new) | supported | NSF Award API: MESA, UNM, PI Swetnam, 2026-07-15 to 2029-05-31. | Keep. |
| c13 Notes: beetle query returns the NEON measurements (new) | unverified | The hierarchy allows it (c9); MESA's query expansion is not in public docs. | "…a query for beetle data *can* find the NEON ground-beetle measurements…" |
| c14 Notes: left column is what a model writes (new) | not applicable | Illustrative framing. | n/a |

- **Half the left column is mappings, not names.** An agent proposes "pinned beetle → specimen" and a curator accepts it. That is the guardrail working, and worth saying on stage.
- "Up to plural" means this talk's validator (evidence/ontology.py) ignores plurals and spacing; OLS lists only the exact forms shown in the first table.
- MESA statements here come from the project's own (developer-written) docs.

Claims and status: [`claims.yaml`](claims.yaml).
