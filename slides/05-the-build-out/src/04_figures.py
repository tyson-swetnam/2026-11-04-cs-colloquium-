"""Charts for the slide, written to figures/ as PNG (for the deck) and SVG.

    fig1_baseline_cpi.png       Moorhouse's chart rebuilt from primary sources (2024 dollars)
    fig2_cumulative_gdp.png     the same programs, plus private booms, as cumulative share of GDP
    fig3_peak_year.png          each build-out's biggest single year as a share of GDP
    fig2b_first_decade_gdp.png  the first ten years of every program, where data centers actually are
    fig4_rank_shift.png         rank under Moorhouse's measure vs. rank under share of GDP
    fig5_boom_intensity.png     average annual spend as a share of GDP, every boom on one ruler

Color does one job: data centers in UNM cherry, private booms in blue, public programs in
gray. Every line is labeled directly, so identity never depends on color.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import yaml  # noqa: E402

import config  # noqa: E402
from evidence import style  # noqa: E402

FIG = config.FIGURES
P = config.PARTIAL_YEAR
PRIVATE = "#2a78d6"
PUBLIC = "#767676"
SHORT = {
    "datacenters_global": "Data centers, global (5 US hyperscalers)",
    "datacenters_us_structures": "Data centers, US buildings only (BEA)",
    "oil_gas_1970s": "Oil & gas boom 1973–82",
    "oil_gas_shale": "Shale boom 2008–15",
    "telecom": "Telecom & fiber 1995–2002",
    "postwar": "Post-war private investment 1946–60",
    "railroads": "US railroads 1830–1900",
    "railroads_vn": "Railroads 1870–90",
    "canals": "Canals 1836–41",
    "electrification": "Electrification 1905–25",
    "highways": "All highways 1956–73",
    "interstate": "Interstate Highways 1956–92",
    "apollo": "Apollo",
    "manhattan": "Manhattan Project",
    "marshall": "Marshall Plan",
    "f35": "F-35",
    "iss": "ISS",
}


def color(pid: str, meta: dict) -> str:
    if pid.startswith("datacenters"):
        return style.CHERRY
    return PRIVATE if meta.get(pid, {}).get("financing") in ("private", "mixed") else PUBLIC


def spread(points: list[tuple[float, float]], gap: float, xwin: float) -> list[float]:
    """Nudge label y-positions apart so labels within `xwin` of each other sit at least `gap` apart."""
    order = sorted(range(len(points)), key=lambda i: points[i][1])
    out = [y for _, y in points]
    for k, i in enumerate(order):
        for j in order[:k]:
            if abs(points[i][0] - points[j][0]) < xwin and out[i] - out[j] < gap:
                out[i] = out[j] + gap
    return out


def lines(ax, norm, col, meta, programs, scale=1.0, label_gap=None, xwin=6):
    """Plot cumulative or annual series per program, starting from (0, 0); dashed into the partial year."""
    ends = []
    for pid in programs:
        g = norm[norm.program == pid].sort_values("year")
        if g.empty:
            continue
        c = color(pid, meta)
        lw = 3.2 if pid.startswith("datacenters") else 2.0
        x = [0, *g.years_since_start]
        y = [0, *(g[col] * scale)]
        n = len(g) - int(g.partial.any())  # points from complete years
        ax.plot(x[: n + 1], y[: n + 1], color=c, lw=lw, solid_capstyle="round")
        if g.partial.any():
            ax.plot(x[n:], y[n:], color=c, lw=lw, ls=(0, (2, 2)))
            ax.plot(x[-1], y[-1], "o", ms=8, mfc="white", mec=c, mew=2)
        ax.plot(x[n], y[n], "o", ms=8, color=c)
        ends.append((pid, x[n], y[n], c, g.iloc[n - 1]))
    if label_gap is not None:
        placed = spread([(e[1], e[2]) for e in ends], label_gap, xwin)
        for (pid, x, y, c, last), ly in zip(ends, placed):
            moved = abs(ly - y) > label_gap / 4
            if moved:
                ax.plot([x, x], [y, ly], color=c, lw=0.8, alpha=0.6)
            ax.annotate(
                SHORT.get(pid, pid),
                (x, ly),
                xytext=(8, 0),
                textcoords="offset points",
                va="center",
                xycoords="data",
                fontsize=13,
                color=style.INK,
                fontweight="bold" if pid.startswith("datacenters") else "normal",
            )
    return ends


def finish(fig, ax, title, subtitle, source, name):
    ax.set_title(title, loc="left", pad=36)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=15, color=style.MUTED)
    fig.text(0.01, -0.02, source, fontsize=11, color=style.MUTED, wrap=True)
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{name}.{ext}")
    plt.close(fig)
    print(f"wrote figures/{name}.png")


def main() -> None:
    style.use()
    FIG.mkdir(exist_ok=True)
    norm = pd.read_csv(config.PROCESSED / "normalized.csv")
    rank = pd.read_csv(config.PROCESSED / "ranking.csv")
    meta = {c["id"]: c for c in yaml.safe_load((config.SLIDE / "comparators.yaml").read_text())["programs"]}
    have = set(norm.program)
    moorhouse_set = [p for p in ("railroads", "interstate", "f35", "apollo", "marshall", "iss", "manhattan", "datacenters_global") if p in have]
    private_set = [p for p in ("oil_gas_1970s", "oil_gas_shale", "telecom") if p in have]
    src = (
        "Sources: SEC EDGAR (hyperscaler capex, data-center share per Moorhouse/Epoch AI); BEA NIPA; MeasuringWorth "
        "(GDP, CPI); program sources in data/raw/programs/SOURCES.md. Dashed = 2026, Q1–Q3 scaled to a full year. "
        "github.com/tyson-swetnam/2026-11-04-cs-colloquium-"
    )

    # 1. Baseline: Moorhouse's measure, our data
    fig, ax = plt.subplots()
    lines(ax, norm, "cum_cpi_real_2024", meta, moorhouse_set, scale=1e-3, label_gap=30, xwin=12)
    for pid in moorhouse_set:
        mh = meta[pid].get("in_moorhouse")
        if mh:
            ax.plot(mh["span_years"], mh["value_busd"], "D", ms=9, mfc="none", mec=style.INK, mew=1.2)
    ax.plot([], [], "D", ms=9, mfc="none", mec=style.INK, label="Value printed on Moorhouse's chart")
    ax.legend(loc="upper right")
    ax.set_xlim(0, 80)
    ax.set_ylim(0, None)
    ax.set_xlabel("Years from start of program")
    ax.set_ylabel("Cumulative cost, billions of 2024 dollars (CPI)")
    finish(fig, ax, "Data centers vs. megaprojects, rebuilt", "Moorhouse's measure: inflation-adjusted dollars", src, "fig1_baseline_cpi")

    # 2. Cumulative share of GDP: Moorhouse's programs, re-measured
    fig, ax = plt.subplots()
    dc_both = [p for p in ("datacenters_global", "datacenters_us_structures") if p in have]
    lines(ax, norm, "cum_share_us_gdp", meta, [p for p in ("railroads", "interstate") if p in have] + dc_both, scale=100, label_gap=3.2, xwin=12)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, None)
    ax.set_xlabel("Years from start of program")
    ax.set_ylabel("Cumulative spend, % of one year's US GDP")
    finish(
        fig,
        ax,
        "Six years vs. 71 years of railroads and 37 of Interstates",
        "Each year's spend as a share of that year's GDP, summed. Cherry: data centers · Blue: private · Gray: public",
        src,
        "fig2_cumulative_gdp",
    )

    # 2b. The first decade, where the data-center build actually is
    fig, ax = plt.subplots()
    first = [*dc_both, "railroads", "interstate", "highways", "apollo", "marshall", "manhattan", *private_set]
    first = [p for p in first if p in have]
    clipped = norm[norm.years_since_start <= 10]
    lines(ax, clipped, "cum_share_us_gdp", meta, first, scale=100, label_gap=0.5, xwin=2.5)
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, None)
    ax.set_xlabel("Years from start of program")
    ax.set_ylabel("Cumulative spend, % of one year's US GDP")
    finish(fig, ax, "The first ten years", "Cumulative spend as a share of GDP; longer programs cut off at year 10. Cherry: data centers · Blue: private · Gray: public", src, "fig2b_first_decade_gdp")

    # 3. Peak year: the most each build-out took from the economy in a single year
    peak_year(norm, meta, [p for p in [*dc_both, "railroads", "canals", "electrification", "highways", "interstate", "apollo", "marshall", "manhattan", *private_set] if p in have], src)

    # 4. Rank shift: CPI dollars vs share of GDP (complete years only)
    r = rank[~rank.program.str.contains(r"\(incl\.") & (rank.program != "postwar")].copy()
    r["rank_cpi"] = r.cpi_real_2024_busd.rank(ascending=False).astype(int)
    r["rank_gdp"] = r.gdp_years_pct.rank(ascending=False).astype(int)
    fig, ax = plt.subplots(figsize=(12, 10))
    for _, row in r.iterrows():
        c = color(row.program, meta)
        lw = 3.2 if row.program.startswith("datacenters") else 2.0
        ax.plot([0, 1], [row.rank_cpi, row.rank_gdp], color=c, lw=lw, marker="o", ms=8)
        name = SHORT.get(row.program, row.program)
        ax.text(-0.04, row.rank_cpi, f"{name}  ${row.cpi_real_2024_busd:,.0f}B", ha="right", va="center", fontsize=13, color=style.INK)
        ax.text(1.04, row.rank_gdp, f"{row.gdp_years_pct:.1f}%  {name}", ha="left", va="center", fontsize=13, color=style.INK)
    ax.set_ylim(len(r) + 0.5, 0.5)
    ax.set_xlim(-0.05, 1.05)
    ax.set_xticks([0, 1], ["Rank in 2024 dollars", "Rank in share of GDP"])
    ax.set_yticks([])
    ax.grid(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    finish(fig, ax, "Same programs, different ruler", "Cumulative cost through the last complete year", src, "fig4_rank_shift")

    boom_intensity(norm, meta, src)


def peak_year(norm, meta, programs, src):
    rows = []
    for pid in programs:
        g = norm[norm.program == pid]
        for label, h in (("", g[~g.partial]), (" (2026 est.)", g[g.partial])):
            if h.empty:
                continue
            top = h.loc[h.share_us_gdp.idxmax()]
            rows.append((SHORT.get(pid, pid) + label, 100 * top.share_us_gdp, int(top.year), color(pid, meta), bool(label)))
    rows.sort(key=lambda r: r[1], reverse=True)
    fig, ax = plt.subplots(figsize=(14, 10))
    for i, (label, val, year, c, est) in enumerate(rows):
        ax.barh(i, val, height=0.62, color="white" if est else c, edgecolor=c, linewidth=2, hatch="//" if est else None)
        ax.text(val + 0.06, i, f"{val:.1f}% in {year}", va="center", fontsize=14, color=style.INK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=14)
    ax.invert_yaxis()
    ax.set_xlim(0, max(r[1] for r in rows) * 1.25)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Spend in the peak year, % of that year's US GDP")
    finish(
        fig,
        ax,
        "How hard each build-out pushed",
        "The single biggest year. Cherry: data centers · Blue: private · Gray: public · Hatched: estimate",
        src + " Marshall Plan FY1949 covers 15 months.",
        "fig3_peak_year",
    )


def boom_intensity(norm, meta, src):
    """Average annual % of GDP per boom, in Van Nieuwerburgh's (2026) Table 1 windows.

    Every bar is computed here except the 2025-32 projection, which is his; 05_validate.py
    checks the historical bars against his table.
    """

    def avg(pid, y0, y1):
        g = norm[(norm.program == pid) & norm.year.between(y0, y1)]
        return 100 * g.share_us_gdp.mean()

    bars = [
        ("Canals 1836–41", avg("canals", 1836, 1841), PUBLIC, "ours"),
        ("Railroads 1870–90", avg("railroads_vn", 1870, 1890), PRIVATE, "ours"),
        ("Electrification 1905–25", avg("electrification", 1905, 1925), PRIVATE, "ours"),
        ("Highways 1956–73", avg("highways", 1956, 1973), PUBLIC, "ours"),
        ("Oil & gas boom 1973–82", avg("oil_gas_1970s", 1973, 1982), PRIVATE, "ours"),
        ("Telecom & fiber 1996–2003", avg("telecom_vn", 1996, 2003), PRIVATE, "ours"),  # = VN 1.10, see 05_validate
        ("Shale boom 2008–15", avg("oil_gas_shale", 2008, 2015), PRIVATE, "ours"),
        ("Data centers 2020–25", avg("datacenters_global", 2020, 2025), style.CHERRY, "ours"),
        ("Data centers 2026 (est.)", avg("datacenters_global", 2026, 2026), style.CHERRY, "ours"),
        ("AI build-out 2025–32 (projected)", 3.63, style.CHERRY, "VN"),
    ]
    fig, ax = plt.subplots(figsize=(14, 9))
    for i, (label, val, c, who) in enumerate(bars):
        projected = "projected" in label or "est." in label
        ax.barh(i, val, height=0.62, color="white" if projected else c, edgecolor=c, linewidth=2, hatch="//" if projected else None)
        tag = "" if who == "ours" else "  (Van Nieuwerburgh)"
        ax.text(val + 0.05, i, f"{val:.2f}%{tag}", va="center", fontsize=14, color=style.INK)
    ax.set_yticks(range(len(bars)), [b[0] for b in bars], fontsize=15)
    ax.invert_yaxis()
    ax.set_xlim(0, 4.6)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Average annual spend, % of that year's US GDP")
    src2 = src + " Windows and the AI 2025–32 projection: Van Nieuwerburgh (2026), BPEA, Table 1."
    finish(fig, ax, "Every boom on one ruler", "Cherry: data centers (global capex of 5 US hyperscalers ÷ US GDP) · Blue: private · Gray: public · Hatched: estimate", src2, "fig5_boom_intensity")


if __name__ == "__main__":
    main()
