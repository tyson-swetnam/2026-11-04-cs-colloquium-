"""Verify every facts.csv quote against the saved document and compute the slide's numbers.

Outputs (data/processed/):
  quote_check.csv      one row per fact: quote found verbatim (whitespace/line-number normalised)?
  numbers.csv          settlement per work, music-publisher statutory maximum
  w3techs_english.csv  English share of websites by year (W3Techs)
  cc_english.csv       English share of pages in each Common Crawl crawl, plus top languages in the latest
"""
import csv
import html
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "data/raw/sources"
OUT = HERE / "data/processed"

spec = importlib.util.spec_from_file_location("facts", HERE / "src/00_write_facts.py")
facts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(facts)


def norm(s: str) -> str:
    s = s.replace("­", "").replace(" ", " ").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"(?<![\d,.$])\b\d{1,2}\b(?![\d,.%])", " ", s)  # court-PDF line numbers and footnote marks
    return re.sub(r"\s+", " ", s).strip()


def text_of(path: Path) -> str:
    if path.suffix == ".pdf":
        raw = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
    else:
        t = path.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", t)
        raw = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return norm(raw)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cache, rows, bad = {}, [], 0
    for r in facts.ROWS:
        fid, quote, fname = r[0], r[3], r[7]
        if fname not in cache:
            cache[fname] = text_of(SRC / fname)
        found = norm(quote) in cache[fname]
        bad += not found
        rows.append({"id": fid, "claim_id": r[1], "file": fname, "quote_found": found})
    with (OUT / "quote_check.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"quotes found: {len(rows) - bad}/{len(rows)}")
    for r in rows:
        if not r["quote_found"]:
            print("  MISSING", r["id"], r["file"])

    fund, works, fees = 1.5e9, 482_460, 101_561_111
    expenses, reserve = 2_635_197.46, 18_220_000
    torrented, trained, statmax = 714, 20_517, 150_000
    numbers = [
        ("bartz_gross_per_work_usd", round(fund / works), "1.5e9 / 482,460 works on the Works List"),
        ("bartz_net_per_work_usd_upper_bound", round((fund - fees - expenses - reserve) / works),
         "after fee award, expenses and cost reserve, before administration and service awards"),
        ("bartz_claimed_share", round(440_490 / works, 4), "works claimed by 2026-04-16"),
        ("music_works_total", torrented + trained, "Exhibit A (torrenting) + Exhibit B (training/output)"),
        ("music_statutory_max_usd", (torrented + trained) * statmax, "x $150,000 willful maximum (17 U.S.C. 504(c))"),
    ]
    with (OUT / "numbers.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value", "how"])
        w.writerows(numbers)
    for n in numbers:
        print(n)

    raw = (SRC / "w3techs_content_language_history_y.html").read_text(encoding="utf-8")
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    hdr = re.search(r"2015 1 Jan .*? 2026 31 Oct", t)
    eng = re.search(r"English ((?:\d+\.\d% ){12}\d+\.\d%)", t).group(1).replace("%", "").split()
    dates = [f"{y}-01-01" for y in range(2015, 2027)] + ["2026-10-31"]
    assert hdr and len(eng) == len(dates)
    with (OUT / "w3techs_english.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "english_pct_of_websites"])
        w.writerows(zip(dates, eng))
    print("W3Techs English:", dict(zip(dates, eng)))

    shares = {}
    with (SRC / "cc_languages.csv").open() as f:
        for r in csv.DictReader(f):
            shares.setdefault(r["crawl"], {})[r["primary_language"]] = float(r["%pages/crawl"])
    crawls = sorted(c for c in shares if "eng" in shares[c])
    latest = crawls[-1]
    with (OUT / "cc_english.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["crawl", "english_pct_of_pages"])
        for c in crawls:
            w.writerow([c, shares[c]["eng"]])
    top = sorted(shares[latest].items(), key=lambda kv: -kv[1])[:8]
    print("Common Crawl", latest, "top languages (% pages):", top)


if __name__ == "__main__":
    main()
