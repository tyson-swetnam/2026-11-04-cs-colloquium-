"""Check that every quote in facts.csv appears verbatim (whitespace-normalised) in a fetched
document, and check the deck text of slide 23 for the CAISP speaker-note claim (c8)."""
import csv
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
SRC = HERE / "data/raw/sources"
OUT = HERE / "data/processed"

URL_TO_FILE = {
    "https://docs.cyverse.org/architecture/system-overview/": "docs.cyverse.org_architecture_system-overview_.html",
    "https://cyverse.org/data-store": "cyverse.org_data-store.html",
    "https://unblockme.cyverse.org/": "cyverse_unblockme.html",
    "https://carc.unm.edu/jobs/postdoc-agentic-ai/": "carc_site_llms-full.txt",
    "https://carc.unm.edu/ai-research-resources/": "carc_site_llms-full.txt",
    "https://idss-mesa.github.io/okf/concepts/mesa-sandbox.md": "mesa_sandbox_concept.md",
    "https://docs.jetstream-cloud.org/alloc/overview/": "docs.jetstream-cloud.org_alloc_overview_.html",
    "https://docs.jetstream-cloud.org/general/vmsizes/": "docs.jetstream-cloud.org_general_vmsizes_.html",
    "https://docs.jetstream-cloud.org/overview/overview-doc/": "docs.jetstream-cloud.org_overview_overview-doc_.html",
    "https://docs.jetstream-cloud.org/inference-service/overview/": "docs.jetstream-cloud.org_inference-service_overview_.html",
    "https://nrp.ai/documentation/userdocs/ai/llm-managed/": "nrp.ai_documentation_userdocs_ai_llm-managed_.html",
    "https://cider.access-ci.org/public/resources/RDR_003540": "cider.access-ci.org_public_resources_RDR_003540.html",
    "https://idss-mesa.github.io/mesa-anyjev/getting-started/gateway/": "mesa_anyjev_llms-full.txt",
    "https://idss-mesa.github.io/llms-full.txt": "mesa_site_llms-full.txt",
    "https://idss-mesa.github.io/okf/concepts/hiring.md": "mesa_site_llms-full.txt",
    "https://docs.jetstream-cloud.org/general/running-llm/": "docs.jetstream-cloud.org_general_running-llm_.html",
    "https://nrp.ai/about/": "nrp.ai_about_.html",
}


def text(path: Path) -> str:
    t = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".html":
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("**", "")
    return re.sub(r"\s+", " ", t)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with open(HERE / "data/raw/research/facts.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["url"].startswith("talk/slides.md"):
                fn, path = "talk/slides.md", REPO / "talk/slides.md"
            elif r["url"].startswith("https://api.nsf.gov/"):
                fn, path = "nsf_award_2632685.json", OUT / "nsf_award_2632685.json"
            else:
                fn = URL_TO_FILE.get(r["url"])
                path = SRC / fn if fn else None
            found = bool(path) and norm(r["quote"]) in text(path)
            rows.append({"id": r["id"], "claim_id": r["claim_id"], "file": fn or "", "quote_found": found})
    with open(OUT / "quote_check.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    bad = [r["id"] for r in rows if not r["quote_found"]]
    print(f"{len(rows) - len(bad)}/{len(rows)} quotes found; missing: {bad}")

    # c8: slide 23 block of talk/slides.md
    deck = (REPO / "talk/slides.md").read_text(encoding="utf-8")
    block = deck.split('<a id="slide-23"></a>')[1].split('<a id="slide-24"></a>')[0]
    body, _, notes = block.partition("> **Notes:**")
    res = {
        "caisp_in_slide_text": "CAISP" in body,
        "caisp_in_notes": "CAISP" in notes,
        "notes_caisp_sentence": next((s.strip() + "." for s in notes.split(".") if "CAISP" in s), ""),
        "notes_says_all_four_bookable": "all four are bookable now" in notes,
        "slide_text": body.strip(),
        "notes": notes.strip(),
    }
    (OUT / "deck_check.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print({k: v for k, v in res.items() if k not in ("slide_text", "notes")})
