"""Paths, data sources and the assumptions every script in this folder shares."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLIDE = HERE.parent
RAW = SLIDE / "data" / "raw"
PROCESSED = SLIDE / "data" / "processed"
FIGURES = SLIDE / "figures"
sys.path.insert(0, str(SLIDE.parents[1]))  # repo root, for `evidence`

# Base year for every constant-dollar and economic-share figure.
REF_YEAR = 2025
# Moorhouse's chart is in 2024 dollars; the baseline reproduction uses this.
MOORHOUSE_YEAR = 2024
# 2026 is incomplete: BEA quarters are averaged (SAAR) and company capex is YTD scaled up.
PARTIAL_YEAR = 2026

UA = "colloquium-evidence/0.1 (UNM CARC research)"
# data.sec.gov asks automated clients to identify themselves; set SEC_USER_AGENT to
# "Name email@domain" to follow SEC's fair-access guidance fully.
SEC_UA = os.environ.get("SEC_USER_AGENT", "UNM CARC colloquium-evidence research")

# Five US hyperscalers in Moorhouse's chart. Concept = the us-gaap tag each one uses for
# "purchases of property and equipment" on the cash-flow statement (gross; finance leases excluded).
HYPERSCALERS = {
    "Amazon": {"cik": "0001018724", "concept": "PaymentsToAcquireProductiveAssets"},
    "Microsoft": {"cik": "0000789019", "concept": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "Alphabet": {"cik": "0001652044", "concept": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "Meta": {"cik": "0001326801", "concept": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "Oracle": {"cik": "0001341439", "concept": "PaymentsToAcquirePropertyPlantAndEquipment"},
}

# Moorhouse: "Assuming DC share scales from ≈55% in 2020 to ≈80% by 2026" (Epoch AI + Platformonomics).
DC_SHARE_START = (2020, 0.55)
DC_SHARE_END = (2026, 0.80)


def dc_share(year: int) -> float:
    (y0, s0), (y1, s1) = DC_SHARE_START, DC_SHARE_END
    t = min(max((year - y0) / (y1 - y0), 0.0), 1.0)
    return s0 + t * (s1 - s0)


# BEA NIPA series (annual flat file, current dollars, millions).
BEA_SERIES = {
    "A191RC": "GDP",
    "A191RD": "GDP price deflator (2017=100)",
    "LA001282": "Private fixed investment in structures: data centers (Table 5.4.5 line 5)",
    "C319RC": "Private structures: petroleum and natural gas wells (Table 5.4.5 line 25)",
    "C314RC": "Private structures: communication (Table 5.4.5 line 23)",
    "C275RC": "Private equipment: communication equipment (Table 5.5.5 line 5)",
    "A007RC": "Private fixed investment (Table 1.1.5 line 8)",
    "A008RC": "Private fixed investment: nonresidential (Table 1.1.5 line 9)",
    "A011RC": "Private fixed investment: residential (Table 1.1.5 line 13)",
}
