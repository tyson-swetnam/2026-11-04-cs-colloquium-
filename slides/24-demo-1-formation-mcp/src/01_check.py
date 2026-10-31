"""Slide 24 (Demo 1, Formation MCP): check the slide's claims against public docs.

Sources: MESA's public docs (idss-mesa.github.io, Markdown twins), CyVerse's core software
docs (docs.cyverse.org, Markdown twins) and the NSF Award API. No MESA or CyVerse code was read.
Each fetched page is saved under data/raw/sources/ and logged in MANIFEST.yaml; each quote
below is searched for (whitespace-normalised) in the saved text.
Output: data/processed/checks.csv, data/processed/nsf_award.csv
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.fetch import record  # noqa: E402
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
MESA = "https://idss-mesa.github.io/docs/"
CYV = "https://docs.cyverse.org/"
PAGES = {
    "formation": MESA + "servers/formation-mcp/index.md",
    "irods": MESA + "servers/irods-mcp-server/index.md",
    "mesa_full": MESA + "llms-full.txt",
    "cy_overview": CYV + "architecture/system-overview/index.md",
    "cy_argo": CYV + "deployment/04-kubernetes/argo/index.md",
    "cy_vice": CYV + "deployment/06-applications/vice/index.md",
}
# (fact id, claim id, page, exact quote)
CHECKS = [
    ("f1", "c4", "formation", "Formation is the CyVerse Discovery Environment's own MCP server"),
    ("f2", "c4", "formation", "**Run by:** CyVerse"),
    ("f3", "c2", "formation", "registers Formation by URL with every client it detects"),
    ("f4", "c2", "formation", "whether Codex, OpenCode, and Antigravity can complete the CyVerse sign-in is not yet confirmed"),
    ("f5", "c2", "formation", "CyVerse does not yet accept that client's sign-in callback."),
    ("f6", "c2", "formation", "OpenCode and Goose cannot complete the sign-in in the apps."),
    ("f7", "c3", "formation", "launch apps, manage analyses, and work with the Data Store"),
    ("f8", "c3", "formation", "Batch (non-interactive) jobs return as soon as they are submitted"),
    ("f9", "c3", "cy_vice", "Interactive analyses run on the workers in the `k8s_vice_workers` inventory group"),
    ("f10", "c3", "cy_argo", "Argo Workflows runs the containerized, non-interactive side of DE analyses inside Kubernetes — the batch counterpart to VICE."),
    ("f11", "c3", "cy_argo", "Deployments that predate it dispatch those jobs to HTCondor instead"),
    ("f12", "c3", "cy_overview", "CyVerse runs mainly on a locally managed K8s cluster, but it can be federated to other K8s clusters."),
    ("f13", "c3", "cy_overview", "DE uses [HTCondor](https://htcondor.org/){target=_blank} for `executable` jobs on CyVerse resources"),
    ("f14", "c3", "mesa_full", "| `ds_*` | iRODS Data Store: list/read/write/move files, directories, AVUs, ACLs, tickets, rules, policies"),
    ("f15", "c3", "irods", "Anonymous access to public data under `/iplant/home/shared`, or authenticated access with iRODS credentials."),
    ("f16", "c3", "mesa_full", "Without it they have anonymous, read-only access to public data."),
    ("f17", "c2", "mesa_full", "After install, the three servers (`mesa-mcp`, `irods`, `formation`) are registered with every client the installer detected"),
    ("f18", "c5", "mesa_full", "Codex and Antigravity run a local `irods` server, and every agent runs a local `mesa` server"),
    ("f19", "c5", "mesa_full", "OpenCode's `irods` is the hosted public endpoint, which reads public data only."),
    ("f20", "c4", "irods", "It is registered under the name `irods` with every detected client"),
]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache", UA)
    raw = SLIDE / "data" / "raw" / "sources"
    raw.mkdir(parents=True, exist_ok=True)
    text = {}
    for key, url in PAGES.items():
        status, body = get(url)
        if status != 200:
            raise SystemExit(f"{url}: HTTP {status}")
        dest = raw / f"{key}{Path(url).suffix or '.md'}"
        dest.write_text(body, encoding="utf-8")
        src = "MESA documentation (idss-mesa.github.io)" if url.startswith(MESA) else "CyVerse Core Software Documentation (docs.cyverse.org)"
        record(dest, url=url, source=src, note="Markdown twin; public docs only")
        text[key] = norm(body)
    rows = [{"fact": f, "claim": c, "url": PAGES[p], "found": q in text[p], "quote": q} for f, c, p, q in CHECKS]
    out = SLIDE / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(out / "checks.csv", index=False)
    print(df[["fact", "claim", "found"]].to_string(index=False))

    # NSF award shown in the slide footer
    url = ("https://api.nsf.gov/services/v1/awards/2632685.json?printFields="
           "id,title,awardeeName,piFirstName,piLastName,startDate,expDate,fundProgramName,estimatedTotalAmt")
    status, body = get(url)
    dest = raw / "nsf_award_2632685.json"
    dest.write_text(body, encoding="utf-8")
    record(dest, url=url, source="NSF Award API", note="Award shown in slide footer")
    award = json.loads(body)["response"]["award"]
    keep = ["id", "title", "awardeeName", "pdPIName", "startDate", "expDate", "fundProgramName", "orgLongName2", "estimatedTotalAmt", "transType"]
    award = [{k: a.get(k) for k in keep} for a in award]
    pd.DataFrame(award).to_csv(out / "nsf_award.csv", index=False)
    print(award)
    if not df.found.all():
        raise SystemExit("some quotes not found")


if __name__ == "__main__":
    main()
