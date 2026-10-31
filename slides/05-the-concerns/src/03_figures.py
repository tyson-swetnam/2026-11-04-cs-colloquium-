"""Figures for slide 05 (PNG for the deck, SVG for editing).

    fig1_capex_vs_cash.png   hyperscaler capex vs. operating cash flow, 2019 to the last 12 months
    fig2_debt.png            total debt per firm, end of FY2024 vs. latest filing
    fig3_new_mexico.png      one proposed campus (Project Jupiter) against New Mexico's electricity use
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import config  # noqa: E402
from evidence import style  # noqa: E402

OUT, FIG = config.PROCESSED, config.FIGURES
CAPEX, CASH = style.CHERRY, "#2a78d6"  # validated pair (see slide 04)
SRC = "Source: SEC EDGAR XBRL filings (cash capex = purchases of property and equipment). github.com/tyson-swetnam/2026-11-04-cs-colloquium-"


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{name}.{ext}")
    plt.close(fig)
    print(f"wrote figures/{name}.png")


def capex_vs_cash():
    annual = pd.read_csv(OUT / "hyperscaler_annual.csv", index_col="year")
    ttm = pd.read_csv(OUT / "hyperscaler_ttm.csv", index_col="calendar_quarter")
    last_q = ttm.index[-1]
    rows = [(str(y), annual.capex[y], annual.ocf[y]) for y in annual.index if not annual.partial[y]]
    rows.append((f"12 mo. to\n{last_q}", ttm.capex.iloc[-1], ttm.ocf.iloc[-1]))
    x = np.arange(len(rows))
    w = 0.38
    fig, ax = plt.subplots()
    ax.bar(x - w / 2 - 0.01, [r[2] / 1e9 for r in rows], w, color=CASH, label="Operating cash flow")
    ax.bar(x + w / 2 + 0.01, [r[1] / 1e9 for r in rows], w, color=CAPEX, label="Capital expenditure")
    for i, (_, capex, ocf) in enumerate(rows):
        ax.text(i, max(capex, ocf) / 1e9 + 15, f"{capex / ocf:.0%}", ha="center", fontsize=15, color=style.INK, fontweight="bold" if i == len(rows) - 1 else "normal")
    ax.set_xticks(x, [r[0] for r in rows])
    ax.set_ylabel("Billions of dollars, five firms combined")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left")
    ax.set_title("Capex is catching up with the cash", loc="left", pad=36)
    ax.text(0, 1.02, "Amazon, Microsoft, Alphabet, Meta, Oracle · % = capex as a share of operating cash flow", transform=ax.transAxes, fontsize=15, color=style.MUTED)
    fig.text(0.01, -0.02, SRC + " Calendar years; Microsoft and Oracle fiscal quarters re-summed.", fontsize=11, color=style.MUTED, wrap=True)
    save(fig, "fig1_capex_vs_cash")


def debt():
    d = pd.read_csv(OUT / "hyperscaler_debt_change.csv")
    d = d.sort_values("latest_debt")
    y = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(14, 7))
    for i, r in enumerate(d.itertuples()):
        ax.plot([r.base_debt / 1e9, r.latest_debt / 1e9], [i, i], color=style.MUTED, lw=2, zorder=1)
        ax.plot(r.base_debt / 1e9, i, "o", ms=11, mfc="white", mec=style.INK, mew=2, zorder=2)
        ax.plot(r.latest_debt / 1e9, i, "o", ms=11, color=CAPEX, zorder=3)
        ax.text(max(r.base_debt, r.latest_debt) / 1e9 + 4, i, f"${r.base_debt / 1e9:.0f}B → ${r.latest_debt / 1e9:.0f}B", va="center", fontsize=14, color=style.INK)
    ax.set_yticks(y, d.company, fontsize=15)
    ax.set_xlim(0, d.latest_debt.max() / 1e9 * 1.3)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Total debt on the balance sheet, $ billions")
    total0, total1 = d.base_debt.sum() / 1e9, d.latest_debt.sum() / 1e9
    ax.set_title(f"Debt up from ${total0:.0f}B to ${total1:.0f}B", loc="left", pad=36)
    ax.text(0, 1.02, "Open circle: end of fiscal 2024 · Filled: latest 10-Q/10-K (Sept. 2026; Oracle May 2026)", transform=ax.transAxes, fontsize=15, color=style.MUTED)
    fig.text(0.01, -0.03, SRC + " Excludes off-balance-sheet leases and project debt.", fontsize=11, color=style.MUTED, wrap=True)
    save(fig, "fig2_debt")


def new_mexico():
    env = pd.read_csv(OUT / "environment_nm.csv").set_index("quantity").value
    facts = pd.read_csv(config.RAW / "environment" / "facts.csv", index_col="id")
    pnm_sales = float(str(facts.loc["D5", "value"]).replace(",", "")) / 1e6  # MWh -> TWh
    bars = [
        ("New Mexico, all retail sales (2024)", env["nm_retail_sales_twh"], style.MUTED, False),
        ("PNM, all retail sales (2024)", pnm_sales, style.MUTED, False),
        ("Project Jupiter at full nameplate (2,462 MW)", env["Project Jupiter at nameplate, TWh/yr (upper bound)"], CAPEX, True),
        ("Project Jupiter at its proposed 1,600 MW cap", env["Project Jupiter at 1,600 MW cap, TWh/yr (upper bound)"], CAPEX, True),
    ]
    fig, ax = plt.subplots(figsize=(14, 6.5))
    for i, (label, v, c, upper) in enumerate(bars):
        ax.barh(i, v, height=0.6, color="white" if upper else c, edgecolor=c, linewidth=2, hatch="//" if upper else None)
        ax.text(v + 0.4, i, f"{v:.1f} TWh", va="center", fontsize=15, color=style.INK)
    ax.set_yticks(range(len(bars)), [b[0] for b in bars], fontsize=15)
    ax.invert_yaxis()
    ax.set_xlim(0, max(b[1] for b in bars) * 1.2)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Electricity per year, terawatt-hours")
    ax.set_title("One proposed campus vs. New Mexico", loc="left", pad=36)
    ax.text(0, 1.02, "Project Jupiter, Santa Teresa (Doña Ana County) · hatched = if run all year; air permit hearing Dec. 7, 2026", transform=ax.transAxes, fontsize=15, color=style.MUTED)
    fig.text(
        0.01, -0.04,
        "Sources: EIA New Mexico Electricity Profile 2024; NMED notice AQB 26-57 (NSR 10883, 2,462 MW fuel cells); "
        "1,600 MW cap per revised application (Albuquerque Journal, Oct. 27, 2026). github.com/tyson-swetnam/2026-11-04-cs-colloquium-",
        fontsize=11, color=style.MUTED, wrap=True,
    )
    save(fig, "fig3_new_mexico")


def main():
    style.use()
    FIG.mkdir(exist_ok=True)
    capex_vs_cash()
    debt()
    new_mexico()


if __name__ == "__main__":
    main()
