# Slide 19 · Every term resolves before it is written

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-19)

## What needs checking

- **`c1`** (factual, high): mouse · Mouse · M. musculus → NCBITaxon:10090 (Mus musculus)
- **`c2`** (factual, high): RNAseq · rna-seq · transcriptome → OBI:0001271 (RNA-seq assay)
- **`c3`** (factual, high): HeLa cells → CLO:0003684 (HeLa cell)
- **`c4`** (technical, medium): A term that will not resolve fails the write
- **`c5`** (technical, medium): OWL carries the class hierarchy, so a question about mammalian transcriptomes finds the mouse

Status and the plan for each claim are in [`claims.yaml`](claims.yaml).

## Evidence

_Nothing yet. Code goes in `src/`, data in `data/`, outputs in `figures/`; see the top-level README._
