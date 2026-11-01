"""Slide 37: check every facts.csv quote appears in its saved source (field value for NSF JSON)."""
import csv, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]; RAW = HERE / "data/raw/sources"
norm = lambda s: re.sub(r"\s+", " ", s)
res = []
for r in csv.DictReader((HERE / "data/raw/research/facts.csv").open()):
    meta = dict(kv.split("=", 1) for kv in re.findall(r"(?:file|field)=[^;\s]+", r["notes"]))
    fname = re.findall(r"file=([^;\s]+)", r["notes"])[-1]
    body = (RAW / fname).read_text()
    if fname.endswith(".json"):
        js = json.loads(body)["response"]["award"]
        hay = " ".join(json.dumps(a, ensure_ascii=False) + " " + " ".join(str(v) for v in a.values()) for a in js)
    else:
        hay = body
    res.append({"id": r["id"], "file": fname, "found": norm(r["quote"]) in norm(hay)})
(HERE / "data/processed/quote_checks.json").write_text(json.dumps(res, indent=2))
bad = [x for x in res if not x["found"]]; print(len(res), "checked;", "missing:", bad)
assert not bad
