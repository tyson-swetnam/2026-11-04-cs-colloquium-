"""Environmental cost in New Mexico terms: one proposed campus vs. the whole state's grid.

Inputs: data/raw/environment/facts.csv (sourced facts, see NOTES.md) and EIA's New Mexico
State Electricity Profile (downloaded here). Output: data/processed/environment_nm.csv.
"""

from __future__ import annotations

import openpyxl
import pandas as pd

import config
from evidence.fetch import fetch

ENV = config.RAW / "environment"
HOURS = 8760


def eia_summary() -> dict[str, float]:
    path = fetch(
        "https://www.eia.gov/electricity/state/xls/SEP%20Tables%20for%20NM.xlsx",
        ENV / "eia_sep_tables_nm_2024.xlsx",
        source="EIA State Electricity Profile, New Mexico, 2024 (Table 1)",
        license="U.S. government work (public domain)",
    )
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)["1. Summary"]
    rows = {r[0]: r[1] for r in ws.iter_rows(values_only=True) if r and isinstance(r[0], str) and r[1] not in (None, "")}
    return {
        "nm_retail_sales_twh": rows["Total sales to ultimate customers (megawatthours)"] / 1e6,
        "nm_generation_twh": rows["Net generation (megawatthours)"] / 1e6,
        "nm_summer_capacity_mw": rows["Net summer capacity (megawatts)"],
        "nm_power_co2_mt": rows["..Carbon dioxide (thousand metric tons)"] / 1e3,
    }


def fact(facts: pd.DataFrame, fid: str) -> float:
    """First number in a fact's value field (values like '2,462' or '192')."""
    raw = str(facts.loc[fid, "value"]).replace(",", "")
    return float(pd.Series([raw]).str.extract(r"([\d.]+)")[0].iloc[0])


def main() -> None:
    facts = pd.read_csv(ENV / "facts.csv", index_col="id")
    nm = eia_summary()
    us_dc_2024 = fact(facts, "A4")  # LBNL 2025 Update, TWh
    jupiter_mw, jupiter_cap_mw = fact(facts, "C3"), fact(facts, "C4")
    pnm_peak = fact(facts, "D6")
    rows = [
        ("US data centers 2024 (LBNL), TWh", us_dc_2024, us_dc_2024 / nm["nm_retail_sales_twh"], "x NM retail sales"),
        ("Project Jupiter nameplate, MW", jupiter_mw, jupiter_mw / pnm_peak, "x PNM all-time peak (2,264 MW)"),
        ("Project Jupiter nameplate, MW", jupiter_mw, jupiter_mw / nm["nm_summer_capacity_mw"], "x NM summer generating capacity"),
        ("Project Jupiter at 1,600 MW cap, TWh/yr (upper bound)", jupiter_cap_mw * HOURS / 1e6, jupiter_cap_mw * HOURS / 1e6 / nm["nm_retail_sales_twh"], "x NM retail sales"),
        ("Project Jupiter at nameplate, TWh/yr (upper bound)", jupiter_mw * HOURS / 1e6, jupiter_mw * HOURS / 1e6 / nm["nm_retail_sales_twh"], "x NM retail sales"),
    ]
    out = pd.DataFrame(rows, columns=["quantity", "value", "ratio", "compared_to"])
    for k, v in nm.items():
        out.loc[len(out)] = [k, v, 1.0, "EIA 2024"]
    config.PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.PROCESSED / "environment_nm.csv", index=False, float_format="%.4g")
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
