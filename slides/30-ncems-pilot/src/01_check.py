"""Slide 30: fetch the public MESA docs, NSF award records and the CyVerse NCEMS story,
check every quote in data/raw/research/facts.csv against the fetched text, and look for any
public record of the NCEMS pilot (collection paths, AVU counts, DuckLake snapshot, OKF bundle)."""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evidence.http import CachedGet
from evidence.fetch import record

HERE = Path(__file__).resolve().parents[1]
RAW = HERE / "data/raw/sources"
RAW.mkdir(parents=True, exist_ok=True)
get = CachedGet(HERE / "data/cache", "colloquium-evidence/0.1 (UNM CARC research)")

AW = "id,title,awardeeName,pdPIName,startDate,expDate,fundProgramName,estimatedTotalAmt,abstractText"
SOURCES = {
    "mesa_docs_llms_full.txt": "https://idss-mesa.github.io/docs/llms-full.txt",
    "mesa_site_llms_full.txt": "https://idss-mesa.github.io/llms-full.txt",
    "mesa_okf_index.md": "https://idss-mesa.github.io/okf/index.md",
    "mesa_okf_news.md": "https://idss-mesa.github.io/okf/concepts/news.md",
    "nsf_award_2632685.json": f"https://api.nsf.gov/services/v1/awards/2632685.json?printFields={AW}",
    "nsf_award_2335029.json": f"https://api.nsf.gov/services/v1/awards/2335029.json?printFields={AW}",
    "cyverse_ncems_news.html": "https://cyverse.org/news/key-role-cyverse-nsfs-newest-synthesis-center",
}
texts, status = {}, {}
for name, url in SOURCES.items():
    st, body = get(url)
    status[name] = st
    if st == 200:
        (RAW / name).write_text(body)
        record(RAW / name, url=url, source=url.split("/")[2], note="slide 30 evidence")
        if name.endswith(".json"):
            body = json.loads(body)["response"]["award"][0]["abstractText"] + " " + json.loads(body)["response"]["award"][0]["title"]
        if name.endswith(".html"):
            body = re.sub(r"<[^>]+>", " ", body).replace("&#039;", "'")
        texts[name] = re.sub(r"\s+", " ", body)

# Public pilot artefacts we would expect to find if the pilot were documented.
probes = {"ncems_portal": "https://ncems.cyverse.org/", "datastore_dav_anon": "https://data.cyverse.org/dav-anon/iplant/projects/"}
for k, u in probes.items():
    try:
        st, _ = get(u)
    except Exception as e:  # connection reset through the proxy
        st = f"error: {type(e).__name__}"
    status[k] = st

mesa = " ".join(v for k, v in texts.items() if k.startswith("mesa_"))
counts = {t: len(re.findall(t, mesa, flags=re.I)) for t in ["NCEMS", "pilot", "DuckLake", "OKF", "AVU", "OLS"]}
ncems_ctx = [mesa[max(0, m.start() - 120): m.end() + 80] for m in re.finditer("NCEMS", mesa)]

# Every quote in facts.csv must appear (whitespace-normalised) in the named saved source.
facts = HERE / "data/raw/research/facts.csv"
checks = []
for row in csv.DictReader(facts.open()):
    src = row["notes"].split("file=")[-1].split(";")[0].strip()
    q = re.sub(r"\s+", " ", row["quote"])
    checks.append({"id": row["id"], "file": src, "found": q in texts.get(src, "")})

out = {"http_status": status, "mesa_public_term_counts": counts, "mesa_ncems_mentions": ncems_ctx, "quote_checks": checks}
(HERE / "data/processed/check_summary.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
assert all(c["found"] for c in checks), [c for c in checks if not c["found"]]
