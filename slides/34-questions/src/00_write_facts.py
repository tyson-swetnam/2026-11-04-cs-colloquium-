"""Slide 34: write data/raw/research/facts.csv (quotes copied from documents fetched by 01/02)."""
import csv
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
API = "https://api.nsf.gov/services/v1/awards/{}.json"
D = "2026-10-31"
def nsf(i, c, a, field, q, note=""):
    return [i, c, f"{field} of NSF award {a}", q, f"NSF Award API: award {a}", "U.S. National Science Foundation", D, API.format(a), "primary", f"{note} file=nsf_award_{a}.json; field={field}".strip()]
rows = [
 nsf("f1", "c1", "2632685", "title", "Research Infrastructure: Category II: MESA (Multidisciplinary Environment for Scientific Advancement)"),
 nsf("f2", "c1", "2632685", "awardeeName", "University of New Mexico"),
 nsf("f3", "c1", "2632685", "orgLongName2", "Office of Advanced Cyberinfrastructure", "Managing division OAC (so 'OAC-2632685' is consistent)."),
 nsf("f4", "c1", "2632685", "fundProgramName", "NAIRR-Nat AI Research Resource", "Funding program is NAIRR; fills the [NAIRR] placeholder."),
 nsf("f5", "c1", "2632685", "startDate", "07/15/2026", "Ends 05/31/2029; $4,617,408 cooperative agreement."),
 ["f6", "c1", "MESA site acknowledgment", "MESA is supported by the U.S. National Science Foundation under Award #2632685", "MESA llms-full.txt", "MESA project (UNM)", D, "https://idss-mesa.github.io/llms-full.txt", "primary", "Same sentence on the home page (split by a link tag). file=mesa_llms_full.txt"],
 ["f7", "c1", "Earlier MESA award 2608717 (title)", "Research Infrastructure: Category II: MESA (Multidisciplinary Environment for Scientific Advancement)", "NSF Award API keyword search (AIIRA): award 2608717", "U.S. National Science Foundation", D, "https://api.nsf.gov/services/v1/awards.json?keyword=AIIRA", "primary", "Earlier award with the same title to University of Arizona, PI Swetnam (06/01/2026-08/31/2026, activeAwd false); appears superseded by UNM award 2632685. file=nsf_search_AIIRA.json"],
 ["f8", "c2", "MESA site links to GitHub org", 'href="https://github.com/idss-mesa"', "MESA home page", "MESA project (UNM)", D, "https://idss-mesa.github.io/", "primary", "idss-mesa.github.io returned HTTP 200 on 2026-10-31; github.com/idss-mesa could not be fetched from this session (proxy 403). file=mesa_site.html"],
 nsf("f9", "c3", "2217817", "title", "NEON Operations and Maintenance: Evolving from a Strong Foundation"),
 nsf("f10", "c3", "2217817", "awardeeName", "Battelle Memorial Institute"),
 nsf("f11", "c3", "2153040", "title", "Full Proposal: Environmental Data Science Innovation and Impact Lab (ESIIL): Accelerating Discovery by Fostering an Open and Diverse Earth Data Revolution"),
 nsf("f12", "c3", "2153040", "awardeeName", "University of Colorado at Boulder"),
 nsf("f13", "c3", "2335029", "title", "Center: National Synthesis Center for Emergence in the Molecular and Cellular Sciences"),
 nsf("f14", "c3", "2335029", "awardeeName", "Pennsylvania State Univ University Park"),
 nsf("f15", "c3", "2438843", "title", "Center: National Synthesis Center for Organismal Resilience to Environmental Change (NSCORE)"),
 nsf("f16", "c3", "2438843", "awardeeName", "Columbia University"),
 nsf("f17", "c3", "2438843", "transType", "Cooperative Agreement", "Starts 09/15/2026."),
 nsf("f18", "c3", "2535855", "title", "Frontier Science with the Event Horizon Telescope", "MIT-led Mid-scale instrumentation standard grant, 10/01/2025-09/30/2027; one of several EHT-related NSF awards."),
 ["f19", "c3", "AIIRA award number and funders", "supported by the National Science Foundation (NSF) and United States Department of Agriculture - National Institute of Food and Agriculture award #2021-67021-35329", "AI Institute for Resilient Agriculture home page", "Iowa State University", D, "https://aiira.iastate.edu/", "primary", "Awardee's own page; NIFA CRIS record (accession 1027030) not retrievable as text (404 / JavaScript-only). file=aiira_home.html.txt"],
 ["f20", "c4", "ESIIL current name", "ESIIL - The Environmental Data Science Innovation &amp; Impact Lab", "ESIIL home page", "University of Colorado Boulder", D, "https://esiil.org/", "primary", "Notes say 'Innovation & Inclusion Lab'; the lab and the NSF record say 'Innovation & Impact Lab'. file=esiil_home.html.txt"],
 ["f21", "c4", "ESIIL grant number", "ESIIL is funded by the National Science Foundation (NSF) under grant #2153040", "ESIIL home page", "University of Colorado Boulder", D, "https://esiil.org/", "primary", "file=esiil_home.html.txt"],
 ["f22", "c4", "AIIRA host and NSF+NIFA support", "The National Science Foundation and the U.S. Department of Agriculture’s National Institute of Food and Agriculture are supporting the researchers’ idea with a five-year, $20 millio", "$20 million federal grant launches AI Institute for Resilient Agriculture", "Iowa State University Office of the Vice President for Research", "2021", "https://research.iastate.edu/?p=8706", "primary", "file=isu_research_aiira_news.html.txt"],
 nsf("f23", "c5", "2632685", "abstractText", "The project will be developed and tested with established NSF-supported synthesis centers in environmental data science (ESIIL) and molecular and cellular science (NCEMS), and in AI in agriculture (AIIRA), as well as the international Event Horizon Telescope (EHT) Collaboration.", "Award names 4 of the 6 'early adopters'; NEON and NSCORE are not named."),
 ["f24", "c5", "MESA site anchor communities", "ESIIL, NCEMS, AIIRA, and the Event Horizon Telescope drive the use cases", "MESA llms-full.txt", "MESA project (UNM)", D, "https://idss-mesa.github.io/llms-full.txt", "primary", "NSCORE not mentioned; NEON appears as a data source (neon-mcp server). file=mesa_llms_full.txt"],
 ["f25", "c5", "MESA NEON MCP server", "server for the NEON Data API", "MESA llms-full.txt", "MESA project (UNM)", D, "https://idss-mesa.github.io/llms-full.txt", "primary", "file=mesa_llms_full.txt"],
 nsf("f26", "c6", "2632685", "pdPIName", "Tyson L Swetnam", "piEmail field = tswetnam@unm.edu (matches slide)."),
]
out = HERE / "data/raw/research/facts.csv"
with out.open("w", newline="") as f:
    w = csv.writer(f); w.writerow("id,claim_id,value,quote,source_title,publisher,date,url,source_type,notes".split(",")); w.writerows(rows)
print(len(rows), "rows")
