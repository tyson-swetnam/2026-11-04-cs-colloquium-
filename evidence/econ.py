"""Ways to put spending from different centuries on one axis.

All series are pandas Series indexed by calendar year. The measures follow
MeasuringWorth's taxonomy (Williamson, "Measures of Worth"), because "how big
was it?" has more than one honest answer:

    real_dollars       what the same basket of goods would cost today (CPI or GDP deflator)
    share_of           fraction of that year's economy (nominal spend / nominal GDP)
    economic_share     the same fraction, expressed in today's dollars (share_t x GDP_ref)
    per_capita_income  spend relative to GDP per person, i.e. adjusted for productivity growth

Moorhouse's chart uses real_dollars. A railroad dollar in 1870 was a far larger
slice of a far less productive economy, which is what the other measures capture.
"""

from __future__ import annotations

import pandas as pd


def rebase(index: pd.Series, base_year: int) -> pd.Series:
    """Rescale a price or output index so `base_year` == 1."""
    return index / index.loc[base_year]


def real_dollars(nominal: pd.Series, price_index: pd.Series, base_year: int) -> pd.Series:
    """Nominal dollars converted to `base_year` dollars with a price index (CPI, GDP deflator)."""
    return nominal / rebase(price_index, base_year).reindex(nominal.index)


def share_of(nominal: pd.Series, denominator: pd.Series) -> pd.Series:
    """Spending as a fraction of a same-year nominal aggregate (usually nominal GDP)."""
    return nominal / denominator.reindex(nominal.index)


def economic_share(nominal: pd.Series, nominal_gdp: pd.Series, ref_year: int) -> pd.Series:
    """Spending scaled to the size of the economy in `ref_year`: (spend_t / GDP_t) x GDP_ref."""
    return share_of(nominal, nominal_gdp) * nominal_gdp.loc[ref_year]


def per_capita_income(nominal: pd.Series, nominal_gdp: pd.Series, population: pd.Series, ref_year: int) -> pd.Series:
    """Spending scaled by nominal GDP per person, expressed in `ref_year` dollars."""
    gdp_pc = nominal_gdp / population
    return nominal / gdp_pc.reindex(nominal.index) * gdp_pc.loc[ref_year]


def program_years(series: pd.Series, start_year: int | None = None) -> pd.Series:
    """Re-index a calendar-year series to years since the program started (start year = 0)."""
    start = series.first_valid_index() if start_year is None else start_year
    out = series.loc[start:].copy()
    out.index = out.index - start
    out.index.name = "years_since_start"
    return out


def cumulative(series: pd.Series) -> pd.Series:
    """Running total, treating missing years as zero spend."""
    return series.fillna(0).cumsum()
