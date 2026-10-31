"""Researchers' work in closed systems: how much training text is scholarly, and under what licence.

    The Pile (open; Gao et al. 2020, Table 1) and BloombergGPT (closed weights; Wu et al. 2023,
    Table 2) are parsed from their arXiv LaTeX sources, read straight from the downloaded tarballs.
    PubMed Central licence counts come from NCBI E-utilities responses saved by
    src/research/pmc_counts.sh on 2026-10-30 (counts change daily).

Output: data/processed/corpus_shares.csv
"""

from __future__ import annotations

import json
import re
import tarfile

import pandas as pd

import config
from evidence.fetch import fetch

CS = config.RAW / "closed_systems"
SCHOLARLY = ["PubMed Central", "ArXiv", "PhilPapers", "PubMed Abstracts", "NIH ExPorter"]
FULL_TEXT = SCHOLARLY[:3]


def arxiv_tex(arxiv_id: str, member_hint: str) -> str:
    """The LaTeX file in an arXiv e-print tarball that contains `member_hint`, without extracting to disk."""
    path = fetch(
        f"https://arxiv.org/e-print/{arxiv_id}",
        CS / "sources" / f"arxiv_{arxiv_id}_src.tar.gz",
        source=f"arXiv e-print source, {arxiv_id}",
        license="arXiv distribution licence; used for table extraction only",
    )
    with tarfile.open(path) as tar:
        for m in tar.getmembers():
            if m.isfile() and m.name.endswith(".tex"):
                text = tar.extractfile(m).read().decode("utf-8", errors="replace")
                if member_hint in text:
                    return text
    raise ValueError(f"no .tex in {arxiv_id} contains {member_hint!r}")


def pile_table() -> pd.DataFrame:
    tex = arxiv_tex("2101.00027", "table:pile_overview")
    body = tex[tex.index(r"\textbf{Component} & \textbf{Raw Size}") : tex.index(r"\label{table:pile_overview}")]
    rows = []
    for line in body.splitlines():
        m = re.match(r"\s*(.+?)\s*&\s*([\d.]+) GiB\s*&\s*([\d.]+)\\%\s*&\s*([\d.]+)\s*&\s*([\d.]+) GiB", line)
        if m:
            rows.append((re.sub(r"\\textsuperscript\{\\textdagger\}", "", m.group(1)).strip(), float(m.group(5))))
    df = pd.DataFrame(rows, columns=["component", "size"])
    assert len(df) == 22 and abs(df["size"].sum() - 1254.20) < 0.1, "Pile Table 1 did not parse as published"
    return df


def bloomberg_table() -> pd.DataFrame:
    tex = arxiv_tex("2303.17564", r"\label{tab:data}")
    body = tex[: tex.index(r"\label{tab:data}")]
    body = body[body.rindex(r"\begin{tabular}") :]
    rows = []
    for line in body.splitlines():
        cells = [c.strip() for c in line.split("&")]
        if len(cells) == 7 and not cells[0].startswith(("\\textit", "\\multicolumn")):
            rows.append((cells[0], float(cells[5].replace(",", ""))))  # tokens, 1e8
    df = pd.DataFrame(rows, columns=["component", "size"])
    total = 7089.0
    assert abs(df["size"].sum() - total) <= 5, f"BloombergGPT Table 2 rows sum to {df['size'].sum()}, not {total}"
    return df


def share(df: pd.DataFrame, names: list[str]) -> float:
    missing = set(names) - set(df.component)
    assert not missing, missing
    return df[df.component.isin(names)]["size"].sum() / df["size"].sum()


def main() -> None:
    rows = []
    pile, bbg = pile_table(), bloomberg_table()
    rows += [
        ("The Pile (open)", "full-text papers (PMC, arXiv, PhilPapers)", 100 * share(pile, FULL_TEXT), "% of effective size"),
        ("The Pile (open)", "all scholarly (+ PubMed abstracts, NIH grants)", 100 * share(pile, SCHOLARLY), "% of effective size"),
        ("BloombergGPT (closed weights)", "all scholarly (+ PubMed abstracts, NIH grants)", 100 * share(bbg, SCHOLARLY), "% of training tokens"),
        ("BloombergGPT (closed weights)", "scholarly tokens", bbg[bbg.component.isin(SCHOLARLY)]["size"].sum() / 10, "billion tokens"),
    ]
    counts = {p.stem.removeprefix("esearch_pmc_"): int(json.loads(p.read_text())["esearchresult"]["count"]) for p in (CS / "pmc").glob("*.json")}
    total = counts["all_pmc"]
    rows += [
        ("PubMed Central", "articles", total, "count (2026-10-30)"),
        ("PubMed Central", "CC licence allowing commercial reuse", 100 * counts["commercial_ok"] / total, "% of articles"),
        ("PubMed Central", "non-commercial CC licence only", 100 * counts["noncommercial_only"] / total, "% of articles"),
        ("PubMed Central", "in neither bulk-reuse subset", 100 * (total - counts["oa_or_am"]) / total, "% of articles"),
    ]
    out = pd.DataFrame(rows, columns=["corpus", "measure", "value", "unit"])
    config.PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.PROCESSED / "corpus_shares.csv", index=False, float_format="%.4g")
    print(out.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
