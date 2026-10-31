# Slide 09 · Years of work, compressed into days

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-09)

| Row | Verdict | What the primary source says | Suggested cell |
|---|---|---|---|
| **AlphaFold** | ✅ supported | 200M+ structures (260M on the current home page); every file is CC-BY 4.0, "for academic and commercial purposes" (checked by downloading four predictions anonymously) | keep |
| **ESM** | 🟧 partly | ESMFold2 (Biohub, May 2026) designed binders for EGFR, PDGFRβ, PD-L1, CTLA-4, CD45; lab hit rates 36–88% for minibinders. **"Days" is the computational search, not the bench work.** "Three to four years" is Biohub's per-candidate baseline. | *ESMFold2: binders for five cancer and immune targets, confirmed in the lab · Design search in days, vs. 3–4 years per candidate (Biohub)* |
| **Evo 2** | 🟧 partly | Nature 2026: **AUROC 0.95** (AUPRC 0.88) for a classifier trained on Evo 2 embeddings, BRCA1 SNVs. "Over 90% accuracy" is the press release's wording, not the paper's metric. Fully open (weights, code, data). | *BRCA1 variants: AUROC 0.95 (classifier on Evo 2 embeddings)* |
| **AlphaGenome** | ✅ supported | Nature 2026: "takes as input 1 Mb of DNA sequence … up to single-base-pair resolution"; a variant takes "less than 1 s on an NVIDIA H100 GPU" | optional: *Up to 1 Mb of context, base-pair output · Variant scored in under 1 s (one H100)* |

**Speaker notes**
- **ESM, "tested them at the bench in days":** not supported. The Biohub release says "a computational search completed in days, rather than several months or years." Suggested wording: *"…designed binders computationally in days and confirmed them in the lab, with hit rates of 36–88% for minibinders."*
- **"Each row compresses a technique that takes a decade to learn":** your framing. No source says it, which is fine for a speaker note.

**Caveats**
- **Developer-reported.** All four rows are the developers' own results. ESMFold2 is a preprint that hasn't been peer reviewed, and its full text was blocked by bioRxiv, so the ESM details come from Biohub's release and the preprint abstract.
- **AlphaGenome isn't fully open.** Its weights and API carry non-commercial terms.
- **Evo 2 zero-shot results are lower.** NVIDIA's reproduction gives AUROC 0.73–0.87, and NVIDIA co-developed the model, so it isn't fully independent. Details are in [`facts.csv`](data/raw/research/facts.csv).

**Reproduce**

```bash
uv run python slides/09-ai-molecular-science/src/01_alphafold.py
```

```bash
uv run python slides/09-ai-molecular-science/src/02_papers.py
```

- `01_alphafold.py` downloads the AlphaFold predictions and reads each file's licence.
- `02_papers.py` reads the Evo 2 and AlphaGenome full texts from Europe PMC.
- The research pass is in `data/raw/research/`: `facts.csv` has quotes and URLs, and `NOTES.md` covers the blocked sources. The source documents themselves aren't committed; their hashes are in `sources/MANIFEST.yaml`.
