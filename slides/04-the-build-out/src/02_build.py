"""Turn the raw downloads into tidy annual series in data/processed/.

Outputs
    macro.csv                      US GDP, deflator, CPI, population, world GDP by year
    bea_series.csv                 the BEA investment lines in config.BEA_SERIES, by year
    hyperscaler_capex_quarterly.csv  capex per company per fiscal quarter (derived from YTD where needed)
    hyperscaler_capex_annual.csv   calendar-year capex per company, DC share, DC capex
"""

from __future__ import annotations

import json

import pandas as pd

import config
from evidence import sec

RAW, OUT = config.RAW, config.PROCESSED
P = config.PARTIAL_YEAR


def read_measuringworth(path, header_row: str) -> pd.DataFrame:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith(header_row))
    df = pd.read_csv(pd.io.common.StringIO("\n".join(lines[start:])), thousands=",")
    return df.rename(columns={"Year": "year"}).set_index("year")


def bea_annual() -> pd.DataFrame:
    a = pd.read_csv(RAW / "bea" / "NipaDataA.txt", thousands=",")
    a.columns = ["code", "year", "value"]
    a = a[a.code.isin(config.BEA_SERIES)].pivot(index="year", columns="code", values="value")
    # The partial year: average of the seasonally adjusted annual-rate quarters published so far.
    q = pd.read_csv(RAW / "bea" / "NipaDataQ.txt", thousands=",")
    q.columns = ["code", "period", "value"]
    q = q[q.code.isin(config.BEA_SERIES) & q.period.str.startswith(str(P))]
    a.loc[P] = q.groupby("code").value.mean()
    a.attrs["partial_quarters"] = sorted(q.period.unique())
    return a  # millions of current dollars (deflator is an index)


def macro(bea: pd.DataFrame) -> pd.DataFrame:
    gdp = read_measuringworth(RAW / "measuringworth_us_gdp.csv", '"Year"')
    cpi = read_measuringworth(RAW / "measuringworth_us_cpi.csv", '"Year"')
    m = pd.DataFrame(
        {
            "gdp_nominal_musd": gdp["Nominal GDP (million of Dollars)"],
            "gdp_deflator_2017": gdp["GDP Deflator (index 2017=100)"],
            "population": gdp["Population"],
            "cpi_1982_84": cpi["U.S. Consumer Price Index *"],
        }
    )
    m.loc[P] = float("nan")
    # Extend MeasuringWorth one year with BEA's growth rates, so the splice has no level break.
    for col, code in (("gdp_nominal_musd", "A191RC"), ("gdp_deflator_2017", "A191RD")):
        m.loc[P, col] = m.loc[P - 1, col] * bea.loc[P, code] / bea.loc[P - 1, code]
    m.loc[P, "cpi_1982_84"] = m.loc[P - 1, "cpi_1982_84"] * m.loc[P, "gdp_deflator_2017"] / m.loc[P - 1, "gdp_deflator_2017"]
    m.loc[P, "population"] = m.loc[P - 1, "population"] ** 2 / m.loc[P - 2, "population"]

    wb = json.loads((RAW / "worldbank_gdp_current_usd.json").read_text())[1]
    world = pd.Series({int(r["date"]): r["value"] / 1e6 for r in wb if r["countryiso3code"] == "WLD" and r["value"]})
    m["world_gdp_nominal_musd"] = world
    if pd.isna(m.loc[P, "world_gdp_nominal_musd"]):
        m.loc[P, "world_gdp_nominal_musd"] = world.loc[P - 1] * m.loc[P, "gdp_nominal_musd"] / m.loc[P - 1, "gdp_nominal_musd"]
    m["partial"] = m.index == P
    m.index.name = "year"
    return m


def quarterly_capex(name: str, firm: dict) -> pd.DataFrame:
    """Discrete fiscal-quarter capex for one firm (see evidence.sec.flow_quarters)."""
    q = sec.flow_quarters(sec.load(RAW / "sec" / f"companyfacts_{name.lower()}.json"), firm["concept"])
    return q.rename(columns={"value": "capex_usd"}).assign(company=name)[["company", "quarter_end", "capex_usd", "derived"]]


def annual_capex(q: pd.DataFrame) -> pd.DataFrame:
    """Calendar-year totals per firm, with the partial year scaled by each firm's seasonality."""
    out = []
    for company, grp in q.groupby("company"):
        a = sec.calendar_years(grp.rename(columns={"capex_usd": "value"}), partial_year=P)
        out.append(a.rename(columns={"value": "capex_usd"}).assign(company=company))
    return pd.concat(out, ignore_index=True)[["company", "year", "capex_usd", "quarters", "partial"]]


def finance_lease_additions() -> pd.DataFrame:
    """Right-of-use assets obtained under finance leases, by fiscal year (10-K annual facts).

    Cash capex leaves these out; Moorhouse's source (reported capex, Epoch AI) appears to include
    them. Used only to reconcile the baseline, so fiscal years are not calendarized.
    """
    rows = []
    for name, firm in config.HYPERSCALERS.items():
        facts = json.loads((RAW / "sec" / f"companyfacts_{name.lower()}.json").read_text())
        tag = facts["facts"]["us-gaap"].get("RightOfUseAssetObtainedInExchangeForFinanceLeaseLiability", {})
        df = pd.DataFrame(tag.get("units", {}).get("USD", []))
        if df.empty:
            continue
        df = df[df.form == "10-K"].copy()
        days = (pd.to_datetime(df.end) - pd.to_datetime(df.start)).dt.days
        df = df[(days > 330) & (days < 380)].sort_values("filed").drop_duplicates("end", keep="last")
        rows += [(name, int(e[:4]), v) for e, v in zip(df.end, df.val)]
    return pd.DataFrame(rows, columns=["company", "fiscal_year", "finance_lease_additions_usd"])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    bea = bea_annual()
    bea.to_csv(OUT / "bea_series.csv", float_format="%.3f")
    macro(bea).to_csv(OUT / "macro.csv", float_format="%.4f")

    q = pd.concat([quarterly_capex(n, f) for n, f in config.HYPERSCALERS.items()])
    q.to_csv(OUT / "hyperscaler_capex_quarterly.csv", index=False)
    a = annual_capex(q)
    a = a[(a.year >= 2015) & (a.year <= P)]
    complete = a.groupby("year").apply(lambda g: (g.partial | (g.quarters == 4)).all() and len(g) == len(config.HYPERSCALERS))
    total = a.groupby("year").capex_usd.sum().to_frame("capex_usd")
    total["complete"] = complete
    total["dc_share"] = [config.dc_share(y) for y in total.index]
    total["dc_capex_usd"] = total.capex_usd * total.dc_share
    total["partial"] = total.index == P
    a.to_csv(OUT / "hyperscaler_capex_annual_by_company.csv", index=False)
    finance_lease_additions().to_csv(OUT / "hyperscaler_finance_lease_additions.csv", index=False)
    total.to_csv(OUT / "hyperscaler_capex_annual.csv")
    print(f"BEA {P} from quarters: {bea.attrs['partial_quarters']}")
    print((total.assign(capex_busd=total.capex_usd / 1e9, dc_busd=total.dc_capex_usd / 1e9)[["capex_busd", "dc_share", "dc_busd", "complete"]]).round(1).to_string())


if __name__ == "__main__":
    main()
