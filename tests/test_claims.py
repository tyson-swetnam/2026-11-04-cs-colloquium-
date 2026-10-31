import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import claims  # noqa: E402


def test_every_claims_file_validates():
    assert claims.validate(claims.load_all()) == []
