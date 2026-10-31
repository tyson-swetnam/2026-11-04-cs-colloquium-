# s09 fact-check notes: "AI in molecular and cellular science" slide

Checked 2026-10-31. Every number is in facts.csv with an exact quote and URL. Raw downloads are in raw/.

## Access problems
- bioRxiv full text for the ESMFold2 preprint (10.64898/2026.06.03.729735) returned HTTP 429 / Cloudflare "error code: 1015". I did not try to get around it. I had only the abstract, from the bioRxiv API JSON and Europe PMC PPR1245895. Europe PMC fullTextXML for the preprint returned HTTP 500.
- The `gh` API for ArcInstitute/evo2 was not enabled for this session. raw.githubusercontent.com worked, so I used it for LICENSE, README and the notebook.
- I read the Nature papers (Evo 2, AlphaGenome) as full text from Europe PMC fullTextXML (PMC13128491, PMC12851941). I did not access nature.com.

## Row 1: ESM
- Organisation: Biohub said on 2025-11-06 that the EvolutionaryScale team "will join Biohub" and that Alex Rives would be head of science. Press calls it a CZI acquisition. ESM stands for "Evolutionary Scale Modeling", not "Models".
- Model: ESMFold2, released with ESMC and ESM Atlas on 2026-05-27. Preprint: Candido ... Rives, bioRxiv 2026-06-04, not peer reviewed. MIT licence.
- Targets: EGFR, PDGFRβ, PD-L1, CTLA-4, CD45. Hit rates: 36–88% for minibinders, 15–29% for antibody-derived formats. PD-L1 binders restored T cell signalling.
- "Days": the release says the *computational search* took days ("a computational search completed in days, rather than several months or years"; "producing experimentally testable designs in days"; "hours or days"). It does NOT say the bench testing took days.
- "Three to four years": this IS in the release, as the baseline: "a single preclinical binder candidate typically takes three to four years to develop". No citation is given. Comparing it with "designs in days" is the developer's own framing. Strictly, it compares candidate development with the initial design search, which are different things.
- All of these results come from the developer (press release plus a preprint). I found no independent replication.
- Earlier documented ESM result: ESM3 esmGFP, Science 2025, 58% identity, "simulating 500 million years of evolution".

## Row 2: Evo 2
- Peer-reviewed: Nature 2026 (published 2026-03-04), doi 10.1038/s41586-026-10176-5.
- BRCA1 data: Findlay et al. 2018 saturation genome editing; SNVs only (coding n=2,077, noncoding n=1,125).
- Zero-shot: the text gives no single number ("strong performance on coding SNVs and outperformed all other models on BRCA1 noncoding SNVs"). The values are in the figures only.
- Supervised: a ridge classifier on Evo 2 40B embeddings scored AUROC 0.95 and AUPRC 0.88 on the test set (n=789).
- "Over 90% accuracy" comes from the Arc Institute press release (2025-02-19). The paper reports AUROC, not accuracy. So "accuracy" is the wrong metric word, and the >0.9 figure is for the supervised classifier.
- NVIDIA's zero-shot replication with smaller models gave AUROC 0.73 (Arc 1B), 0.76 (BioNeMo 1B) and 0.87 (BioNeMo 7B). NVIDIA co-developed Evo 2, so this is not fully independent.
- Open source: code, weights and the OpenGenome2 dataset are all Apache-2.0 (LICENSE file and HF metadata). The paper itself is CC BY-NC-ND.

## Row 3: AlphaGenome
- Peer-reviewed: Nature 2026-01-28, doi 10.1038/s41586-025-10014-0.
- Input "1 Mb of DNA sequence" is confirmed. Output is "up to single-base-pair resolution": RNA-seq, ATAC and DNase tracks at 1 bp, ChIP at 128 bp, contact maps at 2,048 bp.
- Speed: the paper says "Taking less than 1 s on an NVIDIA H100 GPU", for the distilled student model with one device call per variant across all modalities. The blog says "in a second" and gives no hardware. These are developer claims about local inference, not API latency.
- Access: API for non-commercial use. Code is Apache 2.0. Weights are on Kaggle and HF under non-commercial model terms, available since the Jan 2026 publication. The June 2025 blog had said the model would be released "in the future".

## Row 4: AlphaFold DB
- The home page headline says "over 260 million protein structure predictions". The same page's Background section still says "over 200 million entries". The licence is CC-BY-4.0, for academic and commercial use.

## Speaker-note framing not supported by any source
- "tested them at the bench in days": not supported. Only the design/search took days.
- "Each row compresses a technique that takes a decade to learn": no source. This is the speaker's own framing.
