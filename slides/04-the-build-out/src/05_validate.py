"""Check this pipeline against published figures listed in benchmarks.yaml.

Writes data/processed/validation.csv and exits non-zero if any check misses its tolerance.
"""

from __future__ import annotations

import sys

import pandas as pd
import yaml

import config

OUT = config.PROCESSED


def ours(check: dict, norm: pd.DataFrame) -> float | dict:
    kind = check["kind"]
    if kind == "avg_share":
        y0, y1 = check["years"]
        g = norm[(norm.program == check["program"]) & norm.year.between(y0, y1)]
        return 100 * g.share_us_gdp.mean()
    if kind == "share_in_year":
        g = norm[(norm.program == check["program"]) & (norm.year == check["year"])]
        return 100 * g.share_us_gdp.iloc[0]
    if kind == "hyperscaler_capex":
        capex = pd.read_csv(OUT / "hyperscaler_capex_annual.csv", index_col="year").capex_usd / 1e9
        return capex.to_dict()
    if kind == "moorhouse_with_leases":
        rec = pd.read_csv(OUT / "moorhouse_reconciliation.csv", index_col=0).busd_2024
        return rec["with_finance_leases"]
    raise ValueError(kind)


def main() -> int:
    bench = yaml.safe_load((config.SLIDE / "benchmarks.yaml").read_text())
    norm = pd.read_csv(OUT / "normalized.csv")
    rows = []
    for fig in bench["figures"]:
        check = fig.get("check")
        if not check:
            continue
        mine = ours(check, norm)
        published = fig["value"]
        pairs = [(f"{fig['id']}[{y}]", published[y], mine.get(y)) for y in published] if isinstance(published, dict) else [(fig["id"], published, mine)]
        for label, pub, got in pairs:
            diff = (got - pub) / pub if got is not None else float("nan")
            rows.append({"check": label, "source": fig["source"], "published": pub, "ours": got, "rel_diff": diff, "tol": check["tol"], "pass": abs(diff) <= check["tol"]})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "validation.csv", index=False, float_format="%.4f")
    print(df.round(3).to_string(index=False))
    return 0 if df["pass"].all() else 1


if __name__ == "__main__":
    sys.exit(main())
