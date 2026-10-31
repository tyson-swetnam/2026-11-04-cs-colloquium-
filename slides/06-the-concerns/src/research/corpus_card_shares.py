"""Compute scholarly-text shares from numbers parsed out of saved HF dataset cards and PMC esearch JSON.
Usage: python3 -I corpus_card_shares.py <raw_dir>"""
import json, re, sys, os
raw = sys.argv[1]
def card(name): return open(os.path.join(raw, "hf_cards", name), encoding="utf-8").read()

# Dolma v1.7 table: OLMo tokens (billions) column
d = card("allenai_dolma_README.md")
sec = d[d.index("## Summary Statistics (v1.7)"):d.index("## Summary Statistics (v1.6)")]
rows = {}
for line in sec.splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) >= 5 and re.match(r"^\**[\d,\.]+\**$", cells[4]):
        rows[cells[0]] = float(cells[4].strip("*").replace(",", ""))
tot = rows.pop("**Total**")
pes2o = [v for k, v in rows.items() if k.startswith("Semantic Scholar")][0]; arxiv = rows["arXiv"]
print(f"Dolma v1.7: peS2o {pes2o}B + arXiv {arxiv}B = {pes2o+arxiv:.1f}B of {tot}B listed tokens = {100*(pes2o+arxiv)/tot:.2f}%  (sum of rows check {sum(rows.values()):.1f})")

# Dolma v1.6 table: Llama tokens column
sec6 = d[d.index("## Summary Statistics (v1.6)"):d.index("## Download")]
r6 = {}
for line in sec6.splitlines():
    cells = [c.strip().strip("*") for c in line.strip().strip("|").split("|")]
    if len(cells) == 6 and re.match(r"^[\d,\.]+$", cells[5]): r6[cells[0]] = float(cells[5].replace(",", ""))
print(f"Dolma v1.6: PeS2o {r6['PeS2o']}B of {r6['Total']}B Llama tokens = {100*r6['PeS2o']/r6['Total']:.2f}%")

# OLMo 2 mix
o = card("allenai_olmo-mix-1124_README.md"); om = {}
for line in o.splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 5 and re.match(r"^[\d\.]+[BT]$", cells[1]):
        v = float(cells[1][:-1]) * (1000 if cells[1].endswith("T") else 1); om[cells[0]] = v
sch = om["Arxiv"] + om["pes2o"]
print(f"OLMo-2 mix (1124): Arxiv {om['Arxiv']}B + pes2o {om['pes2o']}B = {sch:.1f}B of {om['Total']:.0f}B = {100*sch/om['Total']:.2f}%")

# RedPajama-1T
r = card("togethercomputer_RedPajama-Data-1T_README.md"); rp = {}
for line in r.splitlines():
    m = re.match(r"\|\s*(\w+)\s*\|\s*([\d\.]+)\s*(Billion|Trillion)", line)
    if m: rp[m.group(1)] = float(m.group(2)) * (1000 if m.group(3) == "Trillion" else 1)
print(f"RedPajama-1T: ArXiv {rp['ArXiv']}B of {rp['Total']}B = {100*rp['ArXiv']/rp['Total']:.2f}%")

# PMC license breakdown (E-utilities esearch counts)
c = {}
for f in os.listdir(os.path.join(raw, "pmc", "eutils")):
    if f.endswith(".json"):
        c[f[len("esearch_pmc_"):-5]] = int(json.load(open(os.path.join(raw, "pmc", "eutils", f)))["esearchresult"]["count"])
A = c["all_pmc"]
print(f"PMC total articles: {A:,}")
for k in ["oa_or_am", "open_access", "author_manuscript", "commercial_ok", "noncommercial_only", "cc_by", "cc0"]:
    print(f"  {k:20s} {c[k]:>12,}  {100*c[k]/A:6.2f}%")
print(f"  not in OA subset or author-manuscript dataset: {A-c['oa_or_am']:,} ({100*(A-c['oa_or_am'])/A:.2f}%)")
print(f"  OA/AM but neither commercial-OK nor NC-only CC licence (e.g. TDM-only manuscripts, other): {c['oa_or_am']-c['commercial_ok']-c['noncommercial_only']:,}")
print(f"  commercial-reuse CC licence as share of the reusable (OA or AM) datasets: {100*c['commercial_ok']/c['oa_or_am']:.2f}%")
# Wiley cumulative cross-check
print(f"Wiley AI revenue FY24+FY25+FY26 = 23 + 40 + 49 = {23+40+49} ($M) vs 'lifetime AI revenue surpassed $110 million'")
