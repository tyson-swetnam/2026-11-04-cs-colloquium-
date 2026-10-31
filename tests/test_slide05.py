import sys
from pathlib import Path

import pytest
import yaml

SLIDE = Path(__file__).resolve().parents[1] / "slides" / "05-the-build-out"
sys.path.insert(0, str(SLIDE / "src"))

import config  # noqa: E402


def test_comparators_parse_with_unique_ids():
    doc = yaml.safe_load((SLIDE / "comparators.yaml").read_text())
    ids = [p["id"] for p in doc["programs"]]
    assert len(ids) == len(set(ids))
    for p in doc["programs"]:
        assert p["financing"] in {"public", "private", "mixed"}
        assert p["years"][0] <= p["years"][1]


def test_dc_share_matches_moorhouse_endpoints():
    assert config.dc_share(2020) == pytest.approx(0.55)
    assert config.dc_share(2026) == pytest.approx(0.80)
    assert config.dc_share(2015) == pytest.approx(0.55)  # clamped before the ramp
