"""Check that every quote in facts.csv appears in the saved source (whitespace-normalised, HTML unescaped)."""
import csv, html, re, subprocess, json
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "data/raw/sources"
BY_URL = {
    "https://api.nsf.gov/services/v1/awards/2632685.json": "nsf_award_2632685.json",
    "https://ducklake.select/": "ducklake_home.html",
    "https://ducklake.select/manifesto/": "ducklake_manifesto.html",
    "https://ducklake.select/docs/stable/duckdb/advanced_features/transactions": "ducklake_transactions.html",
    "https://ducklake.select/docs/stable/duckdb/usage/choosing_storage": "ducklake_storage.html",
    "https://ducklake.select/docs/stable/duckdb/guides/access_control": "ducklake_access_control.html",
    "https://ducklake.select/docs/stable/specification/introduction": "ducklake_spec_intro.html",
    "https://ducklake.select/docs/stable/duckdb/usage/time_travel": "ducklake_time_travel.html",
    "https://iceberg.apache.org/": "iceberg_home.html",
    "https://delta.io/": "delta_home.html",
    "https://idss-mesa.github.io/okf/concepts/home.md": "mesa_home.md",
    "https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf": "cidr2021_paper17_lakehouse.pdf",
}
norm = lambda s: re.sub(r"\s+", " ", s).strip()
def text(name):
    p = SRC / name
    if p.suffix == ".pdf":
        t = subprocess.run(["pdftotext", "-l", "3", str(p), "-"], capture_output=True, text=True).stdout
        t = re.sub(r"(\w)-\n(\w)", r"\1-\2", t)  # rejoin hyphenated line breaks
        return norm(t)
    t = p.read_text(encoding="utf-8")
    if p.suffix == ".html":
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return norm(t)
res = []
for row in csv.DictReader((HERE / "data/raw/research/facts.csv").open()):
    f = BY_URL.get(row["url"])
    if not f:
        res.append((row["id"], "computed (not a fetched quote)")); continue
    t = text(f)
    q = norm(row["quote"])
    ok = q in t or q in norm(t.replace(" .", ".").replace(" ,", ","))
    res.append((row["id"], "FOUND" if ok else "MISSING"))
for r in res: print(*r)
(HERE / "data/processed/quote_check.json").write_text(json.dumps(dict(res), indent=2))
