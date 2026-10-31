"""Map each box in slide 14's figure to what MESA's PUBLIC docs say exists (not its code).

Reads the Markdown twins of idss-mesa.github.io (home page) and the docs index,
then records, per figure box, which documented component (if any) it maps to and
whether the docs list it as installable today or as a stated goal.
Output: data/processed/mesa_box_map.csv
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from evidence.http import CachedGet  # noqa: E402

get = CachedGet(HERE / "data" / "cache", "colloquium-evidence/0.1 (UNM CARC research)")
HOME = "https://idss-mesa.github.io/okf/concepts/home.md"
DOCS = "https://idss-mesa.github.io/docs/index.md"
docs = {}
for u in (HOME, DOCS):
    s, body = get(u)
    assert s == 200, (u, s)
    docs[u] = body

# (box, needle that must appear, doc, documented component, status per docs)
CHECKS = [
    ("User request", "Claude Code", DOCS, "Agent clients (Claude Code, Codex CLI, Antigravity, OpenCode) and MESA Portal apps", "third-party clients + MESA Portal; installable today"),
    ("MCP context", "Reference iRODS Data Store MCP server", DOCS, "mesa-mcp, irods-mcp-server, Formation (hosted by CyVerse)", "installable today"),
    ("RAG retrieval", "RAG", HOME, "Layer 02 lists RAG; goal 03 'RAG pipelines over curated metadata'", "stated goal; no RAG component in the installed-server table"),
    ("AI agent orchestrator", "multi-agent orchestration", HOME, "Goal 03 'sandboxed, multi-agent orchestration'; today the orchestrator is the user's own agent client", "stated goal; no MESA orchestrator component in the installed-server table"),
    ("iRODS data mesh", "iRODS Data Store", DOCS, "mesa-mcp (ds_* tools) and irods-mcp-server over the CyVerse Data Store (iRODS)", "installable today (access to the Data Store); federation is goal 02"),
    ("DuckLake data lake", "DuckLake metadata history", DOCS, "mesa-ducklake: AVU metadata-history library backing mesa-mcp", "installable today, but scoped to metadata history; the general lakehouse is goal 01"),
]
installed_table = docs[DOCS].split("| Server | Language | What it does |")[1].split("\n\n")[0]
out = HERE / "data" / "processed" / "mesa_box_map.csv"
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["box", "needle", "needle_found", "in_installed_server_table", "documented_component", "status_per_docs", "source"])
    for box, needle, src, comp, status in CHECKS:
        w.writerow([box, needle, needle in docs[src], needle in installed_table, comp, status, src])
print(out.read_text())
