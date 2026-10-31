"""Fetch the iRODS docs, MESA public pages and the NSF award record used by slide 22."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1]))
from evidence.http import CachedGet
from evidence.fetch import record

get = CachedGet(ROOT / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")
SRC = ROOT / "data/raw/sources"
URLS = {
  "irods_users_permissions.html": "https://docs.irods.org/4.3.4/system_overview/users_and_permissions/",
  "irods_federation.html": "https://docs.irods.org/4.3.4/system_overview/federation/",
  "irods_glossary.html": "https://docs.irods.org/4.3.4/system_overview/glossary/",
  "irods_dynamic_peps.html": "https://docs.irods.org/4.3.4/plugins/dynamic_policy_enforcement_points/",
  "irods_overview.html": "https://docs.irods.org/4.3.4/getting_started/introduction/",
  "irods_trash.html": "https://docs.irods.org/4.3.4/system_overview/configuration/",
  "irods_icommands_user.html": "https://docs.irods.org/4.3.4/icommands/user/",
  "irods_auditing.html": "https://docs.irods.org/4.3.4/capabilities/auditing/",
  "irods_why.html": "https://docs.irods.org/4.3.4/why_irods/",
  "irods_home.html": "https://docs.irods.org/4.3.4/",
  "irods_policy_cookbook.html": "https://docs.irods.org/4.3.4/administrators/policy_cookbook/",
  "irods_rule_engine.html": "https://docs.irods.org/4.3.4/plugins/pluggable_rule_engine/",
  "irods_release_notes.html": "https://docs.irods.org/4.3.4/release_notes/",
  "mesa_okf_home.md": "https://idss-mesa.github.io/okf/concepts/home.md",
  "mesa_irods_mcp_server.md": "https://idss-mesa.github.io/okf/concepts/irods-mcp-server.md",
  "mesa_mesa_mcp.md": "https://idss-mesa.github.io/okf/concepts/mesa-mcp.md",
  "mesa_formation_mcp.md": "https://idss-mesa.github.io/okf/concepts/formation-mcp.md",
  "mesa_mesa_sandbox.md": "https://idss-mesa.github.io/okf/concepts/mesa-sandbox.md",
  "mesa_docs.md": "https://idss-mesa.github.io/okf/concepts/docs.md",
  "mesa_stack.md": "https://idss-mesa.github.io/okf/concepts/stack.md",
  "mesa_llms.txt": "https://idss-mesa.github.io/llms.txt",
  "nsf_award_2632685.json": "https://api.nsf.gov/services/v1/awards/2632685.json?printFields=id,title,agency,awardeeName,piFirstName,piLastName,startDate,expDate,fundsObligatedAmt,abstractText",
}
for name, url in URLS.items():
    st, body = get(url)
    print(name, st, len(body))
    if st == 200:
        p = SRC / name
        p.write_text(body, encoding="utf-8")
        record(p, url=url, source=name.split("_")[0], note="slide 22 evidence")
