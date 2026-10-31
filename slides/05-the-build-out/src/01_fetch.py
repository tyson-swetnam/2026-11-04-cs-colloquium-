"""Download every source this slide uses into data/raw/, logging each in MANIFEST.yaml."""

from __future__ import annotations

import config
from evidence.fetch import fetch

MW = "MeasuringWorth (free for research use with citation)"
BEA = "U.S. Bureau of Economic Analysis, NIPA flat files (public domain)"
SEC = "SEC EDGAR XBRL company facts (public domain)"
WB = "World Bank World Development Indicators (CC BY 4.0)"


def main() -> None:
    raw = config.RAW
    fetch(
        "https://www.measuringworth.com/datasets/usgdp/export.php?year_source=1790&year_result=2025"
        "&use[]=NOMINALGDP&use[]=REALGDP&use[]=GDPDEFLATION&use[]=POPULATION&use[]=NOMGDPCP",
        raw / "measuringworth_us_gdp.csv",
        source="Williamson, 'What Was the U.S. GDP Then?' MeasuringWorth, 2026",
        license=MW,
    )
    fetch(
        "https://www.measuringworth.com/datasets/uscpi/export.php?year_source=1774&year_result=2025",
        raw / "measuringworth_us_cpi.csv",
        source="Officer and Williamson, 'The Annual Consumer Price Index for the United States, 1774-Present,' MeasuringWorth, 2026",
        license=MW,
    )
    for name in ("NipaDataA.txt", "NipaDataQ.txt", "SeriesRegister.txt"):
        fetch(f"https://apps.bea.gov/national/Release/TXT/{name}", raw / "bea" / name, source="BEA NIPA", license=BEA)
    fetch(
        "https://api.worldbank.org/v2/country/WLD;USA/indicator/NY.GDP.MKTP.CD?format=json&date=1960:2026&per_page=500",
        raw / "worldbank_gdp_current_usd.json",
        source="World Bank WDI NY.GDP.MKTP.CD",
        license=WB,
    )
    for name, firm in config.HYPERSCALERS.items():
        fetch(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{firm['cik']}.json",
            raw / "sec" / f"companyfacts_{name.lower()}.json",
            source=f"SEC EDGAR company facts, {name}",
            license=SEC,
            user_agent=config.SEC_UA,
        )


if __name__ == "__main__":
    main()
