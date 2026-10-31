"""Control 1, "It invents citations": make the agent call a real index.

Runs the same checker (evidence/citations.py: DOI registry + arXiv) over two sets:
    hallucinated  100 citations GPTZero found and human-verified in accepted NeurIPS 2025 papers
    real          the 141-entry bibliography of BloombergGPT (arXiv:2303.17564), a published paper

Outputs: data/processed/citations_{hallucinated,real}.csv and citations_summary.csv
"""

from __future__ import annotations

import tarfile

import pandas as pd
from bs4 import BeautifulSoup

import config
from evidence import citations as cit
from evidence.fetch import fetch

RAW, OUT = config.RAW / "citations", config.PROCESSED


def hallucinated() -> pd.DataFrame:
    path = fetch(
        "https://gptzero.me/news/neurips/",
        RAW / "sources" / "gptzero_neurips.html",
        source="GPTZero, 'GPTZero finds 100 new hallucinations in NeurIPS 2025 accepted papers' (Jan. 21, 2026)",
        license="quoted for research; citations themselves are from published NeurIPS papers",
        user_agent=config.UA,
    )
    table = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser").find("table")
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cells) == 4:
            rows.append({"paper": cells[0], "citation": cells[2], "gptzero_comment": cells[3]})
    df = pd.DataFrame(rows)
    df.to_csv(RAW / "gptzero_neurips_2025_hallucinations.csv", index=False)
    return df


def real() -> pd.DataFrame:
    path = fetch(
        "https://arxiv.org/e-print/2303.17564",
        RAW / "sources" / "arxiv_2303.17564_src.tar.gz",
        source="arXiv e-print source, BloombergGPT (Wu et al. 2023)",
        license="arXiv distribution licence; bibliography used as test data",
        user_agent=config.UA,
    )
    with tarfile.open(path) as tar:
        bbl = next(tar.extractfile(m).read().decode("utf-8", "replace") for m in tar.getmembers() if m.name.endswith(".bbl"))
    return pd.DataFrame({"citation": cit.bibitems(bbl)})


def run(df: pd.DataFrame, parser, checker: cit.Checker, label: str) -> pd.DataFrame:
    out = []
    for i, raw in enumerate(df.citation):
        c = parser(raw)
        r = checker.check(c)
        out.append({"title": c.title, "surnames": " ".join(c.surnames), "doi": c.doi, "arxiv_id": c.arxiv_id, "verdict": r.verdict, "detail": r.detail, "index_title": r.index_title})
        if i % 20 == 0:
            print(f"{label}: {i}/{len(df)}", flush=True)
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(out)], axis=1)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checker = cit.Checker(config.CACHE / "citations", config.UA)
    h = run(hallucinated(), cit.parse, checker, "hallucinated")
    r = run(real(), cit.parse_bibitem, checker, "real")
    h.to_csv(OUT / "citations_hallucinated.csv", index=False)
    r.drop(columns=["citation"]).to_csv(OUT / "citations_real.csv", index=False)
    summary = pd.concat(
        [h.verdict.value_counts().rename("hallucinated"), r.verdict.value_counts().rename("real")], axis=1
    ).fillna(0).astype(int)
    summary.loc["total"] = summary.sum()
    summary.to_csv(OUT / "citations_summary.csv")
    print(summary.to_string())
    print(f"flagged: hallucinated {100 * (h.verdict != 'verified').mean():.0f}%  real {100 * (r.verdict != 'verified').mean():.0f}%")


if __name__ == "__main__":
    main()
