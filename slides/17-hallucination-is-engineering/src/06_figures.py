"""Figure for slide 17: what the citation check does to real and to hallucinated references.

    fig1_citation_check.png   verdicts for 100 hallucinated (GPTZero, NeurIPS 2025) and 141 real citations
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

import config  # noqa: E402
from evidence import style  # noqa: E402

# One hue per verdict family: verified (pass) vs. the three ways a citation fails vs. unverifiable.
ORDER = [
    ("verified", "Verified in an index", "#2a78d6", None),
    ("identifier_mismatch", "ID points to another work", style.CHERRY, None),
    ("bad_identifier", "ID does not exist", style.CHERRY, "//"),
    ("author_mismatch", "Title real, authors wrong", style.CHERRY, ".."),
    ("not_found", "Not found (needs review)", "#b4b4b4", None),
]


def main() -> None:
    style.use()
    config.FIGURES.mkdir(exist_ok=True)
    sets = {
        "Hallucinated\n(GPTZero, NeurIPS 2025)": pd.read_csv(config.PROCESSED / "citations_hallucinated.csv"),
        "Real\n(BloombergGPT references)": pd.read_csv(config.PROCESSED / "citations_real.csv"),
    }
    fig, ax = plt.subplots(figsize=(16, 6.5))
    for i, (label, df) in enumerate(sets.items()):
        left, n = 0.0, len(df)
        for key, name, color, hatch in ORDER:
            share = (df.verdict == key).mean() * 100
            if share == 0:
                continue
            ax.barh(i, share, left=left, height=0.55, color="white" if hatch else color, edgecolor=color if hatch else "white", hatch=hatch, linewidth=2 if hatch else 1)
            if share >= 6:
                ax.text(left + share / 2, i, f"{share:.0f}%", ha="center", va="center", fontsize=14, color=style.INK if hatch or color == "#b4b4b4" else "white", fontweight="bold")
            left += share
        ax.text(101, i, f"n = {n}", va="center", fontsize=13, color=style.MUTED)
    ax.set_yticks(range(len(sets)), list(sets), fontsize=15)
    ax.invert_yaxis()
    ax.set_xlim(0, 108)
    ax.set_xlabel("Share of citations, %")
    ax.grid(axis="y", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor="white" if h else c, edgecolor=c, hatch=h, linewidth=2 if h else 0) for _, _, c, h in ORDER]
    ax.legend(handles, [n for _, n, _, _ in ORDER], loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=5, fontsize=12)
    ax.set_title("A real index catches invented citations", loc="left", pad=36)
    ax.text(0, 1.02, "Same checker for both sets: DOI registry + arXiv, by identifier or title, with an author check", transform=ax.transAxes, fontsize=15, color=style.MUTED)
    fig.text(
        0.01, -0.2,
        "Sources: GPTZero (Jan. 2026), 100 human-verified hallucinated citations in accepted NeurIPS 2025 papers; Wu et al. (2023) BloombergGPT "
        "bibliography, arXiv:2303.17564. Indexes: doi.org, arXiv API. github.com/tyson-swetnam/2026-11-04-cs-colloquium-",
        fontsize=11, color=style.MUTED, wrap=True,
    )
    for ext in ("png", "svg"):
        fig.savefig(config.FIGURES / f"fig1_citation_check.{ext}")
    print("wrote figures/fig1_citation_check.png")


if __name__ == "__main__":
    main()
