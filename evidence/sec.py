"""SEC EDGAR XBRL company facts: turn year-to-date filings into quarters and years.

Cash-flow items in 10-Qs are reported year-to-date; balance-sheet items are point-in-time.
These helpers recover discrete fiscal quarters from the former and a clean time series
from the latter, so firms with different fiscal years can be summed by calendar year.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

COMPANYFACTS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"


def load(path: Path) -> dict:
    return json.loads(Path(path).read_text())


def _facts(facts: dict, concepts: str | list[str]) -> pd.DataFrame:
    """All 10-K/10-Q USD facts for the first concepts the filer uses, later concepts filling gaps."""
    frames = []
    for concept in [concepts] if isinstance(concepts, str) else concepts:
        units = facts["facts"]["us-gaap"].get(concept, {}).get("units", {}).get("USD", [])
        if units:
            frames.append(pd.DataFrame(units).assign(concept=concept))
    if not frames:
        raise KeyError(f"none of {concepts} reported by {facts.get('entityName')}")
    rows = pd.concat(frames, ignore_index=True)
    return rows[rows.form.str.match(r"10-[KQ]")].copy()


def flow_quarters(facts: dict, concepts: str | list[str]) -> pd.DataFrame:
    """Discrete fiscal-quarter values of a flow (cash-flow or income) item.

    Within one fiscal year every year-to-date fact shares a start date, so consecutive
    differences are quarters; directly reported three-month facts take precedence.
    Returns columns quarter_end, value, derived.
    """
    rows = _facts(facts, concepts).dropna(subset=["start"])
    rows["start"], rows["end"] = pd.to_datetime(rows.start), pd.to_datetime(rows.end)
    # Earlier concepts in the list win over later ones for the same period, then latest filing.
    rows["rank"] = rows.concept.map({c: i for i, c in enumerate(rows.concept.unique())})
    rows = rows.sort_values(["rank", "filed"], ascending=[False, True]).drop_duplicates(["start", "end"], keep="last")
    rows["months"] = ((rows.end - rows.start).dt.days / 30.44).round().astype(int)

    quarters: dict[pd.Timestamp, tuple[float, bool]] = {}
    for _, r in rows[rows.months == 3].iterrows():
        quarters[r.end] = (r.val, False)
    for _, grp in rows[rows.months.isin([3, 6, 9, 12])].groupby("start"):
        prev_val, prev_m = 0.0, 0
        for _, r in grp.sort_values("end").iterrows():
            if r.months - prev_m == 3 and r.end not in quarters:
                quarters[r.end] = (r.val - prev_val, True)
            prev_val, prev_m = r.val, r.months
    q = pd.DataFrame([(end, v, d) for end, (v, d) in quarters.items()], columns=["quarter_end", "value", "derived"])
    return q.sort_values("quarter_end").reset_index(drop=True)


def instants(facts: dict, concepts: str | list[str]) -> pd.Series:
    """Point-in-time values (balance-sheet items) by period end, latest filing winning."""
    rows = _facts(facts, concepts)
    rows = rows[rows.start.isna()] if "start" in rows else rows
    rows["end"] = pd.to_datetime(rows.end)
    rows["rank"] = rows.concept.map({c: i for i, c in enumerate(rows.concept.unique())})
    rows = rows.sort_values(["rank", "filed"], ascending=[False, True]).drop_duplicates("end", keep="last")
    return rows.set_index("end").val.sort_index()


def calendar_years(q: pd.DataFrame, partial_year: int | None = None) -> pd.DataFrame:
    """Sum fiscal quarters into calendar years by the year each quarter ends in.

    For `partial_year`, the year-to-date total is scaled by the share of the previous
    year's total that the same number of quarters held (that firm's own seasonality).
    Returns columns year, value, quarters, partial.
    """
    q = q.assign(year=q.quarter_end.dt.year)
    a = q.groupby("year").agg(value=("value", "sum"), quarters=("value", "size")).reset_index()
    a["value"] = a.value.astype(float)
    if partial_year is not None:
        ytd = q[q.year == partial_year]
        n = len(ytd)
        if 0 < n < 4:
            last = q[q.year == partial_year - 1].sort_values("quarter_end")
            ratio = last.value.sum() / last.value.iloc[:n].sum()
            a.loc[a.year == partial_year, "value"] = ytd.value.sum() * ratio
    a["partial"] = a.year == partial_year
    return a


def trailing_four(q: pd.DataFrame) -> pd.Series:
    """Rolling sum of the last four fiscal quarters, indexed by quarter end (actuals only)."""
    return q.set_index("quarter_end").value.rolling(4).sum().dropna()
