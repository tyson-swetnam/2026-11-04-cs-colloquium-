"""Financial risk: are the hyperscalers still paying for the build-out out of cash flow?

Outputs (data/processed/)
    hyperscaler_quarterly.csv  capex and operating cash flow per firm per fiscal quarter
    hyperscaler_annual.csv     calendar-year capex, OCF, free cash flow, capex/OCF (2026 scaled)
    hyperscaler_ttm.csv        trailing-four-quarter totals across the five firms (actuals only)
    hyperscaler_debt.csv       total debt per firm at each fiscal year end and the latest quarter
    telecom_bust.csv           BEA telecom investment around the 2000 peak (from slide 05's data)
"""

from __future__ import annotations

import pandas as pd

import config
from evidence import sec
from evidence.fetch import fetch

RAW, OUT = config.RAW, config.PROCESSED


def companyfacts(name: str, firm: dict) -> dict:
    path = fetch(
        sec.COMPANYFACTS.format(cik=firm["cik"]),
        RAW / "sec" / f"companyfacts_{name.lower()}.json",
        source=f"SEC EDGAR company facts, {name}",
        license="SEC EDGAR XBRL company facts (public domain)",
        user_agent=config.SEC_UA,
    )
    return sec.load(path)


def debt(facts: dict) -> pd.Series:
    def get(concept):
        try:
            return sec.instants(facts, concept)
        except KeyError:
            return pd.Series(dtype=float)

    total, noncurrent, current, combined = (get(c) for c in (config.DEBT_TOTAL, *config.DEBT_PARTS, config.DEBT_COMBINED))
    parts = noncurrent.add(current.reindex(noncurrent.index).fillna(0))
    out = total.combine_first(parts).combine_first(combined)
    return out.sort_index()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    quarterly, annual, debts = [], [], []
    for name, firm in config.HYPERSCALERS.items():
        facts = companyfacts(name, firm)
        q = sec.flow_quarters(facts, firm["capex"]).rename(columns={"value": "capex"})
        o = sec.flow_quarters(facts, config.OCF).rename(columns={"value": "ocf"})
        both = q[["quarter_end", "capex"]].merge(o[["quarter_end", "ocf"]], on="quarter_end").assign(company=name)
        quarterly.append(both)
        ya = sec.calendar_years(q.rename(columns={"capex": "value"}), config.PARTIAL_YEAR).rename(columns={"value": "capex"})
        yo = sec.calendar_years(o.rename(columns={"ocf": "value"}), config.PARTIAL_YEAR).rename(columns={"value": "ocf"})
        annual.append(ya[["year", "capex", "partial"]].merge(yo[["year", "ocf"]], on="year").assign(company=name))
        d = debt(facts)
        debts.append(pd.DataFrame({"company": name, "date": d.index, "debt": d.values}))

    qdf = pd.concat(quarterly, ignore_index=True)
    qdf["calendar_quarter"] = qdf.quarter_end.dt.to_period("Q").astype(str)
    qdf.to_csv(OUT / "hyperscaler_quarterly.csv", index=False)

    # Trailing four quarters, summed across firms, only where every firm has four actual quarters.
    ttm = []
    for name, g in qdf.groupby("company"):
        g = g.sort_values("quarter_end").set_index("calendar_quarter")
        ttm.append(g[["capex", "ocf"]].rolling(4).sum().dropna().assign(company=name))
    ttm = pd.concat(ttm).reset_index()
    agg = ttm.groupby("calendar_quarter").agg(capex=("capex", "sum"), ocf=("ocf", "sum"), firms=("company", "nunique"))
    agg = agg[agg.firms == len(config.HYPERSCALERS)]
    agg["capex_to_ocf"] = agg.capex / agg.ocf
    agg.to_csv(OUT / "hyperscaler_ttm.csv")

    adf = pd.concat(annual, ignore_index=True)
    tot = adf[adf.year.between(2019, config.PARTIAL_YEAR)].groupby("year").agg(capex=("capex", "sum"), ocf=("ocf", "sum"), partial=("partial", "any"))
    tot["fcf"] = tot.ocf - tot.capex
    tot["capex_to_ocf"] = tot.capex / tot.ocf
    adf.to_csv(OUT / "hyperscaler_annual_by_company.csv", index=False)
    tot.to_csv(OUT / "hyperscaler_annual.csv")

    ddf = pd.concat(debts, ignore_index=True)
    ddf.to_csv(OUT / "hyperscaler_debt.csv", index=False)
    # Debt at each firm's last fiscal year end in 2024 vs. its latest filing.
    rows = []
    for name, g in ddf.groupby("company"):
        g = g.set_index("date").debt
        base = g[g.index.year == 2024].iloc[-1:]
        rows.append({"company": name, "base_date": base.index[0].date(), "base_debt": base.iloc[0], "latest_date": g.index[-1].date(), "latest_debt": g.iloc[-1]})
    change = pd.DataFrame(rows)
    change.to_csv(OUT / "hyperscaler_debt_change.csv", index=False)
    print(change.assign(base_debt=change.base_debt / 1e9, latest_debt=change.latest_debt / 1e9).round(1).to_string(index=False))
    print(f"total debt {change.base_debt.sum() / 1e9:.0f}B -> {change.latest_debt.sum() / 1e9:.0f}B")

    # The last private capex boom that ended in a bust, from slide 05's BEA extract.
    bea = pd.read_csv(config.ROOT / "slides" / "05-the-build-out" / "data" / "processed" / "bea_series.csv", index_col="year")
    tel = (bea.C275RC + bea.C314RC).loc[1995:2005]
    pd.DataFrame({"telecom_musd": tel, "pct_gdp": 100 * tel / bea.A191RC.loc[1995:2005]}).to_csv(OUT / "telecom_bust.csv")

    print((tot.assign(capex=tot.capex / 1e9, ocf=tot.ocf / 1e9, fcf=tot.fcf / 1e9)).round(2).to_string())
    print(agg.assign(capex=agg.capex / 1e9, ocf=agg.ocf / 1e9).round(2).tail(8).to_string())
    print(f"telecom 2000 -> 2002: {100 * (tel.loc[2002] / tel.loc[2000] - 1):.0f}%")


if __name__ == "__main__":
    main()
