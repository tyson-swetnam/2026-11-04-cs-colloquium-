# Slide 01 · How I Learned to Stop Worrying and Love the AI

Section: Opening · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-01)

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` Wed. Nov. 4, 2026, 2 p.m., Larrañaga Engineering Auditorium (Centennial 1041) | supported | UNM CS colloquium page lists exactly this; Python confirms Nov. 4, 2026 is a Wednesday | none |
| `c2` Host bio: Assoc. Prof. of CS, CARC Director, 12 years, PI/co-PI on OAC and DBI projects | partially supported | Faculty profile and CARC pages confirm both titles. Profile dates his CyVerse work from 2013, which makes 13 years. The NSF API has 8 records: 7 projects, since MESA appears twice (Arizona, then UNM). He is now PI on one active OAC award (MESA, 2632685) and one active award from DBI's Capacity program (2152673, to Aug. 2027, now labelled IIC after BIO's reorganization). He has no current OAC or DBI co-PI role (he is listed as former co-PI on 1954556, a CISE award), and he does not have "multiple" awards from each unit | "more than a decade"; "has been PI or co-PI on NSF awards from OAC and the Division of Biological Infrastructure; now leads MESA, an NSF NAIRR award at UNM" |
| `c3` Tyson L. Swetnam, PhD, CARC, UNM | supported | Faculty profile (PhD, Univ. of Arizona, 2013); CARC welcome post | none |
| `c4` CS Colloquium; title "...Love the AI" | supported | Colloquium listing title matches; "Super Intelligence" reveal is a slide gag | none |

## Evidence

- `data/raw/research/facts.csv`: exact quotes from the colloquium page, faculty profile, CARC pages and NSF Award Search API.
- `src/02_capacity_programs.py`: checks which NSF division label the API gives to awards in BIO's Capacity programs (expired ones show DBI, active ones show IIC). It also flags the duplicate MESA record and his "(Former)" co-PI flag. Outputs go to `data/processed/capacity_divisions.csv` and `data/processed/capacity_summary.txt`.
- `src/01_nsf_awards.py`: queries the NSF Award Search API for PI and co-PI awards and checks the talk date's weekday. Outputs go to `data/processed/nsf_awards.csv` and `data/processed/summary.txt`.
- Fetched pages are in `data/raw/sources/` (gitignored, logged in MANIFEST.yaml).

Caveats: CARC pages are on `carc-temp.unm.edu`. That IIC ("Infrastructure, Institutes, & Centers") is DBI's post-reorganization label is inferred from API patterns and NSF's note on the BIO reorganization; no NSF page fetched here names IIC. The NSF API does not show subawards or senior-personnel roles.
