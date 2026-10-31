"""Check slide 06's SEC-derived series against published figures in benchmarks.yaml."""

from __future__ import annotations

import sys

import pandas as pd
import yaml

import config


def main() -> int:
    bench = yaml.safe_load((config.SLIDE / "benchmarks.yaml").read_text())
    annual = pd.read_csv(config.PROCESSED / "hyperscaler_annual.csv", index_col="year")
    rows = []
    for fig in bench["figures"]:
        check = fig.get("check")
        if not check:
            continue
        for year, pub in fig["value"].items():
            ours = annual.loc[year, check["column"]] / 1e9
            diff = (ours - pub) / pub
            rows.append({"check": f"{fig['id']}[{year}]", "published": pub, "ours": ours, "rel_diff": diff, "tol": check["tol"], "pass": abs(diff) <= check["tol"]})
    df = pd.DataFrame(rows)
    df.to_csv(config.PROCESSED / "validation.csv", index=False, float_format="%.4f")
    print(df.round(3).to_string(index=False))
    return 0 if df["pass"].all() else 1


if __name__ == "__main__":
    sys.exit(main())
