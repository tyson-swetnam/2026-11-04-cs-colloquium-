"""Slide 27: pull the ontology-backed AVUs MESA has written on a public NEON beetle collection
(read with src/02_datastore.py) and set them beside the AVU rows drawn on the slide.

In: data/raw/sources/datastore_konz_dp1_10022_metadata.json
Out: data/processed/mesa_avus_observed.csv
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
SRC = SLIDE / "data" / "raw" / "sources" / "datastore_konz_dp1_10022_metadata.json"
OUT = SLIDE / "data" / "processed" / "mesa_avus_observed.csv"
CURIE = re.compile(r"^[A-Za-z]+:\d+$")


def main() -> None:
    sc = json.loads(SRC.read_text())["result"]["structuredContent"]
    rows = []
    for a in sc["irods-avus"]:
        unit = a.get("unit", "")
        rows.append({"path": sc["path"], "attribute": a["attr"], "value": a["value"], "unit": unit,
                     "curie_in_unit": bool(CURIE.match(unit)),
                     "curie_in_value": bool(re.search(r"\b[A-Za-z]+:\d{4,}\b", a["value"]))})
    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(f"{len(df)} AVUs; {df.curie_in_unit.sum()} with a CURIE in the unit slot; "
          f"{df.curie_in_value.sum()} with a CURIE in the value slot")
    print(df[df.curie_in_unit][["attribute", "value", "unit"]].to_string(index=False))


if __name__ == "__main__":
    main()
