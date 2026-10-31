"""Build facts.csv for slide 22 and check every quote appears verbatim in the fetched document text."""
import csv, html, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/raw/sources"

def text(name):
    s = (SRC / name).read_text(encoding="utf-8")
    if name.endswith(".html"):
        s = re.sub(r"(?s)<(script|style).*?</\1>", "", s)
        s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"\s+", " ", s)

D = "https://docs.irods.org/4.3.4"
M = "https://idss-mesa.github.io/okf/concepts"
IR, MS = "iRODS Consortium / RENCI", "MESA / University of New Mexico"
F = [
 # id, claim, value, quote, title, publisher, date, url, file, type, notes
 ("f1","c4","Unified namespace over distributed storage","iRODS implements data virtualization, allowing access to distributed storage assets under a unified namespace","iRODS Docs home (4.3.4)",IR,"2026-10-31",D+"/","irods_home.html","primary","Supports 'one namespace'"),
 ("f2","c4","Data stays where it is stored","It virtualizes data storage resources, so users can take control of their data, regardless of where and on what device the data is stored.","iRODS Docs home (4.3.4)",IR,"2026-10-31",D+"/","irods_home.html","primary","Supports 'data stays where it lives'"),
 ("f3","c4","MESA states one policy engine and data stays where it lives","One policy engine across the CyVerse Data Store and its federated peers, with CILogon, Globus Auth, and ORCID handling identity. The lakehouse and the mesh interoperate — your data stays where it lives, and still shows up where you work.","MESA home page (Markdown twin)",MS,"2026-10-31",M+"/home.md","mesa_okf_home.md","primary","Project's own description (developer-reported)"),
 ("f4","c4;c6","PEPs run before and after every operation","Within the REPF, there are dynamically created policy enforcement points that are checked before and after every operation.","Pluggable Rule Engine",IR,"2026-10-31",D+"/plugins/pluggable_rule_engine/","irods_rule_engine.html","primary","Basis for 'rules fire on ingest' (pep_api_data_obj_put_*) and for a pre-check on every request"),
 ("f5","c4;c5;c6","A failing _pre PEP blocks the operation","Note that if pep_PLUGINOPERATION_pre() fails, the PLUGINOPERATION will not be called.","Dynamic Policy Enforcement Points",IR,"2026-10-31",D+"/plugins/dynamic_policy_enforcement_points/","irods_dynamic_peps.html","primary","Mechanism to deny deletes before they touch data; a policy must be written, it is not default"),
 ("f6","c6","Fail-early gives admin control over allowed operations","This ability to fail early allows for fine-grained control of which plugin operations may or may not be allowed as defined by the policy of the data grid administrator.","Dynamic Policy Enforcement Points",IR,"2026-10-31",D+"/plugins/dynamic_policy_enforcement_points/","irods_dynamic_peps.html","primary",""),
 ("f7","c6","Delete has its own pre-PEP","pep_api_data_obj_unlink_prersComm_t * rsCommdataObjInp_t * dataObjUnlinkInp","Dynamic Policy Enforcement Points (API PEP table)",IR,"2026-10-31",D+"/plugins/dynamic_policy_enforcement_points/","irods_dynamic_peps.html","primary","Table cells run together after HTML stripping; rsComm carries the requesting user, dataObjInp the path"),
 ("f8","c6","PEP context carries the requesting user and zone","user_rods_zone=tempZone++++user_sys_uid=0++++user_user_name=rods","Dynamic Policy Enforcement Points (example *COMM)",IR,"2026-10-31",D+"/plugins/dynamic_policy_enforcement_points/","irods_dynamic_peps.html","primary","'Who is asking' and 'which zone' are available to the rule"),
 ("f9","c4","Default delete goes to trash; -f bypasses","By default, the data objects are moved to the trash collection (/myZone/trash) unless the -f option is used.","iCommands: irm",IR,"2026-10-31",D+"/icommands/user/","irods_icommands_user.html","primary","'No deleted datasets' is not default behaviour; it needs a policy"),
 ("f10","c8","iRODS 4.3 has 10 permission levels","The iRODS Permission Model is linear with 10 levels.","iCommands: ichmod",IR,"2026-10-31",D+"/icommands/user/","irods_icommands_user.html","primary","own / modify_object / read_object are three of the ten"),
 ("f11","c8","write/read are aliases","To maintain backwards compatibility, 'write' and 'read' are provided as aliases to 'modify_object' and 'read_object' respectively.","iCommands: ichmod",IR,"2026-10-31",D+"/icommands/user/","irods_icommands_user.html","primary",""),
 ("f12","c5","Delete needs delete_object; read-only account cannot delete","- irm - requires 'delete_object' or greater - imv - requires 'delete_object' or greater, due to removal of old name - iput - requires 'modify_object' or greater - iget - requires 'read_object' or greater","iCommands: ichmod",IR,"2026-10-31",D+"/icommands/user/","irods_icommands_user.html","primary","An account with read_object only cannot delete, move or overwrite"),
 ("f13","c9","Owner has full control and can share","The owner of a Data Object has full control of the file and can grant and remove access to other users and groups.","Users and Permissions",IR,"2026-10-31",D+"/system_overview/users_and_permissions/","irods_users_permissions.html","primary",""),
 ("f14","c9","Creator gets own by default","By default, the original creator of a dataObject has 'own' permission.","iCommands: ichmod",IR,"2026-10-31",D+"/icommands/user/","irods_icommands_user.html","primary",""),
 ("f15","c7","Audit plugin emits a message per PEP","The iRODS Audit Rule Engine Plugin provides the iRODS platform a C++ rule engine that emits a single AMQP message to the configured topic for every policy enforcement point (PEP) encountered by the iRODS server.","Auditing",IR,"2026-10-31",D+"/capabilities/auditing/","irods_auditing.html","primary","Optional plugin that must be installed and configured; not on by default"),
 ("f16","c7","Zones are independent administrative units","iRODS zones are independent administrative units.","Federation",IR,"2026-10-31",D+"/system_overview/federation/","irods_federation.html","primary",""),
 ("f17","c7","One iCAT per zone","There is one iCAT database per iRODS Zone.","Glossary",IR,"2026-10-31",D+"/system_overview/glossary/","irods_glossary.html","primary","Federated zones keep their own catalogs"),
 ("f18","c7","Federation preserves local control","Rather than a single iRODS zone managed by one administrator, they may need two (or more) cooperating iRODS systems managed locally, primarily for security and/or authorization reasons.","Federation",IR,"2026-10-31",D+"/system_overview/federation/","irods_federation.html","primary",""),
 ("f19","c5","MESA's Formation connector acts as the signed-in user, with delete","every tool then acts as that user.","Formation (hosted MCP server)",MS,"2026-10-31",M+"/formation-mcp.md","mesa_formation_mcp.md","primary","Tool list includes delete_data: this connector does not use a separate read-only agent account"),
 ("f20","c5","Formation tools include delete_data","`set_metadata`, `delete_data`.","Formation (hosted MCP server)",MS,"2026-10-31",M+"/formation-mcp.md","mesa_formation_mcp.md","primary",""),
 ("f21","c5","Public connector is anonymous read","CyVerse Data Store — public collections under `/iplant/home/shared`, anonymous read","MESA MCP stack",MS,"2026-10-31",M+"/stack.md","mesa_stack.md","primary","The one documented read-only agent identity"),
 ("f22","c5","mesa-sandbox: agents get user's permissions, not a read-only account; untested","agents **with the user's permissions but without the user's secrets**,","mesa-sandbox",MS,"2026-10-31",M+"/mesa-sandbox.md","mesa_mesa_sandbox.md","primary","Agent jobs carry the user's permissions; same page also plans a separate agent identity (f26) and says the Kubernetes profiles are untested on a cluster (f23)"),
 ("f23","c5","mesa-sandbox status","the Kubernetes profiles are untested on a cluster.","mesa-sandbox",MS,"2026-10-31",M+"/mesa-sandbox.md","mesa_mesa_sandbox.md","primary","Developer-reported status 2026-09-06"),
 ("f26","c5","mesa-sandbox design: each agent job gets its own UID, service account and credentials (planned)","each autonomous agent job runs as a separate pod with its own UID, service account, lifetime, credentials, and egress policy, sharing only the workspace volume.","mesa-sandbox",MS,"2026-10-31",M+"/mesa-sandbox.md","mesa_mesa_sandbox.md","primary","Supports 'its own account' as MESA's planned design (developer-reported, untested on a cluster per f23); nothing on the page says that account is read-only"),
 ("f27","c5","mesa-sandbox credentials come from a broker","An OpenBao broker issues short-lived credentials","mesa-sandbox",MS,"2026-10-31",M+"/mesa-sandbox.md","mesa_mesa_sandbox.md","primary","Separate short-lived agent credentials; rights level not stated"),
 ("f24","c10","NSF award 2632685 is MESA at UNM","Research Infrastructure: Category II: MESA (Multidisciplinary Environment for Scientific Advancement)","NSF Award API record 2632685","U.S. National Science Foundation","2026-07-26","https://api.nsf.gov/services/v1/awards/2632685.json","nsf_award_2632685.json","primary","Awardee University of New Mexico; PI Tyson L Swetnam; start 2026-07-15, end 2029-05-31; $4,617,408 obligated FY2026"),
 ("f25","c10","Abstract names iRODS and policy-driven governance","MESA will be implemented as a federated, cloud-native data-mesh and data lakehouse coupled to an agentic AI layer operating as an integrated data system and service.","NSF Award API record 2632685","U.S. National Science Foundation","2026-07-26","https://api.nsf.gov/services/v1/awards/2632685.json","nsf_award_2632685.json","primary","Planned work, not delivered capability"),
]
rows, bad = [], []
for f in F:
    fid, cid, val, q, title, pub, date, url, fname, st, notes = f
    t = text(fname) if not fname.endswith(".json") else re.sub(r"\s+"," ", json.dumps(json.loads((SRC/fname).read_text())["response"]["award"][0], ensure_ascii=False))
    ok = re.sub(r"\s+"," ",q) in t
    if not ok: bad.append(fid)
    rows.append(dict(id=fid, claim_id=cid, value=val, quote=q, source_title=title, publisher=pub, date=date, url=url, source_type=st, notes=notes))
out = ROOT/"data/raw/research/facts.csv"
with out.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with (ROOT/"data/processed/quote_check.csv").open("w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["fact_id","source_file","quote_found"])
    for f in F: w.writerow([f[0], f[8], f[0] not in bad])
print("missing:", bad)
