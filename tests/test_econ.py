import pandas as pd
import pytest

from evidence import econ


@pytest.fixture
def toy():
    years = pd.Index([2000, 2001, 2002], name="year")
    spend = pd.Series([10.0, 20.0, 30.0], index=years)
    gdp = pd.Series([1000.0, 1100.0, 1200.0], index=years)
    cpi = pd.Series([80.0, 90.0, 100.0], index=years)
    pop = pd.Series([10.0, 10.0, 12.0], index=years)
    return spend, gdp, cpi, pop


def test_real_dollars_rebases_to_base_year(toy):
    spend, _, cpi, _ = toy
    real = econ.real_dollars(spend, cpi, 2002)
    assert real.loc[2002] == pytest.approx(30.0)
    assert real.loc[2000] == pytest.approx(12.5)


def test_economic_share_holds_gdp_fraction_constant(toy):
    spend, gdp, _, _ = toy
    es = econ.economic_share(spend, gdp, 2002)
    assert (es / gdp.loc[2002]).tolist() == pytest.approx(econ.share_of(spend, gdp).tolist())


def test_per_capita_income_scales_by_gdp_per_person(toy):
    spend, gdp, _, pop = toy
    out = econ.per_capita_income(spend, gdp, pop, 2002)
    assert out.loc[2002] == pytest.approx(30.0)
    assert out.loc[2000] == pytest.approx(10.0 / 100.0 * 100.0)


def test_program_years_and_cumulative(toy):
    spend, *_ = toy
    py = econ.program_years(spend)
    assert list(py.index) == [0, 1, 2]
    assert econ.cumulative(py).iloc[-1] == pytest.approx(60.0)
