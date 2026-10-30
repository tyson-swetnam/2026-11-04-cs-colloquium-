"""Put every comparator on the same axes, under every measure.

Outputs
    spend_long.csv   program, year, nominal spend (millions), source, partial-year flag
    normalized.csv   one row per program-year with each measure, annual and cumulative
    ranking.csv      one row per program: totals under each measure, peak and first-6-year intensity
"""

from __future__ import annotations

import pandas as pd
import yaml

import config
from evidence import econ

OUT = config.PROCESSED
REF, P = config.REF_YEAR, config.PARTIAL_YEAR

# Private comparators taken straight from BEA NIPA (current dollars, millions).
BEA_PROGRAMS = {
    "oil_gas_1970s": (["C319RC"], 1973, 1982),
    "oil_gas_shale": (["C319RC"], 2008, 2015),
    "telecom": (["C275RC", "C314RC"], 1995, 2002),
    "postwar": (["A007RC"], 1946, 1960),
    "datacenters_us_structures": (["LA001282"], 2020, P),
}


def spend_long() -> pd.DataFrame:
    bea = pd.read_csv(OUT / "bea_series.csv", index_col="year")
    frames = []
    for pid, (codes, y0, y1) in BEA_PROGRAMS.items():
        s = bea.loc[y0:y1, codes].sum(axis=1)
        frames.append(pd.DataFrame({"program": pid, "year": s.index, "nominal_musd": s.values, "source": "BEA NIPA " + "+".join(codes)}))

    dc = pd.read_csv(OUT / "hyperscaler_capex_annual.csv", index_col="year").loc[2020:P]
    frames.append(
        pd.DataFrame(
            {
                "program": "datacenters_global",
                "year": dc.index,
                "nominal_musd": dc.dc_capex_usd.values / 1e6,
                "source": "SEC EDGAR capex x DC share (Moorhouse assumption)",
            }
        )
    )
    # Railroads and the public megaprojects: annual series assembled by hand from the
    # sources documented in data/raw/programs/SOURCES.md.
    for path in sorted((config.RAW / "programs").glob("*.csv")):
        p = pd.read_csv(path).dropna(subset=["nominal_usd_millions"])
        frames.append(pd.DataFrame({"program": path.stem, "year": p.year, "nominal_musd": p.nominal_usd_millions, "source": f"programs/{path.name}"}))
    out = pd.concat(frames, ignore_index=True)
    out["partial"] = out.year == P
    return out


def normalize(spend: pd.DataFrame, macro: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pid, g in spend.groupby("program", sort=False):
        s = g.set_index("year").nominal_musd.groupby(level=0).sum()
        world = pid == "datacenters_global"
        m = pd.DataFrame(
            {
                "nominal": s,
                "cpi_real": econ.real_dollars(s, macro.cpi_1982_84, REF),
                "cpi_real_2024": econ.real_dollars(s, macro.cpi_1982_84, config.MOORHOUSE_YEAR),
                "deflator_real": econ.real_dollars(s, macro.gdp_deflator_2017, REF),
                "share_us_gdp": econ.share_of(s, macro.gdp_nominal_musd),
                "economic_share": econ.economic_share(s, macro.gdp_nominal_musd, REF),
                "per_capita_income": econ.per_capita_income(s, macro.gdp_nominal_musd, macro.population, REF),
                "share_world_gdp": econ.share_of(s, macro.world_gdp_nominal_musd) if world else float("nan"),
            }
        )
        for col in list(m.columns):
            m[f"cum_{col}"] = econ.cumulative(m[col]) if m[col].notna().any() else float("nan")
        m["program"] = pid
        # Moorhouse's x-axis: spend in the first calendar year is plotted at x = 1.
        m["years_since_start"] = m.index - m.index.min() + 1
        m["partial"] = m.index == P
        rows.append(m.reset_index())
    return pd.concat(rows, ignore_index=True)


def ranking(norm: pd.DataFrame, meta: dict) -> pd.DataFrame:
    out = []
    for pid, g in norm.groupby("program", sort=False):
        variants = [(pid, g)]
        if g.partial.any():  # report the complete-years total as its own row
            variants = [(pid, g[~g.partial]), (f"{pid} (incl. {P} est.)", g)]
        for label, h in variants:
            last = h.iloc[-1]
            out.append(
                {
                    "program": label,
                    "name": meta.get(pid, {}).get("name", pid),
                    "financing": meta.get(pid, {}).get("financing", ""),
                    "first_year": int(h.year.min()),
                    "last_year": int(h.year.max()),
                    "years": int(last.years_since_start),
                    "nominal_busd": last.cum_nominal / 1e3,
                    "cpi_real_2024_busd": last.cum_cpi_real_2024 / 1e3,
                    f"cpi_real_{REF}_busd": last.cum_cpi_real / 1e3,
                    f"deflator_real_{REF}_busd": last.cum_deflator_real / 1e3,
                    "gdp_years_pct": 100 * last.cum_share_us_gdp,
                    f"economic_share_{REF}_busd": last.cum_economic_share / 1e3,
                    f"per_capita_income_{REF}_busd": last.cum_per_capita_income / 1e3,
                    "peak_annual_pct_gdp": 100 * h.share_us_gdp.max(),
                    "first6_gdp_years_pct": 100 * h[h.years_since_start <= 6].share_us_gdp.sum(),
                    "world_gdp_years_pct": 100 * last.cum_share_world_gdp,
                }
            )
    return pd.DataFrame(out).sort_values("gdp_years_pct", ascending=False)


def reconcile(norm: pd.DataFrame, macro: pd.DataFrame) -> None:
    """Our data-center total vs. Moorhouse's, with and without finance leases, in 2024 dollars."""
    dc = norm[(norm.program == "datacenters_global") & ~norm.partial]
    ours = dc.cpi_real_2024.sum() / 1e3
    fl = pd.read_csv(OUT / "hyperscaler_finance_lease_additions.csv")
    fl = fl[fl.fiscal_year.between(dc.year.min(), dc.year.max())].groupby("fiscal_year").finance_lease_additions_usd.sum() / 1e6
    fl_dc = fl * pd.Series({y: config.dc_share(y) for y in fl.index})
    fl_real = econ.real_dollars(fl_dc, macro.cpi_1982_84, config.MOORHOUSE_YEAR).sum() / 1e3
    pd.DataFrame(
        {
            "busd_2024": {
                "cash_capex_dc_share": ours,
                "finance_lease_additions_dc_share": fl_real,
                "with_finance_leases": ours + fl_real,
                "moorhouse_printed": 930.0,
            }
        }
    ).to_csv(OUT / "moorhouse_reconciliation.csv", float_format="%.1f")
    print(f"Data centers 2020-2025, 2024$: cash capex {ours:,.0f}B; + finance leases {ours + fl_real:,.0f}B; Moorhouse ≈930B")


def main() -> None:
    macro = pd.read_csv(OUT / "macro.csv", index_col="year")
    comparators = yaml.safe_load((config.SLIDE / "comparators.yaml").read_text())
    meta = {c["id"]: c for c in comparators["programs"]}

    spend = spend_long()
    spend.to_csv(OUT / "spend_long.csv", index=False, float_format="%.3f")
    norm = normalize(spend, macro)
    norm.to_csv(OUT / "normalized.csv", index=False, float_format="%.6g")
    rank = ranking(norm, meta)
    rank.to_csv(OUT / "ranking.csv", index=False, float_format="%.3f")
    reconcile(norm, macro)
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(rank.drop(columns=["name", "financing"]).round(1).to_string(index=False))


if __name__ == "__main__":
    main()
