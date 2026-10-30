#!/usr/bin/env bash
# Rebuild data/raw/programs/*.csv from the source documents in data/raw/programs/sources/.
# The documents are not committed; fetch them from the URLs in sources/MANIFEST.yaml first.
# Needs poppler's pdftotext and openpyxl/xlrd (uv run --with openpyxl --with xlrd).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
data="$here/../../data/raw/programs"
mkdir -p "$data/work"
pdftotext -layout "$data/sources/fhwa_summary95_fa203.pdf" "$data/work/fa203.txt"
pdftotext -layout "$data/sources/ulmer1960_appendices_c1498.pdf" "$data/work/ulmer.txt"
pdftotext -layout "$data/sources/rhode2002_nber_w8860.pdf" "$data/work/rhode.txt"
python "$here/parse_ulmer.py" "$data/work/ulmer.txt" "$data/work/ulmer.json"
python "$here/parse_gallman.py" "$data/work/rhode.txt" "$data/work/gallman.json"
python "$here/build.py"
