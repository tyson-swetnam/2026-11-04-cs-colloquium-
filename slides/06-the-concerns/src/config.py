"""Paths and shared settings for slide 06."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLIDE = HERE.parent
RAW = SLIDE / "data" / "raw"
PROCESSED = SLIDE / "data" / "processed"
FIGURES = SLIDE / "figures"
ROOT = SLIDE.parents[1]
sys.path.insert(0, str(ROOT))  # for `evidence`

PARTIAL_YEAR = 2026
SEC_UA = os.environ.get("SEC_USER_AGENT", "UNM CARC colloquium-evidence research")

# Same five firms and capex tags as slide 05; operating cash flow and debt added here.
HYPERSCALERS = {
    "Amazon": {"cik": "0001018724", "capex": "PaymentsToAcquireProductiveAssets"},
    "Microsoft": {"cik": "0000789019", "capex": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "Alphabet": {"cik": "0001652044", "capex": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "Meta": {"cik": "0001326801", "capex": "PaymentsToAcquirePropertyPlantAndEquipment"},
    "Oracle": {"cik": "0001341439", "capex": "PaymentsToAcquirePropertyPlantAndEquipment"},
}
OCF = "NetCashProvidedByUsedInOperatingActivities"
# Total debt, per period end, from the first of these that the filer reported for that date:
# LongTermDebt (incl. current portion), else noncurrent + current, else Oracle's combined tag.
DEBT_TOTAL = "LongTermDebt"
DEBT_PARTS = ("LongTermDebtNoncurrent", "LongTermDebtCurrent")
DEBT_COMBINED = "DebtLongtermAndShorttermCombinedAmount"
