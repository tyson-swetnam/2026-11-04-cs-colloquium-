"""Slide 28 checks.

1. Licence for every component named in the stack figure (deps.dev project API for software;
   facilities and services are marked not-applicable). -> data/processed/licences.csv
2. Does MESA's public site/docs mention each compute site the slide says it runs on?
   -> data/processed/site_mentions.csv
3. Live check of the MESA endpoints on CyVerse. -> data/processed/endpoints.csv
4. Every facts.csv quote appears verbatim (whitespace-normalised) in the fetched document.
   -> data/processed/quote_check.csv

Run 01_fetch_sources.py first.
"""
from __future__ import annotations

import csv
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

import requests

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
SRC = HERE / "data/raw/sources"
OUT = HERE / "data/processed"
get = CachedGet(HERE / "data/cache", UA)

# layer, component (as in the figure), kind, deps.dev project (github.com/...) or None, note
COMPONENTS = [
    ("User interface", "Laptop / Desktop", "hardware", None, "Hardware; licence not applicable"),
    ("User interface", "K8s Container", "software", "kubernetes/kubernetes", ""),
    ("Agentic AI", "Agentic AI (unnamed in figure)", "software", None,
     "Figure names no product; MESA supports Claude Code, Codex CLI, Antigravity, OpenCode (rows below)"),
    ("Agentic AI", "Claude Code (MESA client)", "software", "anthropics/claude-code",
     "Anthropic terms of service, not an OSI licence (facts f08)"),
    ("Agentic AI", "Codex CLI (MESA client)", "software", "openai/codex", ""),
    ("Agentic AI", "Antigravity (MESA client)", "software", None, "Google product; licence not checked"),
    ("Agentic AI", "OpenCode (MESA client)", "software", "sst/opencode", ""),
    ("Data management", "DuckLake", "software", "duckdb/ducklake", ""),
    ("Data management", "S3 API", "interface", None,
     "Amazon's API; no open-source licence, but implemented by open-source servers"),
    ("Data management", "iRODS", "software", "irods/irods", ""),
    ("Data management", "K8s CSI", "specification", "container-storage-interface/spec", ""),
    ("Compute", "CyVerse", "facility", None, "Facility/service; licence not applicable"),
    ("Compute", "TACC", "facility", None, "Facility; licence not applicable"),
    ("Compute", "ACCESS-CI", "program", None, "Allocation program; licence not applicable"),
    ("Compute", "NAIRR", "program", None, "Program; licence not applicable"),
    ("Object storage", "OSN", "service", None, "Storage service (Ceph-based pods); licence not applicable"),
    ("Object storage", "AWS S3", "commercial service", None, "Proprietary cloud service (facts f06)"),
    ("Object storage", "VAST", "commercial software", None, "Proprietary EULA (facts f04, f05)"),
    ("Object storage", "Lustre", "software", "lustre/lustre-release",
     "lustre.org: open-source (facts f03); deps.dev reports 'non-standard' (GPL-2.0 with exceptions)"),
]

OPEN = {"MIT", "Apache-2.0", "BSD-3-Clause", "non-standard"}


def licences() -> None:
    rows = []
    for layer, comp, kind, proj, note in COMPONENTS:
        lic = ""
        if proj:
            code, body = get(f"https://api.deps.dev/v3/projects/{quote('github.com/' + proj, safe='')}")
            lic = json.loads(body).get("license", "") if code == 200 else f"HTTP {code}"
            lic = lic or "(none reported)"
        if kind in {"hardware", "facility", "program", "service"}:
            verdict = "not applicable"
        elif comp == "Lustre" or lic in OPEN - {"non-standard"}:
            verdict = "open source"
        elif kind in {"commercial service", "commercial software"} or comp.startswith("Claude Code"):
            verdict = "proprietary"
        elif comp == "S3 API":
            verdict = "proprietary interface (open implementations exist)"
        else:
            verdict = "not checked"
        rows.append({"layer": layer, "component": comp, "kind": kind,
                     "deps_dev_project": f"github.com/{proj}" if proj else "",
                     "deps_dev_licence": lic, "verdict": verdict, "note": note})
    with open(OUT / "licences.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['layer']:16} {r['component']:32} {r['deps_dev_licence']:16} {r['verdict']}")


def text(path: Path) -> str:
    t = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".html":
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", " ", t)
    elif path.suffix == ".json":
        aw = json.loads(t)["response"]["award"][0]
        # abstract plus every other string field (e.g. fundProgramName), one per segment
        t = " | ".join([aw["abstractText"]] + [str(v) for k, v in aw.items() if k != "abstractText" and isinstance(v, str)])
    t = html.unescape(t).replace("**", "")
    return re.sub(r"\s+", " ", t)


def site_mentions() -> None:
    terms = {"TACC": r"\bTACC\b|Texas Advanced Computing", "Jetstream": r"Jetstream",
             "NAIRR": r"\bNAIRR\b", "ACCESS-CI": r"ACCESS[- ]CI|access-ci", "CyVerse": r"CyVerse"}
    rows = []
    for fn in ["mesa_stack.html", "mesa_docs_llms-full.txt"]:
        t = text(SRC / fn)
        for k, p in terms.items():
            rows.append({"document": fn, "term": k, "mentions": len(re.findall(p, t))})
    with open(OUT / "site_mentions.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(rows)


def endpoints() -> None:
    rows = []
    for u in ["https://mesa.cyverse.org/", "https://mcp-public.cyverse.ai/mcp",
              "https://de.cyverse.org/formation/mcp"]:
        try:
            code = requests.get(u, headers={"User-Agent": UA}, timeout=30).status_code
        except requests.RequestException as e:
            code = f"error: {e.__class__.__name__}"
        rows.append({"url": u, "status": code})
    with open(OUT / "endpoints.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url", "status"])
        w.writeheader()
        w.writerows(rows)
    print(rows)


URL_TO_FILE = {
    "https://ducklake.select/": "ducklake_select.html",
    "https://irods.org/license/": "irods_license.html",
    "https://www.lustre.org/": "lustre_org.html",
    "https://www.vastdata.com/legal/end-user-services-and-license-agreement": "vast_eula.html",
    "https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html": "aws_s3_api_welcome.html",
    "https://www.openstoragenetwork.org/": "osn_home.html",
    "https://code.claude.com/docs/en/legal-and-compliance": "claude_code_legal.html",
    "https://idss-mesa.github.io/docs/llms-full.txt": "mesa_docs_llms-full.txt",
    "https://idss-mesa.github.io/stack.html": "mesa_stack.html",
    "https://api.nsf.gov/services/v1/awards/2632685.json": "nsf_award_2632685.json",
}


def quote_check() -> None:
    norm = lambda s: re.sub(r"\s+", " ", s).strip()  # noqa: E731
    rows = []
    with open(HERE / "data/raw/research/facts.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["url"].startswith("talk/"):
                fn, t = "talk/slides.md", norm((REPO / "talk/slides.md").read_text(encoding="utf-8"))
            else:
                fn = URL_TO_FILE[r["url"]]
                t = text(SRC / fn)
            rows.append({"id": r["id"], "claim_id": r["claim_id"], "file": fn,
                         "quote_found": norm(r["quote"]) in t})
    with open(OUT / "quote_check.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    bad = [r["id"] for r in rows if not r["quote_found"]]
    print("quotes not found:", bad or "none")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    licences()
    site_mentions()
    endpoints()
    quote_check()
