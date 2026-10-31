"""AlphaFold, "published open": fetch predictions anonymously and read the licence in each file.

No account, key or agreement is involved: the AlphaFold DB API returns the prediction metadata and
the mmCIF file, and the file states its own licence. Proteins span three kingdoms.

Output: data/processed/alphafold_open.csv
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
ACCESSIONS = {
    "P69905": "human hemoglobin alpha",
    "P01942": "mouse hemoglobin alpha",
    "P0A7V8": "E. coli ribosomal protein S4",
    "Q9FY48": "Arabidopsis E3 ligase KEG",
}


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache" / "alphafold", UA)
    rows = []
    for acc, what in ACCESSIONS.items():
        status, body = get(f"https://alphafold.ebi.ac.uk/api/prediction/{acc}")
        if status != 200:
            rows.append({"accession": acc, "protein": what, "served": False})
            continue
        meta = json.loads(body)[0]
        status, cif = get(meta["cifUrl"])
        licence = re.search(r'"Data in this file is available under a ([^"]+)\."', cif)
        rows.append(
            {
                "accession": acc,
                "protein": meta.get("uniprotDescription", what),
                "organism": meta.get("organismScientificName"),
                "served": status == 200,
                "model_version": meta.get("latestVersion"),
                "mean_plddt": meta.get("globalMetricValue"),
                "licence_in_file": licence.group(1) if licence else None,
                "commercial_use_stated": "AVAILABLE FOR ACADEMIC AND COMMERCIAL PURPOSES" in cif.replace("\n", " "),
            }
        )
    df = pd.DataFrame(rows)
    out = SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "alphafold_open.csv", index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
