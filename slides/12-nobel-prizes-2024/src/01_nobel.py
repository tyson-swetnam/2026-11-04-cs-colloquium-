"""Check the slide's laureates, shares and prize wording against the Nobel Prize API (v2.1),
and pull the Academy's own description of the chemistry prize from its press release.

Output: data/raw/nobel_2024_{phy,che}.json (API responses, CC0), data/processed/nobel_check.csv,
data/processed/nobel_quotes.csv (sentences quoted from the press release, which is not committed)
"""

from __future__ import annotations

import html
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.fetch import fetch  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
# What the slide says, verbatim.
ON_SLIDE = {
    "phy": {"laureates": ["John Hopfield", "Geoffrey Hinton"], "wording": "Foundational discoveries enabling machine learning with artificial neural networks"},
    "che": {"laureates": ["David Baker", "Demis Hassabis", "John Jumper"], "wording": "Computational protein design, and protein structure prediction"},
}


def surname(name: str) -> str:
    return name.split()[-1].lower()


QUOTES = [  # sentences to quote from the chemistry press release, located by these fragments
    "developed an AI model to solve a 50-year-old problem",
    "In 2003, David Baker succeeded",
    "predict the structure of virtually all the 200 million proteins",
    "revealed proteins’ secrets through computing and artificial intelligence",
]


def press_release_quotes() -> pd.DataFrame:
    path = fetch(
        "https://www.nobelprize.org/prizes/chemistry/2024/press-release/",
        SLIDE / "data" / "raw" / "sources" / "nobel_2024_chemistry_press_release.html",
        source="The Royal Swedish Academy of Sciences, press release, 9 Oct. 2024",
        license="© The Nobel Foundation; quoted, not redistributed",
        user_agent=UA,
    )
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8", errors="ignore")))).replace("\u00ad", "")
    rows = []
    for frag in QUOTES:
        i = text.find(frag)
        if i < 0:
            raise ValueError(f"not in press release: {frag}")
        # Sentences end at a full stop; link captions on the page end at " (pdf)" or start after ": ".
        start = max(text.rfind(". ", 0, i) + 2, text.rfind(": ", 0, i) + 2, i - 200)
        ends = [p for p in (text.find(".", i + len(frag)) + 1, text.find(" (pdf)", i + len(frag))) if p > 0]
        end = min(ends)
        rows.append({"fragment": frag, "sentence": text[start:end].strip()})
    return pd.DataFrame(rows)


def main() -> None:
    rows = []
    for cat, slide in ON_SLIDE.items():
        path = fetch(
            f"https://api.nobelprize.org/2.1/nobelPrizes?nobelPrizeYear=2024&nobelPrizeCategory={cat}",
            SLIDE / "data" / "raw" / f"nobel_2024_{cat}.json",
            source="Nobel Prize API v2.1 (Nobel Prize Outreach)",
            license="CC0 (nobelprize.org data)",
            user_agent=UA,
        )
        prize = json.loads(path.read_text())["nobelPrizes"][0]
        laureates = prize["laureates"]
        official_names = [l["knownName"]["en"] for l in laureates]
        motivations = list(dict.fromkeys(l["motivation"]["en"] for l in laureates))
        official = "; ".join(motivations)
        rows.append(
            {
                "prize": prize["categoryFullName"]["en"],
                "official_laureates": "; ".join(f"{l['knownName']['en']} ({l['portion']})" for l in laureates),
                "slide_laureates": "; ".join(slide["laureates"]),
                "laureates_match": sorted(map(surname, official_names)) == sorted(map(surname, slide["laureates"])),
                "official_motivation": official,
                "slide_wording": slide["wording"],
                "wording_similarity": round(SequenceMatcher(None, slide["wording"].lower(), official.lower()).ratio(), 2),
            }
        )
    df = pd.DataFrame(rows)
    out = SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "nobel_check.csv", index=False)
    quotes = press_release_quotes()
    quotes.to_csv(out / "nobel_quotes.csv", index=False)
    for r in rows:
        print(f"{r['prize']}: laureates match={r['laureates_match']} ({r['official_laureates']})")
        print(f"  official: {r['official_motivation']}")
        print(f"  slide:    {r['slide_wording']}  (similarity {r['wording_similarity']})")
    for q in quotes.sentence:
        print("  press release:", q)


if __name__ == "__main__":
    main()
