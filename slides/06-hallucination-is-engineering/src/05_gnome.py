"""The slide's example: "GNoME proposed 380,000 crystals; independent labs confirmed under 5%."

Reads the GNoME paper's open-access full text (Merchant et al., Nature 2023; Europe PMC) for its
own numbers, and the DOI registry for the published critique (Cheetham & Seshadri, Chem. Mater. 2024).

Output: data/processed/gnome_check.csv
"""

from __future__ import annotations

import html
import json
import re

import pandas as pd

import config
from evidence.http import CachedGet

GNOME_PMC = "PMC10700131"
CRITIQUE_DOI = "10.1021/acs.chemmater.4c00643"


def number(text: str, pattern: str) -> tuple[int, str]:
    m = re.search(pattern, text)
    if not m:
        raise ValueError(f"pattern not found in GNoME text: {pattern}")
    start = max(text.rfind(". ", 0, m.start()) + 2, m.start() - 110)
    end = text.find(". ", m.end()) + 1
    return int(m.group(1).replace(",", "")), text[start:end]


def main() -> None:
    get = CachedGet(config.CACHE / "gnome", config.UA)
    status, xml = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{GNOME_PMC}/fullTextXML")
    assert status == 200, status
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", xml)))
    stable, stable_q = number(text, r"of which ([\d,]+) are newly discovered stable materials")
    realized, realized_q = number(text, r"Of the stable structures, ([\d,]+) have already been independently experimentally realized")
    status, csl = get(f"https://doi.org/{CRITIQUE_DOI}", accept="application/vnd.citationstyles.csl+json")
    meta = json.loads(csl) if status == 200 else {}
    rows = [
        {"quantity": "new stable crystals (DFT-verified)", "value": stable, "source": "Merchant et al. 2023, Nature (PMC10700131)", "quote": stable_q},
        {"quantity": "already independently realized in a lab", "value": realized, "source": "Merchant et al. 2023, Nature (PMC10700131)", "quote": realized_q},
        {"quantity": "realized / stable, %", "value": round(100 * realized / stable, 2), "source": "computed", "quote": ""},
        {
            "quantity": "published critique",
            "value": "",
            "source": f"{', '.join(a.get('family', '') for a in meta.get('author', []))}, {meta.get('container-title', '')} {meta.get('volume', '')}, {meta.get('page', '')} ({meta.get('issued', {}).get('date-parts', [['']])[0][0]})",
            "quote": meta.get("title", ""),
        },
    ]
    df = pd.DataFrame(rows)
    config.PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.PROCESSED / "gnome_check.csv", index=False)
    print(df.to_string(index=False, max_colwidth=90))


if __name__ == "__main__":
    main()
