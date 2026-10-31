"""Control 3, "It varies run to run": an output contract, validated in the agent.

A JSON Schema for one dataset-metadata record, and the ways sampled model output actually
breaks it. The schema guarantees shape; it says nothing about truth, which is why controls
1 and 2 check identifiers and terms against real indexes after the shape is accepted.

Output: data/processed/schema_checks.csv
"""

from __future__ import annotations

import json

import pandas as pd
from jsonschema import Draft202012Validator

import config

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Dataset record written by an agent",
    "type": "object",
    "additionalProperties": False,
    "required": ["title", "organism", "assay", "n_samples", "doi"],
    "properties": {
        "title": {"type": "string", "minLength": 10},
        "organism": {"type": "string", "pattern": r"^NCBITaxon:\d+$"},
        "assay": {"type": "string", "pattern": r"^OBI:\d{7}$"},
        "cell_line": {"type": "string", "pattern": r"^CLO:\d{7}$"},
        "n_samples": {"type": "integer", "minimum": 1},
        "doi": {"type": "string", "pattern": r"^10\.\d{4,9}/\S+$"},
    },
}

GOOD = {"title": "Mouse liver RNA-seq time course", "organism": "NCBITaxon:10090", "assay": "OBI:0001271", "n_samples": 24, "doi": "10.1038/s41586-023-06735-9"}

# What sampled output looks like when nothing enforces a contract.
OUTPUTS = [
    ("conforming record", json.dumps(GOOD)),
    ("prose around the JSON", "Sure! Here is the record:\n" + json.dumps(GOOD)),
    ("missing required field", json.dumps({k: v for k, v in GOOD.items() if k != "doi"})),
    ("number as a string", json.dumps(dict(GOOD, n_samples="24"))),
    ("free text instead of a CURIE", json.dumps(dict(GOOD, organism="mouse"))),
    ("invented extra field", json.dumps(dict(GOOD, confidence="high"))),
    ("trailing comma", json.dumps(GOOD)[:-1] + ",}"),
    ("well-formed but false (fake DOI)", json.dumps(dict(GOOD, doi="10.1109/TNNLS.2021.3071234"))),
]


def main() -> None:
    validator = Draft202012Validator(SCHEMA)
    rows = []
    for case, text in OUTPUTS:
        try:
            record = json.loads(text)
        except json.JSONDecodeError as e:
            rows.append({"case": case, "accepted": False, "errors": f"not JSON: {e.msg}"})
            continue
        errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
        rows.append({"case": case, "accepted": not errors, "errors": "; ".join(e.message for e in errors)})
    df = pd.DataFrame(rows)
    config.PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.PROCESSED / "schema_checks.csv", index=False)
    (config.PROCESSED / "dataset_record.schema.json").write_text(json.dumps(SCHEMA, indent=2))
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
