import pandas as pd
import pytest

from evidence import sec


def fact(start, end, val, form="10-Q", filed="2026-01-01"):
    return {"start": start, "end": end, "val": val, "form": form, "filed": filed}


@pytest.fixture
def june_fy_filer():
    """Fiscal year July-June; cash flow reported year-to-date, like Microsoft."""
    capex = [
        fact("2024-07-01", "2024-09-30", 10),
        fact("2024-07-01", "2024-12-31", 25),
        fact("2024-07-01", "2025-03-31", 45),
        fact("2024-07-01", "2025-06-30", 70, form="10-K"),
        fact("2025-07-01", "2025-09-30", 30),
    ]
    cash = [{"end": "2025-06-30", "val": 5, "form": "10-K", "filed": "2025-08-01"}]
    return {"entityName": "Test", "facts": {"us-gaap": {
        "Capex": {"units": {"USD": capex}},
        "Cash": {"units": {"USD": cash}},
    }}}


def test_flow_quarters_differences_ytd(june_fy_filer):
    q = sec.flow_quarters(june_fy_filer, "Capex")
    assert q.value.tolist() == [10, 15, 20, 25, 30]
    assert q.derived.tolist() == [False, True, True, True, False]


def test_calendar_years_and_partial_scaling(june_fy_filer):
    q = sec.flow_quarters(june_fy_filer, "Capex")
    a = sec.calendar_years(q, partial_year=2025).set_index("year")
    assert a.loc[2024, "value"] == 25  # Jul-Dec 2024 quarters only
    assert a.loc[2025, "quarters"] == 3
    assert a.loc[2025, "partial"] and not a.loc[2024, "partial"]


def test_trailing_four(june_fy_filer):
    q = sec.flow_quarters(june_fy_filer, "Capex")
    assert sec.trailing_four(q).tolist() == [70, 90]


def test_instants_and_fallback(june_fy_filer):
    assert sec.instants(june_fy_filer, ["Missing", "Cash"]).tolist() == [5]
    with pytest.raises(KeyError):
        sec.flow_quarters(june_fy_filer, "Missing")
