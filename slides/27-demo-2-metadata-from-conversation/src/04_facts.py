"""Slide 27: write data/raw/research/facts.csv and check that every quote appears in the
saved source document (HTML tags and runs of whitespace are ignored when matching).
"""

from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

SLIDE = Path(__file__).resolve().parents[1]
SRC = SLIDE / "data" / "raw" / "sources"
OUT = SLIDE / "data" / "raw" / "research" / "facts.csv"

MESA = ("mesa_llms_full.txt", "MESA documentation (llms-full.txt)", "IDSS-MESA (developer-written docs)", "2026-10-31", "https://idss-mesa.github.io/docs/llms-full.txt", "primary")
DS = "https://mcp-public.cyverse.ai/mcp"

# id, claim_id, value, quote, (file, title, publisher, date, url, type), notes
FACTS = [
    ("f1", "c2", "mesa-mcp writes ontology terms as iRODS AVUs, CURIE in the unit slot",
     "Metadata is written as `(attribute, value, unit)` triples, where `unit` is reserved for the ontology CURIE when the AVU came from OBO/OLS.",
     MESA, "Section 'The AVU contract' of https://idss-mesa.github.io/docs/servers/mesa-mcp/"),
    ("f2", "c3", "mesa_avu_* tools put the CURIE in the unit slot",
     "Apply ontology terms and DataCite fields as AVUs (with the CURIE in the `unit` slot)",
     MESA, "mesa-mcp tool-group table"),
    ("f3", "c2", "mesa-mcp runs locally; MESA docs point Claude Desktop users at Formation instead",
     "The installer's `mesa-mcp` and `irods` servers run on your own computer and are for",
     MESA, "https://idss-mesa.github.io/docs/claude-ai/ ; the sentence continues 'Claude Code and the other agent clients.'"),
    ("f4", "c2", "Clients MESA's installer supports",
     "the one-line install of the MESA MCP stack for Claude Code, Codex CLI, Antigravity, and OpenCode, and CyVerse's hosted Formation server for claude.ai.",
     MESA, "Site description; Claude Desktop is not in the installer's client list"),
    ("f5", "c2", "Claude Desktop gets MESA via custom connectors (Formation)",
     "On claude.ai and in Claude Desktop, MCP servers are added as **connectors**.",
     MESA, "https://idss-mesa.github.io/docs/claude-ai/"),
    ("f6", "c2", "MESA Portal shows and edits AVUs that mesa-mcp reads and writes",
     "AVUs are what the [mesa-mcp](https://idss-mesa.github.io/docs/servers/mesa-mcp/) server reads and writes, so an AI agent can find and curate the same metadata.",
     MESA, "https://idss-mesa.github.io/docs/portal/data/"),
    ("f7", "c4", "mesa_ols_* tools search OLS; no documented refusal at write time",
     "Browse OBO/OLS ontologies: search terms, fetch hierarchies, generate AVU templates",
     MESA, "mesa-mcp tool-group table"),
    ("f8", "c4", "In mesa-anyjev a curator's decision is authoritative",
     "a curator's pick, reject or decline (authoritative; becomes labels)",
     MESA, "https://idss-mesa.github.io/docs/servers/mesa-anyjev/ (status: draft)"),
    ("f9", "c5", "iRODS AVU definition",
     "Metadata attribute-value-units triples (AVUs) consist of an Attribute-Name, Attribute-Value, and an optional Attribute-Units.",
     ("irods_5.0.2_icommands_metadata.html", "imeta (icommands metadata)", "iRODS Consortium", "2026-10-31", "https://docs.irods.org/5.0.2/icommands/metadata/", "primary"), ""),
    ("f10", "c2", "Claude Desktop can run local MCP servers",
     "This guide demonstrates how to connect to local MCP servers using Claude Desktop as an example, one of the many clients that support MCP.",
     ("mcp_connect_local_servers.html", "Connect to local MCP servers", "Model Context Protocol", "2026-10-31", "https://modelcontextprotocol.io/docs/develop/connect-local-servers", "primary"), "Configured by hand in claude_desktop_config.json"),
    ("f11", "c3", "NCBITaxon:41073 = Carabidae (current)",
     '"label" : "Carabidae"',
     ("ols_NCBITaxon_41073.json", "OLS4 term NCBITaxon:41073", "EMBL-EBI", "2026-10-31", "https://www.ebi.ac.uk/ols4/api/ontologies/ncbitaxon/terms?obo_id=NCBITaxon:41073", "primary"), "is_obsolete false; see data/processed/terms.csv"),
    ("f12", "c3", "UO:0000016 = millimeter; 'millimetre' and 'mm' are synonyms",
     '"synonyms" : [ "millimetre", "mm" ]',
     ("ols_UO_0000016.json", "OLS4 term UO:0000016", "EMBL-EBI", "2026-10-31", "https://www.ebi.ac.uk/ols4/api/ontologies/uo/terms?obo_id=UO:0000016", "primary"), "Label is 'millimeter'"),
    ("f13", "c3", "DP1.10022.001 = ground beetles from pitfall traps; data at 47 sites, 2013-07 to 2026-10",
     '"productName":"Ground beetles sampled from pitfall traps"',
     ("neon_DP1.10022.001.json", "NEON data product DP1.10022.001", "NEON (Battelle/NSF)", "2026-10-31", "https://data.neonscience.org/api/v0/products/DP1.10022.001", "primary"), "Site count and months computed by src/01_check.py (data/processed/neon_product.csv)"),
    ("f14", "c8", "Award 2632685 is MESA, UNM, PI Swetnam",
     '"title":"Research Infrastructure: Category II: MESA (Multidisciplinary Environment for Scientific Advancement)"',
     ("nsf_award_2632685.json", "NSF Award 2632685", "U.S. National Science Foundation", "2026-10-31", "https://api.nsf.gov/services/v1/awards/2632685.json", "primary"), "data/processed/nsf_award.csv"),
    ("f15", "c3", "MESA-written AVU on a public NEON beetle collection: CURIE in unit slot",
     '"attr": "ncbitaxon.carabidae",\n          "value": "Carabidae",\n          "unit": "NCBITaxon:41073"',
     ("datastore_konz_dp1_10022_metadata.json", "AVUs on /iplant/home/shared/mesa/lakehouse/neon/neon-ducklake/sites/KONZ/raw/DP1.10022.001", "CyVerse Data Store (public MCP server)", "2026-10-31", DS, "primary"), "Not the neon-beetle-seg collection; the KONZ site folder of MESA's NEON lakehouse"),
    ("f16", "c3", "MESA-written millimetre AVU: attribute uo.millimeter, value = column, unit = UO:0000016",
     '"attr": "uo.millimeter",\n          "value": "bet_parataxonomistID.totalLength",\n          "unit": "UO:0000016"',
     ("datastore_konz_dp1_10022_metadata.json", "AVUs on .../neon-ducklake/sites/KONZ/raw/DP1.10022.001", "CyVerse Data Store (public MCP server)", "2026-10-31", DS, "primary"), ""),
    ("f17", "c7", "neon-beetle-seg collection not public per CyVerse's public Data Store server",
     'Path is not publicly accessible \\"/iplant/home/tswetnam/neon-beetle-seg\\"',
     ("datastore_neon_beetle_seg_metadata.json", "get_metadata /iplant/home/tswetnam/neon-beetle-seg", "CyVerse Data Store (public MCP server)", "2026-10-31", DS, "primary"), "data.cyverse.org/dav-anon/... redirected to unblockme.cyverse.org (bot check); not bypassed"),
]


def text_of(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    if path.suffix == ".html":
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    bad = 0
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "claim_id", "value", "quote", "source_title", "publisher", "date", "url", "source_type", "notes"])
        for fid, cid, value, quote, (fname, title, pub, date, url, stype), notes in FACTS:
            ok = re.sub(r"\s+", " ", quote) in text_of(SRC / fname)
            if not ok:
                bad += 1
                print(f"QUOTE NOT FOUND: {fid} in {fname}")
            w.writerow([fid, cid, value, re.sub(r"\s+", " ", quote), title, pub, date, url, stype, f"Saved as data/raw/sources/{fname}. {notes}".strip()])
    print(f"{len(FACTS)} facts, {bad} quotes not found")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
