"""Evo 2 and AlphaGenome: read the headline numbers out of the peer-reviewed papers themselves.

Full texts come from Europe PMC (open access). Each check is a sentence the slide depends on.
Output: data/processed/paper_checks.csv
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
PAPERS = {
    "Evo 2 (Brixi et al., Nature 2026)": ("PMC13128491", [
        ("BRCA1 classifier on Evo 2 embeddings", r"AUROC = (0\.\d+), AUPRC = (0\.\d+)"),
        ("BRCA1 data: coding SNVs", r"coding \( n = ([\d,]+) SNVs\)"),
        ("openness", r"(fully open, including model parameters, training code)(?: \d+ ?)?, (inference code and the OpenGenome2 dataset)"),  # a reference number sits after "training code"
    ]),
    "AlphaGenome (Avsec et al., Nature 2026)": ("PMC12851941", [
        ("input length and resolution", r"takes as input (1 Mb) of DNA sequence and predicts thousands of functional genomic tracks up to (single-base-pair) resolution"),
        ("variant scoring time", r"Taking (less than 1 s on an NVIDIA H100 GPU)"),
    ]),
}


def sentence(text: str, m: re.Match) -> str:
    start = max(text.rfind(". ", 0, m.start()) + 2, m.start() - 250)
    end = text.find(". ", m.end())
    return text[start : end + 1 if end > 0 else m.end()]


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache" / "europepmc", UA)
    rows = []
    for paper, (pmcid, checks) in PAPERS.items():
        status, xml = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", xml))) if status == 200 else ""
        for what, pattern in checks:
            m = re.search(pattern, text)
            rows.append({"paper": paper, "pmcid": pmcid, "check": what, "found": bool(m), "values": "; ".join(m.groups()) if m else "", "sentence": sentence(text, m) if m else ""})
    df = pd.DataFrame(rows)
    out = SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "paper_checks.csv", index=False)
    print(df[["paper", "check", "found", "values"]].to_string(index=False))


if __name__ == "__main__":
    main()
