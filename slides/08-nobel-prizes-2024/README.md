# Slide 08 · Two Nobel Prizes for AI-related work

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-08)

All three claims check out against the Nobel Prize API and the Royal Swedish Academy's press release (`src/01_nobel.py`, [`nobel_check.csv`](data/processed/nobel_check.csv), [`nobel_quotes.csv`](data/processed/nobel_quotes.csv)).

| | Official record | On the slide |
|---|---|---|
| **Physics 2024** | John J. Hopfield (1/2), Geoffrey Hinton (1/2): "for foundational discoveries **and inventions** that enable machine learning with artificial neural networks" | Hopfield & Hinton: "Foundational discoveries enabling machine learning with artificial neural networks" |
| **Chemistry 2024** | David Baker (1/2) "for computational protein design"; Demis Hassabis (1/4) and John Jumper (1/4) "for protein structure prediction" | Baker, Hassabis & Jumper: "Computational protein design, and protein structure prediction" |

- **Physics:** the slide drops "and inventions." The exact wording is listed as an optional edit in [`CLAIMS.md`](../../CLAIMS.md).
- **"AI-related":** this matches the Academy's own framing. Its popular-science background is titled "They have revealed proteins' secrets through computing and artificial intelligence," and the press release says Hassabis and Jumper "developed an AI model to solve a 50-year-old problem." If someone pushes back: Baker's landmark 2003 design was computational (the Rosetta software), not AI.
- **For slide 09:** the same press release says AlphaFold2 has been used "to predict the structure of virtually all the 200 million proteins that researchers have identified."

```bash
uv run python slides/08-nobel-prizes-2024/src/01_nobel.py
```
