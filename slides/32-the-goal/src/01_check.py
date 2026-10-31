"""Slide 32: check the links on the slide and the timing of 'Spring 2026' versus the talk date.

Run from the repo root:  uv run python slides/32-the-goal/src/01_check.py
"""
from __future__ import annotations

import csv
import datetime as dt
import re
from pathlib import Path

import requests

from evidence.http import CachedGet

HERE = Path(__file__).resolve().parents[1]
UA = "colloquium-evidence/0.1 (UNM CARC research)"
get = CachedGet(HERE / "data" / "cache", UA)
OUT = HERE / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

LINKS = {
    "c6": "https://carc.unm.edu/docs/getting-started",
    "c6_overview": "https://carc.unm.edu/docs/getting-started/overview/",
    "c7_help": "https://carc.unm.edu/docs/support/help/",
    "c7_office_hours": "https://carc.unm.edu/user-support-2/office-and-consultation-hours.html",
    "c9_dust": "https://unm-carc.github.io/dust-2026/llms.txt",
}

rows = []
for key, url in LINKS.items():
    # Follow redirects explicitly to record the final URL (CachedGet stores only status and body).
    r = requests.head(url, allow_redirects=True, timeout=60, headers={"User-Agent": UA})
    status, body = get(url)
    title = re.search(r"<title>(.*?)</title>", body, re.S)
    rows.append({"key": key, "url": url, "final_url": r.url, "status": status,
                 "title": (title.group(1).strip() if title else body.splitlines()[0][:80])})

with (OUT / "link_check.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

# Timing: UNM's Spring 2026 finals week is May 11-16, 2026 (schedule.unm.edu finals PDF).
spring_end = dt.date(2026, 5, 16)
talk = dt.date(2026, 11, 4)
with (OUT / "timing.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item", "date", "days_before_talk"])
    w.writerow(["Spring 2026 finals week ends", spring_end.isoformat(), (talk - spring_end).days])
    w.writerow(["Talk", talk.isoformat(), 0])

for r in rows:
    print(r)
print("Spring 2026 ended", (talk - spring_end).days, "days before the talk")
